# ARENA — paste this whole block, then state your task

You are running ARENA. Read this block once, then execute it on the TASK.

**TASK** = the request the user just made. If they pasted this block with no task, the TASK is
their most recent request in this conversation, and your last answer to it is the BASELINE (the
answer they were not satisfied with).

You are the orchestrator. You do not compete and you do not get to skip rounds.

---

## BUDGET — pick one tier, say it in one line, then start

| tier | candidates | rounds | use when |
| --- | --- | --- | --- |
| light | 4 | 2 | a short answer, a headline, a small decision |
| normal | 8 | 3 | most tasks, most writing, most plans |
| hard | 16 | 4 | the user is unhappy, the task is long, the stakes are real |

Never go past 16 candidates in a single reply. If the task is huge, say so and offer 16 with a
second pass instead of pretending to run 100.

## STEP 1 — the task file (internal, five lines at most)

Restate: the request in the user's own words; every stated constraint (audience, length, format,
stack, deadline, must-not-change); what "done" looks like; and if there is a BASELINE, exactly what
was wrong with it, in their words. Everything below is judged against this file and nothing else.
Do not add requirements the user never gave.

## STEP 2 — deal the cards

Every candidate gets a distinct card: one reasoning mode × one workflow × one strategy, no repeats.

Reasoning modes: first principles · inversion (what would make this fail) · constraint first ·
working backwards from the finished result · adversarial reviewer · analogy from another field ·
cheapest test first · expected value · pre-mortem · steelman the opposite · decompose by owner ·
base rates first · user-journey · failure-mode-first · relax the tightest constraint · find the
binding constraint.

Workflows: requirements checklist · outline first · three drafts then pick · red-team pass ·
minimal answer then extend · example-driven · decision table · timeline · cost/benefit ·
reference implementation · test-first · question-and-answer pairs.

Strategies: numbers, names and steps instead of adjectives · shortest correct answer · pre-empt the
three most likely objections · make every claim checkable · plain language, no jargon · prefer
reversible options · do the hard part first · quantify the trade-off · name the failure mode and its
fix · end with one executable next step · state assumptions explicitly · write for the harshest
expert reader.

## STEP 3 — the candidates (internal, never shown unless asked)

Write N complete, standalone answers, one per card. Rules that make the tournament real:

- Draft each candidate from its card, not from the candidate you wrote just before it.
- No candidate may reuse another's sentences. Overlap only where the facts force it.
- Each candidate is a finished answer, in full, ready to hand to the user.

## STEP 4 — the bracket (internal, single elimination, seeded in draw order)

For **every match**, run all three passes:

1. **ATTACK.** For solution A, list the strongest concrete attacks (tag each MAJOR, MINOR or FATAL):
   a false claim, a missed requirement, a step that cannot be executed, a counterexample, a
   constraint broken. Same for B against A's solution.
2. **DEFEND.** For each attack: CONCEDE and fix it, or REBUT with evidence from the task or a
   concrete check. A rebuttal that only insists you are right counts as a concession. Strip every
   rejected claim out of the candidate.
3. **JUDGE.** Score both revised candidates on the rubric. Higher weighted total wins. A verdict
   marked FATAL cannot beat one that is not fatal, whatever the totals say.

Judges never know the cards and never reward length, confidence, or writing about quality.

## THE RUBRIC — 0 to 10 on each, use the whole scale (7 is not a polite default)

| criterion | weight | the question |
| --- | --- | --- |
| Correctness | 30 | nothing false, no logic error, no step that cannot be run |
| Completeness | 25 | every requirement the task states — judged against the task, not against taste |
| Specificity | 15 | the reader can act on it right now, without guessing |
| Robustness | 20 | every attack fixed or correctly rebutted, nothing new broken |
| Clarity | 10 | obvious how to use it, no padding |

Weighted total = (correctness×30 + completeness×25 + specificity×15 + robustness×20 + clarity×10) / 10.

Ties: fewer standing attacks wins; then higher correctness; then the one you would hand over, and
say why in one line.

## STEP 5 — merge, then finalise

The champion is not finished. Apply every fix that was conceded anywhere in the tournament to the
surviving answer, if the fix survives scrutiny. One answer leaves.

## STEP 6 — output, and this is all the user sees

In the language of the TASK:

1. **The champion** — the full answer, clean, with no trace of the tournament in it.
2. **Its card** — one line: reasoning mode + workflow + strategy.
3. **Rounds** — e.g. "8 candidates in, 3 rounds, 1 left."
4. **The attacks it survived** — 3 to 6 one-liners, concrete.
5. **Against the rejected answer**, if there was one — honestly, including the case where the old
   answer wins on some point.
6. **What the arena could not fix** — the champion's remaining weaknesses, stated plainly.

## RULES

- Do not narrate the tournament. No candidates, attacks, scores or brackets on screen unless the
  user says "show the bracket".
- Never invent facts to fill a card. Uncertainty stays uncertainty, and it survives into the champion.
- If the task is a code change, the champion is the code, not a description of the code.
- If the task touches health, law, money or safety, correctness and the fatal rule outrank
  everything, and the champion must say what a human still has to check.
- If the user says "again" or "arena again": take the champion as one entrant, run a fresh set of
  cards against it, and report the new survivor. That is round two, not a rewrite.
