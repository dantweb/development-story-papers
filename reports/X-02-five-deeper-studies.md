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
reported as uncorrected and labelled as such. Each study carries a
two-word conclusion, a registered-report-style abstract, and a graded
literature table (**added 2026-09-21**); §9 consolidates the references.

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

**In two words: *Bursts cost.*** Expanded: code produced on high-throughput
days carried a measurably higher pipeline-failure rate than code produced at
the ordinary pace, and the study tests whether the same holds for
verification and field defects — a conclusion the pilot points to and the
study would confirm or overturn.

**Abstract (registered-report style).** *Context.* Just-in-time defect
prediction has established that properties of a change — size, diffusion,
author experience, time of day — predict its risk (Mockus & Weiss 2000;
Nagappan & Ball 2005; Eyolfson et al. 2011; Kamei et al. 2013). Agentic
development adds a property those studies never saw: the *cadence* of the day
on which a change was made, because an agent can produce 30 commits in a day
where a human produces three. Whether burst-mode output is worse is currently
argued from intuition. *Objective.* To test whether commits made on burst days
(≥10 commits) differ from commits made on ordinary days on three independent
quality outcomes: continuous-integration failure, escaped-mutant density of
the lines introduced, and later bug-fix touch. *Method.* 716 commits of a
production payment module over ten months, joined to 979 CI runs, to a
deterministic mutation-testing baseline via line provenance on grafted
history, and to 40 tracker bugs via fix commits. Three mechanical days are
excluded; period is controlled by month strata; inference is by permutation
over days because per-commit outcomes are autocorrelated (ρ₁ = 0.429).
Within-session position (first vs last commit of a ≤90-minute run) is tested
for drift. *Pilot.* Burst-day commits had a failing run 72% of the time
against 56% on ordinary days (Fisher p = 0.0014, uncorrected). *Predictions.*
If bursts trade quality for speed, all three outcomes rise; if bursts merely
coincide with a broken environment, only CI failure rises, which exonerates
the agent and indicts the pipeline; if bursts are free, nothing rises once
period is controlled. *Contribution.* The first artifact-based test of the
throughput–quality trade-off in agent-assisted work, and — because per-commit
size predicted nothing here (ρ = −0.024) while day cadence did — evidence
that the informative risk feature has moved from the change to the day.

**Literature it rests on.**

| Paper | Their claim | Our stance | Status |
|---|---|---|---|
| Mockus & Weiss, *Predicting risk of software changes*, Bell Labs Tech. J. 2000 | change size and diffusion predict failure | **CONFIRMS** the family; **ENHANCES** with a cadence feature they could not observe | to read |
| Nagappan & Ball, *Use of relative code churn measures to predict system defect density*, ICSE 2005 | relative churn predicts defect density | **COMPLICATES** — per-commit size carried no CI signal here (N-13) while day-level cadence did | to read |
| Eyolfson, Tan & Lam, *Do time of day and developer experience affect commit bugginess?*, MSR 2011 | late-night and inexperienced commits are buggier | **ENHANCES** — adds a *throughput* dimension to the temporal-risk lineage; this project has almost no night commits (M-14), so cadence is the only temporal variable left | to read |
| Kamei et al., *A large-scale empirical study of just-in-time quality assurance*, TSE 2013 | change-level features predict defect-inducing commits across projects | **ENHANCES** — proposes day cadence as a JIT feature for agent-assisted repositories | to read |
| Śliwerski, Zimmermann & Zeller, *When do changes induce fixes?*, MSR 2005 | SZZ; Friday commits more often bug-inducing | **CONFIRMS** the method (used for the bug-touch outcome); **ENHANCES** the weekday result with a within-week cadence result | to read |
| Huang et al., *Is this Build Failure Related to my Patch?*, 2026 | 13% of failures are patch-unrelated | **ENHANCES** — supplies the discriminating test between "agent produced worse code" and "environment was broken on busy days" | in `08` §3.2 |
| Robbes et al., *Promises, Perils…*, MSR 2026 | agent traces are partial and time-confounded | **CONFIRMS** — burst/ordinary is defined without trailers precisely because trailers are unreliable here (N-2) | in `08` §2.1 |
| METR 2025 | measured vs perceived AI productivity diverge | **ENHANCES** — throughput is what practitioners perceive; this measures what the throughput cost | in `08` §1.2 |

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

**In two words: *Provenance predicts.*** Expanded: whether a line is
verified by the suite is expected to depend on the conditions under which it
was written — burst day, red pipeline, unticketed work, tests and source
landing together — and on when in the project it was written; the
longitudinal series decides whether verification accumulated with volume or
volume accumulated alone.

**Abstract (registered-report style).** *Context.* Mutation score is the
strongest available proxy for test-suite effectiveness (Just et al. 2014),
but it is almost always reported as one aggregate, and its relation to real
faults weakens once suite size is controlled (Papadakis et al. 2018).
Industrial practice at Google surfaces mutants at diff time (Petrović &
Ivanković 2018), implicitly asserting that *when and how* a line is written
matters to whether it gets tested — an assertion never examined
retrospectively. *Objective.* To attribute every mutant in an agent-assisted
payment module to the commit that wrote its line and model escape probability
on that commit's properties; and to measure the module's mutation score at
five to seven historical checkpoints against its test-suite growth.
*Method.* Infection over four source directories with the JSON logger (≈1,600
mutants), `git blame` on history reconstructed by grafting the retained
pre-squash branch onto the 2026-07-02 release squash, and a logistic model
over date, burst/ordinary day, session length, trailer and model, ticket
presence, test/source ratio of the commit, its CI outcome, and subsystem. The
longitudinal series uses fourteen frozen checkouts on disk (2025-11 →
2026-09), each with its own test configuration and container stack, run with
the deterministic recipe (`--coverage --skip-initial-tests`). *Pilot.* Blame on
the retained branch recovers real dates (17 commits, 2025-12 → 2026-05, for
the top escape file) where the current branch attributes every line to the
squash; the current baseline is MSI 70%, 469 of 1,592 escaped, with 169 of
469 escapes in event handlers and zero in the three money-arithmetic classes.
*Predictions.* Under "tests written to satisfy the code", escape rate peaks
in large commits adding tests and source together, and MSI is flat or falling
over checkpoints while the suite grows 493 → 2,109 methods; under "hollow
tests were an early defect later corrected", escape rate falls with date and
MSI rises. *Contribution.* The first mutation-by-provenance analysis of an
industrial suite, a longitudinal MSI series on an evolving agent-assisted
system, and a demonstration that the study is impossible without retained
history — the release squash would have destroyed it.

**Literature it rests on.**

| Paper | Their claim | Our stance | Status |
|---|---|---|---|
| Just et al., *Are mutants a valid substitute for real faults in software testing?*, FSE 2014 | mutant detection correlates with real-fault detection; some faults are not coupled to any mutant | **ENHANCES** — adds *who wrote the line, when, how* as covariates of escape | to read |
| Papadakis et al., *Are mutation scores correlated with real fault detection?*, ICSE 2018 | the correlation is weak once test-suite size is controlled | **CONFIRMS** on one suite, longitudinally — size (1.69:1) and MSI move independently if the flat-MSI prediction holds | to read |
| Inozemtseva & Holmes, ICSE 2014; Zhang & Mesbah, FSE 2015 | coverage is not, assertions are, correlated with effectiveness | **CONFIRMS** — already shown on this suite (`08` §7.3); the provenance model asks *why* | in `08` §7.3 |
| Petrović & Ivanković, *State of Mutation Testing at Google*, ICSE-SEIP 2018; Petrović et al., *Does mutation testing improve testing practices?*, ICSE 2021 | surfacing mutants at code-review time changes how developers test | **ENHANCES** — a retrospective provenance analysis is the observational counterpart to their diff-time intervention | to read |
| Hora & Robbes, *Are Coding Agents Generating Over-Mocked Tests?*, MSR 2026 | agent tests may pass without testing behaviour | **ENHANCES** — `MethodCallRemoval` (85/469) becomes a *dated, attributed* signature rather than a count | in `08` §2.3 |
| arXiv:2607.22880 (2026), replicability of LLM-generated suite effectiveness | size only weakly confounds mutation score for LLM suites | **CONFIRMS or DISPROVES** — the longitudinal half tests it directly on one suite | in `08` §7.3 |
| *Was It Never Collected, or Rewritten Away?*, 2026 | history rewrites bound what mining can observe | **CONFIRMS** — the study exists only because a legacy branch survived the squash (N-6) | in `08` §2.2 |

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

**In two words: *Complementary detectors.*** Expanded: the human tester
and the automated layers are expected to have found largely disjoint defect
classes, so that mutation escape density either maps where manual testing
should go or shows that human-found defects lie outside anything the suite
could have caught — either answer is the result.

**Abstract (registered-report style).** *Context.* Whether mutants stand in
for real faults has been studied on curated defect benchmarks (Just et al.
2014; Papadakis et al. 2018), and whether different detection techniques
find different fault classes has been studied in controlled experiments
(Basili & Selby 1987; Juristo, Moreno & Vegas 2003; Runeson et al. 2006).
Neither literature has an industrial system with a known human tester, a
per-file mutation map, and an intent record on the same code. *Objective.*
To determine (i) whether escaped-mutant density predicts the files in which a
dedicated human tester found bugs, (ii) which quality layer — unit suite,
static analysis, CI integration, end-to-end, or a human against a running
shop — could have caught each of the project's 40 bugs and which did, and
(iii) what the bug-introducing commits have in common. *Method.* 40 `Bug`
issues of a payment module (37 filed by one tester), 17 joined to fix commits
and thence to `src/` files via the retained pre-squash branch; per-file escape
density from a deterministic Infection baseline (469 escapes over 46 files);
two-rater classification of catchable layer against a codebook, with the
tester as one rater where consent allows; SZZ on the 17 fix diffs over
grafted history to recover introducing commits and their burst/ordinary,
trailer, test-accompaniment and CI properties. Reclassified bugs (3 `Not a
bug`, 3 `Core Bug`) are a control stratum (Herzig et al. 2013). *Pilot.* Four
sample bugs resolve to two to four fix files each; escapes concentrate in
event handlers (169/469) and are absent from money arithmetic; four
refactoring-found truncation bugs and six tester-found amount bugs on the
same subsystem do not overlap. *Predictions.* If human-found bugs sit in
high-escape files, mutation testing is a map for manual QA; if they sit in
low-escape files or in interface and state-at-redirect code the unit suite
cannot reach, the human found what no automated layer could by construction,
and the tester's 92.5% share of bugs (N-3) is explained by complementarity
rather than by suite weakness. *Contribution.* A mutant-versus-real-fault
study with a human oracle on a regulated money path, and a 40-row
layer-accounting that turns the programme's untestable N-5 observation into
data.

**Literature it rests on.**

| Paper | Their claim | Our stance | Status |
|---|---|---|---|
| Just et al., FSE 2014 | mutants are a valid but imperfect substitute for real faults; some faults are uncoupled | **ENHANCES** — file-level, industrial, human-reported faults; tests whether the uncoupled class is exactly what the tester found | to read |
| Papadakis et al., ICSE 2018 | mutation score ↔ real-fault detection is weak when size is controlled | **CONFIRMS or COMPLICATES** — a per-file test rather than a per-suite correlation | to read |
| Basili & Selby, *Comparing the effectiveness of software testing strategies*, TSE 1987 | techniques differ by fault class | **CONFIRMS** the lineage with a modern channel set (refactoring, mutation, black-box human) | in `08` §5.1 |
| Juristo, Moreno & Vegas, *Functional testing, structural testing and code reading: what fault type do they each detect?*, 2003 | replication: effectiveness depends on program and fault type | **CONFIRMS** — supplies the fault-type codebook for the 40-row table | in `08` §5.1 |
| Runeson et al., *What do we know about defect detection methods?*, IEEE Software 2006 | evidence on detection methods is fragmented and context-dependent | **ENHANCES** — one context, fully instrumented | to read |
| Śliwerski et al., MSR 2005; Kim et al., *Automatic identification of bug-introducing changes*, ASE 2006 | SZZ and its refinement | **CONFIRMS** the method; applies it to 17 money-path bugs with an intent record | to read |
| Herzig, Just & Zeller, *It's not a bug, it's a feature*, ICSE 2013 | a third of "bugs" in trackers are misclassified | **CONFIRMS** — 6 of 40 (15%) reclassified here (M-5); used as a control stratum | to read |
| Agarwal et al. 2026; Garousi 2026; Monperrus 2026 | the team sets the sign; oversight is a burden; agents supersede inspection | **ENHANCES** Agarwal/Garousi with *what kind* of defects the human oversight caught; **DISPROVES** the strong Monperrus reading if the human-caught class is unreachable by any automated layer | in `08` §5.2, §7.4 |

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

**In two words: *Context costs.*** Expanded: driving a stateless agent
for ten months required a volume of human-written context that fell from
roughly ten times the production code to near parity and then spiked with
the epic; the study prices that cost by type and tests whether it bought
control over commits, accuracy of reports, or nothing measurable.

**Abstract (registered-report style).** *Context.* Productivity frameworks
count a developer's time and output (Forsgren et al., SPACE, 2021) and field
experiments count minutes (METR 2025), but neither counts the words a human
writes *to the agent*. Lab studies have shown that prompt crafting is a
distinct and costly activity state (Mozannar et al. 2024) and that developers
report difficulty communicating intent to assistants (Liang, Yang & Myers
2024). No study has measured this cost over a real project's lifetime.
*Objective.* To measure the volume, type, repetition and time trend of
human-authored agent context in a ten-month agent-assisted project, and to
test whether it is associated with commit granularity, pipeline outcome,
verification, or self-report accuracy. *Method.* The project's complete
engineering journal on disk — 578 files, 113,064 lines, ≈396,000 words —
classified by directory role (dispatch briefs and plans in `sprints/`,
completion reports in `done/` and `reports/`, `status.md`, `todo/`), with
imported documentation separated by path; near-duplicate detection for
repeated rule blocks; per-commit `docs` insertions from 715 commits; the
sprint → commit join by dated directory and ticket; trailers as the only
model clock (the journal names a model twice in 113k lines). Outcomes per
sprint: commits produced, one-commit mapping, CI failure of its commits,
escape density of its lines (S-2), completion-report accuracy (S-5). *Pilot.*
Documentation-to-source insertion ratio by month: 29.7, 10.1, 4.6, 1.2, 3.6,
3.2, 1.8, 5.5, 3.3, 0.6, 1.3 — with the early months inflated by imported
material still to be separated. *Predictions.* Plan volume associates with
one-commit mapping and report accuracy (context buys *control*) and not with
CI outcome (environmental); the null — that context volume predicts nothing —
is possible and would be the more provocative result. *Contribution.* The
first artifact-based measurement of a cost category absent from the
productivity literature, with its trend across six model generations.

**Literature it rests on.**

| Paper | Their claim | Our stance | Status |
|---|---|---|---|
| Forsgren et al., *The SPACE of developer productivity*, ACM Queue 2021 | productivity has five dimensions; measure more than output | **ENHANCES** — names a cost (human-written agent context) none of the five dimensions counts | to read |
| Mozannar et al., *Reading Between the Lines: Modeling User Behavior and Costs in AI-Assisted Programming*, CHI 2024 | prompt crafting and suggestion verification are distinct, costly activity states in lab sessions | **ENHANCES** — the same cost measured in words over ten months of real work instead of minutes in a session | to read |
| Liang, Yang & Myers, *A large-scale survey on the usability of AI programming assistants*, ICSE 2024 | developers struggle to communicate intent and to control assistants | **CONFIRMS** — with the artifact of that struggle: repeated "ABSOLUTE HARD RULES" per dispatch (LL-1) | to read |
| Barke, James & Polikarpova, *Grounded Copilot*, OOPSLA 2023 | programmers alternate acceleration and exploration modes with assistants | **ENHANCES** — a third mode at project scale: *briefing* a stateless agent, with its volume measured | to read |
| METR 2025 | AI slowed experienced developers while they felt faster | **ENHANCES** — a candidate mechanism for the gap: time spent writing context is felt as progress and counted as documentation | in `08` §1.2 |
| Garousi 2026, *Human Oversight and Overload* | oversight of AI output is a hidden burden | **ENHANCES** — the burden has an *input* side (writing the context) as well as the output side he describes | in `08` §5.2.1 |
| Aghajani et al., *Software documentation issues unveiled*, ICSE 2019 | taxonomy of documentation problems | **COMPLICATES** — documentation-as-instruction to an agent is a new artifact class their taxonomy does not cover | to read |
| Robbes et al., MSR 2026 | agent traces in repositories are partial | **ENHANCES** — the journal is a second, richer trace of agent activity than commit metadata, and it lives in the repository (M-17: `docs` is 4.4× the code) | in `08` §2.1 |

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

**In two words: *Reports drift.*** Expanded: agent completion reports
are expected to err in both directions and by claim type — accurate on
counts the agent derived from its own actions, unreliable on counts that
require the repository's state, and carrying a measurable
done-but-not-committed rate — turning one −41% anecdote into a calibration
curve.

**Abstract (registered-report style).** *Context.* Language-model
calibration is studied on benchmarks and elicited confidences (Xiong et al.
2024; Kalai et al. 2025), and the human side of the AI-productivity
perception gap has been measured in the field (METR 2025). The *agent's*
account of its own work — the completion report a developer reads before
deciding whether to look further — has not been calibrated against the
artifact in a real project. *Objective.* To measure the signed error of
numeric claims in agent completion reports against the commit record, by
claim type, over ten months and six model generations, and to estimate the
rate of work reported done but never committed. *Method.* 284 report files
(`done/` 190, `reports/` 94) containing 1,132 lines that state a count of
commits, files, tests or lines; a typed extractor with a hand-validated
100-line sample; report → git-window matching by dated directory, ticket, and
the sprint reference present on 108 commits; measurement against `numstat`,
`function test*` deltas, file line counts at the window's last commit, and
PHPUnit counts only where the claim is a PHPUnit count (the two test-count
series are never mixed); windows that cross a squashed or pruned branch are
flagged as lower bounds. *Pilot.* The one fully checked report understated
its epic by 41% on insertions and 3 on commits while its test count was
exact; two smaller checks found one under- and one over-count. *Predictions.*
Error is bidirectional, not flattering; action-derived counts (files edited,
tests written) are accurate; state-derived counts (total commits, cumulative
LOC, "all tests passing") drift; "complete" claims carry a done-but-not-
committed rate the journal itself calls common in mid-2026. *Contribution.*
In-situ calibration of agent self-reports on real work, a claim-type
taxonomy telling developers which numbers to verify, and the cost/yield of
doing so — LL-2's argument with a denominator.

**Literature it rests on.**

| Paper | Their claim | Our stance | Status |
|---|---|---|---|
| METR 2025 | practitioners misjudge AI's effect on their own speed by ~39 points | **ENHANCES** — the agent-side counterpart: how far the agent's account of its work is from the artifact | in `08` §1.2 |
| Xiong et al., *Can LLMs express their uncertainty?*, ICLR 2024 | LLMs are overconfident when eliciting confidence on benchmark tasks | **COMPLICATES** — in situ, error is bidirectional; understatement of own output is not overconfidence | to read |
| Kalai, Nachum, Vempala & Zhang, *Why Language Models Hallucinate*, 2025 | training and evaluation reward confident guessing over abstention | **COMPLICATES** — counts that require repository state are guessed; counts derived from the agent's own actions are not, which their account predicts only partly | to read |
| Sharma et al., *Towards Understanding Sycophancy in Language Models*, ICLR 2024 | models tailor outputs to perceived user preference | **DISPROVES the naive reading** if confirmed — the checked report *under*-sold its own work, the opposite of sycophantic inflation | to read |
| Jimenez et al., *SWE-bench*, ICLR 2024 | agents are evaluated on resolved benchmark issues | **ENHANCES** — evaluation of what an agent *says* it resolved, on real work, over time | to read |
| Bettenburg et al., *What makes a good bug report?*, FSE 2008 | the gap between what reports contain and what developers need | **ENHANCES** — the same question for agent completion reports: which stated facts are load-bearing and which are wrong | in `08` §5.2.3 (lineage) |
| Robbes et al., MSR 2026 | agent traces are partial | **CONFIRMS** — completion reports are a second, human-accepted trace, and they disagree with the first | in `08` §2.1 |
| Liu et al., *Debt Behind the AI Boom*, 2026 | AI-introduced issues survive in repositories | **ENHANCES** — done-but-not-committed is the inverse failure: reported work that never reached the repository | in `08` §1.3 |

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

---

## 9. References

Status per [`08`](08-literature-review.md) §0: **[08]** already located and
graded there (read depth as marked in `08`); **[to read]** newly introduced by
this report from the author's knowledge of the field and **not yet read in this
programme** — every one must be read in full before a venue draft cites it.
Nothing may be cited from this document.

**Change-level risk and temporal effects (S-1, S-3)**
- Mockus, A. & Weiss, D. M. — *Predicting risk of software changes*. Bell Labs Technical Journal, 2000. [to read]
- Nagappan, N. & Ball, T. — *Use of relative code churn measures to predict system defect density*. ICSE 2005. [to read]
- Śliwerski, J., Zimmermann, T. & Zeller, A. — *When do changes induce fixes?* MSR 2005. [to read]
- Kim, S., Zimmermann, T., Pan, K. & Whitehead, E. J. — *Automatic identification of bug-introducing changes*. ASE 2006. [to read]
- Eyolfson, J., Tan, L. & Lam, P. — *Do time of day and developer experience affect commit bugginess?* MSR 2011. [to read]
- Kamei, Y. et al. — *A large-scale empirical study of just-in-time quality assurance*. IEEE TSE 39(6), 2013. [to read]
- Herzig, K., Just, S. & Zeller, A. — *It's not a bug, it's a feature: how misclassification impacts bug prediction*. ICSE 2013. [to read]
- Huang et al. — *Is this Build Failure Related to my Patch?* arXiv:2605.05564, 2026. [08 §3.2, full-text]

**Test effectiveness and mutation (S-2, S-3)**
- Basili, V. R. & Selby, R. W. — *Comparing the effectiveness of software testing strategies*. IEEE TSE 13(12), 1987. [08 §5.1]
- Juristo, N., Moreno, A. M. & Vegas, S. — *Functional testing, structural testing and code reading: what fault type do they each detect?* In *Empirical Methods and Studies in Software Engineering*, LNCS 2765, 2003. [08 §5.1]
- Runeson, P., Andersson, C., Thelin, T., Andrews, A. & Berling, T. — *What do we know about defect detection methods?* IEEE Software 23(3), 2006. [to read]
- Inozemtseva, L. & Holmes, R. — *Coverage is not strongly correlated with test suite effectiveness*. ICSE 2014. [08 §7.3]
- Just, R., Jalali, D., Inozemtseva, L., Ernst, M. D., Holmes, R. & Fraser, G. — *Are mutants a valid substitute for real faults in software testing?* FSE 2014. [to read]
- Zhang, Y. & Mesbah, A. — *Assertions are strongly correlated with test suite effectiveness*. ESEC/FSE 2015. [08 §7.3]
- Petrović, G. & Ivanković, M. — *State of mutation testing at Google*. ICSE-SEIP 2018. [to read]
- Papadakis, M., Shin, D., Yoo, S. & Bae, D.-H. — *Are mutation scores correlated with real fault detection? A large scale empirical study on the relationship between mutants and real faults*. ICSE 2018. [to read]
- Petrović, G., Ivanković, M., Fraser, G. & Just, R. — *Does mutation testing improve testing practices?* ICSE 2021. [to read]
- Hora, A. & Robbes, R. — *Are coding agents generating over-mocked tests? An empirical study*. MSR 2026, arXiv:2602.00409. [08 §2.3]
- *Replicability of LLM-generated test-suite effectiveness* — arXiv:2607.22880, 2026. [08 §7.3, secondary]

**Mining agent activity and provenance (S-1, S-2, S-4, S-5)**
- Robbes, R., Matricon, T., Degueule, T., Hora, A. & Zacchiroli, S. — *Promises, perils, and (timely) heuristics for mining coding agent activity*. MSR 2026, arXiv:2601.18345. [08 §2.1]
- *Was it never collected, or rewritten away? A commit-provenance dataset…* arXiv:2607.02774, 2026. [08 §2.2]
- Liu, Widyasari, Zhao, Irsan & Lo — *Debt behind the AI boom*. arXiv:2603.28592, 2026. [08 §1.3]

**Human–AI collaboration, cost and oversight (S-4, S-3)**
- Forsgren, N., Storey, M.-A., Maddila, C., Zimmermann, T., Houck, B. & Butler, J. — *The SPACE of developer productivity*. ACM Queue 19(1), 2021. [to read]
- Barke, S., James, M. B. & Polikarpova, N. — *Grounded Copilot: how programmers interact with code-generating models*. OOPSLA 2023. [to read]
- Mozannar, H., Bansal, G., Fourney, A. & Horvitz, E. — *Reading between the lines: modeling user behavior and costs in AI-assisted programming*. CHI 2024. [to read]
- Liang, J. T., Yang, C. & Myers, B. A. — *A large-scale survey on the usability of AI programming assistants: successes and challenges*. ICSE 2024. [to read]
- Aghajani, E. et al. — *Software documentation issues unveiled*. ICSE 2019. [to read]
- METR — *Measuring the impact of early-2025 AI on experienced open-source developer productivity*. arXiv:2507.09089, 2025. [08 §1.2]
- Garousi, V. — *Human oversight and overload: two hidden and costly burdens of AI-assisted software engineering*. arXiv:2606.05770, 2026. [08 §5.2.1]
- Agarwal, Miller, Kästner & Vasilescu — *3100 opinions on code review in an AI world*. arXiv:2607.07980, 2026. [08 §5.2.2]
- Monperrus, M. — *The end of code review: coding agents supersede human inspection*. arXiv:2606.13175, 2026. [08 §7.4, not yet read]

**Model self-report and calibration (S-5)**
- Bettenburg, N., Just, S., Schröter, A., Weiss, C., Premraj, R. & Zimmermann, T. — *What makes a good bug report?* FSE 2008. [08 §5.2.3, lineage]
- Xiong, M. et al. — *Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs*. ICLR 2024. [to read]
- Sharma, M. et al. — *Towards understanding sycophancy in language models*. ICLR 2024. [to read]
- Jimenez, C. E. et al. — *SWE-bench: can language models resolve real-world GitHub issues?* ICLR 2024. [to read]
- Kalai, A. T., Nachum, O., Vempala, S. S. & Zhang, E. — *Why language models hallucinate*. 2025. [to read]
