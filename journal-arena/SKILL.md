# Skill: journal-arena v3 — علم‌سنجی کامل هم‌محور مقاله + اصلاح ردیاب‌پذیر برای Energy & Buildings
### (v2 backup: SKILL.v2.bak.md — v3 shifts the center of gravity from writing-review to
### scientific merit: literature-grounded evaluation, novelty/gap/method/code audit,
### elite council verdict, and a PRIVATE humanizer module for the writers.)

## 0. The laws (every agent, every model, every phase)
1. **One-duty law** — each agent owns EXACTLY one part; out-of-duty observations go to
   at most one forwarded note (`group: <gid>`, severity `style`).
2. **Dual-grounding law (v3)** — every evaluative judgment carries TWO anchors:
   (a) an exact quote from the STUDIED LITERATURE with source id + locator
   (`[L:g4-037 §Results ¶2]` from that group's reading ledger), and
   (b) an exact quote from the manuscript, ONLY where a claim is being mapped.
   A finding without (a) is quarantined, never counted. The v2 rule "quote the
   manuscript" survives only as claim-mapping, not as evidence.
3. **Decision-value law (v3)** — every agent output = verdict + at most 3 actionable
   moves + the quotes. No paraphrase-only summaries. The central ledger deduplicates;
   activity without a decision is waste and is logged as such.
4. **Evidence-tier law (v3)** — body > abstract > metadata. Paywalled body =
   `abstract-level` tag and HALF voting weight in council aggregation. Every quote
   carries its tier.
5. **Verification license** — read-only toward sources; the manuscript never leaves
   the workspace EXCEPT the writer pipeline under `humanizer_mode: distilled-brief`
   (owner-approved; draft prose + DISTILLED-BRIEF.md only).
6. **PRIV-1…PRIV-6** — `humanizer/SECURITY.md` is binding: the humanizer module
   (files + `engine/humanize.py`) is never exported/uploaded; guard before any
   package build: `python3 engine/guard_private.py scan <target>` must print
   `VERDICT: clean` (public builds: `guard_private.py stage <src> <dst>`).
7. **No-fabrication law** — never invent numbers; missing value = `[number needed]`,
   resolved only by the author. No detector score ever decides anything.
8. **No-exaggeration law** — no claim bigger than its evidence; claim inflation is a
   scored, vetoable offense (arena rubric keeps `claim_inflation` weight).

## 1. Decisions on record (owner, 2026-10-09)
- `code_scope = research_code` — Group 5 audits the research's analysis/reproducibility
  code (existence/absence, correctness, architecture, libraries, algorithms, performance
  on an ordinary PC). If absent, the Tier-3 elite coders build a minimal reproducibility
  kit (scripts reproducing every table/figure number from the deposited data). The
  journal-arena engine itself is NOT a review target in this run.
- `tier1_journals = [Energy & Buildings, Applied Energy, Building & Environment,
  Energy, Journal of Building Engineering, Energy and AI]` — owner decision
  2026-10-09, re-confirmed AFTER the axis correction (residential-energy axis;
  the earlier water/environmental trio was chosen under a wrong axis reading and
  is superseded).
- `corpus_axis = manuscript-derived` — single source of truth: `work/corpus/axis.json`
  (current ENB submission: leakage-audited uncertainty-calibrated pipeline for
  residential energy prediction, RECS 18,496 households).
- `corpus_counting = body-access-only` — owner decision 2026-10-11: the countable-100
  per group = papers with FULL-TEXT access, from ANY journal; journal choice priority:
  (1) axis-fit with the manuscript topic, (2) journal score/level. Abstract-only papers:
  mandatory key-abstract reading, NOT counted in the 100, earn a special BONUS score per
  group (reserved for a future scoring edition).
- `humanizer_mode = distilled-brief` — writer briefs to the external model carry
  `humanizer/DISTILLED-BRIEF.md` only; all gate measurement stays local
  (`engine/humanize.py`).

## 2. Pipeline v3 (resumable via work/plan.json `next`)
init → plan → **corpus** (axis from manuscript → per-group reading lists + ledger) → waves (Tier-1
evaluation, 10 agents/wave) → matrix (v3 schema) → arena (contested revisions) →
**council** (Tier-2 elite verdict) → apply (owner-approved revisions) → **humanize**
(Tier-3 writers, T1–T6 + local gates) → validate → kit (guard scan FIRST).

## 3. Topology v3
**Tier 0 — mandatory corpus for EVERY agent (before any duty work):**
the 24 live sources (sources/CORPUS.md) + ALL manuscript references (auto-extracted via
`corpus seeds`; abstract + body where accessible, tier-tagged) + ENB guide-for-authors + Elsevier policy set.

**Mandatory training gate:** هر ایجنت پیش از موج، برنامهٔ آموزشی گروهش را در
`task/14-training-and-refresh.md` تکمیل و یادداشت ≤۱۰ خطی در `work/training/<gid>.md`
ثبت می‌کند (منابع + تاریخ). بدون آن، خروجی گروه قابل پذیرش نیست.

**Tier 1 — ten evaluation groups** (each: core laws + own rule module in
`task/10-group-<n>.md` + own corpus ≥100 papers on the shared axis, drawn from the
target journal and the tier-1 list, snowballed from references):
| gid | name | duty (ONE part) | headline criteria |
|---|---|---|---|
| E1 | claims-evidence | map every manuscript claim to literature quotes | over/underclaim, claim-vs-effect-size |
| E2 | novelty-contribution | verify novelty vs corpus + last-24-months works | what exactly is added to the literature |
| E3 | gap-positioning | audit the claimed gap | gap↔goal fit, position on the literature map |
| E4 | methodology-scientometrics | design, statistics, power/MDES, sampling, QC, standards | methodological defect hunt |
| E5 | research-code-reproducibility | audit analysis code & reproducibility (see §1) | correctness, architecture, ordinary-PC performance |
| E6 | data-results-integrity | numbers cross-check, tables/figures coherence, reference existence, image integrity | traceability of every digit |
| E7 | journal-fit | vs ENB + tier-1 papers of last 24 months | scope, article type, positioning |
| E8 | ethics-policy | SAGER, CRediT, data deposit, COI, GenAI, licences | policy gate completeness |
| E9 | writing-structure | SECONDARY layer: structure, flow, tables | never the verdict axis |
| E10 | devils-advocate | simulate TWO independent reviewers + editor | fatal-flaw hunt across all groups |

**Tier 2 — elite council:** the best-read agents (≥100 papers across ≥2 axes + full
Tier-0). Mandatory written answers: (1) what does this research add to the literature?
(2) is it submittable after fixing the listed defects, or is development essential —
and if essential, exactly why? (3) verdict ∈ {submittable, revise-then-submit,
develop-first} + prioritized roadmap. Abstract-level quotes count half.

**Tier 3 — elite executors:** coders (reproducibility kit per §1; ordinary-PC
constraint) and writers (humanizer T1–T6 per `humanizer/TASKS.md`; external model
receives DISTILLED-BRIEF.md only; local gates `engine/humanize.py` must print
`VERDICT: gates clear` before `validate.py`).

## 4. Corpus & reading ledger
**Axis law:** the shared corpus axis is ALWAYS derived from the manuscript submitted to
the target journal (title + keywords → `corpus axis` → `work/corpus/axis.json`).
Hardcoding a topic axis anywhere is a defect; the built-in list is fallback-only.
`work/ledger.jsonl` — one line per studied paper:
`{gid, source_id, cite, doi_or_url, tier: body|abstract|metadata, date_read,
takeaway_3_lines, quote_bank: [{quote, locator}]}`.
The quote bank is the ONLY pool from which `[L:…]` anchors may be drawn (law 2).
Reading budget: ≥100 papers/group; ≥60% body-tier where open access permits;
paywall → abstract tier + half weight, logged transparently.

## 5. Efficiency (v3 additions)
- Waves of 10 agents; hard cap 100 agents per run.
- Matrix v3 columns: `claim_id, verdict, lit_quote_id, ms_quote, effect_vs_claim,
  severity, action, owner_group, tier_of_evidence`.
- Dedup via ledger before arena; contested items only go to bracket.
- Every finding must survive the decision-value schema or it is dropped.

## 6. Humanizer module — PRIVATE (see §0 law 6)
`humanizer/` holds the owner's Humanizer-Academic-EN skill (READ-ONLY originals),
`DISTILLED-BRIEF.md` (the sole exportable payload), `SECURITY.md` (PRIV laws +
recorded mode). `engine/humanize.py` scores the TASKS.md master gates locally and
never edits text. Public builds: `python3 engine/guard_private.py stage . <dst>`
strips the module and §6-equivalent text, then auto-scans.

## 7. Model-agnostic contract & layout
Every brief is self-contained (paste into ANY chat model). Engine entry:
`python3 engine/run.py init|plan|corpus|next|matrix|arena|council|apply|humanize|validate|kit|stage`
(migration note: orchestrate.py still carries the v2 16-group topology until the
wave-④ engine rebuild; this SKILL.md is authoritative — v3 briefs are generated from
`task/` playbooks). Layout: `checklists/ engine/ humanizer/ prompts/ sources/ task/
templates/ work/` — training curriculum: `task/14-training-and-refresh.md`.
