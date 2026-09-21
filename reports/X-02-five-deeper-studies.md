# X-02 — Five Deeper Studies the Data Can Carry

*Written 2026-09-21 · supersedes the positioning-against-papers approach of
[`X-01`](X-01-five-articles-against-the-literature.md), which is kept as a record*

[`X-01`](X-01-five-articles-against-the-literature.md) proposed five articles
defined by their stance toward published papers. That makes them safe and
shallow: each one says "we agree / disagree with X" and stops. This report
starts from the other end. It asks **what questions this corpus can answer that
no other available dataset can**, because of the joins it uniquely permits —
an intent record (the journal), a commit record with retained pre-squash
history, an issue tracker with a known human tester, a CI history, a
mutation-testing baseline, and **fourteen frozen checkouts of the module on
disk spanning 2025-11 → 2026-09** (§0.2). Each of the five studies below is a
question developers using coding agents actually argue about, and for which
the field has essentially no artifact-based evidence. Each was **piloted on
2026-09-21** against the CSVs before being proposed; the pilot numbers are
reported as uncorrected and labelled as such.

---

## 0. Ground rules and what is newly on disk

### 0.1 What "deeper" means here

A study is in this report only if it meets all four:

1. **The question is one practitioners are currently guessing about** — not
   one the literature has already settled and we merely instantiate.
2. **It needs a join that only this corpus supplies.** If it could be done on
   any public repository, it is not here.
3. **It has a falsifiable prediction with a direction**, and the pilot did not
   already refute it. Where the pilot ran the *opposite* way, the study is
   listed in §5 with the number, not promoted.
4. **The unit of analysis is inside the project** (commits, lines, mutants,
   bugs, sprints, sessions) so that n is in the hundreds or thousands, not 1.
   The n = 1 caveat still binds any claim about AI-assisted development in
   general; it does not bind claims about *what happened here*, tested across
   hundreds of units.

### 0.2 Assets this review located that the earlier reports did not use

| Asset | Where | Why it matters |
|---|---|---|
| **14 frozen checkouts of `stripe`** dated 2025-11-25, 2026-01-27, 01-28, 02-03, 02-09 (×2), 03-24, 03-25, 05-05, 05-18, 05-20, 05-21, 09-18 (+ a 2024 ancestor) | `/home/dtkachev/osc/strp*/source/extensions/stripe`, `strpwt7-*`, `opc-test-1` | each has `tests/phpunit.xml`, `tests/Unit/`, a `docker-compose.yml`, and (from 2026-01) `infection.json5` — **a longitudinal mutation series is feasible** without rebuilding historical environments |
| **3 checkouts of `payment-base`** (2026-03-26, 05-21, 09-04) | same tree | second package for the same series |
| **The complete dev log** — 578 files, 113,064 lines, ≈396k words | `strpwt7-nov26/…/.claude/worktrees/sprint-132-forged-payment-proof/docs/oe_payments_docs/daniil_dev_log` | the corpus `01`–`08` cite by path; `done/` 190 files (192k words), `reports/` 94 (90k), `sprints/` 40 (85k), `status.md` ×49 (29k) |
| **`origin/b-7.4.x-LEGACY`** with continuous pre-squash history | newest checkout | `git blame` on the current branch attributes **every** line of the top escape file to the 2026-07-02 squash; blame on `LEGACY` recovers 17 commits and real dates. A `git replace --graft` of the squash onto the legacy tip (`58464a7`) restores continuous blame for the whole tree |
| **Infection's JSON logger** | `infection.json5` currently writes text + summary only | adding `"json"` yields **every mutant with its line and kill status**, not only the 469 escapes — required for rates |

### 0.3 Pilot results computed for this report

All uncorrected, all from the existing CSVs, none yet in `stats.py`. They
exist to show the studies are live, not to be cited.

| Pilot | Result | Reading |
|---|---|---|
| **P1** commits on burst days (≥10 commits/day) vs ordinary days: any failing CI run | **107/151 (71%)** vs **164/293 (56%)**, Fisher **p = 0.0028**; excluding the three mechanical days (package split, rename, squash): **100/138 (72%)** vs **160/284 (56%)**, **p = 0.0014** | the peak is not only *not the rate* — it may be **worse** than the rate |
| **P2** CI failure streaks that ended in green, per repo × workflow | **74** streaks; median **2 runs / 4.1 h** to green; **23** streaks of ≥5 runs; longest **358 h** | repair is a measurable, heavy-tailed cost in human time |
| **P3** `stripe-wallet` runs within 72 h after a `payment-base` commit vs not | **45.4%** fail (n = 392) vs **60.8%** (n = 472) | **opposite** to "upstream breaks downstream"; time-confounded — demoted to §5 |
| **P4** documentation-to-source insertion ratio by month | 29.7 (2025-10), 10.1, 4.6, **1.2** (2026-01), 3.6, 3.2, 1.8, **5.5** (2026-05), 3.3, 0.6, 1.3 | the "context tax" is large, variable, and falls then spikes with the epic; October/November include imported documentation that must be separated |
| **P5** numeric self-claims in the dev log | **1,132** lines stating a count of commits / files / tests / LOC across **220** files | enough claims to estimate an error *distribution*, not one −41% anecdote |
| **P6** model per dispatch in the journal | "opus 4.7" ×1, "opus 4.8" ×1 in 113k lines | the journal does **not** record which model ran which dispatch; only trailers (149 commits) do |

---

## 1. Study S-1 — *Is the peak worse than the rate?* Burst-mode agentic work and what it costs later

**The question developers argue about.** Whether to let a coding agent run in
long, high-throughput bursts (a 64-commit two-day epic) or pace it. The
argument is conducted entirely on intuition. `06` N-11 established that this
project's cadence is bursty (dispersion 6.93) and that the peak is not the
rate. The next question — **is the code produced at the peak different?** —
has never been asked of an artifact.

**Unit of analysis.** 716 commits, classified by the day's commit count
(burst ≥10; ordinary otherwise; the three mechanical days excluded), and by
position within their session (first / middle / last commit of a ≤90-min run,
from `sessions.csv`).

**Outcomes, each already computable or one join away:**

| Outcome | Source | Pilot |
|---|---|---|
| any failing CI run on the commit | `actions_by_commit.csv` | **72% vs 56%, p = 0.0014** (P1) |
| test/source insertion ratio of the commit | `commit_loc_by_category.csv` | 1.91 vs 1.80 (raw) |
| escaped-mutant density of the lines the commit introduced | S-2's blame join | not yet run |
| lines later touched by a bug-fix commit | S-3's SZZ join | not yet run |
| ticket reference present; subject reused | `commits.csv` | not yet run |
| self-report accuracy of the sprint that produced it | S-5 | not yet run |

**Predictions, stated before the analysis.** If burst-mode work is *merely
faster*, all outcomes should be flat across burst/ordinary once period is
controlled. If it *trades quality for speed*, CI failure, escape density and
later bug-touch should all be higher on burst days, and the effect should
persist within the epic when comparing early to late commits (fatigue or
context-drift). If burst days are simply *days when the environment was
broken*, CI failure will be higher but escape density and bug-touch will not
— which would exonerate the agent and indict the pipeline, and is itself a
useful result.

**Why it is deep.** It is the first artifact-based test of the
throughput–quality trade-off in agentic work, with three independent quality
outcomes (pipeline, verification, field defects) on the same commits. And it
answers a concrete operating question: how big a dispatch should be.

**Confounds to control.** Period (burst days cluster in Jan, May and Aug;
failure rates differ by period) — stratify by month or model with month fixed
effects. Mechanical days — excluded. The epic is a single event — report with
and without it. Per-commit CI outcomes are autocorrelated at 0.429 — use a
permutation test over days, not a naive Fisher.

**Still needed.** S-2's blame join and S-3's SZZ join; a permutation version
of P1 added to `stats.py`; within-session position analysis (does the last
commit of a long session fail more than the first?).

**Venue.** MSR or ICSE-SEIP as research; the practitioner version is the
single most useful talk in the programme ("how big should a dispatch be, and
what does the artifact say happens when it is too big"). **Gate:** none.
**Effort:** medium; depends on S-2 and S-3 for two of the five outcomes but
publishable on CI and ratio alone.

---

## 2. Study S-2 — *Verification provenance.* Which lines does the suite actually verify, and under what conditions were they written?

**The question developers argue about.** Whether agent-written tests verify
agent-written code, or whether the two are written to satisfy each other. `05`
M-30 gives a single number (MSI 70%) over the whole scope. The deeper question
is **where** the 30% lives in *process* terms: was it written on burst days,
in trailered commits, in unticketed work, in commits whose CI was red, in
handlers rather than services, early or late in the project?

**Unit of analysis.** Every mutant (≈1,600 with the JSON logger; currently only
the 469 escapes are on disk), attributed via `git blame` to the commit that
last wrote its line, and thence to that commit's properties.

**The join that only this corpus permits.**

```
mutant (file, line, killed|escaped)
  → git blame on grafted history (LEGACY ⊕ post-squash)
  → introducing commit: date, burst/ordinary, session length, trailer + model,
    ticket_ref, tests_ins/src_ins, CI outcome, subsystem
```

**Outcome.** Escape *rate* (escaped / all mutants) per provenance class, with
a logistic model over the covariates. The dependent variable is a mutant, so
n ≈ 1,600; the covariates come from the commit.

**Then the longitudinal half.** Run the same deterministic Infection recipe
(`--coverage --skip-initial-tests`) on **five to seven of the frozen
checkouts** (2025-11, 2026-01, 02, 03, 05, 09) and report MSI over time beside
the suite-size series in `test_trajectory.csv` (493 → 2,109 methods). The
question is whether **verification accumulated with volume, or volume
accumulated alone** — the single-project, longitudinal version of the
size-versus-effectiveness debate, which the literature runs cross-sectionally.

**Predictions.** If the "tests written to satisfy the code" hypothesis holds,
escape rate should be highest in commits where tests and source were added
together in one large commit, and flat or falling MSI over time despite
growth. If the "hollow tests were an early defect later corrected" hypothesis
holds (the journal's own account: R-1.5, the silent-skip fix), escape rate
should fall with date and MSI should rise over checkpoints. The two
hypotheses make opposite predictions on the time axis.

**Why it is deep.** Mutation results are reported as aggregates everywhere;
joining them to line provenance and to process covariates is essentially
absent from the literature, and a longitudinal MSI series on an evolving
industrial system is rare. For developers it answers: *what kind of work
produces code the suite does not really check* — which is the question that
decides where review effort should go.

**Confounds and hazards.** Blame attributes a line to its *last* writer;
refactors move lines. Report both last-writer and first-writer (via
`--reverse` / `-C -C -M`). Equivalent mutants inflate escapes uniformly and
are unlikely to correlate with provenance, but a 100-mutant triage sample is
cheap insurance. The squash: **without the graft this study is impossible**,
which is worth one paragraph — the release procedure documented in `06` N-6
would have destroyed the study.

**Still needed.** (1) `git replace --graft 6e828a242d6b 58464a7`, verify blame
continuity on three files. (2) Add `"json": "reports/infection.json"` to
`infection.json5`, re-run the deterministic recipe once (≈ the existing
runtime). (3) For the longitudinal half: `composer require --dev
infection/infection` in each snapshot's environment, bring up its compose
stack, run the recipe; budget one day per checkpoint including environment
repair, and expect the 2025-11 snapshot to need pre-rename namespaces handled.
(4) Triage 100 random escapes for equivalence.

**Venue.** ESEM or ICST (test effectiveness) or MSR (the join is the method).
**Gate:** none. **Effort:** high for the longitudinal half, medium for the
provenance half; the provenance half is publishable alone.

---

## 3. Study S-3 — *Do mutants predict where humans find bugs?* A defect-by-defect accounting of a money path's quality system

**The question the field has never had the data for.** The mutant–real-fault
coupling literature (Just et al., Papadakis et al.) asks whether mutation
score predicts real-fault detection, on curated defect benchmarks. This
project has **40 real bugs filed by a known human tester against a running
payment system**, 17 of them joined to fix commits, plus 4 refactoring-found
truncation bugs — and a per-file escaped-mutant map. Nobody has both on one
industrial system with an intent record.

**Unit of analysis.** Each of the 40 bugs; each of the 46 files with escapes
plus the files without.

**Three joins, in order of ambition.**

1. **Escape density predicts bug location (cheap, do first).** For the 17
   bugs with fix commits, take the `src/` files their fixes touched (pilot:
   `STRP-103` → 4 files, `STRP-131` → 4, `STRP-116` → 3, `STRP-138` → 2, via
   `git log --grep` on `LEGACY`). Compare escaped-mutant density (escapes per
   100 lines, or per mutant once S-2's JSON exists) of bug-touched files
   against untouched files. **Prediction:** human-found bugs concentrate in
   the files the suite verifies least. If true, mutation escape density is a
   **map for manual QA** — a directly actionable result. If false, the
   tester found what the suite could not have found by construction
   (interface, state-at-redirect, configuration), which is the finding
   instead.
2. **Which layer caught what (medium).** Classify each of the 40 bugs by the
   layer that *could* have caught it (unit suite / static analysis / CI
   integration / E2E / only a human against a running shop) using the bug
   summary, the fix diff, and the journal's account; record which *did*. The
   tester's 6 amount bugs and the refactor's 4 truncation bugs on the same
   subsystem (`06` N-5) become two rows of a 40-row table rather than an
   untestable anecdote. Cross with M-5's 15% reclassified (`Not a bug`, `Core
   Bug`).
3. **SZZ on the 17 (ambitious).** From each fix diff, blame the removed lines
   on grafted history to the bug-introducing commit; record its date,
   burst/ordinary, trailer, test/source ratio, CI outcome, and whether the
   introducing commit *added tests for the lines it broke*. **Prediction:**
   bug-introducing commits over-represent burst days and under-represent
   test-accompanied changes. Bugs with no fix commit (e.g. `STRP-137`, `150`,
   `125`, `152`) are located via ticket mentions in commit bodies and the
   journal, or recorded as fixed-under-umbrella / unfixed.

**Why it is deep.** It is a mutant-versus-real-fault study on an industrial
money path with a human oracle, and it turns the programme's most
conceptually interesting but untestable item (N-5) into a table with 40 rows.
For developers it answers whether running mutation testing tells you where to
point your tester.

**Confounds.** 17 bugs is small; report exact tests and effect sizes, no
regression. Fix-touched files are a biased sample of "where the bug was"
(fixes can land elsewhere). SZZ is noisy on refactor-heavy code; report the
share of introducing commits that are themselves refactors.

**Still needed.** The graft (shared with S-2); a bug-by-bug spreadsheet
(summary, layer-that-could, layer-that-did, fix commits, fix files,
introducing commit); the S-2 JSON for per-mutant rates. Layer classification
should be done by two people independently, with the tester as one of them
if consent permits — which also delivers the corroboration `06` §6 asks for.

**Venue.** ISSTA / ICST (mutation ↔ real faults) or ESEM. **Gate:** bug
summaries are internal but non-sensitive; anonymise the reporter by role;
none of the 40 is a security finding (those are `STRP-99/108`, excluded).
**Effort:** medium.

---

## 4. Study S-4 — *The context tax.* What it costs to drive a stateless agent for ten months, and what the writing bought

**The question every agent user is guessing about.** How much human-written
context — plans, rules, status, completion reports — an agent needs, whether
it pays back, and whether the need falls as models improve. Practice ranges
from a one-page `CLAUDE.md` to this project's ≈396,000 words. There is **no
measurement** of this cost category in a real project anywhere in the
literature `08` searched.

**What is on disk.** 578 journal files; by role: `done/` 190 files (192k
words — completion reports), `reports/` 94 (90k), `sprints/` 40 (85k — plans
and dispatch briefs), `status.md` ×49 (29k). Per-commit `docs_ins` in
`commit_loc_by_category.csv` (212 of 715 commits carry documentation).
Monthly docs-to-source insertion ratio (P4): 29.7 → 10.1 → 4.6 → **1.2** →
3.6 → 3.2 → 1.8 → **5.5** → 3.3 → 0.6 → 1.3.

**Three measurements, then one test.**

1. **The cost, by type and over time.** Words and lines written *for the
   agent* (dispatch briefs, repeated hard rules, plans) vs *for the human*
   (retrospectives, status), per month, per sprint, per commit, per hour of
   session time; and the share that is *repeated* (LL-1 documents that scope
   rules were restated on every dispatch — measure the repetition rate with
   near-duplicate detection). The October–November 2025 spikes must be
   separated into imported documentation vs authored journal by path.
2. **The shape.** The plan → dispatch → completion-report cycle: how many
   words of plan per commit produced; how that ratio changed across the six
   model generations that the trailers date (P6 shows the journal itself does
   not name models, so the trailer is the only model clock).
3. **What it bought.** For each sprint with a plan file: commits produced,
   one-commit mapping (PM-1's failed convention), CI outcome of its commits,
   escape density of its lines (S-2), and completion-report accuracy (S-5).
   **Prediction:** plan length is positively associated with one-commit
   mapping and with self-report accuracy, and unassociated with CI outcome
   (environmental) — if plans buy *control*, not *correctness*. The null —
   that plan volume predicts nothing — would be the more provocative finding
   and is entirely possible.

**Why it is deep.** It names and prices a cost category the agentic-SE
productivity literature omits entirely (METR counts the developer's minutes,
not their words), and it is the first artifact-based evidence on the "how
much context" question. For developers it turns folklore into a number with a
trend: the tax fell from ≈10× to ≈1.2× code in three months and then spiked
5.5× at the epic — is that learning, model improvement, or task mix?

**Confounds.** Documentation volume is partly the *research corpus itself*
(`05` M-17's caveat): the journal was kept partly to be studied. Separate
operational context (briefs, rules, status) from reflective writing before
computing any ratio. Model change and human learning are collinear in time.

**Still needed.** A path-based classifier for the dev-log tree (role by
directory: `done/`, `reports/`, `sprints/`, `status.md`, `todo/`); a
near-duplicate pass for repeated rule blocks; the sprint → commit join by
day-directory date and ticket (the `sprint_ref` column covers only 108
commits, so it cannot be the key).

**Venue.** CHASE / ICSE-SEIP (human factors of agentic work) or a
practitioner venue where it would land hardest (QCon, LeadDev). **Gate:**
employer approval — the journal is internal; excerpts must be cleared.
**Effort:** medium; the corpus is on disk and the joins are dates.

---

## 5. Study S-5 — *How wrong are agent completion reports?* Calibration of ≈200 self-reports against the commit record

**The question developers face daily.** Whether to believe the agent's
summary of what it just did. The programme has **one** data point — the epic
report understated insertions by 41% and commits by 3 (`05` M-2) — and two
smaller ones (a "said 4, was 3" baseline miscount; an over-claimed "boundary
sealed"). That is an anecdote about direction. The corpus can supply a
**distribution**.

**What is on disk.** 190 completion-report files in `done/` and 94 in
`reports/`, containing **1,132 lines that state a count** of commits, files,
tests or LOC (P5) — e.g. "**61 commits**: 59 on … + 2 in payment-base",
"274 tests passing", "~120 LOC for 7 × 6 assertions", "3 unit tests
covering…". The git record can check most of them.

**Method.**

1. **Extract** every numeric claim with its type (commits, files changed,
   insertions/deletions, tests added, tests passing, LOC of a named file,
   PHPMD baseline count) and its scope (a sprint, a commit, a file).
2. **Match** each report to its git window: by the day-directory date (all
   report files sit under dated `YYYYMMDD/` dirs), the ticket in the filename
   or body, and — for the 108 commits that carry one — the sprint reference.
   Ambiguous windows are recorded as such, not resolved by hand.
3. **Measure** the claim against the artifact: commits in window, `numstat`
   insertions, `function test*` deltas, `wc -l` of the named file at the
   window's last commit, PHPUnit-reported counts where the claim is a PHPUnit
   count (the two test-count series must not be mixed — `05` M-1).
4. **Report** signed relative error by claim type; the share of claims that
   are unverifiable and *why* (no commit in window, "done" but not committed,
   claim about a PHPUnit count with no CI artifact); and drift over time and
   across model generations (trailer-dated).

**Predictions.** Error is *not* uniformly flattering: `07` LL-2 already has
one understatement and one overstatement. The interesting hypotheses are
about **type**: counts the agent can compute from its own actions (files it
edited, tests it wrote) should be accurate; counts that require the
repository state (total commits, cumulative LOC, "all tests passing") should
drift; and "completion" claims should have a measurable **done-but-not-
committed** rate, which the journal itself flags as common in mid-2026.

**Why it is deep.** It is calibration of LLM agent self-reports **in situ**,
on real work, over ten months — where the existing literature measures
overclaiming on benchmarks. It complements METR (the *human's* perception
gap) with the *agent's* report gap on the same kind of project. For
developers it yields a checklist with numbers: which claim types to grep
before believing, and how often that grep will find a discrepancy — the
cost/yield argument LL-2 makes qualitatively.

**Confounds and limits.** Reports are written by the assistant and edited by
the human; authorship of a given sentence is not recoverable — the unit is
"the report the project accepted", which is the practically relevant one.
Some claims are forward-looking plans, not reports; the extractor must use
the file's role (`sprints/` vs `done/`). Squash and pruning make some
windows lower bounds (`06` N-6) — a claim *higher* than git may be git's
fault; flag windows that cross a lost branch.

**Still needed.** The extractor (regex over 1,132 candidate lines, then hand
validation of a 100-line sample); the window matcher; a claim-type codebook.
No new measurement of the system is required.

**Venue.** MSR or FSE-Industry as research; ACM Queue / IEEE Software as the
practitioner cut LL-2 already targets. **Gate:** employer approval for
journal excerpts; hashes and ticket ids anonymised externally. **Effort:**
medium; entirely desk work on data already on disk.

---

## 6. Considered, piloted, and not promoted

| Candidate | Pilot / reason | Status |
|---|---|---|
| **Upstream breaks downstream** — do `payment-base` changes precede `stripe-wallet` CI failures? | P3: runs within 72 h *after* a `payment-base` commit fail **less** (45.4% vs 60.8%). Time-confounded: `payment-base` commits concentrate in the later, lower-failure period. | Worth one stratified test inside S-1's CI analysis; not a study. If the reversal survives stratification it is a curiosity worth a paragraph — the two repos were repaired together. |
| **Time-to-green as the human cost of CI** | P2: 74 streaks, median 4.1 h, 23 of ≥5 runs, max 358 h. Real and quotable. | Folded into S-1 as the *cost* axis of burst-day failures (do burst days also produce longer streaks?). Alone it is a descriptive statistic, not a question. |
| **Six model generations as a natural experiment** | P6: the journal names a model twice in 113k lines; trailers date 149 commits across six strings, 73/33/31/6/5/1. | Underpowered for any outcome except as a covariate. Used as the model clock in S-2, S-4, S-5; not a study. |
| **The 2023–2025 prehistory** — 55 issues before any commit | `05` M-21; no artifact but tracker summaries. | Cannot be measured beyond what M-21 says. |
| **Security audit re-scored independently** | `07` gate 3; AI-authored self-scored audit. | Not a data study; an assessment engagement. |

---

## 7. Dependencies and order

```
graft LEGACY onto the squash ──┬──► S-2 provenance half ──► S-1 (escape outcome)
                               └──► S-3 SZZ + file join ──► S-1 (bug outcome)
Infection JSON re-run ─────────────► S-2 rates ───────────► S-3 per-mutant density
dev-log role classifier ───────────► S-4 ─────────┐
claim extractor + window matcher ──► S-5 ─────────┴──► S-4 "what it bought" (accuracy outcome)
frozen checkouts + compose ────────► S-2 longitudinal half (independent, slowest)
```

**Suggested order.** (1) The graft and the JSON re-run — two hours, unblock
three studies. (2) **S-1 on CI and ratio alone** — the pilot is already
significant and it is the most talk-worthy result; add the permutation test
to `stats.py` as T11. (3) **S-3 join 1** — cheap, and its answer changes how
S-2 is written. (4) **S-5** — desk work, no environment. (5) **S-2
provenance half.** (6) **S-4.** (7) **S-2 longitudinal half** last; it is the
only one that needs historical environments to boot.

**Gates.** S-1, S-2, S-3 need none beyond ordinary employer sign-off. S-4 and
S-5 quote the journal and need excerpt clearance. S-3 join 2 is stronger with
the tester's participation, which is the same conversation `07` gate 2
requires for LL-6.

---

## 8. Summary

| # | Question | Unit (n) | Pilot | New join required |
|---|---|---|---|---|
| **S-1** | Is code produced in bursts worse? | commits (716) | burst-day CI failure **72% vs 56%, p = 0.0014** | none for CI; S-2/S-3 for the rest |
| **S-2** | Which lines does the suite verify, and how were they written? MSI over time | mutants (≈1,600); checkpoints (5–7) | blame recovers real dates on `LEGACY`; snapshots have configs | graft; JSON logger; snapshot environments |
| **S-3** | Do escaped mutants predict where the human tester found bugs? Which layer caught what? | bugs (40; 17 with fixes) | 4 sample bugs → 2–4 fix files each | graft; bug spreadsheet |
| **S-4** | What did ten months of agent context cost, and what did it buy? | sprints / months / commits | docs:src **29.7 → 1.2 → 5.5 → 1.3** by month; ≈396k words by role | role classifier; sprint→commit by date |
| **S-5** | How wrong are agent completion reports, by claim type? | claims (≈1,100) | 1,132 numeric claims in 220 files | extractor; window matcher |

None of the five is about agreeing or disagreeing with a paper. Each is a
question that people running coding agents are currently answering by
instinct, and each has a falsifiable prediction that this corpus — and, as
far as `08`'s searches show, no other — can test.
