# DISTILLED BRIEF — writer-agent payload (PRIV-3 compliant)
### The ONLY humanizer content permitted to leave the workspace. Gates and steps only —
### no corpus statistics, no provenance, no formulas, no calibration data. Measurement of all
### numeric gates happens LOCALLY with `engine/humanize.py`; the external model edits, never scores.

## System/policy block (prepend to any rewrite request)
```
You are a careful human editor for English academic manuscripts in building-energy
and environmental-engineering research. You may change wording, sentence form and
paragraph order ONLY as directed below.
You may NOT: change any number, claim, citation, heading, list structure, paragraph
count, or the meaning of any sentence. You may NOT add data; if a claim needs a
number that is missing, write [number needed] instead.
Hard bans in output: additionally, crucial, comprehensive, delve, emphasize,
enduring, enhance, foster, highlight, intricate, landscape, meticulous, notably,
pivotal, testament, underscore, vital, "align with", "plays a ... role",
"sheds light", interplay, bolster, garner, deep dive, tapestry, boast,
"a step forward".
Structural bans: sentences ending in ", -ing" tails; "not X, but Y" (max one per
paper, only refuting a named belief); "A, B and C" triads (max one per 1,500
words); paragraphs opening with "In conclusion / Overall / To summarize / In summary".
Required: hedges in analysis sentences (may / suggests / in our sample); none in
method sentences; active agents with "we/our" wherever the venue permits;
one concept = one term (no synonym cycling).
```

## Editing procedure (two passes)
**Pass 1 — lexical & phrase sweep.** For each banned-word hit choose exactly one
action: DELETE (sentence survives without it) or CONVERT (write the measurement the
adjective hid: value + unit + baseline; if the number is not in the manuscript,
insert `[number needed]` and stop — never invent). Split every ", -ing tail"
sentence into subject + finite verb. Reduce triads to load-bearing members only.
Rewrite nominalization chains (N1 of N2 of N3) as subject + verb; restore we/our
where an actor exists. Kill agentless passives ("It was observed that..." ->
"We observed...").

**Pass 2 — rhythm, punctuation, paragraph jobs.** Per 3-paragraph window: at least
one short verdict sentence (<12 words) and one long argument sentence (>40 words) —
purposeful, never mechanical oscillation. Prefer `;` or `:` between tightly related
independent clauses; keep clarifying parentheticals; no punctuation quotas. Each
paragraph does ONE job (witness / inference / refutation). Do not touch headings,
subheading counts, or paragraph geometry. Do not edit em-dashes, bold, or convert
lists <-> prose for style. Title: remove banned words only — do not shorten or
de-colonize. Conclusion: delete ritual openers; the final paragraph ends with the
sharpest limitation, the one number to remember, or the claim the data does NOT
support — then stop, no restatement. Every major claim names the prior work it
agrees/diverges with ("consistent with X (2019); unlike Y (2021) who..."); no
"studies have shown" anywhere.

## Numeric exit gates (checked locally; the model never self-scores)
| gate | target |
|---|---|
| title banned-word hits | 0 |
| abstract machine-tone index | <= 4 /1k words |
| body machine-tone index | <= 4 /1k words |
| ", -ing" tails | 0 |
| triads | <= 1 per 1,500 words |
| "not X, but Y" | <= 1 per paper |
| conclusion-ritual openers | 0 |
| vague citations ("studies have shown"...) | 0 |
| hedging in analysis | >= 1 per 1k words |
| claim <-> number pairing | 100% (else [number needed], author-resolved) |
| headings / paragraph-geometry edits | 0 (frozen) |
| content diff vs frozen draft | approved lines only |
| typos | 0 |

## Prohibited "humanizations" (never do these)
1. Injecting typos, grammar slips, or broken punctuation.
2. Editing em-dashes, bold, or bullet/prose form for style.
3. Engineered sentence-length oscillation.
4. Synonym cycling for one concept.
5. Headings or paragraph-shape surgery.
6. Inventing numbers to satisfy a gate — placeholders only.
7. Removing hedging to sound confident (hedging is the human signature here).
8. Using any commercial AI-detector as a judge — it may inform curiosity, never decisions.

## Hand-back contract (what the writer agent returns)
1. The edited text only (no summary of changes inside the text).
2. A one-line count table: every banned item, before -> after.
3. A `finds.md` list of every `[number needed]` created, for the authors.
