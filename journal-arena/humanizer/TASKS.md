# TASKS — the humanization workflow for one manuscript
### Nine steps (T0–T8), each with inputs, steps, and a numeric exit gate. Companion to `RULES.md` (the law) and `SKILL.md` (the skill file for LLM agents).

Working unit: one manuscript (title, abstract, body, references). All gates below are computed
with the tools listed in T0; never with a commercial detector (see T7).

---

## T0 · Baseline & setup (10 min, once per manuscript)
**Input:** final content draft.
**Steps**
1. Freeze content state: commit/save `draft_v0`; from here, style passes never edit science.
2. Extract plain text (strip template; keep paragraph breaks — they matter for counting, not for editing).
3. Run feature dump: `python3 -c "import sys; sys.path.insert(0,'scripts'); from metrics_lib import extract_features; …"`
   on title, abstract, body. Save `metrics_v0` — specifically: `L03b_aivocab16_per1k`,
   `L19_triads_n`, `L15_ingtails_per1k`, `P17_punct_entropy`, `T04_abs_len`, `X10_in_conclusion` (body).
4. Compute MTI (definition in SKILL.md) and write it at the top of `checklist.md`.
**Exit gate:** `metrics_v0` + MTI recorded. No editing yet.

---

## T1 · Title & abstract pass (the highest-signal surface)
**Why first:** title is the one place the *era* data gives a bright line — machine-vocabulary
in E&B titles jumped 0.64 → 1.13 → **8.28/1k** across the three windows; title length and
colons did *not* move since 2020 (don't touch them).
**Steps**
1. Title: remove every blacklist word (target: 0). Do **not** shorten or de-colonize it.
2. Abstract: apply Pass-1 sweep from SKILL.md (lexicals → delete-or-convert; "-ing tails" split;
   triads ≤1; "not-but" ≤1).
3. Length: if `T04_abs_len` − venue norm > +25 words (venue norms: EB/BL ≈ 200–215,
   Energy Reports ≈ 180–230), cut *evaluative scaffolding* first, method/limits last.
4. Numbers: every improvement claim gets value + unit + baseline; a standalone
   "significant/considerable/substantial" must be numbered or deleted. Missing? `[number needed]`.
**Exit gate:** title blacklist = 0 · abstract MTI ≤ 4 · claim-number match = 100% ·
`T04_abs_len` ≤ norm + 15.

---

## T2 · Body lexical sweep (mechanical, batched)
**Steps**
1. Global regex list (SKILL.md PASS-1 step 1). Process in batches of 10 occurrences max per editing
   sitting — each hit decided individually: delete vs convert. Conversions cite data already in
   the manuscript (never outside it).
2. Nominalization chains → verbs+agents (`we measured`, not `measurement of was performed`).
3. "align with best practice(s)/standards" → name the standard and the conformity status
   ("follows ISO 52016; weather file is 2015 TMYx").
4. Keep a `finds.md` log of every `[number needed]` you created for the authors to fill.
**Exit gate:** body blacklist density ≤ 4/1k · zero unconverted umbrella adjectives ·
`finds.md` handed to authors.

---

## T3 · Phrase-pattern surgery
**Steps**
1. All sentences ending `", -ing …"` → split (corpus anchors: EB abstracts 0.48 ⇄ 0.91/1k;
   within-author bodies +0.14, 29↑/11↓, p=0.001 — target: 0 remaining).
2. Triads: enumerate `X, Y and Z` matches; keep only load-bearing; cap 1/1,500 words.
3. "not X but Y": keep ≤1 in the whole paper, and only refuting a *named* belief.
4. Hedging audit (per paragraph): analysis sentences keep ≥1 hedge where evidence is partial;
   method sentences have 0; conclusion keeps 1 honest limitation-hedge. (Humans in this field
   hedge MORE: EB 3.57 ⇄ 1.84/1k — stripping hedges is the single most common
   "humanization" mistake; do the opposite.)
**Exit gate:** -ing-tails = 0 · triads ≤ cap · not-but ≤ 1 · hedge map attached.

---

## T4 · Rhythm & punctuation (bounded — do not over-engineer)
**Steps**
1. Read per 3-paragraph window: insert ≥1 <12-word verdict sentence where a paragraph
   over-argues; split/extend one sentence past 40 words where a chain of mid-length ones
   flattens. Purposeful only.
2. Punctuation breadth, not quota: replace full stops with `;`/`:` between tightly-related
   independent clauses (roughly once per page where natural); keep clarifying parentheticals.
   (Corpus: human punctuation entropy 3.07 ⇄ 2.77; within-author loss −0.18, p=1e‑5 — this
   *is* a real signature; the specific `;/,` ratio is not, so never set a semicolon quota.)
3. Explicitly forbidden: em-dash edits, bold edits, bullet↔prose conversion for style.
   Print-PDF bold ≈ 0 in both arms; dash tell obsolete; lists only judged by reader load.
**Exit gate:** `P17_punct_entropy` up ≥ +0.05 vs `metrics_v0` OR author override logged ·
0 forbidden edits executed.

---

## T5 · Structure & conclusions (the two verified moves)
**Steps**
1. Conclusion openers: delete `In conclusion|Overall|To summarize|In summary` paragraph
   starts (bodies, BL layer: 3.3 ⇄ 12.5 per 1k — EB bodies are not openly retrievable; within-author
   +1.96, 29↑/14↓, p=0.0067 —
   this is the strongest *structural* tell after vocabulary). Rewrite the opening sentence
   as the claim itself: "Retrofits cut winter gas use 6.2%; the 2021 scheme did not replicate it."
2. Last paragraph = limitation / number-to-remember / unsupported-claim — no restatement.
3. Headings and paragraph counts: **freeze** (corpus verdict: within-author p=0.55 / 0.29 —
   not author-level signals; venue templates govern them).
4. Dialogue-with-literature check (per major claim): one named prior work + how this paper
   agrees/diverges ("consistent with X (2019); unlike Kim (2021) who…"). No
   "studies have shown" anywhere.
**Exit gate:** conclusion-ritual = 0 · final-paragraph type ∈ {limitation, number, boundary} ·
headings diff = 0 · vague-citation count = 0.

---

## T6 · Integrity gate (before any re-scoring)
**Steps**
1. Diff `draft_v0` → `draft_v1` claim-by-claim: every number, unit, table/figure callout,
   citation, and heading identical or *author-approved*; every `[number needed]` resolved
   by an author (never by the editor/model).
2. Terminology sheet: one term per concept (flag any new synonym introduced by rewriting —
   remove it).
3. Zero-error law: spell-check + punctuation normalization (typos are not humanization).
**Exit gate:** content-diff = empty except approved lines · `[number needed]` count = 0 ·
0 unregistered synonyms.

---

## T7 · Optional: human blind review & (rejected) detector caution
**Steps**
1. If the venue team exists: exchange two paragraphs with a colleague, unlabelled, next to
   two paragraphs from a 2015 paper in the same journal; coders mark "reads machine". Record
   agreement, act on it qualitatively only. (This is the batch design from the study — 10 ⇄ 10
   blind packets; agreement α ≥ 0.70 before conclusions.)
2. Commercial "AI detectors": may be run for curiosity, **must not** change the text and must
   never be quoted to authors — published bias against ESL academic English (Liang et al.:
   >50% of TOEFL essays flagged; one 98%) makes verdicts unusable in an international field.
**Exit gate:** notes archived; no detector score in the manuscript file.

---

## T8 · Maintenance: re-calibrate per venue, per era
**Steps**
1. New journal/field? Before trusting MTI, sample ~100 human abstracts from the venue's
   *pre-2021* window and recompute baseline means for L03b / triads / -ing / punctuation
   entropy — then re-anchor the bands (default ≤4/1k may need ±50%).
2. Style drifts *within authors* (MTI +2.3/1k across careers, p=0.0004): a manuscript polished
   once in 2024 will score differently in 2026. Re-run T0 at every major revision cycle.
3. Quarterly: rerun the corpus pipeline (`scripts/05 → 11 → 14`) if you maintain the study;
   update the "known-tells" section of SKILL.md — tells age (em-dash died in ~2 years).
**Exit gate:** baselines dated < 12 months · SKILL.md version bumped on any threshold change.

---

### Master exit summary (the whole manuscript at once)

| gate | target |
|---|---|
| title blacklist hits | 0 |
| abstract MTI | ≤ 4 /1k |
| body MTI | ≤ 4 /1k (human-range ≈2–3; gray 4–8; machine >8) |
| "-ing tails" | 0 |
| triads | ≤ 1 per 1,500 words |
| "not X but Y" | ≤ 1 per paper |
| conclusion-ritual openers | 0 |
| claim ↔ number pairing | 100% (or `[number needed]`, authored) |
| hedging in analysis | ≥ 1 per 3 paragraphs |
| headings/paragraph geometry edits | 0 (frozen) |
| content diff vs `draft_v0` | only approved lines |
| typo count | 0 |

*Rules with measured corpus support: T1 (title 0.64/1.13/8.28 era jump), T2 (3.3⇄14.5),
T3 (EB -ing 0.48⇄0.91; within-author +0.14, p=0.001; hedging 3.57⇄1.84), T4 (entropy 3.07⇄2.77; within-author
−0.18), T5 (In-conclusion 3.3⇄12.5; freeze-rule from p=0.55/0.29 non-replication),
T6–T8 from the study's ethics and design. Full numbers: `outputs/ANALYSIS_v1.md`,
`outputs/M08_authors.md`, `outputs/M08_bodies.md`, `outputs/era_drift_EB.md`.*
