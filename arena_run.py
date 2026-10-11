#!/usr/bin/env python3
"""arena_run.py - run the Arena skill headless, outside Claude Code.

The original skill (github.com/Jakeschincariol/arena-skill) is a Claude Code
skill: SKILL.md tells Claude to spawn sub-agents with the Agent tool, while
bracket.py keeps the tournament state. This script replaces the Claude Code
part only. It drives bracket.py directly, renders the exact same sub-agent
briefs that SKILL.md contains, and calls a model for every job over HTTP
(OpenAI-compatible, Anthropic, Gemini) or through any local CLI.

Nothing about the tournament changes: same strategy cards, same single
elimination bracket, same attacks/defences, same rubric arithmetic.

Examples
--------
  # machinery test, no API key, no network (12 fake agents)
  python3 arena_run.py --provider mock --agents 12 --task "Write a launch plan"

  # real run on any OpenAI-compatible endpoint
  export OPENAI_API_KEY=sk-...
  python3 arena_run.py --provider openai --model gpt-4o-mini --quick \
      --task "Rewrite our pricing page headline" --workdir ./run1

  # put several models in the ring (the original can't do this)
  python3 arena_run.py --provider openai --models gpt-4o,o4-mini,gpt-4o-mini

  # a local model through Ollama (OpenAI-compatible shim)
  python3 arena_run.py --provider openai --models llama3.1 \
      --base-url http://localhost:11434/v1 --api-key ollama

  # any CLI that reads a prompt on stdin and writes the answer to stdout
  python3 arena_run.py --provider cmd --cmd "claude -p"      # or: llm -m ...
  python3 arena_run.py --provider cmd --cmd "ollama run qwen2.5"

  # resume an interrupted run (bracket.py skips finished jobs)
  python3 arena_run.py --resume --workdir ./run1
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# --------------------------------------------------------------------- setup

CANDIDATE_SKILL_DIRS = (
    os.environ.get("ARENA_SKILL_DIR"),
    "./arena-skill/skills/arena",
    "../arena-skill/skills/arena",
    "~/.claude/skills/arena",
    "~/.config/claude/skills/arena",
)

_LOCK = threading.Lock()
LOG_FH = None


def log(msg="", job=None):
    stamp = time.strftime("%H:%M:%S")
    tag = "[%s] " % job if job else ""
    line = "%s %s%s" % (stamp, tag, msg)
    with _LOCK:
        print(line, flush=True)
        if LOG_FH:
            LOG_FH.write(line + "\n")
            LOG_FH.flush()


def find_skill_dir(explicit=None):
    for cand in (explicit,) + CANDIDATE_SKILL_DIRS:
        if not cand:
            continue
        path = os.path.abspath(os.path.expanduser(cand))
        if os.path.isfile(os.path.join(path, "bracket.py")) and \
           os.path.isfile(os.path.join(path, "SKILL.md")):
            return path
    raise SystemExit(
        "bracket.py not found. Clone the skill and pass --skill-dir:\n"
        "  git clone https://github.com/Jakeschincariol/arena-skill\n"
        "  python3 arena_run.py --skill-dir arena-skill/skills/arena ..."
    )


def load_bracket(skill_dir):
    path = os.path.join(skill_dir, "bracket.py")
    spec = importlib.util.spec_from_file_location("arena_bracket", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["arena_bracket"] = mod
    spec.loader.exec_module(mod)
    return mod


def ns(**kw):
    """bracket.py's commands take an argparse namespace; give them one."""
    return argparse.Namespace(**kw)


# ------------------------------------------------------------ job -> prompt

PATH_RE = re.compile(r"(?:/[\w@.+\-]+)+\.(?:md|json|txt|py|jsonl|ya?ml|csv)")
FILE_RE = re.compile(
    r"<<<ARENA-FILE:\s*(?P<path>.+?)\s*>>>\s*\n(?P<body>.*?)\n?\s*<<<ARENA-END>>>",
    re.S,
)

WRAPPER = """You are one worker in an arena that is running offline.

You have NO tools and NO file access. Everything you are allowed to know is pasted
below, and everything you must produce comes back in this single reply.

=== YOUR BRIEF (follow it exactly; it is your whole job) ===
{brief}
=== END OF YOUR BRIEF ===

{filedump}

=== HOW TO RETURN YOUR WORK ===
Do not describe what you would do. Produce the work itself.

For every file the brief tells you to write, emit one block in exactly this shape:

<<<ARENA-FILE: {first_out}>>>
the full contents of that file
<<<ARENA-END>>>

Use the exact paths the brief gave you, one block per file, in any order. Nothing
after the last block. If the file is a verdict, the block must contain the JSON
object and nothing else. Write no commentary outside the blocks.

Write every file the brief asks for:
{outlist}
"""


def build_prompt(job, text, max_chars):
    """Inline every file the brief points at, so a tool-less model can do the job."""
    outputs = set(os.path.abspath(p) for p in job.get("outputs", []))
    seen, parts, budget = set(), [], max_chars
    for raw in PATH_RE.findall(text):
        path = os.path.abspath(os.path.expanduser(raw))
        if path in seen or path in outputs:
            continue
        seen.add(path)
        if not os.path.isfile(path):
            parts.append("--- BEGIN FILE: %s ---\n(MISSING. Treat it as NO OUTPUT / empty.)\n--- END FILE: %s ---\n"
                         % (path, path))
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                body = fh.read()
        except OSError as exc:
            parts.append("--- BEGIN FILE: %s ---\n(UNREADABLE: %s)\n--- END FILE: %s ---\n" % (path, exc, path))
            continue
        if len(body) > budget:
            body = body[:budget] + "\n\n...[truncated: file is longer than this run's context budget]...\n"
            budget = 0
        else:
            budget -= len(body)
        if not body.strip():
            body = "(empty file)"
        parts.append("--- BEGIN FILE: %s ---\n%s\n--- END FILE: %s ---\n" % (path, body, path))
    filedump = "=== FILES THE BRIEF REFERS TO ===\n" + "\n".join(parts) if parts else ""
    outs = job.get("outputs") or ["(the file the brief asks for)"]
    return WRAPPER.format(
        brief=text,
        filedump=filedump,
        first_out=outs[0],
        outlist="\n".join("  - %s" % p for p in outs),
    )


def parse_files(reply, job):
    """Pull the ARENA-FILE blocks out of a reply; tolerate sloppy models."""
    blocks = {os.path.abspath(m.group("path").strip().strip('`"\'')): m.group("body") for m in FILE_RE.finditer(reply)}
    wanted = [os.path.abspath(p) for p in job.get("outputs", [])]
    written = {}
    for path in wanted:
        if path in blocks:
            written[path] = blocks[path]
    missing = [p for p in wanted if p not in written]
    if missing and len(wanted) == 1:
        # No markers at all: take the whole reply, or the JSON object inside it.
        body = reply.strip()
        if wanted[0].endswith(".json"):
            body = extract_json_loose(body) or body
        if not FILE_RE.search(reply):
            body = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", body).strip()
        written[wanted[0]] = body
    return written, missing


def extract_json_loose(text):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None
    blob = text[start:end + 1]
    try:
        json.loads(blob)
        return blob
    except json.JSONDecodeError:
        return None


# ----------------------------------------------------------------- providers

def http_json(url, payload, headers, timeout, retries=1):
    data = json.dumps(payload).encode("utf-8")
    last = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")[:400]
            last = "HTTP %s: %s" % (exc.code, body)
            if exc.code in (400, 401, 403, 404, 422):
                break
        except Exception as exc:  # noqa: BLE001 - network, DNS, timeout
            last = "%s: %s" % (type(exc).__name__, exc)
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(last or "request failed")


def call_openai(prompt, model, args):
    key = args.api_key or os.environ.get(args.api_key_env or "OPENAI_API_KEY", "")
    if not key and "localhost" not in args.base_url and "127.0.0.1" not in args.base_url:
        raise RuntimeError("no API key: set %s or pass --api-key" % (args.api_key_env or "OPENAI_API_KEY"))
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }
    out = http_json(args.base_url.rstrip("/") + "/chat/completions", payload,
                    {"Content-Type": "application/json", "Authorization": "Bearer " + key}, args.timeout)
    if "choices" not in out:
        raise RuntimeError("unexpected reply: %s" % json.dumps(out)[:300])
    return out["choices"][0]["message"]["content"]


def call_anthropic(prompt, model, args):
    key = args.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise RuntimeError("no API key: set ANTHROPIC_API_KEY or pass --api-key")
    payload = {"model": model, "max_tokens": args.max_tokens, "temperature": args.temperature,
               "messages": [{"role": "user", "content": prompt}]}
    out = http_json(args.base_url.rstrip("/") + "/v1/messages", payload,
                    {"Content-Type": "application/json", "x-api-key": key,
                     "anthropic-version": "2023-06-01"}, args.timeout)
    if "content" not in out:
        raise RuntimeError("unexpected reply: %s" % json.dumps(out)[:300])
    return "".join(part.get("text", "") for part in out["content"])


def call_google(prompt, model, args):
    key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
    if not key:
        raise RuntimeError("no API key: set GEMINI_API_KEY or pass --api-key")
    url = "%s/v1beta/models/%s:generateContent?key=%s" % (args.base_url.rstrip("/"), model, key)
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"temperature": args.temperature, "maxOutputTokens": args.max_tokens}}
    out = http_json(url, payload, {"Content-Type": "application/json"}, args.timeout)
    try:
        return out["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("unexpected reply: %s" % json.dumps(out)[:300])


def call_cmd(prompt, model, args):
    if not args.cmd:
        raise RuntimeError("--provider cmd needs --cmd")
    proc = subprocess.run(shlex.split(args.cmd), input=prompt, capture_output=True,
                          text=True, timeout=args.timeout)
    if proc.returncode != 0:
        raise RuntimeError("command failed (%d): %s" % (proc.returncode, proc.stderr.strip()[:300]))
    return proc.stdout


def call_mock(prompt, model, job):
    """Deterministic stand-in: exercises the whole bracket without a model.

    It proves the machinery, not the intelligence. Every 'solution' is filler
    text; the judges hand every match to the first-listed agent with fixed
    scores, so a mock run is a test of this script and of bracket.py only.
    """
    kind = job.get("kind", "competitor")
    task = ""
    m = re.search(r"=== (?:THE )?TASK[^=]*===\n(.*?)\n=== END", prompt, re.S)
    if m:
        task = m.group(1)
    first = job["outputs"][0]
    card = ""
    m = re.search(r"Reasoning mode: ([^\n]+)", prompt)
    if m:
        card = m.group(1).strip()
    seed = abs(hash(job["id"])) % 9
    if kind == "competitor":
        body = ("# MOCK SOLUTION (%s)\n\nTask received: %s\n\n"
                "This file was produced by --provider mock. It contains no real work; "
                "it only proves that the arena machinery moves a solution from round 0 "
                "to a champion without a model behind it.\n" % (card, task.strip()[:200]))
    elif kind == "attacker":
        body = ("ATTACK 1: MAJOR. The solution is filler text and answers nothing.\n"
                "ATTACK 2: MINOR. It names no constraint from the task.\n"
                "ATTACK 3: MAJOR. There is no evidence for any claim in it.\n")
    elif kind == "defender":
        body = ("ATTACK 1: CONCEDE. Fixed by stating that this is a mock run.\n"
                "ATTACK 2: CONCEDE. Fixed.\n"
                "ATTACK 3: REBUT. The check the attacker asks for cannot settle anything here.\n")
    elif kind == "judge":
        a, b = job["a"], job["b"]
        body = json.dumps({
            "match": job["match"],
            "scores": {
                a: {"correctness": 6 + seed % 3, "completeness": 6, "specificity": 5,
                    "robustness": 7, "clarity": 8, "fatal": False},
                b: {"correctness": 5, "completeness": 5, "specificity": 4,
                    "robustness": 6, "clarity": 7, "fatal": False},
            },
            "winner": a,
            "reason": "mock judge: first-listed solution scored higher on correctness",
            "survived": ["no real attacks in a mock run"],
            "standing": {b: ["answers nothing"]},
        }, indent=1)
    elif kind == "final":
        body = json.dumps({
            "scores": {"X": {"correctness": 7, "completeness": 7, "specificity": 6,
                             "robustness": 7, "clarity": 8, "fatal": False},
                       "Y": {"correctness": 5, "completeness": 5, "specificity": 4,
                             "robustness": 5, "clarity": 6, "fatal": False}},
            "winner": "X",
            "reason": "mock final check: X scored higher",
            "fixed": ["mock difference"],
        }, indent=1)
    else:
        body = "MOCK OUTPUT\n"
    if kind == "defender":
        sol = job["outputs"][1]
        return ("<<<ARENA-FILE: %s>>>\n%s\n<<<ARENA-END>>>\n"
                "<<<ARENA-FILE: %s>>>\n%s\n<<<ARENA-END>>>\n" % (first, body, sol, body.replace("ATTACK", "REVISED")))
    return "<<<ARENA-FILE: %s>>>\n%s\n<<<ARENA-END>>>\n" % (first, body)


# --------------------------------------------------------------------- driver

def run_one_job(args, job, model):
    if args.attempts.exhausted(job["id"]):
        log("skip %-28s already attempted %d time(s); not trying again"
            % (job["id"], args.attempts.data["attempts"][job["id"]]), job=job.get("kind"))
        return False
    args.attempts.bump(job["id"])
    text = open(job["prompt"], encoding="utf-8").read()
    prompt = build_prompt(job, text, args.max_context)
    attempts, last_err = args.retries + 1, None
    for attempt in range(attempts):
        started = time.time()
        try:
            if args.provider == "mock":
                reply = call_mock(prompt, model, job)
            elif args.provider == "openai":
                reply = call_openai(prompt, model, args)
            elif args.provider == "anthropic":
                reply = call_anthropic(prompt, model, args)
            elif args.provider == "google":
                reply = call_google(prompt, model, args)
            elif args.provider == "cmd":
                reply = call_cmd(prompt, model, args)
            else:
                raise RuntimeError("unknown provider %s" % args.provider)
            written, missing = parse_files(reply, job)
            if missing and len(job["outputs"]) > 1:
                raise RuntimeError("reply did not contain blocks for: %s" % ", ".join(missing))
            for path, body in written.items():
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(body if body.endswith("\n") else body + "\n")
            if missing:
                raise RuntimeError("no usable content for %s" % ", ".join(missing))
            log("ok  %-28s %5.1fs  %s" % (job["id"], time.time() - started, model), job=job["kind"])
            return True
        except Exception as exc:  # noqa: BLE001 - any failure means: try once, then NO OUTPUT
            last_err = exc
            log("fail %-27s attempt %d/%d: %s" % (job["id"], attempt + 1, attempts, exc), job=job["kind"])
    for path in job["outputs"]:
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("NO OUTPUT\n")
    log("gave up on %s: %s" % (job["id"], last_err), job=job["kind"])
    return False


class Attempts:
    """Per-job attempt counter, on disk, so a broken verdict cannot loop forever.

    bracket.py deletes an unreadable verdict and asks for the judge again, so a
    model that keeps returning unusable JSON would spin the driver for ever.
    SKILL.md's rule is: re-run a failing job once, then NO OUTPUT, and give a
    failing judge a third try. Past that, the honest move is to stop.
    """

    def __init__(self, run_dir, limit):
        self.path = os.path.join(run_dir, "driver.json")
        self.limit = limit
        self.data = {"attempts": {}}
        if os.path.isfile(self.path):
            try:
                with open(self.path, encoding="utf-8") as fh:
                    self.data = json.load(fh)
            except (OSError, json.JSONDecodeError):
                pass
        self.data.setdefault("attempts", {})

    def bump(self, job_id):
        with _LOCK:
            n = self.data["attempts"].get(job_id, 0) + 1
            self.data["attempts"][job_id] = n
            self.save()
            return n

    def exhausted(self, job_id):
        return self.data["attempts"].get(job_id, 0) >= self.limit

    def save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh, indent=1)
            fh.write("\n")
        os.replace(tmp, self.path)


def drive(bracket, args):
    step = 0
    while True:
        if args.max_steps and step >= args.max_steps:
            log("stopping: --max-steps %d reached" % args.max_steps)
            return 1
        step += 1
        state = bracket.load_state(args.bargs)
        phase, left, jobs = bracket.next_action(state)

        if phase in bracket.PHASES:
            jobs = bracket.write_prompts(state, phase) or jobs
            todo = bracket.missing_jobs(jobs)
            if todo and all(args.attempts.exhausted(j["id"]) for j in todo):
                log("stopping: every job left in phase '%s' has failed %d time(s)."
                    % (phase, args.attempts.limit))
                log("The tournament cannot go past this point. Read arena-run.log, then fix the"
                    " model output or switch models and continue with: --resume")
                return 1
            log("--- step %d: %s, %d job(s), %d to run ---" % (step, phase, len(jobs), len(todo)))
            results = []
            with ThreadPoolExecutor(max_workers=max(1, args.parallel)) as pool:
                futures = []
                for i, job in enumerate(todo):
                    try:
                        slot = int(job["agent"][1:]) if job.get("agent") else i + step * 97
                    except (TypeError, ValueError):
                        slot = i + step * 97
                    model = args.models[slot % len(args.models)]
                    futures.append(pool.submit(run_one_job, args, job, model))
                for fut in futures:
                    results.append(fut.result())
            if results and not any(results):
                log("every job in this step failed.")
        elif phase == "collect":
            log("--- step %d: collect ---" % step)
            bracket.cmd_collect(args.bargs)
        elif phase == "advance":
            log("--- step %d: advance ---" % step)
            bracket.cmd_advance(args.bargs)
        elif phase == "done":
            break
        else:
            log("unexpected phase %r" % phase)
            return 1
    log("tournament over.")
    return bracket.cmd_winner(args.bargs)


def main(argv=None):
    global LOG_FH
    p = argparse.ArgumentParser(description="Run the Arena skill headless (no Claude Code).",
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=__doc__.split("Examples")[-1])
    p.add_argument("--skill-dir", help="folder holding bracket.py/SKILL.md (default: ./arena-skill/skills/arena)")
    p.add_argument("--workdir", default=".", help="where .arena/ lives (default: .)")
    p.add_argument("--dir", dest="run_dir", help="an existing run folder; --resume uses .arena/LATEST")
    p.add_argument("--resume", action="store_true", help="pick up the run named in .arena/LATEST")
    p.add_argument("--dry-run", action="store_true", help="print the plan and stop")

    p.add_argument("--provider", default="openai", choices=("openai", "anthropic", "google", "cmd", "mock"))
    p.add_argument("--model", help="one model for every job")
    p.add_argument("--models", help="comma-separated; dealt round-robin per competitor")
    p.add_argument("--base-url", default="https://api.openai.com/v1", help="endpoint root (OpenAI-compatible)")
    p.add_argument("--api-key", help="or set the env var: OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY")
    p.add_argument("--api-key-env", help="read the key from this env var instead of the default")
    p.add_argument("--cmd", help="for --provider cmd, e.g. \"claude -p\" or \"ollama run llama3.1\"")
    p.add_argument("--temperature", type=float, default=0.8, help="sub-agents should not all be 0.2")
    p.add_argument("--max-tokens", type=int, default=8000)
    p.add_argument("--timeout", type=float, default=600, help="seconds per model call")
    p.add_argument("--retries", type=int, default=1, help="extra attempts per job, as SKILL.md says")
    p.add_argument("--parallel", type=int, default=4, help="jobs in flight (Claude Code uses 10)")
    p.add_argument("--max-context", type=int, default=60000, help="chars of inlined files per job")
    p.add_argument("--max-steps", type=int, default=0, help="safety valve: stop after N driver steps")
    p.add_argument("--max-job-attempts", type=int, default=3,
                   help="give up on a single job after N tries across the whole run (default 3)")
    p.add_argument("--ignore-attempts", action="store_true",
                   help="forget the attempt counters (use after switching models)")

    p.add_argument("--agents", type=int, help="competitors (default 100)")
    p.add_argument("--quick", action="store_true", help="16 competitors")
    p.add_argument("--seed", type=int)
    p.add_argument("--wave", type=int, default=10, help="only used for the plan printout")
    p.add_argument("--task")
    p.add_argument("--task-file")
    p.add_argument("--baseline-file", help="the answer the user was not satisfied with")
    args = p.parse_args(argv)

    args.models = [m.strip() for m in (args.models or args.model or "gpt-4o-mini").split(",") if m.strip()]
    os.makedirs(args.workdir, exist_ok=True)
    os.chdir(args.workdir)
    LOG_FH = open("arena-run.log", "a", encoding="utf-8")

    skill_dir = find_skill_dir(args.skill_dir)
    bracket = load_bracket(skill_dir)
    log("skill: %s" % skill_dir)
    log("provider: %s  models: %s" % (args.provider, ", ".join(args.models)))

    args.bargs = ns(dir=args.run_dir, json=False)

    if args.dry_run or not (args.resume or args.run_dir or args.task_file or args.task):
        n = bracket.QUICK_AGENTS if args.quick else (args.agents or bracket.DEFAULT_AGENTS)
        log("plan: no task given%s" % ("" if args.dry_run else " -- nothing to run"))
        return bracket.cmd_plan(ns(agents=n, quick=False, wave=args.wave, json=False))

    if args.resume:
        latest = os.path.join(".arena", "LATEST")
        if not os.path.isfile(latest):
            raise SystemExit("nothing to resume: %s does not exist" % latest)
        args.bargs.dir = open(latest, encoding="utf-8").read().strip()
        log("resuming %s" % args.bargs.dir)
    else:
        rc = bracket.cmd_init(ns(
            agents=args.agents, quick=args.quick, seed=args.seed, wave=args.wave,
            task=args.task, task_file=args.task_file, baseline_file=args.baseline_file,
            dir=args.run_dir,
        ))
        if rc:
            return rc
        args.bargs.dir = open(os.path.join(".arena", "LATEST"), encoding="utf-8").read().strip()

    args.attempts = Attempts(args.bargs.dir, args.max_job_attempts)
    if args.ignore_attempts:
        args.attempts.data["attempts"] = {}
        args.attempts.save()

    rc = drive(bracket, args)
    log("log: %s" % os.path.abspath("arena-run.log"))
    log("full record: %s" % args.bargs.dir)
    return rc


if __name__ == "__main__":
    sys.exit(main())
