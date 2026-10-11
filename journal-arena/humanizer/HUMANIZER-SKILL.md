# Humanizer-Academic-EN — a skill for de-machine-ing English scientific prose
### (energy & buildings field, journal-norm aware; built on a 1,176-text six-journal corpus, 120 full bodies, 139 within-author pairs, and a 1990s calibration window)

```
name: humanizer-academic-en
version: 1.0
domain: English academic manuscripts (Energy and Buildings and sibling venues)
task: rewrite draft prose so it carries an author's judgment, agents, and varied rhythm,
      WITHOUT changing claims, numbers, citations, headings, or paragraph geometry.
never: fabricate numbers; inject errors; touch scientific content; use a detector as a judge.
```

## When to use
- After the *content* draft is final and before submission/language-service handoff.
- When the MTI (see Scoring) of your abstract exceeds 4/1k, or your title contains any
  blacklisted marker word.
- When a paper has gone through one or more LLM "polish" passes (each pass measurably moves
  prose toward the suspicious-arm distribution — see *Within-author drift* in Scoring).

## Operating model (read this first)
Three facts from the corpus decide everything below:
1. **What survives within-author comparison**: machine-vocabulary density, "-ing tails",
   triads, "not X but Y", conclusion-ritual openers, punctuation-entropy loss, and abstract
   inflation. These are the real targets.
2. **What does NOT survive**: subheading counts, paragraph-fragmentation, title length and
   colon titles (all of those are 1990s→2020s genre drift or venue template; editing them is
   theater), em-dash and bold tells (obsolete / near-zero in print), first-person rules
   outside one venue.
3. **The reverse tells**: humans in this field *hedge more*, not less (keep hedging in
   analysis!), and machine text *opens sentences with MORE variety*, not less — so the
   popular "vary your sentence openings" advice is counter-productive here.

## The procedure (two passes + audit)

### PASS 1 — Lexical & phrase-pattern sweep
1. Detect (regex, case-insensitive, whole words):
   `additionally|crucial|comprehensive|delv\w*|emphasiz\w*|enduring|enhanc\w*|foster\w*|
   highlight\w*|intricate|landscap\w*|meticul\w*|notably|pivotal|testament|underscor\w*|vital`
   plus phrases: `plays a (vital|crucial|pivotal|key) role|sheds? light|interplay|bolster\w*|
   garner\w*|deep dive|tapestries?\b|boast\w*`
2. For each hit, choose exactly one action:
   - **DELETE** if the sentence survives without it;
   - **CONVERT** by writing the measurement the adjective hid: value + unit + baseline
     (if the number is not in the author's data → insert `[number needed]` and stop there —
     never invent).
3. Split every sentence ending `", (ensuring|highlighting|providing|enabling|reflecting|
   supporting|fostering) …"` into a new sentence with a subject and a finite verb.
4. Triads `X, Y and Z`: keep only if all three are load-bearing; otherwise drop the weakest
   or give each member its own condition. Hard cap: 1 per 1,500 words.
5. `not (merely|just|so much)? …, but …`: keep at most 1 per paper, and only when the
   refuted belief is named and real.
6. Nominalization chains `N1 of N2 of N3` (implementation/evaluation/investigation/
   optimization…): rewrite as subject + verb ("we implemented…"). Restore "we/our" where the
   venue allows it and an actor exists.

### PASS 2 — Rhythm, punctuation, paragraph jobs
1. Per 3-paragraph window: ≥1 sentence <12 words (a verdict) and ≥1 sentence >40 words
   (an argument). Do not chase any other rhythm statistic.
2. Punctuation: where two independent clauses are tightly related, use `;` or `:` instead of
   a full stop; keep one `(` … `)` where a qualification belongs. Breadth of marks, not quota.
3. Paragraphs: one job each (witness / inference / refutation). Do not merge or split for
   appearance.
4. Conclusion: delete any opening of `In conclusion|Overall|To summarize|In summary`;
   close with one of: the sharpest limitation, the one number to remember, or the claim the
   data does NOT support. Then stop — no restatement.
5. Analysis sentences keep their hedges (`may`, `suggests`, `in our sample`); method
   sentences lose theirs (`we measured`, not `we may have measured`).

### AUDIT — score before/after and hand back a diff summary
Compute on the edited text: hits/1k of the PASS-1 list, triad count, -ing-tail count.
Exit gate: **MTI ≤ 4** for abstracts; **0 blacklisted words in the title**; **no `[number
needed]` left unanswered** before submission. Report the three counts to the author in one
line (they are the author's property, not a verdict on them).

## Scoring

**MTI (Machine-Tone Index)** = (blacklist hits + triad hits + -ing-tail hits) / words × 1000,
computed on the abstract (or body). Calibrated bands from the EB arm means:

| band | MTI | meaning |
|---|---|---|
| human-range | ≤ 4 | matches 2010–2020 human mean (3.3/1k) |
| gray | 4–8 | partially polished |
| machine-range | > 8 | matches 2025–26 suspicious mean (14.5/1k) |

*Within-author drift* (why MTI decays and why re-running this skill is a maintenance task,
not a vanity): in 89 same-author pairs, abstract MTI vocabulary rose **+2.28/1k** between
their 2010s paper and their 2025–26 paper (p=0.0004; 47 up vs 19 down), and on full bodies
**+1.18/1k** (p=2.5e‑5). Prose drifts toward the machine distribution even without anyone
"using AI" — through shared tools, shared polishing, and shifting genre norms.

Era guard: MTI is only meaningful against a *venue+era* baseline. Re-calibrate before trusting
thresholds in a new field (see `scripts/14_era_drift_titles.py` for the recipe).

## Ready-to-paste LLM prompts

**System/policy block (prepend to any rewrite request):**
```
You are a careful human editor for English academic manuscripts in building energy research.
You may change wording, sentence form and paragraph order ONLY as directed below.
You may NOT: change any number, claim, citation, heading, list structure, paragraph count,
or the meaning of any sentence. You may NOT add data; if a claim needs a number that is
missing, write [number needed] instead.
Hard bans in output: additionally, crucial, comprehensive, delve, emphasize, enduring,
enhance, foster, highlight, intricate, landscape, meticulous, notably, pivotal, testament,
underscore, vital, "plays a … role", "sheds light", interplay, bolster, garner, deep dive,
tapestry.
Structural bans: sentences ending in ", -ing" tails; "not X, but Y" (max one per paper);
"A, B and C" triads (max one per 1,500 words); paragraphs opening with
"In conclusion/Overall/To summarize".
Required: hedges in analysis ("may/suggests/in our sample"); none in method;
active agents with "we" wherever the venue permits.
```

**Task prompt (Pass 1):** "Return the abstract rewritten per the policy block, plus a one-line
count table of every banned item before → after. Do not summarize your changes."
**Task prompt (Pass 2):** "Now rewrite only the final paragraph of the Discussion per the policy
block. It must end with either a limitation, the single number to carry away, or the claim the
data refuses to support."
**Self-audit prompt:** "Score this text: (1) count banned words per 1,000; (2) count '-,' tail
sentences; (3) count triads; (4) check first two words of the last paragraph. Output four
numbers only."

## Integration (tools in this workspace)
- `scripts/metrics_lib.py` → `extract_features(title, abstract, body=...)` returns
  `L03b_aivocab16_per1k`, `L19_triads_n`, `L15_ingtails_per1k`, `P17_punct_entropy`, …
- Quick CLI-style check on a pasted abstract:
  `python3 - <<'PY' … from metrics_lib import extract_features; print(extract_features(open('t.txt').read()))`
- Batch scoring before/after submission edits: run `scripts/05_run_analysis.py --limit` style
  feature dumps against your own file, compare MTI.

## Known limits (say them out loud)
The suspicious arm is defined by *style scores*, not authorship. This skill makes prose
read like 2010–2020 human practice in this field — it does not certify non-machine
authorship, and no reviewer should treat its output as evidence of either.
