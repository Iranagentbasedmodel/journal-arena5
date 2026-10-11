# Skill: journal-arena — سخت‌داوریِ هم‌محور مقاله و اصلاح ردیاب‌پذیر برای Energy & Buildings

Portable, **model-agnostic** editorial board: duty-separated review agents that **study the
28-source corpus live**, verify sources on the web (read-only license), produce a ranked
revision matrix, resolve conflicts in an arena bracket, and apply only author-approved
revisions — goal: **acceptance at Energy & Buildings (ENB)**, never gratuitous critique.

## 0. The four laws (every agent, every model, every phase)
1. **Axis law** — every finding serves the manuscript's core claim (leakage-audited,
   uncertainty-calibrated, energy-conserving residential energy prediction from RECS 2020
   microdata, honest nulls, retrofit bounds) OR an explicit ENB requirement.
   Missing `axis_link` ⇒ `validate.py` rejects.
2. **Evidence law** — exact `quote` + rule id (`ENB-*`, `POL-*`, `SAGER-*`, `DAT-*`, `CRED-*`,
   `REF-*`, `CLM-*`, `TTL-*`) or quarantined.
3. **Traceability law** — no in-place edits; only approved `revisions.json` → new file +
   CHANGELOG + point-by-point letter.
4. **Claim-size law** — no claim, suggestion or revision bigger than the evidence
   (evidence ladder L1 measured → L4 speculative; checklists/07). G11 meta-audits every
   other agent's suggestion; inflated rows are quarantined by `review_matrix.py`.

## 1. Pipeline (files in/out, resumable via work/plan.json `next`)
```
P0  map        engine/manuscript_map.py            -> work/manuscript-map.json
P1  precheck   engine/precheck.py                  -> work/precheck-report.{md,json}
P1.5 LEARNING  each agent studies its SRC ids LIVE -> work/playbooks/<gid>-playbook.md
P2  review     engine/orchestrate.py --mode division (16 duty groups, waves of 10)
                                                   -> work/findings/<aid>.json
P3  matrix     engine/review_matrix.py             -> work/review-matrix.{md,json}
P4  arena      engine/orchestrate.py --mode arena  (contested edits only; rubric incl. claim_inflation)
P5  approve    author sets approved:true           -> work/revisions.json
P6  apply      engine/apply_revisions.py + validate.py -> ms_revN.txt + CHANGELOG + point-by-point
P7  kit        checklists/06 + templates/          -> inventory, cover letter, highlights, GA
P8  response   templates/response-letter.md        -> work/response-letter.md
```

## 2. Duty-separated topology (16 groups; --agents 16…100; each duty = ONE part)
G1 **TITLE (dedicated group)** · G2 abstract · G3 keywords/highlights/graphical abstract ·
G4 introduction-gap · G5 **literature review (پیشینه)** · G6 **methodology & coding** ·
G7 **data** · G8 results-consistency · G9 statistics-UQ · G10 discussion-claims ·
G11 **recommendations + meta-audit of suggestions (ضد اغراق)** · G12 references-integrity ·
G13 ethics-policy (AI/CRediT/COI/SAGER) · G14 formatting-kit · G15 language-style ·
G16 reviewer-simulation (2 reviewers + editor meta-review).
Each brief = Phase A learning (write playbook with urls + access dates) → Phase B review.
Arena (contested edits): strategy cards (conservative-editor, reviewer-2-adversarial,
statistician, policy-auditor, plain-language, scope-guardian, data-steward, typesetter,
claim-auditor), single-elimination, rubric
`3*axis + 2*journal + 2*evidence + (5-risk) + (5-effort) + 2*(5-claim_inflation)`, median of 3 judges.

## 3. Source corpus & verification license (sources/CORPUS.md)
28 sources (manuscript, EASE SAGER PDF, Springer SAGER table, Elsevier GenAI/ethics/data/
LaTeX/highlights/GA/share-link pages, NISO CRediT, ISSN LTWA, CSL, Mendeley, Researcher
Academy, EM pre-submission video, ENB guide/insights/call-for-papers, arena-skill repo).
Every agent may fetch/search public pages read-only to VERIFY (references via CrossRef/DOI,
dataset versions, journal scope, LTWA, policy wording) and records `verified_via` with access
dates. **Forbidden:** uploading manuscript text to any online/GenAI tool (POL-AI-5),
submitting, contacting humans. Offline runtimes fall back to checklists/ (`source_mode: distilled`).

## 4. Model-agnostic contract
Plain JSON/Markdown state only; deterministic scripts for everything computable; each brief
self-contained (role, duty boundary, SRC ids, schema, laws) so ANY chat model can run it by
copy-paste; `validate.py` is the schema+evidence gate; `orchestrate.py next` resumes after
context compaction; numbers never invented (derived values need formula in rationale).

## 5. Layout
```
skills/journal-arena/
├── SKILL.md · README-fa.md
├── sources/CORPUS.md            28 sources + verification license
├── checklists/01-enb-guide … 06-submission-kit, 07-claims-and-overclaim, 08-title-front-door
├── engine/ manuscript_map.py precheck.py orchestrate.py review_matrix.py
│           apply_revisions.py validate.py
├── templates/ finding.schema.json revisions.schema.json statements.md
│              submission-inventory.md response-letter.md
└── task/00-intake … 07-response-to-reviewers (+01b-playbooks)
Demo (no revisions applied): arena-portable/demo-paper/
```
