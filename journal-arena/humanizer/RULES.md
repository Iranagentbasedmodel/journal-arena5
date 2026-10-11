# RULES — De-machine-ing English Scientific Prose
### A countable rulebook for Energy & Buildings–field manuscripts (English text only)

Every rule below states: **directive → numeric target → how to check → example**.
Every rule is anchored in measured distributions from our six-journal, three-era corpus
(abstracts 2010–2020 ⇄ 2025H2–2026, 120 full bodies, 139 within-author pairs, and a
1990s calibration window of 582 E&B titles). Bracketed evidence tags show where a number
comes from. Rules are *style* rules only — they never touch claims, data, or citations.

> **Prime directive.** Humanizing = restoring *judgment, agenthood, and rhythmic variety*
> to prose that has become uniformly fluent. It is NOT error injection, NOT cosmetic
> variety, and NOT fabrication. If a number is missing, leave `[number needed]` — never
> let a model invent one.

---

## R1 · Lexical rules (strongest evidence in the corpus)

**R1.1 — Umbrella-adjective blacklist.** These words are 5–7× over-represented in
post-2024 prose in this field (EB abstracts: 3.3 ⇄ 14.5 hits/1k words; Buildings full
bodies: 2.1 ⇄ 14.5, δ = −1.0; and they *increase within the same authors* over time,
+2.3/1k, p=4e‑4). Delete or convert every occurrence:

    additionally · crucial · comprehensive · delve/delves into · emphasize/emphasizing ·
    enduring · enhance/enhancing · foster/fostering · highlight/highlighting · intricate ·
    landscape (= "field") · meticulous(ly) · notably · pivotal · testament · underscore ·
    vital · align with
    secondary list: interplay · bolster · garner · deep dive · boasts · tapestry ·
    "plays a vital/key role" · "sheds light" · "a step forward"

*Conversion*, not deletion, is the preferred move: the adjective was hiding a measurement.

    ✗ The comprehensive framework enhances retrofit outcomes.
    ✓ The framework cuts monthly meter error to <6% across 42 buildings.
    [target] blacklist density ≤ 4/1,000 words; [check] grep -i -o "\bword\b" | count

**R1.2 — One concept, one term; no thesaurus spin.** Elegant variation (model-era synonym
cycling: *approach/method/framework/strategy* for the same thing within one page) reduces
readability for reviewers. Pick one term per concept; list it in the terminology sheet.
[Evidence note: "elegant variation" was an older-model artifact, now weak as a detector —
but still bad for readers; keep it as a quality rule, not a tell.]

**R1.3 — Evaluative adjectives must be earned or removed.** Density of self-praise
(*significant, remarkable, substantial, robust, seamless, novel*) is 2–4× higher in the
suspicious arm (EB 3.6 ⇄ 7.7/1k). Each surviving occurrence must sit next to the number
that earns it: *robust → within 10% for noise ≤0.5 K; diverges beyond that*.

---

## R2 · Phrase-pattern rules

**R2.1 — Break obligatory triads.** "A, B and C" list-clauses appear in ~1.06/abstract in
the suspicious arm vs 0.20 human (ER). One triad per 1,500 words maximum. Either drop the
weakest member or give each member its own condition/number.

    ✗ …fosters resilience, efficiency and sustainability.
    ✓ …cuts peak load 11% — measured only in climates where nights stay below 18 °C.

**R2.2 — No detached "-ing tails".** ", ensuring X / highlighting Y / providing Z"
sentence-final participles are the most transferable machine tell to body text
(full bodies: δ −0.60…−0.92 across four journals; rises *within* authors too, p=0.0013).
Split: subject + finite verb + object.

    ✗ …was repeated three times, ensuring reproducibility.
    ✓ …was re-run three times; spread stayed under 0.4%.

**R2.3 — "not X, but Y": at most one per paper.** Count: 0.03 ⇄ 0.16–0.29 per abstract;
body texts 1.2 ⇄ 5.9 occurrences (EB/BL arms). Allowed only when it refutes a named,
actually-held misconception.

**R2.4 — Kill agentless passive where an actor exists.** "It was observed that…",
"The implementation of the assessment was performed…" → "We observed…", "We implemented…".
Our corpus: first-person density in Frontiers-in-Energy abstracts 2.90 ⇄ 0.83/1k — the
suspicious arm strips agents. [check: "we/our" ≥ 2/1k where the journal allows first person]

---

## R3 · Rhythm rules (gentle — the corpus says rhythm is partly a myth)

**R3.1 — Vary sentence length *naturally*, don't engineer it.** Sentence-length CV shows
no consistent population gap at abstract level (EB 0.34 ⇄ 0.33) — mechanical "length
oscillation" games are unsupported. What *does* survive: within 3 paragraphs, have ≥1
short punch line (<12 words) and ≥1 long argument sentence (>40 words). Purposeful, not random.

**R3.2 — Never open two consecutive sentences with the same structure** ("The results… The
results…"), and **do not** try to *increase* sentence-opening variety to look human: opening
diversity is *higher* in machine text in this field (L20 entropy reverses in 5/6 layers).
You cannot out-vary the model; cut the formulaic connectors instead (R5.2).

---

## R4 · Punctuation rules

**R4.1 — Punctuation *entropy* is a real, small, verified human signature.** Human arms
show a more varied mark mix (EB 3.07 ⇄ 2.77, δ=+0.64; it survives within-author: −0.18/period,
p=1e‑5). Practical: when two independent clauses are related, prefer `;` or `:` over full stop;
let parentheticals exist where they clarify. **Do not** impose quotas ("3 semicolons per 100
commas") — the semicolon *ratio itself* is not discriminative (P03 n.s.); it's the distribution
breadth that matters.

**R4.2 — Em-dashes, bold, bullet-mania: hands off.** Dash-frequency and bold-usage carry no
signal in this corpus (X18 bold ≈ 0 in *both* arms of print-derived PDFs; the em-dash tell was
already obsolete by 2026 as flag models learned to suppress it). Editing these is theater.

**R4.3 — Quotation marks stay for terms and speech only;** curly-vs-straight is a typesetting
artifact, not a style choice — never "humanize" with it.

---

## R5 · Paragraph & section rules

**R5.1 — Conclusion paragraphs must not open with a ritual.** "In conclusion / Overall /
To summarize" frequency in full bodies: BL 3.3 ⇄ 12.5 per 1k (FE 1.8 ⇄ 6.5); it rises
*within the same authors* over time (+1.96, p=0.007). End the paper instead with one of:
the sharpest limitation, the single number to carry away, or what the data refuses to support.

**R5.2 — One argument connector per paragraph is the *maximum*, not the goal.**
"Moreover/Furthermore/Additionally" as sentence-openers: cut to ≤2 per page. Human text in
this corpus uses connectors at ~1.1–1.8/1k in *both* arms — this rule is about reader load,
not detection.

**R5.3 — Do NOT touch headings or paragraph geometry as "humanization".** Subheading
inflation and paragraph fragmentation look like AI signatures in population means
(heads/1k: FE 1.2 ⇄ 3.8; para lengths 487 ⇄ 245), but **they do not replicate within the
same authors** (p=0.55 and p=0.29) — they are venue/generation drift. Editing them changes
nothing about humanness and damages journal template compliance. One deliberate exception:
write headings that name the question ("Peak-load shift under night setback") when the venue
allows it — for readers, not for detectors.

**R5.4 — Paragraphs do one job** (witness / inference / refutation). If a paragraph does
two, split; if zero, cut. [universal editorial rule; kept because the suspicious arm's short
fragments (1–2-sentence paragraphs: FB 0.12 ⇄ 0.35 of body paragraphs) show what happens
when rhythm outruns argument.]

---

## R6 · Title & abstract rules (era-calibrated)

**R6.1 — Do not "fix" colon-heavy or long titles.** The colon title and the 15-word title
are *30-year genre drift*, fully pre-AI: E&B titles of the 1990s average 10.6 words with
13% colons; 2010–2020, 14.9 words with 45%; 2025–26 suspicious: 15.1 words, 46% — flat
since 2020 (δ(A⇄H)=+0.003). Reverting them reads as anachronism, not humanity.

**R6.2 — But scrub markers from titles.** Machine-vocabulary density in titles is the one
title metric that jumps post-2020: 0.64 (1990s) ⇄ 1.13 (2010s) ⇄ **8.28**/1k (2025–26),
p=0.0098. A "Comprehensive…: A Novel… for Pivotal…" title is a costume — title gets
0 blacklist words, and "novel" only if the field's convention demands it (≤2.7% of titles
in the suspicious arm; 0 in 1990s).

**R6.3 — Abstract length: return toward venue baseline.** Suspicious EB abstracts run
+41.6 words over their own journal's human arm (197 ⇄ 239) and abstract inflation is
genuinely within-author (+24.5 words, p=0.0004). If the venue norm is ~200, ship ~180–210.
Trim by removing evaluative scaffolding (R1), not by deleting method or limits.

**R6.4 — Numbers: match each *claim*, not a quota.** Raw digit-count per abstract is higher
in the suspicious arm (EB 0.70 ⇄ 1.34) — models sprinkle figures; the real gap is *claim-bound*
quantification (share of abstracts with **no decimal figure** is higher in the human arm:
BL 0.84 ⇄ 0.43). So the rule: every improvement claim carries value+unit+baseline; every
standalone "significant" without a number is either numbered or deleted.

---

## R7 · Voice & epistemics rules (the counter-intuitive cluster)

**R7.1 — Hedging is human here; protect it.** In this field, human arms hedge *more*
(EB 3.57 ⇄ 1.84/1k; ER 2.28 ⇄ 0.70) — reversing the popular "AI is too cautious" story.
Keep may/might/suggests in analytic sentences; delete them from method descriptions.
Note the era warning: hedging has been *declining within authors* (−1.11/1k, p=0.016) —
so "brave naked claim" style is 2026 genre drift, AI or not; if you want human-and-old-school,
hedge honestly.

**R7.2 — Cite by name where you position yourself.** "Consistent with Alvarez (2019) for
offices; contradicts Kim (2021) — their sample lacks night setback." The suspicious arm
defaults to vague communal attribution ("studies have shown"); within-literature dialogue is
cheap, reader-trusting, and machine-rare.

**R7.3 — Let one judgment show, once, with a witness.** "We consider the 2015 TMY a
limitation for the summer scenarios; it biases savings upward." One. With data. (This is the
"author's voice" fingerprint — the corpus cannot count it, and that's exactly why it works.)

---

## R8 · Prohibited "humanizations" (each of these is either neutral or harmful)

1. Typos, grammar slips, broken punctuation, random half-widths — zero discriminative value,
   pure editorial damage.
2. Deliberate em-dash removal or insertion (R4.2).
3. Forced list→prose or prose→list conversion (X18/lists ≈ 0 effect in print PDFs).
4. Length "oscillation" engineered per sentence (R3.1).
5. Synonym-cycling (R1.2 in reverse).
6. Headings or paragraph-shape surgery (R5.3).
7. Invented numbers to satisfy R6.4 — placeholders only.
8. Removing hedging to sound "confident human" (R7.1 shows caution is the human signature here).
9. Second opinions via commercial AI-detectors as gatekeepers — biased against ESL authors in
   published tests (Liang et al.); may inform, never decide.

---

### Appendix A — Machine-Tone index (MTI) for a quick score

MTI = (blacklist hits + triad hits + "-ing-tail" hits) / total words × 1000, on the abstract.
Calibrated bands from our EB arm distributions: **≤4 = human-range** (human mean 3.3),
4–8 = gray, **>8 = machine-range** (suspicious mean 14.5). Full-body variant (18+9 list,
per 1k): human-range ≈2, suspicious ≈9–14. Run `scripts/metrics_lib.py` (fields
`L03b_aivocab16_per1k`, `L19_triads_n`, `L15_ingtails_per1k`) to compute honestly.

### Appendix B — what each rule's evidence tag means

*population* = arms of 1,176 abstracts / 120 full bodies across six journals;
*within-author* = 89 abstract pairs / 50 body pairs, same author, same journal, two eras —
the design that neutralizes venue-template and author-generation effects;
*era* = 582 E&B titles of the 1990s as the deep-time baseline.
