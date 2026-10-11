#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run.py — v3 dispatcher (single entry point).

python3 engine/run.py <cmd> [args...]
  init/plan/next   -> orchestrate.py (v2 topology; migration note in SKILL.md §7)
  corpus           -> corpus.py  (axis|seeds|queries|fetch|topup|bodies|coverage ...)
  ledger           -> ledger.py  (init|check|anchors ...)
  matrix           -> matrix3.py matrix  <findings.jsonl> <out.md>
  council          -> matrix3.py council <findings.jsonl> <out.md>
  check            -> matrix3.py check   <findings.jsonl>
  humanize         -> humanize.py score  <draft> [--title T] [--abstract A]
  guard            -> guard_private.py scan <targets...>
  stage            -> guard_private.py stage <src> <dst>
  validate         -> validate.py
  apply            -> apply_revisions.py
Unknown/missing args print this help. Every shipped-package step must pass `guard` first.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAP = {
    "init": ("orchestrate.py", None), "plan": ("orchestrate.py", None),
    "next": ("orchestrate.py", None),
    "corpus": ("corpus.py", None),
    "matrix": ("matrix3.py", ["matrix"]), "council": ("matrix3.py", ["council"]),
    "check": ("matrix3.py", ["check"]),
    "ledger": ("ledger.py", None),
    "humanize": ("humanize.py", ["score"]),
    "guard": ("guard_private.py", ["scan"]), "stage": ("guard_private.py", ["stage"]),
    "validate": ("validate.py", None), "apply": ("apply_revisions.py", None),
}


def main(argv):
    if not argv or argv[0] not in MAP or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if not argv else 2
    script, prefix = MAP[argv[0]]
    cmd = [sys.executable, os.path.join(HERE, script)] + (prefix or []) + argv[1:]
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
