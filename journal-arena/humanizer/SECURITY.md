# SECURITY — humanizer module (PRIVATE / PROPRIETARY)

**Classification:** خصوصی — authored by the project owner. NOT for publication,
distribution, or external disclosure until the owner explicitly authorizes it.
The scope of this policy: the three files in this directory (`HUMANIZER-SKILL.md`,
`RULES.md`, `TASKS.md`) — READ-ONLY originals — **plus `engine/humanize.py`** (the
derived gate implementation); working derivatives live in `work/` and are equally private.

## PRIV laws (binding on every agent, model, and export step)

- **PRIV-1 — No export.** Nothing from `humanizer/` may enter any submission kit,
  GitHub package, zip, appendix, response letter, or shared archive. Public builds
  must use a staging copy of the skill WITHOUT this directory and without §6 of SKILL.md.
- **PRIV-2 — No upload.** Never send these files (HUMANIZER-SKILL.md, RULES.md,
  TASKS.md), `engine/humanize.py`, or the corpus statistics and provenance (sample
  sizes, within-author pair counts, p-values, MTI bands), to any external model,
  site, detector, or tool. Owner-approved exception in `distilled-brief` mode: the
  DISTILLED-BRIEF.md payload plus the draft prose being rewritten may go to the
  owner-designated model — writer pipeline only; the evidence base stays local
  regardless.
- **PRIV-3 — Minimal disclosure.** The sole payload permitted to leave this workspace
  is `humanizer/DISTILLED-BRIEF.md` (banned-word list + numeric gates + procedure).
  NEVER the evidence base: no corpus sizes, no within-author statistics, no p-values,
  no arm means, no MTI formula or era tables, no provenance notes. All numeric gates
  are measured locally with `engine/humanize.py`; the external model edits, never scores.
- **PRIV-4 — Export guard.** Before building ANY zip/kit/package, run
  `python3 engine/guard_private.py scan <target>`; it must print `VERDICT: clean`
  (exit 0). A blocked export may not be shipped, renamed, or re-tried without fixing
  the violation.
- **PRIV-5 — Integrity.** Do not edit the originals. Re-calibration (TASKS T8) and
  gate runs are logged in `work/humanize-log.json`.
- **PRIV-6 — Attribution.** Internal references read "humanizer module
  (author-provided, private)". No external citation, credit, or mention without the
  owner's written go-ahead.

## Mode switch (owner's decision, recorded in work/plan.json)
- `humanizer_mode: local-only` — all humanizer tasks run inside this workspace.
- `humanizer_mode: distilled-brief` — DISTILLED-BRIEF.md may appear in external briefs.

**RECORDED DECISION (2026-10-09, owner):** `humanizer_mode: distilled-brief` — the
100-agent/humanize tooling will be connected to another language model; writer briefs
carry `DISTILLED-BRIEF.md` only; scoring stays local.
