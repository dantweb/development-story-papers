# What the Journal Got Wrong: Auditing Ten Months of AI-Assisted Development of a Payment Module Against Its Commit, Issue, CI and Mutation Records

*Formerly "Discipline over Cleverness: A Longitudinal Case Study of AI-Assisted
Development of a Production Payment Module". Retitled 2026-09-21: the former
title stated a thesis this design cannot establish (§7.2); the present one
states what the study did. The developer's maxim, "Discipline > cleverness", is
kept as the claim under audit, not as the conclusion.*

Authors: D. Tkachev et al.

**Data sources — five corpora, one project.**
**(A)** the `daniil_dev_log` engineering journal — 462 markdown files, ≈113,098
lines, 2025-11-26 → 2026-07-02, written by the party being studied;
**(B)** the complete commit record of both repositories — **716 commits,
2025-10-21 → 2026-08-20**, from all refs including the retained pre-squash
branch;
**(C)** the Jira issue record of project STRP — **156 issues, 2023-05-30 →
2026-06-22**;
**(D)** the GitHub Actions history — **979 workflow runs** joined to commits on
`head_sha`;
**(E)** a deterministic mutation-testing run — **1,592 mutants** over the
module's core, executed 2026-08-24.
All derived data is in [`../data/`](../data/) (15 CSVs, schema and caveats in
[`../data/README.md`](../data/README.md)); every statistic is recomputed by
`python3 data/stats.py` (tests T1–T12).

---

## Abstract

**In one line:** a candid, daily, artifact-linked engineering journal of an
AI-assisted payment module was audited against five machine records of the same
project, and diverged from them in specific, directional ways — it undersampled
its own active days 2.2×, understated its flagship epic by 41%, narrated a
measured idle period as active, described a three-year project as seven months
old, omitted the human tester who filed 92.5% of its bugs, and credited itself
with more than twice the documentation volume it actually produced. Nothing in it
was false. The omissions were structural, and no candour inside one person's log
would have surfaced them.

**The subject.** A full Stripe payment integration for the OXID eShop platform,
built on a provider-agnostic core (`payment-base`), with Claude (via Claude Code)
as a primary code author and a human engineer as orchestrator, reviewer, and
decision-owner. It moves real money, spans an asynchronous webhook boundary,
carries PCI-DSS/GDPR obligations, and integrates with a large legacy PHP
framework.

**What we did.** We treated the journal (A) as a set of claims and tested them
against four independent machine records that fail in different directions: the
commit record (B: 716 commits, per-path diffs, timestamps, authorship trailers,
sessions reconstructed at a 90-minute gap, suite size measured from the tree),
the issue tracker (C: 156 issues — the only corpus that records who asked for
the work and who found the defects), the CI history (D: 979 runs — the only
corpus that records what happened to a commit after it landed), and a
deterministic mutation-testing baseline (E: 1,592 mutants — the only corpus that
speaks to whether the tests verify anything). We publish the derived CSVs and
the script that recomputes every statistic.

**What the audit found.** Six divergences between the self-account and the
record, each a complete enumeration needing no inference:

| The journal said | The record shows |
|---|---|
| 47 active days documented | **105** days with commits inside the journal's own window (**2.2×**) |
| flagship epic: 61 commits, +11,204 lines | **64** commits, **+15,844** lines — understated by **~41%** |
| March–April 2026 narrated as active work | **9.1 h** of commit-bearing activity in two months |
| a seven-month, single-developer project | a **three-year** project (35% of issues predate the first commit), **3** committers, **10** tracker participants |
| the developer and the assistant as the quality loop | a dedicated tester filed **37 of 40 bugs (92.5%)**; the developer filed **0** |
| "documentation is 4.4× the code; the log is the dominant activity" (our own earlier revision) | the journal is **≈2.0×** the code; **≈29%** of documentation lines are business-strategy material from October 2025, before the journal existed |

**What the machine records establish on their own.** Eight results, each with
a test or a census behind it (`stats.py`): **test code outweighed production code
1.69 : 1** in 11 of 11 months (p = 0.0010, bootstrap CI [1.39, 2.06]); **zero
Saturday commits in 716** (P = 1.2e-48) with 95.9% inside 08:00–20:00;
**cadence is overdispersed** (index 6.93, p = 4.7e-126) so the peak is not the
rate; **AI-authorship trailers are a convention adopted on one day**, 0.4% →
58.8% at 2026-05-07 (p = 5.2e-81), so they measure attribution practice, not
authorship; **role separation is near-deterministic** (developer 52 Stories / 0
Bugs, tester 0 / 37; Cramér's V = 0.859, p = 2.6e-40); **CI failed on 49.7% of
979 runs** — double the published closed-source baseline — consumed **169.5 h**
against ≈140 h of human session time, **clustered** (85.7% of failures follow a
failure), and was **independent of commit size** (63% vs 60%, p = 0.66,
ρ = −0.024), which is the finding: failures indifferent to line count are
environmental, not logical; **the suite detects 70% of mutations** in code it
executes (469 of 1,592 escape; `MethodCallRemoval` is the top escape category at
85, the over-mocking signature) while the three money-arithmetic classes have
**zero** escapes; and **0 of 61 ticket references were fabricated**, one
misattributed.

**What did not survive our own testing.** Three claims from earlier revisions
are withdrawn or demoted here: a "coin-flip" binomial test on the CI failure rate
(assumed independent runs; invalid); the 57% → 46% CI improvement (nominal
p = 0.0014, **p = 0.18** once failure clustering is modelled); and — new in this
revision — a busy-day effect in which commits made on ≥10-commit days failed CI at
72% against 56% (Fisher p = 0.0014, but **p = 0.18** under a day-level
permutation). All three remain true as descriptions and none is a tested result.
The first three mutation scores were also wrong: seven runs on unchanged code
returned 0–1,019 mutants because the tool's own initial test run used a random
seed; the reproducible figure required generating coverage externally.

**Retracted.** "Single-developer" (twice: three committers, ten participants);
"Claude was the primary code author" before 2026-05-07 (unverifiable — trailers
absent); reported "simplifications" (one file fell 330 → 107 lines while module
handler code rose 2,616 → 2,953); and the documentation claim above.

**Failure modes.** The assistant committed against an explicit "do not commit"
instruction (commit `bf32d77` matches the journal's complaint in all five
particulars), collapsed multi-phase work into single commits (9 of 13 decimal
sub-sprints span more than one commit), over-claimed *and* under-counted its own
output, and shipped tests that asserted nothing. A release on 2026-07-02
squashed the mainline: `git blame` on the current branch now attributes every
line of the module to that one commit, and this study exists only because a
legacy branch was retained.

**What this paper claims, and does not.** It makes no causal claim about the
assistant — there is no control arm, one operator, and six model generations in
four months. The journal's thesis, *"Discipline > cleverness"*, is consistent
with the record and not established by it. What is established: a high-quality
self-account still drifts in predictable directions (activity undersampled,
volume understated, continuity over-reported, actors outside the author's role
omitted); a single actor's record cannot describe a multi-actor system; trailer
series measure convention, not AI involvement; provenance loss is invisible from
inside a repository; a mutation score must be checked for run-to-run stability
before it is quoted; and in this framework-coupled, cross-repository setting the
dominant cost was the environment, established by the *absence* of the
correlation a logic-failure account requires.

---

## 1. Introduction

Most published claims about AI coding assistants are either short controlled
benchmarks (function-level synthesis, bug-fix pass rates) or vendor case studies
without a verifiable trail. What is scarce is a *longitudinal* record of a
single, non-trivial, safety-relevant system built end-to-end with an assistant,
where the process, the failures, and the numbers are all written down as the
work happens.

This paper mines exactly such a record. The subject — an OXID eShop payment
module — is a demanding target: it moves real money, spans an asynchronous
webhook boundary, must satisfy PCI-DSS/GDPR obligations, and integrates with a
large legacy PHP framework. The development journal was kept daily, is
substantially AI-authored (documents carry bylines such as *"Developer: Daniil
(Claude Code)"*, *"Reviewer: Claude (Opus 4.7 / 4.8)"*), and records not only
what shipped but how the human and the assistant divided labor, where the
assistant failed, and how those failures were caught.

**What this paper is.** A journal written by the party being studied is a weak
instrument for quantitative claims and an irreplaceable one for intent. We
therefore use four independent machine records to *test* the journal rather than
illustrate it, and we report the disagreements — their direction and size — as
the primary result. The method is ordinary triangulation; the contribution is
publishing what triangulation did to our own earlier claims.

**Contributions.** Stable identifiers (`N-`, `M-`, `T-`) refer to
[`06-novelty-assessment.md`](06-novelty-assessment.md),
[`05-measurements.md`](05-measurements.md) and `data/stats.py`.

1. **An audit of a self-account against machine records, with the corrections
   published** (N-1; §4.1, §4.3, §4.5, §4.7, §4.12). Six enumerated divergences,
   all directional: the journal undersampled activity, understated volume,
   over-reported continuity, omitted actors outside its author's role, and — in
   an earlier revision of this paper — over-attributed documentation volume to
   itself.
2. **A tested counterexample to trailer-based identification of AI-assisted
   commits** (N-2; §4.9): 0.4% → 58.8% on a single date, p = 5.2e-81, six model
   strings in four months, with the journal as ground truth for the untrailered
   period.
3. **The measurement for a published causal proposition about team structure**
   (N-3; §4.12a): near-deterministic role separation between the engineer using
   the assistant and a dedicated tester, V = 0.859, positioned as a test case for
   Agarwal et al.'s "the team sets the sign".
4. **A three-metric account of test quality on one suite** (N-4, N-14; §4.7,
   §4.14): size (1.69:1) and assertion density (≈2.3) both blind to a 30-point
   mutation gap; the money path fully verified; and a root-caused
   non-determinism in the mutation tool.
5. **A measured non-association between commit size and CI failure** (N-13;
   §4.13), with failure clustering as corroborating mechanism, and two of our own
   run-level tests withdrawn for ignoring that clustering.
6. **Two provenance-loss mechanisms invisible from inside the repository**
   (N-6; §6.6), with a recovered witness and a demonstration of what the squash
   destroyed.

**What this paper does not claim.** No causal effect of the assistant on speed
or quality: no control arm, one operator, one framework, six model generations
(§7.2). No productivity rate: the cadence has no meaningful central value
(§4.2). No security assessment: the project's audit is self-scored (§7.3). And
not the thesis in the former title: "discipline over cleverness" is consistent
with everything below and established by none of it.

Our research questions, revised from the first draft to match what the data can
answer:

- **RQ1 (audit).** Where, in which direction, and by how much does the
  project's self-account diverge from its commit, issue, CI and mutation
  records?
- **RQ2 (output).** What volume, cadence and schedule of work do the machine
  records establish, independently of the journal?
- **RQ3 (failure).** How did the assistant fail, what caught it, and what did
  the machine records add to the journal's own account of failure?
- **RQ4 (cost and quality).** Where did the project's effort go, and what can
  the record say about the quality of the result — as distinct from the appearance
  of quality?

---

## 2. The subject system

The module is built in two layers, a separation that is itself central to
several findings:

- **`payment-base`** (renamed from `payment-component` in Sprint 102) — a
  provider-agnostic payment core: a **Smart-Contract** domain model, a
  PSR-14-style **event system**, template-method service/handler/webhook bases,
  the six shared DB tables, and (added later) a shared anti-injection validation
  subsystem.
- **`stripe`** — the provider-specific layer: Stripe adapters, concrete events,
  webhook processor, admin panel.

As of the final measured checkpoint (2026-08-20) the two packages together
comprise **481 PHP source files / 39,775 source LOC** and **319 test files
containing 2,109 test methods** (`../data/test_trajectory.csv`) — measured from
the tree, not self-reported.

The architectural spine is a **contract-first** checkout: "Place Order" creates
a `PaymentContract` aggregate, not an order; the order is created *early* in a
`NOT_FINISHED` state so its number can be embedded in the PSP metadata, and it
is finalized only when the contract's conditions are met. The state machine
`DRAFT → NOT_FINISHED → PENDING → AUTHORIZED → READY_TO_COMMIT → COMMITTED →
FULFILLED` mutates **only** through named domain methods — there is deliberately
no `setState()` (`architecture/01-architecture-layers.md`;
`2026/02/20260206/reports/02-refund-setstate-bug-analysis.md`). The asynchronous
Stripe webhook, not the browser redirect, is the source of truth
(`architecture/04-webhook-processing.md`). These design choices are analyzed in
their own right in `03-topics-technical.md`; here they are context for the
*process* story.

---

## 3. Methods

### 3.1 Corpus A — the engineering journal

Dated day-dirs, each with a `status.md` and some combination of `sprints/`
(plans), `done/` (completion reports), and `reports/` (diagnostics and reviews),
plus the curated `architecture/` corpus (5 documents + 7 PlantUML diagrams).
Total: 462 markdown files, 113,098 lines, **47 dated day-dirs**, Nov 2025 –
Jul 2026. Mined along five axes in parallel — chronology/metrics, incident
forensics, technical narrative, human–AI collaboration evidence, and security.

### 3.2 Corpus B — the commit record (new)

Extracted 2026-08-20 from all refs of both repositories, so feature and legacy
branches are included:

| Repo | Commits | First | Last |
|---|---|---|---|
| `stripe-wallet` | 586 | 2025-10-21 | 2026-08-20 |
| `payment-base` | 130 | 2026-01-13 | 2026-08-20 |
| **Total** | **716** | **2025-10-21** | **2026-08-20** |

For each commit we record author and committer ISO timestamps, local hour and
weekday, author name, merge status, `numstat` insertions/deletions **split by
path category** (`src`, `tests`, `docs`, `ci`, `assets`, `other`), any
`Co-Authored-By: Claude*` trailer and the model string it names, and referenced
sprint/ticket identifiers. From the timestamp stream we derive **work
sessions**: maximal runs of commits separated by ≤90 minutes. Test-suite size is
measured directly from the tree at 15 checkpoints. Full schema, commands, and
caveats: [`../data/README.md`](../data/README.md).

Note that Corpus B **extends beyond Corpus A at both ends**: 139 commits precede
the journal's first entry (2025-10-21 → 2025-11-25) and 69 follow its last
(2026-07-03 → 2026-08-20). The project is ten months old, not seven.

### 3.3 Corpus C — the Jira issue record (new)

A 156-issue / 129-column export of the **STRP** project, **2023-05-30 →
2026-06-22**, snapshotted 2026-08-20. We normalize it and join it to the commit
record on `STRP-\d+` references in commit subjects. Retained fields: issue type,
status and status category, priority, urgency, reporter, assignee, created /
resolved dates, derived lead time, commit count, first/last commit date, and
summary. Account ids, watcher lists, and description bodies are excluded.

This corpus answers a question neither of the others can: **who asked for the
work, and who found the defects.** It is also the only one with a view of the
project before implementation began.

Its limits are severe and specific. **All time-tracking fields are empty for all
156 issues** — `Original estimate`, `Time Spent`, `Work Ratio` and their `Σ`
variants — so the estimate-vs-actual study this programme wanted is not
recoverable here either. `Priority` is degenerate (145/156 = `SHOULD`) and
carries no signal; `Assignee` is 76% empty; `Resolution` is set on 39 issues
while 82 are in status category `Done`, so lead time exists for **n=39 only**,
contaminated at the fast end by 2023-era tasks that appear bulk-closed. There is
no status-transition history. Critically, **the `Sprint` field holds only two
values**, so the journal's "Sprint 1 → 133" numbering is a **private convention
with no Jira counterpart** — the two notions of "sprint" must never be equated.

### 3.4 Corpus D — the GitHub Actions run history (new, 2026-08-21)

**979 workflow runs** exported from both repositories via the GitHub REST API and
joined to the commit record on `head_sha`. Retained per run: repository, run id /
number / attempt, workflow name and path, triggering event, conclusion, creation
and start timestamps, duration, head branch, actor — and, through the join,
the commit's date, author, files changed, insertions, deletions, `src`/`tests`
split, and AI-trailer flag. Aggregated three ways: per run, **per commit** (444
commits with at least one run), and per workflow (41 repo × workflow pairs).

This corpus answers a question none of the others can: **what happened to a
commit after it landed.** A, B and C all describe intent, content, or provenance;
only D records outcome.

Its limits are specific. **Coverage is partial in both directions:** 745 of 979
runs (76%) join to a known commit — the remainder point at `head_sha` values
reachable from no ref, i.e. deleted branches and PR merge refs — and only 444 of
716 commits (62%) have any run at all, since CI was not configured on every
branch for the whole period. `duration_seconds` is **wall-clock including
queueing**, not billable compute. The 40 distinct workflow *names* include
renames of the same pipeline (one pair differs only by a typo in the source).
And the export is a **snapshot** subject to GitHub's run-retention window, so
runs older than that window are already unrecoverable — a fourth, independent
instance of the provenance problem in §6.6.

### 3.5 Corpus E — the mutation-testing run (new, 2026-08-24)

Infection 0.31.9 over four source directories of `stripe`
(`EventSystem/Handler`, `Core`, `Webhook`, `Service`) against the full unit
suite (1,522 tests / 3,971 assertions), inside the project's PHP 8.3 container
with the module set matched to CI. Coverage is generated by PHPUnit and passed
in (`--coverage=<dir> --skip-initial-tests`), because Infection's own initial
test run is non-deterministic (§4.14). The result — **1,592 mutants, 1,123
killed, 469 escaped, Covered Code MSI 70%** — is byte-identical across
`--threads=1/4/8`, three runs each. Escaped mutants are exported per file, line
and mutator (`../data/mutation_escaped.csv`, 469 rows).

Its limits: covered code only (`--with-uncovered` aborts on shop-coupled
classes), `stripe` only, unit suite only, no equivalent-mutant triage, and one
snapshot in time. It is the only corpus that speaks to whether the tests verify
anything, and the only one produced by experiment rather than extraction.

### 3.6 What we can and cannot measure

The corpora fail in different directions, which is why we use all of them.

**Corpus A (journal) limitations,** unchanged from the first draft:

1. **Effort is mostly not clock-stamped.** True HH:MM developer-schedule
   intervals exist in only **three files**
   (`2026/01/20260123/status.md`, `2025/20251203/status.md`,
   `20260508/done/sprint-102-completion-report.md`). Elsewhere, "timestamps" are
   server logs, CI run times, order-lifecycle traces, or hardcoded test
   fixtures, and must not be read as effort.
2. **It is written by the party being studied.** Candid about failure (which
   strengthens it) but not an independent audit.
3. **"Done" ≠ "committed."** Much 2026 work is explicitly "working-tree only /
   commits held."

**Corpus C (Jira) limitations** are set out in §3.3 and are the most restrictive
of the four: no effort data, no severity signal, no transition history, and a
snapshot-only view. **Corpus D (Actions) limitations** are in §3.4: partial
coverage both ways, wall-clock rather than compute, and retention-limited.

**Corpus B (git) limitations,** new and equally real:

1. **Sessions are a lower bound on effort.** A session cannot see thinking,
   reading, or debugging that produces no commit, and it ends at its last
   commit rather than when work stopped. 100 of 227 sessions are single-commit
   and contribute zero measured duration.
2. **A squash destroyed provenance.** On 2026-07-02 `stripe-wallet`'s mainline
   was rewritten (`6e828a242d6b`, "squashed history"), re-adding 562 files as
   new. Pre-July mainline history survives only on `origin/b-7.4.x-LEGACY`. We
   flag and exclude this commit from LOC aggregates; without the legacy branch
   the first eight months would be unmeasurable.
3. **Trailer coverage is partial and late.** `Co-Authored-By: Claude*` appears
   on 149/716 commits (20.8%), but the convention was adopted routinely only
   from 2026-05-07. Absence of a trailer is **not** evidence of absence of AI
   involvement, so this field measures *attribution practice*, not authorship.
4. **Test methods ≠ PHPUnit test count.** We count `function test*`
   declarations; PHPUnit expands data providers. Our series is systematically
   lower than the journal's and the two must never be mixed.

Where the corpora disagree we report both and say which we trust (§4.9, §4.12).

---

## 4. Results — output and cadence (RQ1)

### 4.1 The journal undersampled its own project

| | Journal (A) | Git (B) |
|---|---|---|
| Window | 2025-11-26 → 2026-07-02 | 2025-10-21 → 2026-08-20 |
| Active days | 47 documented day-dirs | **143** with commits |
| Active days *within* the journal window | 47 | **105** |

The journal recorded fewer than half the days on which the project actually
shipped code. This is the single most consequential correction in the revision:
every velocity figure in the first draft was computed over a denominator that
was **2.2× too small**, and the first draft's own hedge — "we treat velocity
numbers as lower bounds on activity on active days" — turns out to have been
correct for the right reason but the wrong magnitude.

### 4.2 Cadence is bimodal, not steady

Across 143 active days: **median 3 commits/day, mean 5.0, maximum 35**. The
distribution is formally **overdispersed**: variance 34.71 against mean 5.01
gives a **dispersion index of 6.93** where a steady (Poisson) process would give
1.0 — χ² = 984.4, df = 142, **p = 4.7e-126**. Only **18 days carry ≥10
commits**, and those days contain the project's structural events:

| Date | Commits | What it was |
|---|---|---|
| 2026-01-16 | 35 | the `payment-base` package split |
| 2026-05-27 | 33 | code-review-114 remediation, day 1 |
| 2026-05-28 | 31 | code-review-114 remediation, day 2 |
| 2026-08-19 | 26 | Sprint 133 honest-failure-paths epic |
| 2025-11-03 | 21 | early contract/event layer build-out |
| 2026-01-15 | 21 | package-split preparation |

The distribution matters for how such claims should be read. "Tens of
gate-passing commits per day" is true of this project, but of **18 days out of
143**; the modal day is three commits. Reporting the peak as the rate — which
the first draft came close to doing — overstates sustained throughput by an
order of magnitude.

### 4.3 Session-derived effort: the journal's biggest gap, partially closed

The first draft could report real effort for **three days**. Commit timestamps
give a lower bound for all of them: **227 sessions, ≈140.1 hours** of active
time (93.5 h within the journal's own window).

| Month | Sessions | Hours | Commits | h/session |
|---|---|---|---|---|
| 2025-10 | 12 | 14.4 | 48 | 1.20 |
| 2025-11 | 28 | 25.7 | 110 | 0.92 |
| 2025-12 | 22 | 13.3 | 52 | 0.61 |
| 2026-01 | 21 | 15.8 | 85 | 0.75 |
| 2026-02 | 27 | 19.9 | 97 | 0.74 |
| 2026-03 | 21 | 5.2 | 36 | 0.25 |
| 2026-04 | 20 | 3.9 | 34 | 0.20 |
| 2026-05 | 29 | 13.6 | 111 | 0.47 |
| 2026-06 | 26 | 17.8 | 71 | 0.68 |
| 2026-07 | 14 | 6.8 | 30 | 0.48 |
| 2026-08 | 7 | 3.8 | 42 | 0.55 |
| **Total** | **227** | **140.1** | **716** | |

Median multi-commit session: **37 minutes**; mean 66; longest 376 (2025-12-01).
Within sessions of more than two commits, the **median rate is 4.4
commits/hour**. (The mean rate, 11.0, is inflated by bursts in which a queued
set of commits lands within a minute or two; the median is the honest figure.)

Two observations. First, the "one sprint is hours, not days" claim from the
journal is corroborated: the modal unit of work is well under an hour of
commit-bearing time. Second, **March–April 2026 is a genuine trough** (9.1 h
across two months, 0.20–0.25 h/session) that the journal narrates as ongoing
work; the git record shows the project nearly idle. Journals record intent,
commits record delivery.

### 4.4 Sustained output without crunch

An unexpected result, and one only timestamps could produce:

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|
| 104 (14.5%) | 132 (18.4%) | **181 (25.3%)** | 156 (21.8%) | 142 (19.8%) | **0 (0.0%)** | 1 (0.1%) |

**Zero Saturday commits across ten months, and a single Sunday commit.** Peak
hours are 13:00 (110 commits), 16:00 (94), 14:00 (85), 12:00 (76), 17:00 (68);
only **29 commits (4.1%) fall outside 08:00–20:00** local time.

This is consistent with the journal's account of a disciplined process, and it
is orthogonal to everything the journal claims — but it is evidence about
*schedule*, not about what produced the schedule. The output described in §4.2
was produced inside ordinary working hours. Whatever the mechanism — the
harness, the assistant, the operator, or an employment context that supplies an
obvious alternative explanation — it did not run on overtime.

Under a null of commits distributed uniformly across all seven days, the
probability of observing **zero** Saturdays in 716 commits is **1.2e-48**. Even
within Mon–Fri the spread is not uniform (χ² = 22.8, df = 4, **p = 0.0001**) —
Wednesday carries 181 commits against an expected 143.

Out-of-hours work is **concentrated rather than absent**, and the concentration
is itself informative. The 29 out-of-hours commits fall on **11 distinct days**,
but **13 of the 29 (45%) land on a single one** — 2026-05-27, the epic's day 1,
running 21:30 → 22:12 (§4.5); an exact binomial against uniformity over those 11
days gives **p = 4.8e-07**. The remaining ten days carry one to three commits
each, mostly just past 20:00. So the picture is not "no evening work ever" but
"evening work was rare, shallow, and once — during the hardest sprint in the
record — sustained." The weekend result carries no such qualification: zero
Saturdays and one Sunday commit across ten months.

### 4.5 The anchor epic, re-measured

The best-instrumented episode is the **code-review-114 remediation**
(2026-05-27/28, `20260527/reports/117-final-achievement-summary.md`): a prior
AI-authored code review ("five parallel deep reviews," reviewer byline *Claude
(Opus 4.7)*) produced 45 findings plus 7 untested classes; remediation ran as 13
numbered sub-sprints (114.0–114.13). The journal's reported outcome, checked
against git:

| Metric | Journal claim | Git-measured | Verdict |
|---|---|---|---|
| Commits | 61 (59 `stripe` + 2 `payment-base`) | **64** (62 + 2) | claim low by 3 |
| Files touched | 178 | **183 unique code files** (88 src + 89 tests + 6 pb); 238 incl. docs; 339 file-change events | ✅ consistent |
| LOC | +11,204 / −5,876 | **+15,844 / −6,075** | claim low by ~41% on insertions |
| Tests added | +202 | **+196 test methods** (1,517 → 1,713) | ✅ consistent |
| Duration | ≈9.5 h "agent compute" across 15 dispatches | **8.2 h** in 4 sessions; calendar spans 11.7 h (day 1, 10:28→22:12) + 5.1 h (day 2, 08:58→14:05) | ✅ same order |
| AI-attributed | not stated | **60 of 64 commits** carry a Claude trailer (94%) | — |
| Findings closed | 54/54 (0 deferred) | not measurable from git | — |
| Quality gates | 61/61 green, 0 new suppressions | not measurable from git | — |

The episode survives verification and is, if anything, understated: **more
commits and ~41% more inserted lines than reported**, in slightly less measured
time. Note the direction of error — a self-report that *undersells* the work is
a different and more trustworthy failure than one that oversells it, and it is
consistent with §6.3, where the assistant's counting errors ran in both
directions.

Two claims in the table are **not checkable from git at all**: findings closed
and quality-gate pass rate. They remain single-sourced to an AI-authored
completion report, and should be read as such.

### 4.6 The test trajectory, measured — and the package split vindicated

The first draft flagged the 2026-01-16 package split as "the single most
important gotcha" for anyone quoting test counts, and could not resolve it.
Measuring both trees at checkpoints resolves it cleanly:

| Checkpoint | Test methods | Test files | Src files | Src LOC | Scope |
|---|---|---|---|---|---|
| 2025-11-01 | 493 | 53 | 112 | 6,837 | stripe |
| 2025-12-01 | 952 | 109 | 197 | 20,234 | stripe |
| 2026-01-01 | 1,215 | 158 | 232 | 25,682 | stripe |
| 2026-01-17 | 1,130 | 152 | 230 | 25,604 | **stripe + payment-base** |
| 2026-02-01 | 1,066 | 141 | 227 | 24,718 | both |
| 2026-03-01 | 1,203 | 175 | 321 | 28,157 | both |
| 2026-04-01 | 1,267 | 182 | 327 | 28,878 | both |
| 2026-05-01 | 1,326 | 194 | 362 | 30,558 | both |
| 2026-05-27 | 1,517 | 230 | 393 | 32,710 | both |
| 2026-05-29 | 1,713 | 263 | 437 | 35,346 | both |
| 2026-07-01 | 1,995 | 300 | 468 | 37,803 | both |
| 2026-08-20 | **2,109** | 319 | 481 | 39,775 | both |

Across the split, `stripe-wallet` fell 1,215 → 478 test methods (232 → 77 src
files) while `payment-base` appeared with 652 methods and 153 src files. The
combined totals move 1,215 → 1,130 methods and 25,682 → 25,604 src LOC — a
**≤7% change in methods and ≤1% in source LOC**. The split was *conservative*:
code was relocated, not lost, and the apparent "regression" in any single-repo
series is entirely an artifact of scope. Anyone quoting a growth curve across
2026-01-16 must sum both packages.

The corrected, scope-consistent growth statement is: **493 → 2,109 test methods
and 6,837 → 39,775 source LOC over ten months**, monotone upward apart from the
split artifact and a small February dip.

### 4.7 Test code outweighs production code 1.69 : 1

Splitting every diff by path category (squash commit excluded) gives the
project's clearest quality signal:

| Category | File-changes | Insertions | Deletions |
|---|---|---|---|
| `docs` | 4,005 | **585,998** | 194,375 |
| `tests` | 2,429 | **150,321** | 62,008 |
| `src` | 2,918 | **88,896** | 40,888 |
| `assets` | 491 | 31,123 | 9,326 |
| `ci` | 288 | 10,074 | 1,894 |
| `other` | 382 | 38,188 | 9,438 |

**1.69 lines of test code were written per line of production code**, and the
result is not an artifact of one period: test insertions exceeded source
insertions in **11 of 11 months** (exact sign test, **p = 0.0010**), and a
percentile bootstrap over commits (20,000 resamples) puts the 95% CI on the ratio
at **[1.39, 2.06]**, with the ratio above 1 in **100%** of resamples. The journal
*asserts* TDD ("if a test never went red, you didn't TDD it"); this measures it. A project that merely claimed TDD while writing tests as an
afterthought could not produce this ratio, and no self-report was needed to
establish it.

Two further readings. First, **`docs` is the largest artifact class by volume**
— 585,998 inserted lines, 4.4× the production code — and an earlier revision of
this paper read that as "the log-as-memory practice is the project's dominant
activity." **That reading was wrong, and correcting it belongs in a paper about
auditing self-accounts.** Decomposing the `docs` insertions by path in the
repository (all refs, squash excluded) gives approximately:

| Documentation class | Inserted lines | Share | What it is |
|---|---|---|---|
| the engineering journal (`daniil_dev_log`) | **≈177,600** | **≈30%** | Corpus A — plans, dispatch briefs, completion reports, status |
| `docs/payment-component/vc` | ≈168,200 | ≈29% | business-strategy and market-hypothesis material, HTML decks, committed under `STRP-52` on 2025-10-27 — **before the journal existed** |
| `scopus` | ≈18,300 | ≈3% | literature export |
| architecture, PlantUML, implementation notes, HTML API docs, other | remainder | ≈38% | project documentation proper |

So the journal that this paper studies is **≈2.0× the production code**, not
4.4×: still the single largest class of authored output, and still a real cost
of driving a stateless agent (§5.5), but half the figure previously quoted. The
error was a category one — `docs/` was read as "the dev log" because the dev
log lives there — and it is the same error in kind as the "330 → 107"
simplification in §4.11: a true aggregate, attributed to the wrong thing. It
was found on 2026-09-21 while pricing the journal for
[`X-02`](X-02-five-deeper-studies.md) S-4; the `docs` category in
`commit_loc_by_category.csv` is unchanged and still correct as a path category.

Second, deletions run at ~46% of insertions in `src` — substantial ongoing
rewriting rather than accretion, consistent with the refactoring discipline the
journal describes.

### 4.8 Retraction: this was not a single-developer project

The first draft listed "single-developer" among its confounds. The commit record
refutes it:

| Author | Commits | Insertions | Deletions | Claude-trailered | Active range |
|---|---|---|---|---|---|
| Daniil Tkachev | 621 | 920,178 | 310,716 | 140 (22.5%) | 2025-10-21 → 2026-08-20 |
| Bartosz Sosnowski | 61 | 66,048 | 6,288 | 8 (13.1%) | 2025-11-05 → 2026-08-18 |
| Mario Lorenz | 19 | 526 | 870 | 0 | 2025-12-05 → 2026-04-07 |
| `dependabot[bot]` | 8 | 44 | 44 | 0 | 2025-10-21 → 2026-07-07 |
| `dantweb` | 3 | 554 | 11 | 1 | 2025-10-21 → 2026-05-27 |
| `Deve L. Oper` | 2 | 4 | 0 | 0 | 2025-10-21 → 2026-01-13 |
| `Bartek Sosnowski` | 2 | 0 | 0 | 0 | 2025-11-07 → 2025-11-11 |

Consolidating aliases (`dantweb` → Daniil; `Bartek` → Bartosz; `Deve L. Oper`
is a placeholder identity), the project had **three human contributors**, with a
dominant one at **87% of commits** and a second at **8.8%** who was active
across the entire ten months, not a drive-by.

This does not overturn the paper's thesis — the harness argument concerns how
work was executed, not how many people executed it — but it does weaken any
inference from this case to *solo* productivity, and it introduces an
unmeasured confound: we cannot tell from git how the second contributor's
practices differed. It also means "n=1" was never quite the right description.
Corrected in §7.2.

**The Jira record goes further.** Git counts only people who *committed*. §4.12
shows a **10-person participant base** with strict role separation, including a
dedicated tester who filed 92.5% of the project's bugs. The "single-developer"
framing was not merely imprecise; it omitted the project's entire quality-
assurance function.

### 4.9 AI-authorship share: what we can and cannot claim

The trailer data is the revision's most uncomfortable result.

| Model string | Commits | Insertions | Deletions | First | Last |
|---|---|---|---|---|---|
| Claude Opus 4.7 | 73 | 19,268 | 9,074 | 2026-05-07 | 2026-08-13 |
| Claude Opus 5 | 33 | 6,559 | 366 | 2026-08-19 | 2026-08-20 |
| Claude Opus 4.8 | 31 | 3,268 | 436 | 2026-06-09 | 2026-07-31 |
| Claude Sonnet 4.6 | 6 | 2,641 | 86 | 2026-05-07 | 2026-05-28 |
| Claude (unversioned) | 5 | 62 | 33 | 2025-12-05 | 2026-07-13 |
| Claude Fable 5 | 1 | 40 | 1 | 2026-08-18 | 2026-08-18 |
| **Total** | **149** | **31,838** | **9,996** | | |

Monthly trailer share: 0% through April 2026, then **65% (May), 27% (June),
67% (July), 86% (August)**. The first two trailers appear on 2025-12-05, then
nothing until 2026-05-07. Split at that date, the change is categorical:
**2/466 (0.4%)** before versus **147/250 (58.8%)** after — Fisher exact,
**p = 5.2e-81**. This is a convention being adopted, not a practice emerging.

The honest conclusion: **the git record cannot substantiate "Claude was the
primary code author" for the first seven months of this project.** It
substantiates it well for May–August 2026, where trailers are routine and reach
86% of commits. Before that, the only evidence of AI authorship is the journal's
own bylines — which are real evidence, but not independent of the subject. The
abstract of this revision is worded accordingly ("a primary code author", not
"the primary code author"), and readers should treat the pre-May-2026 authorship
split as **documented but unverified**.

A secondary finding worth its own study: the trailers name **six distinct model
generations** across four months, with each new generation displacing its
predecessor within days of becoming available (Opus 4.7 → 4.8 → 5). A
multi-month project of this kind is not "built by a model"; it is built across a
succession of models, which complicates any attempt to attribute outcomes to
model capability.

### 4.10 Sprint cadence

Sprints run from a global counter **1 → 133** (~108 distinct numbers referenced
in the journal; the git record extends the series to Sprint 133 in August 2026),
plus named epics. Cadence is typically *multiple sprints per active day* (e.g.
8–13 on 01-23; 63–70 on 02-23/24; 120–121 on 06-05). A novel convention emerged
for large, reviewable epics: **decimal sub-sprints** (102.1–102.5; 114.0–114.13)
used so that each finding or phase maps to its own commit. Commit subjects
corroborate this directly — the August 2026 epic commits read "Sprint 133 S15
(F15): one invariant, one reaction", i.e. sprint, step, and finding identifiers
carried into the commit message itself, making the journal↔git join possible in
the first place. TDD-first is stated explicitly and pervasively — 99 journal
files use RED→GREEN phrasing, and dedicated "RED" sprints (e.g. 83a) precede
their GREEN/REFACTOR counterparts.

### 4.11 Reported "simplifications" were incomplete

Verifying the topic abstracts (`03-topics-technical.md`, `05-measurements.md`)
against the trees surfaced a systematic reporting bias in the project's
refactoring claims. Three figures are exact:

| Claim | Measured | |
|---|---|---|
| webhook dispatch 330 → 107 lines | `StripeWebhookProcessor.php`: **330 → 107** | ✅ exact |
| `LazyStripeAdapter` −183 LOC | `b23f3de`: **0 insertions / 183 deletions** | ✅ exact |
| PHPMD baseline 4 → 3 | `phpmd.baseline.xml`: **4 entries → 3** | ✅ exact |
| cents-math 22 call sites → 1 | source says "~22"; **0 raw `* 100` sites remain** outside the converter | ✅ and it held |
| `ModuleConfigurationServiceInterface` 25 methods | **25 public methods** | ✅ exact |

The precision is notable in its own right — a self-report that matches the
artifact to the line, repeatedly, is evidence for the journal's reliability on
*mechanical* facts.

But the shrinking number is only half of what that commit did. `4a0c0b9`
("Sprint 114.4b") cut `StripeWebhookProcessor.php` from 330 to 107 lines
(+18/−241) by moving the dispatch logic into **8 new handler classes totalling
600 lines of production code**, accompanied by **9 test files (+856 lines)**.
Measured across the module, production handler code went **2,616 → 2,953 LOC**
at that commit and stands at **3,147 LOC across 24 files** today. The largest
individual handler did shrink — the "worst offender" capture handler is now
**305 lines**, down from the cited 389 — so per-unit complexity genuinely fell
while aggregate handler code rose.

The commit as a whole was close to LOC-neutral (**26 files, +1,766/−1,701**),
because it deleted the superseded handlers and their tests as it added the new
ones. That is a well-executed refactor by any standard. The point is narrower
and it is about measurement, not engineering: **"330 → 107" describes one file
and reads as a 68% reduction, when the module-level effect was +337 lines of
handler code and roughly flat totals.**

This is not a bad refactor. Distributing a 330-line `match` into testable,
open-closed handler classes is the right move, and it is what made that epic's
+196 test methods possible. It is a **bad measurement**. Every before/after pair
in the corpus quotes the shrinking number and omits the growing one, which turns
a redistribution into an apparent reduction. The honest formulation, which we
adopt throughout: **these refactors reduced per-unit complexity and increased
total code volume.**

The same caution applies to a claim the first draft repeated without
qualification — "~2,020 LOC of dead code removed." Net `src` deletions across the
whole project run at 46% of insertions, consistent with substantial rewriting,
but no single-figure "LOC removed" claim in the corpus is stated net of the code
added to replace it. Note this is a reporting convention, not dishonesty: the
figures that *can* be checked are exact (see the table above), which is why the
convention is worth naming rather than treating as a credibility problem.

One further verification worth recording, because it is the strongest single
confirmation in the set. `03-topics-technical.md` (TECH-3) proposed a criterion
for detecting fake interface segregation — *count the consumers that typehint the
narrow interface* — and predicted the answer was zero. It is **exactly zero**:
each of the four Stripe adapter sub-interfaces is referenced precisely twice, by
its own definition file and by the composite interface that extends it, while 4
files typehint the wide composite. The assistant's own self-correction (*"the
split is fake… ISP without narrowed consumers buys nothing"*) is confirmed by
measurement rather than accepted on authority — an instance of the assistant
being right about its own earlier mistake.

### 4.12 The Jira record: who asked, who tested, and a three-year prehistory

The issue tracker answers questions neither prose nor commits can, and it changes
the shape of the case study.

**(a) Strict role separation across 10 participants.** Cross-tabulating reporter
against issue type (`../data/jira_roles.csv`) produces an unusually clean
division of labour:

| Reporter | Story | Task | Bug | Sub-task | Total | Share |
|---|---|---|---|---|---|---|
| Daniil Tkachev | **52** | 5 | **0** | 0 | 57 | 36.5% |
| Zerfas Razvan | 0 | 5 | **37** | 0 | 42 | 26.9% |
| Daniel Paniagua | 0 | **26** | 0 | 0 | 26 | 16.7% |
| Mario Lorenz | 6 | 4 | 0 | 8 | 18 | 11.5% |
| René Gust | 0 | 5 | 0 | 0 | 5 | 3.2% |
| Szabo Botond | 0 | 0 | 3 | 0 | 3 | 1.9% |
| 4 others | 0 | 5 | 0 | 0 | 5 | 3.2% |
| **Total** | **58** | **50** | **40** | **8** | **156** | |

The developer who wrote the code with the assistant filed **52 Stories and zero
Bugs**. A different person filed **37 of the 40 Bugs (92.5%) and zero Stories**.
A third filed **26 of 50 Tasks and nothing else**.

The separation is statistically near-deterministic, and this is the most robust
result in the paper: Fisher's exact test on the developer×tester / Story×Bug
2×2 — `[[52,0],[0,37]]` — gives **p = 6.7e-26**, and the full reporter×type table
gives **χ² = 199.4, df = 6, p = 2.6e-40, Cramér's V = 0.859**. (These corpora are
censuses rather than samples, so the null being rejected is "reporter is
independent of issue type," not a claim about projects in general — see §7.2.)

This finding has a published theoretical frame, and the paper should use it rather
than claim discovery. Agarwal, Miller, Kästner and Vasilescu
(arXiv:2607.07980), synthesising 3,100 coded practitioner documents into a causal
model, argue that *"review is the control point through which a coding agent's
effect on software is decided, and that AI does not fix the sign of that effect:
the team sets it, through the expertise its humans bring and how it structures
the review process."* Their theory is explicitly falsifiable and rests on
discourse; **§4.12a is a measured instance of it** — one team, one structure, and
a near-deterministic association (V = 0.859) between role and defect discovery.
Garousi (arXiv:2606.05770) independently characterises the "oversight burden" of
AI-assisted work qualitatively but does not ask *who* bears it. Full positioning
in `08-literature-review.md` §5.2.

This is the single most important addition in this revision, because it changes
what the case is evidence *for*. The paper's thesis — that a process harness
makes AI-assisted output trustworthy — was built from the journal's account of
TDD, quality gates, and the developer's own claim-checking. That account is
accurate but **incomplete**: there was also an independent human tester
generating defect reports the pair then worked from. "Trust-but-verify" was not
only the developer grepping the agent's claims (§6.3); at the project level it
included a person whose role was to find what the pair had got wrong. Any
attempt to generalise from this case must carry that structure with it — the
result is not "one developer plus an AI can ship a payment module," it is "one
developer plus an AI, fed by a dedicated tester and a project manager, can."

**(b) Implementation coverage is partial and type-dependent.** Of 156 issues,
**61 (39%) have at least one commit referencing them**:

| Issue type | With code | Total | Coverage |
|---|---|---|---|
| Story | 40 | 58 | **69%** |
| Bug | 17 | 40 | **42%** |
| Task | 4 | 50 | 8% |
| Sub-task | 0 | 8 | 0% |

Coverage is not independent of issue type: χ² = 47.4, df = 3, **p = 2.9e-10**.

Stories convert to code at 69%; Tasks at 8%, which is consistent with Tasks
being coordination rather than engineering. The most-referenced issues are
`STRP-145` "DevLog review" (64 commits), `STRP-78` "Extract Component" (57),
`STRP-52` "Develop Strategy" (33) and `STRP-60` "Provider SDK integration" (32)
— i.e. a handful of umbrella issues absorb the bulk of the history, which is why
ticket references are a poor unit of work for this project.

**(c) Zero fabricated ticket numbers.** All **61** distinct `STRP-nnn` ids in
commit messages resolve to real issues. Across 436 ticket-bearing commits the
assistant never invented an identifier — a concrete, checkable rebuttal to the
most common worry about LLM-authored commit metadata. The one defective case is
a *mislabelling*, dissected in §6.1.

**(d) Formal triage corroborates the journal's "not-a-bug" claim.** §6.7 reports
that "a meaningful fraction of reported bugs resolved on investigation to
configuration, data, or infrastructure." Jira has the statuses to prove it:
**3 issues closed `Not a bug`** and **3 more marked `Core Bug`** — defects
triaged to the OXID platform rather than the module. Six of 40 bug reports (15%)
were reclassified away from the module.

**(e) A three-year prehistory the paper did not know about.** **55 of 156 issues
(35%) were created before the git record begins**, the earliest on
**2023-05-30** — overwhelmingly `Task` (44) and `Sub-task` (8), of which 44 are
`Done`. The STRP project is roughly **three years old**; the AI-assisted
implementation phase this paper studies is its final ten months. The framing of
a "7-month" or even "10-month" project describes the *coding*, not the effort.
Whatever strategy, vendor evaluation, and design work those 2023–2025 tasks
represent is a cost this study does not count and cannot attribute.

**(f) Lead time, weakly.** For the 39 issues with a `Resolution`, median
Created→Resolved is **17 days** (mean 28, max 91). This is the corpus's weakest
number: `Resolution` is set on 39 issues while 82 sit in status category `Done`,
and several 0-day resolutions are 2023-era tasks that look bulk-closed. Report
it as an order of magnitude, not a cycle-time measurement.

**What Jira does not contain.** No effort data of any kind (§3.3), no usable
severity signal, no status-transition history — and, decisively for one hoped-for
result, **no estimates**. The estimate-vs-actual study proposed in
`02-topics-project-management.md` (PM-3) is not recoverable from any of the three
corpora.

### 4.13 The CI record: failure was the environment, not the code

Corpus D settles a question the journal asserts repeatedly and could not
demonstrate — that the dominant engineering cost was the build and integration
environment rather than application logic (§6.7).

**(a) CI failed on half of all runs — an outlier rate.** Of **979 workflow
runs**: **487 failure, 453 success, 39 cancelled** — a **49.7% failure rate**
(51.8% of decided runs). For ten months, pushing this project's code produced a
red pipeline about as often as a green one.

Two corrections to how this was first reported. First, an earlier revision
attached an exact binomial test against a 50/50 null (p = 0.28); **that test
assumed independent runs, and runs here are strongly autocorrelated (g), so it is
withdrawn.** The proportion is a census fact and needs no test. Second, published
baselines put build-failure rates at **26%** for closed-source projects, **19%**
for large long-lived projects, **>38%** for Java OSS CI workflows and **~12%** for
industrial hardware-in-the-loop systems — so **our rate is roughly double the
closed-source baseline** and is a property of *this* project rather than a general
fact about CI. That strengthens rather than weakens the argument in (c): an
unusually fragile build environment is exactly where patch-unrelated failures
should dominate.

**(b) The machine spent longer on this project than the humans did.** Summed run
duration is **169.5 h**, against **≈140.1 h** of session-derived human activity
(§4.3) — and **90.1 h of it (53%) was consumed by runs that failed**. The two
figures are not commensurable (CI wall-clock is concurrent and includes queueing;
sessions are a lower bound), so the claim is only "the same order, machine ≥
human." Even hedged, it reframes where a small AI-assisted project's time goes.

The cost has a shape as well as a size (`stats.py` T12). Walking runs in time
order within each repository × workflow, **74 failure streaks ended in a green
run**; the median streak was **2 runs and 4.1 hours** from first red to next
green, the 75th percentile **28.7 hours**, and the longest **358 hours** — about
fifteen days. **23 streaks ran to five or more consecutive failures.** These are
calendar hours including nights and weekends, so they bound repair *latency*,
not effort; but a pipeline that stays red for a median half-day and a tail of
two weeks is not functioning as a gate during those intervals.

**(c) Commit size does not predict CI failure — and that is the finding.**
Joining runs to per-commit diffs (n = 444 commits with CI):

| Commit size | Commits with ≥1 failing run |
|---|---|
| ≥500 insertions | 77/123 (**63%**) |
| <500 insertions | 193/321 (**60%**) |

Fisher exact **p = 0.66**; Spearman **ρ = −0.024** (p = 0.61). There is
**no association whatsoever** between how much code a commit changed and whether
its pipeline failed.

This negative result is the section's substantive contribution. The intuitive
model — bigger changes break more builds — predicts a clear gradient, and there
is none. If these failures were *logic* failures they would scale with volume of
changed logic. They do not, because they were dependency-auth failures, PHP
version skew, namespace-generation ordering, and flaky E2E — none of which is
sensitive to line count. The journal's environmental account of its own pain
(§6.7, `03-topics-technical.md` TECH-4) is thereby corroborated by the *absence*
of a correlation, which is a stronger test than any of its narrative evidence.

**(d) AI-attributed commits were no more CI-fragile.** Commits carrying a Claude
trailer had a failing run **29/49 (59%)** of the time; those without,
**241/395 (61%)** — Fisher **p = 0.88**. Given how readily the opposite is
assumed, a stated null is worth reporting. It must be read narrowly, though:
trailered commits cluster in 2026-05→08 when the failure rate was already
falling (e), n = 49 on one side, and trailers measure attribution practice rather
than authorship (§4.9). This is *not* evidence that AI-written code is as good;
it is evidence that this project's CI did not discriminate.

**(e) The failure rate improved by 11 points — descriptively.** Split at
2026-04-01: **270/473 (57%)** of decided runs failed before, **217/467 (46%)**
after; nominal Fisher **p = 0.0014**. **Corrected for the autocorrelation in (g),
this falls to p = 0.18 and is no longer statistically significant.** The
descriptive change is real and coincides with a *process* claim: the hardening the journal describes (permanent TDD
probes after the namespace break, converged cross-repo dependency auth) shows up
in the artifact as a real reduction. The caveat is composition — Playwright E2E
and load-test workflows arrive later in the period, so some of the shift may be
workflow mix rather than reliability, and the split point is chosen rather than
derived.

**(g) Failures cluster, and the clustering carries both a substantive and a
methodological result.** Walking runs in time order within each repository ×
workflow: **409 of 477 failures (85.7%) are immediately preceded by another
failure**, against a published multi-project benchmark of ">50%". Outcome
**transitions occur on just 15.9%** of consecutive pairs where independence
predicts **49.9%**, and **lag-1 autocorrelation is 0.680** — an effective sample
size of roughly **179 against a nominal 940**.

Substantively this is what an environmental account predicts: a broken build
environment stays broken until someone repairs it, whereas defects in changed
logic would produce far more independent outcomes. Methodologically it obliges
the corrections in (a) and (e), and it means **any run-level test on CI data of
this kind must model the dependence** — ours initially did not. We found it only
by testing a published claim against our data, which is the same
verify-against-an-outside-reference discipline the paper argues for elsewhere
(§7.4).

**(f) A fourth provenance loss.** 234 of 979 runs (24%) point at `head_sha`
values reachable from no ref in either repository — CI ran against branches that
no longer exist. And GitHub retains run history for a limited window, so runs
older than it are **already gone**, unrecoverably. Corpus D thus arrives
carrying the same survivorship problem as Corpus B (§6.6), from a third
independent mechanism.

**(h) Busy days fail more — as a description, and not as a tested result.**
§4.2 established that cadence is bursty. Joining that to CI outcome asks whether
the code produced on burst days differs from the rest (`stats.py` T11). On the
17 days with ≥10 commits (the three mechanical days — package split, namespace
rename, release squash — excluded), **100 of 138 commits (72%)** had a failing
run; on ordinary days, **160 of 284 (56%)**. Treating commits as independent,
Fisher gives p = 0.0014. **Commits are not independent**: outcomes cluster
within days as they do within workflows (g), and a permutation test that
shuffles the *burst* label across the 128 active days with CI — preserving
within-day clustering — gives **p = 0.18**. The direction holds in both halves
of the record (74% vs 54% before 2026-04-01; 66% vs 59% after), and burst-day
commits carried *more* test code per source line (1.94 vs 1.65), so a "rushed,
under-tested" account is not what the data show. We report this exactly as we
report (e): a real descriptive difference of 16 points, compatible with worse
code, with a broken environment on the days the project pushed hardest, or with
period effects — and not a finding. The outcomes that would discriminate
between those accounts (escape density and later bug-touch of burst-day lines)
are specified in [`X-02`](X-02-five-deeper-studies.md) S-1.

### 4.14 Mutation testing: 70% of mutations detected — and a measurement that took four attempts

The test-effectiveness literature holds that suite **size** is the wrong proxy
and that neither size nor assertion density settles the question. §4.7's 1.69:1
ratio is a size metric. We therefore ran mutation testing — and the more
instructive half of what follows is that **we got the wrong answer three times
first.**

**The result, reproducible across `--threads=1`, `4` and `8`, three consecutive
runs each:**

| | Baseline (`b-7.4.x`) | After the remediation sprint |
|---|---|---|
| Mutants generated | 1,578 | **1,592** |
| Killed | 1,084 | **1,123** |
| Escaped | 494 | **469** |
| **Covered Code MSI** | **68%** | **70%** |

So the suite executes the mutated code and detects **70%** of the semantic
changes made to it; **30% go unnoticed**. Neither §4.7's write ratio nor an
assertion count (≈2.3/test) predicted that, which is the literature's point.

**Why the first three attempts failed, and why it matters.** The initial run
reported 462 mutants and MSI 73%, and that figure was published as a measured
result. It was not reproducible: seven repeat runs against unchanged code
returned **0 to 1,019 mutants and 0% to 73% MSI**. Changing the coverage driver
(installing pcov after discovering `xdebug.mode` was `debug,profile` and had
never included `coverage`), raising the timeout tenfold, and clearing every cache
did **not** fix it.

The cause was upstream of all of that. Infection's *generated* initial-test
configuration runs PHPUnit **with a random seed**, and that run terminates early
at a variable point — one observed run derived its coverage from 143 of 1,522
tests. Meanwhile **PHPUnit's own coverage is perfectly deterministic**: 185
files, 3,539 covered statements, byte-identical file sets across three runs. The
fix is to generate coverage with PHPUnit and pass it in
(`--coverage=<dir> --skip-initial-tests`).

A contributing defect turned up en route: a test carried a `CoversClass`
attribute pointing at a **class that does not exist** (`Service\ReconciliationResult`
rather than `Service\Result\ReconciliationResult`), and the resulting PHPUnit
warning is what halted the run at a random position.

**This episode is itself a finding, and it belongs in §7.4.** A single invocation
of the tool returned a confident-looking percentage every time. The instability
was invisible without running it three times — which is not standard practice,
and which no paper reporting an industrial MSI that we located reports doing.

**What the corrected numbers say.** Escapes concentrate in the orchestration
layer — `StripeCaptureRequestHandler` (54), `StripeCheckoutSessionHandler` (36),
`ReturnSessionSecurityService` (34), `CaptureService` (27) — and the largest
mutator category is **`MethodCallRemoval` (85 of 469)**: a call can be deleted
with the suite still green, the signature of tests asserting against doubles
rather than behaviour. That is the phenomenon the project documented in its own
hollow tests and banned in rule R-1.5 (§6.5), still present in quantity after
that remediation.

The converse is as informative. The three classes into which the project
consolidated its money arithmetic — `AmountConverter`, `MinorUnitConverter`,
`CapturableAmount` — have **zero escaped mutants**, re-verified on the corrected
469-row set rather than the retracted first draw. The cents-truncation bugs of
§7.1 were fixed by moving arithmetic into value objects; mutation testing shows
that move produced fully verified code, and that the remaining risk sits in the
orchestration around it. Where escapes concentrate is therefore not a random
sample of the module but a map of its *glue*: 169 of 469 in event handlers, 39
in webhook handlers, and the rest in services.

**And the remediation is measurable.** Thirteen tests written against three of
the worst files closed **25 escapes** and moved MSI **68% → 70%**, with the
targeted files going 27→8, 7→4 and 3→0. Four of those kills were additionally
verified by hand — applying the mutation to the production file and observing
exactly one failure where there had been none.

**Caveats.** Covered code only (`--with-uncovered` aborts on shop-coupled
classes). `stripe` only; `payment-base` has no baseline. The 469 escapes were not
triaged for equivalent mutants, and at least one demonstrably *is* equivalent, so
**100% MSI is not a coherent target**. Unit suite only.

---

## 5. Results — the collaboration model (RQ2)

The journal does not describe "using an AI to write code." It describes a
**process harness** in which the assistant operates, and the harness is
remarkably specific. This section remains journal-sourced; git can corroborate
its *outputs* (§4.4, §4.7) but not its internal rules.

### 5.1 The quality gate is the commit boundary

290 of 462 journal files reference the gate: `phpcs` (PSR-12) /
`PHPStan --level=max` / `PHPMD` / `PHPUnit`, bundled as `pre-commit-check.sh`.
The rule is absolute: gates green *before* commit, no new suppressions. The
S114 epic reports 61/61 green and a shrinking suppression baseline. The gate is
not advisory scaffolding; it is the definition of "done." *(Not independently
verifiable from git — see §4.5.)*

### 5.2 TDD is literal, not aspirational

Completion reports carry RED-test tables and the maxim *"If a test never went
red, you didn't TDD it."* Refactors are guarded by characterization tests first.
The rule set (`_engineering_requirements.md`, R-1…R-10) even forbids
re-implementing the method-under-test inside a test double (R-1.5) — a subtle
self-deception the project had actually committed earlier and then banned (the
"false-positive tests," §6.5). **This is the one process claim the git record
independently confirms**, via the 1.69:1 test-to-source write ratio (§4.7) and
the +196 test methods added during the two-day epic (§4.5).

### 5.3 Dispatch-oriented orchestration

The core execution vehicle is a named custom sub-agent, **`tdd-solid-engineer`**,
dispatched **one phase per invocation**. Two orchestration rules are recorded as
hard-won:

- *"The dispatch boundary is a hard constraint; the prompt is a soft one."*
  When per-commit granularity mattered, the human split the work into more
  dispatches rather than asking one dispatch nicely — because the assistant
  would otherwise collapse phases (§6.2). (`118-lessons-learned.md`)
- *"Sequential, not parallel."* Concurrent dispatches share the one Docker
  MySQL/OXID cache and cause flakiness; worktree isolation is wrong here because
  the container mounts a fixed host path. So agents run one at a time.
  (`118-lessons-learned.md`)

The commit record is consistent with sequential execution: within the epic's
sessions, commits are serialized with no interleaving pattern suggesting
concurrent branches of work.

### 5.4 Division of labor

- **Assistant:** the bulk of planning docs, test authoring, code generation,
  refactoring, diagnosis, and completion reports.
- **Human:** scope rules (restated as *ABSOLUTE HARD RULES* atop every dispatch,
  because "agents work from the prompt, not from session history"), ambiguous
  and security decisions (STOP-and-ask), commit/merge/scope gating, and
  independent verification of the assistant's claims.

Note that this division is asserted by the journal and only partly verifiable
(§4.9). The human remained the *committer* throughout — every commit is authored
by a human identity, with the assistant credited via trailer — so the
commit/merge gating claim is at least structurally consistent with the record.

**The journal's two-party framing is incomplete.** §4.12 shows the division of
labour extended beyond the developer–assistant pair: a dedicated tester supplied
92.5% of bug reports and a project manager supplied half the Tasks. The pair
described here is the *implementation* unit, not the *quality* system. The
journal never mentions this, presumably because it is a developer's own log —
which is exactly the kind of blind spot a self-reported corpus produces.

### 5.5 The log as memory

The journal is not documentation-after-the-fact; it is the pair's working
memory. `20260529/done/handoff.md` is a session-to-session handoff containing
exact `git status`, commit-sequencing scripts, a *"Resume command (paste at
session start)"*, and prescribed updates to a persistent `MEMORY.md` "so future
Claude sessions don't re-litigate these decisions." The daily-log discipline is
itself an engineered mitigation for a stateless assistant — and, per §4.7, the
single largest category of output the project produced.

---

## 6. Results — failure modes (RQ3)

An honest account is the most useful part of this case. The assistant failed in
characteristic ways; the value lay in the mechanisms that caught it.

### 6.1 Instruction violation

*"⚠️ Agent committed as `bf32d77 "STRP-138 AGB complience"` against the 'do not
commit' instruction — typo, unconfirmed ticket number, no `Co-Authored-By`
trailer, status.md committed empty."* (`20260622/status.md`) — a clear, logged
breach of an explicit human constraint.

This is the one incident where all three corpora meet, so it is worth resolving
completely. Every element of the complaint checks out against the commit object
(2026-06-22 13:33:39 +0200, 12 files, +875/−11):

| Journal complaint | Artifact |
|---|---|
| committed against "do not commit" | commit exists, on the logged date ✅ |
| typo | subject is `STRP-138 AGB complience` ✅ (33 subjects in the corpus carry spelling errors) |
| no `Co-Authored-By` trailer | zero trailers ✅ — one of the untrailered commits in a month otherwise running at 27% |
| `status.md` committed empty | `docs/…/20260622/status.md` at **0 changed lines** ✅ |
| "unconfirmed ticket number" | **see below — validated, and more interesting than it looks** |

The ticket complaint is the instructive one. `STRP-138` is **not** fabricated —
Jira has it as a real Bug, now `Passed QA`: *"Order now button stays disabled
after returning from external payment page."* But the commit's **code** is
Terms-and-Conditions consent work (`agb_validation_controller.js`,
`StripeOrderControllerAgbConsentTest.php`, `StripeOrderController`,
`order.html.twig`), which is a **different Jira issue** — `STRP-139`,
*"Terms and Conditions checkbox can be unchecked after clicking Order now."*
Meanwhile the dev-log file the commit also carries is named
`sprint-128-strp-xxx-order-button-disabled-after-external-payment-return.md` —
the agent's own planning document had a **literal `strp-xxx` placeholder** where
the ticket id belonged.

So the failure was not invention but **conflation**: two related bugs worked
together (an earlier commit, `fcfed0e`, is honestly labelled `STRP-138-139`),
then landed as one commit under one of the two ids, with the other ticket's
documentation attached and a placeholder left in the plan. **`STRP-139` appears
in no commit message anywhere in the corpus** — the T&C bug was fixed but never
attributed.

Three things follow. First, the human's terse "unconfirmed ticket number" was
**correct**, and cheap claim-checking (§6.3) caught in seconds something that
took this study three corpora and a join to reconstruct. Second, this is
simultaneously an instance of **commit-granularity collapse** (§6.2) — two
tickets, one commit — which suggests the two failure modes share a cause rather
than being independent. Third, and reassuringly, the *class* of error is mild:
across 436 ticket-bearing commits the assistant produced **zero fabricated
identifiers** (§4.12c) and exactly one traceable mislabel.

### 6.2 Commit-granularity collapse

Despite a prompt asking for per-phase commits, "the agent collapsed phases 2–4
into one commit." Mitigation: split the dispatch (§5.3).

The commit record lets the mitigation be checked, and it did not do what the
journal believed. The decimal sub-sprint scheme (114.0 → 114.13) was introduced
so that one phase would map to one dispatch and one commit. Measured: **9 of 13
sub-sprints (69%) span more than one commit, median 5.** The convention failed
on its own terms. Whether it was nonetheless *better than* ordinary sprint
numbering is untestable with 13 groups against 6 (31% vs 33% single-commit,
Fisher p = 1.00) — an earlier revision of the companion report called this
"refuted", which overstated it; the data are silent. The transferable point
survives either way: if one unit per commit matters, the harness must produce
it, because a naming scheme measurably did not.

### 6.3 Over-claiming and miscounting

The human, treating agent reports as *hypotheses*, caught: a "boundary sealed"
claim that was approximate (two legitimate SDK imports remained); a baseline
miscount ("agent said '4 baselined' but baseline was actually 3"); and stale
line-numbers from an earlier review. Rule drawn: *"never trust a finding's line
numbers more than a fresh grep; the cost is 1–2 minutes and catches both
overclaims and undocumented exceptions."*

§4.5 adds a data point to this class: the epic's completion report **undercounted
its own output** by 3 commits and ~4,600 inserted lines. Miscounting was
bidirectional, which is itself informative — the assistant was unreliable at
arithmetic over its own work, not systematically self-flattering.

### 6.4 Documentation-vs-implementation drift

An early architecture review contains an explicit *"Hallucination Analysis"*
classifying documented-but-unbuilt models as aspirational rather than
fabricated — an honest reckoning that design docs had run ahead of code.
(`2025/20251128/ARCHITECTURE_REVIEW.md` §12)

§4.3 shows the inverse drift at project scale: during the March–April 2026
trough the journal continues to narrate active work while the git record shows
9.1 hours of commit-bearing activity across two months. Documentation ran ahead
of code not only in design but in reported progress.

### 6.5 Test dishonesty — the most instructive class

Several defects were *tests that passed without testing*:

- **False-positive tests** — assertions hidden inside `willReturnCallback` that
  effectively ran `assertTrue(true)`
  (`2025/20251209/done/sprint-17-fix-false-positive-tests-report.md`).
- **Silent skips** — the integration suite reported 157 tests with **53 silently
  skipped** (~34%) when Stripe credentials were absent: a green CI hiding a
  third of the layer, later hard-gated to zero silent skips (`117` §5).
- **Suppression hiding a real crash** — every admin refund crashed on a call to
  the nonexistent `setState('REFUNDED')`; PHPStan had *caught* it, but a
  `phpstan.neon` ignore had silenced the signal, turning a static error into a
  latent runtime money-path crash (`2026/02/20260206/*`, the STRP-89 bug).

The recurring house rule that emerged — *never suppress, fix the code* — is
directly traceable to this class of failure. Note the tension with §4.7: a high
test-to-code ratio is necessary but not sufficient, since this project
demonstrably produced *volume* of test code that included tests asserting
nothing.

### 6.6 A failure only git could see: the history squash — and a survivorship problem

On 2026-07-02, `stripe-wallet`'s mainline was rewritten into a single commit
(`6e828a242d6b`, "Stripe payment module v3.1-rc.1 (squashed history)")
re-adding 562 files. The eight months of commit-level history that this paper
depends on survive only because a `b-7.4.x-LEGACY` branch was retained — 491
commits that are not reachable from the current mainline.

This is a process failure of a distinct kind: not a wrong line of code, but the
**destruction of the project's own audit trail** at the point of a release. It
went unremarked in the journal.

**Stated precisely, because the compliance claim is narrower than it first
appears.** PCI DSS 6.4/6.5 requires an auditable change-control record —
documented impact, approval by authorised parties, testing, and back-out
procedures — but it does **not** stipulate that the record must be the version
control graph; an organisation could satisfy it through a separate
change-management system while squashing its history. The defensible claim is
conditional: **where a project's change-control evidence *is* its commit history,
as it was here — the dev log and commit trail being the only record of what
changed, why, and with what testing — destroying that history at release removes
the artifact the audit depends on.** It is also a cautionary note for this
research programme: had the legacy branch been pruned, §4.1–§4.7 would have been
impossible.

**A second mechanism, found by accident, and it generalises the problem.**
Comparing the measured corpus against a **stale local checkout frozen at
2026-05-22** (`strp-test-may-21`) revealed a commit that exists nowhere on the
canonical remote: `ce96dc86085b` — 25 files, +1,710/−60, subject **"test"** — the
working tip of the feature branch `b-7.4.x-webhook-STRP-144`. That branch, and
`b-7.4.x-fixing-ci`, have since been **deleted from the remote**.

Unlike the squash, this is *routine* practice: the work was consolidated onto the
mainline as `3a50c1c` "STRP-144 Webhook registration" (61 files,
+5,431/−1,255 — a further-developed version, different tree) and the branch was
then pruned. All five source files survive in the current tree. **No code was
lost; the incremental history of how that feature was built was.**

Three consequences, and the third is the important one.

1. **The measurement impact is negligible.** One commit out of 717 known
   (0.14%). We deliberately **do not** add it to the corpus: its content overlaps
   `3a50c1c`, so including both would double-count the same work. Every figure in
   §4 remains as reported, over the history reachable from the canonical remote.
2. **It refines the message-hygiene finding** (§4.10, M-17). The orphan's subject
   is literally `test`. Feature-branch commits were casual; the mainline commit
   that superseded it is properly titled. Commit-message quality in this project
   was a function of **branch role**, not of author or period — which is a more
   charitable and more accurate reading of the 102 reused subjects than
   "carelessness."
3. **Git-based research on this repository measures the surviving history, not
   the actual one.** Two independent mechanisms — a mainline squash and ordinary
   branch pruning — removed provenance during the study window, and *neither is
   detectable from inside the repository*. We found the second only because a
   stale checkout happened to exist on the same machine. Any commit-mining study
   of a project that squashes releases and deletes merged branches inherits an
   invisible survivorship bias, and should say so. §7.3 records this as a
   standing limitation rather than a resolved one.

The orphan's status is worth one further sentence, because it illustrates how
thin this margin is. In the working checkout the commit is a **dangling
object** — present in the local object database from a fetch that predates the
branch deletion, reachable from no ref, and referenced by nothing on the remote.
It would not survive a `git gc`. The provenance of that feature is currently one
routine maintenance command away from permanent loss, and the same is true of
whatever else is dangling in checkouts nobody has thought to compare.

**What the squash destroyed can be shown, not only asserted.** Running
`git blame` on the current mainline attributes **every line** of the module's
largest file — all 305 lines of `StripeCaptureRequestHandler.php` — to the
2026-07-02 squash commit; the same file blamed on the retained legacy branch
resolves to **17 commits dated 2025-12 through 2026-05**. Any question that
requires knowing *when and under what conditions a line was written* — which
lines the suite fails to verify (§4.14), which commits introduced the bugs the
tester found — is unanswerable on the mainline and answerable only by grafting
the legacy branch back onto the squash. Two of the five studies proposed in
[`X-02`](X-02-five-deeper-studies.md) depend on that graft and would otherwise
not exist.

The provenance problem also has a partial remedy that is worth naming because
it lies outside version control. Fourteen frozen checkouts of the module,
dated 2025-11-25 through 2026-09-18, survive on the developer's machine as
by-products of installation testing. They are independent witnesses to the
repository's state at fourteen dates, immune to squash and pruning, and they
are what surfaced the orphaned commit above. A study that intends to be
auditable should keep such snapshots deliberately rather than rely on their
accidental survival.

### 6.7 Frequency and severity

The incident forensics pass catalogs **~75 distinct bugs/CI failures/
regressions**. The largest cluster is **CI/infra & cross-repo dependency auth**
(fragile private dependency tokens, PHP 8.2-vs-8.3 skew,
fresh-install-vs-persisted-local divergence); the deepest cluster is the
**contract state-machine × OXID `finalizeOrder`/`sess_challenge`** interaction,
which produced empty-order shells repeatedly (including once as a *regression
inside a fix*). Notably, a meaningful fraction of reported "bugs" resolved on
investigation to configuration, data, or infrastructure — the assistant's triage
correctly reclassified them as not-a-bug.

The git record corroborates the CI cluster's prominence: `ci`-category commits
number 288 file-changes, and commit subjects in the "ci:" prefix family recur
across the whole span (e.g. "ci: fix composer resolution — payment-base alias
and dev stability", 2026-08-19).

**Corpus D converts this from prominence to dominance** (§4.13): CI failed on
**49.7% of 979 runs**, consumed **169.5 h** of wall-clock with **53% of that in
failing runs**, and — decisively — failed **independently of commit size**
(Fisher p = 0.66, ρ = −0.024). The journal's ranking of infrastructure above
logic as a cost centre is measured, not merely asserted.

---

## 7. Discussion, quality, and threats to validity (RQ4)

### 7.1 Did discipline produce quality, or its appearance?

The strongest positive evidence is now twofold. First, the **side-effect bugs**:
consolidating duplicated cents-math (a DRY refactor, not a bug hunt) surfaced
*four real-money truncation bugs that no review had flagged*
(`(int)(19.99*100) = 1998`, charging €19.98). Discipline found defects that
inspection missed — an *observation*, not a tested result: the tester filed six
different amount-related bugs on the same subsystem with zero overlap, but the
probability of zero overlap cannot be computed without the size of the defect
pool, which is unknowable (`06` N-5). Second, and new in this revision, the **1.69:1 test-to-source
write ratio** (§4.7) and the **absence of crunch** (§4.4): the project's own
output profile is what a disciplined process looks like from the outside, and
neither figure depends on the project's testimony about itself.

A third strand, from Corpus D: **CI failure did not scale with the amount of code
changed** (§4.13c, Fisher p = 0.66, ρ = −0.024). That matters for this question
because it locates the friction *outside* the code the process governs — the
harness cannot be credited or blamed for failures that were indifferent to what
was written.

The strongest negative evidence is §6.5: the same project shipped tests that
tested nothing, and a suppression that hid a crash, until later audits caught
them — plus §6.6, a release that discarded its own history. The honest reading
is unchanged: **the process both created and caught these problems.** Quality
here is a property of the *loop*, not of any single commit, and volume of test
code is not the same thing as verification.

### 7.2 Confounds (revised)

**A standing caveat on every p-value in this paper.** Both machine corpora are
**censuses**, not samples: every commit and every issue in the window is present.
So the tests in §4 reject specific chance-arrangement nulls — reporter
independent of issue type, commit timing independent of weekday, months
exchangeable with respect to which category grew faster — and none of them
licenses an inference to AI-assisted development *in general*. That inference
requires a second case, which this study does not have (§7.4). A full inventory
of which claims carry a test, which are census facts needing none, and which are
underpowered or out of reach is maintained in
`07-lessons-learned.md`.


- **Not single-developer, and not a two-party process.** Three human
  contributors committed code, dominated by one at 87% of commits (§4.8); the
  Jira record shows a **10-person participant base** with a dedicated tester
  filing 92.5% of bugs and a project manager filing half the Tasks (§4.12a). The
  first draft's "single-developer" claim is retracted twice over. The tester's
  contribution is a **confound we cannot size**: we do not know how much of the
  observed quality is the harness and how much is an independent human finding
  defects.
- **The studied window is a phase, not the project.** 35% of Jira issues predate
  the commit record, the earliest by 2.4 years (§4.12e). Strategy, evaluation and
  design costs incurred 2023–2025 are invisible to every velocity figure here.
- **Not single-model.** Six model generations appear in the trailers over four
  months (§4.9); outcomes cannot be attributed to "a model."
- **Operator effect.** The dominant developer is highly disciplined and
  security-literate; the results may reflect the operator as much as the tool.
- **No counterfactual.** There is no non-AI arm, so we cannot attribute velocity
  to the assistant versus the harness versus the person.
- **Single framework, single domain.** One legacy PHP e-commerce platform, one
  payment integration. Corpus D sharpens why this matters: half of all pipeline
  outcomes were environmental friction specific to *this* framework's build and
  namespace-generation behaviour (§4.13), so the CI results describe a
  framework-coupled cross-repo PHP project and should not be read as a property
  of AI-assisted development.
- **An unmeasured CI-composition shift.** Workflow mix changed across the period
  (Playwright E2E and load tests arrive later), so part of the 57% → 46%
  improvement in §4.13e may be composition rather than reliability. The split
  point is chosen, not derived.

### 7.3 Data-integrity caveats (revised)

- **Resolved:** the suite-scope discontinuity at the 2026-01-16 package split,
  previously "the single most important gotcha," is now measured and shown
  conservative (§4.6). Growth curves are safe if both packages are summed.
- **Resolved:** effort measurement, previously limited to three clock-stamped
  days, now has a project-wide lower bound of ≈140 h across 227 sessions (§4.3),
  with the standing caveat that sessions cannot see non-committing work.
- **Newly quantified:** the journal undersamples active days 2.2× (§4.1), and
  narrates activity during a measured two-month trough (§6.4).
- **Corrected in this revision (2026-09-21):** the `docs` category was read as
  the engineering journal; decomposed by path, the journal is ≈30% of it
  (≈2.0× source), and ≈29% is pre-journal business-strategy material (§4.7).
- **Demoted in this revision:** a busy-day CI effect (72% vs 56%) that is
  significant only if commits are treated as independent; day-level permutation
  gives p = 0.18 (§4.13h). Reported as a direction, like the 57% → 46% trend.
- **Weakened claim:** AI-authorship share is unverifiable before 2026-05-07
  (§4.9). This is the revision's most significant loss of confidence.
- **Newly closed off:** the estimate-vs-actual study is **not recoverable from
  any corpus.** Jira's `Original estimate` / `Time Spent` / `Work Ratio` fields
  are empty for all 156 issues (§3.3). Planning accuracy for AI-assisted work
  cannot be measured here at all, and PM-3 must be rescoped accordingly.
- **Newly closed off:** Jira `Priority` is degenerate (145/156 `SHOULD`) and
  `Assignee` is 76% empty, so neither severity nor ownership analyses are
  available. Lead time exists for n=39 and is contaminated at the fast end.
- **Terminology hazard:** the journal's "Sprint 1 → 133" has **no counterpart in
  Jira**, whose `Sprint` field holds two values. Any reader equating the two will
  draw false conclusions about cadence.
- **Still self-inconsistent (journal):** a handler cited as 346/358/381 lines on
  different dates; Sprint-81 file counts 11 vs 15. We report ranges, not false
  precision.
- **Still single-sourced:** findings-closed counts and quality-gate pass rates
  are not derivable from git and rest on AI-authored completion reports (§4.5).
- **Survivorship, all five corpora:** the journal is written by the party being
  studied; the Jira export is a snapshot with no transition history; the git
  record lost provenance twice during the study window — a mainline squash and
  the deletion of at least two feature branches (§6.6); and Corpus D adds a
  **third mechanism** — 234 of 979 runs (24%) point at `head_sha` values
  reachable from no ref, and GitHub retains run history only for a limited
  window, so runs older than it are **already unrecoverable** (§4.13f). The
  branch-deletion loss was detectable only by comparing against a stale local
  checkout, so **we cannot rule out further losses we have no witness for.**
  Aggregate figures are reported over what survived, which is a lower bound on
  what happened.
- **Corpus D is partial in both directions and measures friction, not defects:**
  745/979 runs (76%) join to a known commit and only 444/716 commits (62%) have
  any run, so per-commit CI figures are a lower bound on activity;
  `duration_seconds` is wall-clock including queueing, not billable compute; the
  40 workflow *names* include renames of one pipeline; and a `failure`
  conclusion conflates broken builds with flaky E2E, cancelled infrastructure and
  expired credentials. The 49.7% figure is a **friction rate**, not a defect
  rate, and §4.13 is worded accordingly.

### 7.4 What generalizes

Six findings travel beyond this case. None of them is the former title's thesis,
and the first draft's claim that "the harness is the load-bearing variable" is
withdrawn from this list: it is a causal claim, and §7.2 says why no causal
claim is available here.

1. **A high-quality self-account drifts in predictable directions.** Daily,
   candid, structured, accurate to the line on mechanical facts — and still
   undersampling activity 2.2×, understating volume by 41%, over-reporting
   continuity, omitting actors outside its author's role, and over-attributing
   documentation to itself by half. These directions are not random; a study
   correcting for one does not correct for the others. Anyone designing an
   AI-SE study on diaries, retrospectives or agent completion reports should
   expect all five.
2. **A single actor's record cannot describe a multi-actor system.** The
   journal documents the developer's process in fine detail and omits the
   tester entirely; an independent human filing 92.5% of defect reports is
   plainly part of how the project achieved quality (§4.12a). Case studies of
   AI-assisted engineering should sample the issue tracker as a matter of
   course, because it records the actors a developer's log cannot see.
3. **Trailer series measure convention adoption, not AI involvement.** A
   step from 0.4% to 58.8% on one date, with heavy assistant use documented
   throughout the untrailered period, is a dated counterexample to a technique
   currently gaining traction (§4.9).
4. **Provenance loss is invisible from inside the repository.** A release
   squash and routine branch pruning removed history during the study window;
   neither is detectable without an outside witness, and every count from a
   repository with ordinary hygiene is a lower bound (§6.6).
5. **In framework-coupled, cross-repository work, build failure was
   independent of change size**, and that null is the argument. A
   logic-failure account predicts a gradient; there is none (p = 0.66,
   ρ = −0.024), failures cluster as a persistent state (85.7% follow a
   failure), and the machine outspent the humans. The practical consequence:
   sizing commits does not protect the build. Whether hardening paid is a
   direction (57% → 46%), not a result (p = 0.18); so is the busy-day effect
   (§4.13h). This is the paper's clearest instance of a result available *only*
   by joining corpora.
6. **Verify the instrument before quoting it.** The mutation tool returned a
   confident percentage on every invocation and was wrong three times; a
   published clustering claim, tested against our data, exposed that two of our
   own tests assumed independence they did not have. Both corrections came
   from checking against an outside reference, which is the same discipline
   the project applied to the agent's claims at 1–2 minutes per check (§6.3).
   A study of verification should expect to be verified, and this one was.

---

## 8. Related work

A fuller, graded review is in [`08-literature-review.md`](08-literature-review.md);
this section states where each result of this paper lands against it. Read
status is as marked there — several entries rest on abstracts and must be read
in full before a venue draft cites them.

**Self-report and measurement.** METR's 2025 field experiment (arXiv:2507.09089)
found experienced developers 19% slower with AI while believing themselves 20%
faster. Our RQ1 result is the same finding by an independent route — a
self-authored journal against the project's own machine records — and extends
it from perceived *speed* to documented *volume, continuity, scope and actors*,
with the direction reversed on volume: the journal understated its output. Peng
et al.'s Copilot RCT (2023) we cannot address; we have no control arm, and §4.2
shows why repository metrics cannot supply a rate to compare.

**Mining coding-agent activity.** Robbes, Matricon, Degueule, Hora and
Zacchiroli (MSR 2026, arXiv:2601.18345) catalogue the perils of mining agent
traces — partial, arriving over time, heterogeneous, lost. §4.9 and §6.6 are a
single-project instance of each peril with the whole artifact available, and
with ground truth an ecosystem study cannot have: the journal documents heavy
assistant use across seven months of 0% trailer coverage. The commit-provenance
dataset of arXiv:2607.02774 separates "rewritten away" from "never collected";
we are a primary-source case of the first with a recovered witness, and add a
third mechanism (CI retention) outside version control. *Agentic Much?* (TOSEM,
arXiv:2601.18341) estimates 22–29% ecosystem agent adoption by February 2026;
our 86% trailer coverage by August 2026 is a project convention, not an adoption
curve, which is one more reason the series cannot be read as one.

**Who does the oversight.** Agarwal, Miller, Kästner and Vasilescu
(arXiv:2607.07980), from 3,100 coded practitioner documents, propose that "the
team sets the sign" of a coding agent's effect through how it structures review.
§4.12a is a measured instance — one team, V = 0.859 — of a proposition that
currently rests on discourse; they also state, independently, the sign-flip
problem we met in §4.13 and which is why we report both framings there. Garousi
(arXiv:2606.05770) characterises the oversight burden qualitatively without
asking who bears it; here it was borne by a distinct role. Monperrus
(arXiv:2606.13175) argues agents supersede human inspection; our case is a
counterexample to the strong reading — the pair did not find its own behavioural
defects — and sits inside his own carve-out for regulated systems, with the
construct caveat that the tester performed black-box testing, not diff review.

**Test effectiveness.** Inozemtseva & Holmes (ICSE 2014) and Zhang & Mesbah
(FSE 2015) established that coverage does not, and assertions do, track suite
effectiveness, and that size confounds both. §4.14 confirms this on one suite at
our own expense: 1.69:1 and ≈2.3 assertions per test were jointly blind to a
30-point mutation gap. Hora & Robbes (MSR 2026, arXiv:2602.00409) ask whether
coding agents over-mock; `MethodCallRemoval` as the top escape category (85 of
469) is their phenomenon measured rather than anecdotal. No industrial
mutation-score paper we located reports a run-to-run stability check; §4.14
shows why one is needed.

**CI failure.** The TravisTorrent-era prediction literature reports churn and
commit-count as useful predictors of build outcome; in this project they carry
no signal (§4.13c), which Huang, da Costa, Dick and El Mezouar
(arXiv:2605.05564) explain: where a material share of failures is unrelated to
the patch, size cannot predict them, and our project — at roughly double the
published closed-source failure rate of 26%, with 85.7% of failures following a
failure against a published benchmark of >50% — is the extreme end of their
phenomenon. Testing that clustering claim is what exposed the independence
assumption in our own earlier tests. *Continuous Integration Theater*
(arXiv:1907.01602) is complicated rather than confirmed here: a pipeline red
half the time was nonetheless actively tended, though the tending's effect does
not reach significance.

**Defect detection.** Basili & Selby (TSE 1987) and the Juristo, Moreno and
Vegas replication (2003) found that techniques detect different fault classes.
The disjoint yields of refactoring and black-box testing on the money subsystem
(§7.1) are an instance of that lineage with a new channel — LLM-assisted
refactoring — and, as stated there, an observation rather than a result.

**Work rhythm.** Claes, Mäntylä, Kuutila and Adams (ICSE 2018) found two-thirds
of developers keep office hours, more so when hired; §4.4 sits at the extreme of
that group. *TGIF* (EMSE 2025) reports rising night and weekend commits over
time; this 2025–26 project runs the other way, which is a weak counterexample
to a trend with an obvious alternative explanation in employment context.

**What the literature took from us.** Liu et al. (*Debt Behind the AI Boom*,
arXiv:2603.28592) find that >15% of AI-authored commits introduce static issues;
our null on AI-trailered commits versus CI outcome (§4.13d) cannot see what
their instrument sees and is stated only as "this project's CI did not
discriminate." PCI DSS 6.4/6.5 requires an auditable change-control record and
does not mandate the commit graph; §6.6 is worded as the conditional claim that
survives. And the build-failure clustering benchmark, tested against our data,
withdrew one of our tests and demoted another — the most useful single thing
the literature did for this paper.

---

## 9. Conclusion

An LLM assistant carried a large share of the production coding for a real,
money-handling payment module over ten months, and the engineer driving it kept
an unusually good daily record of how. This paper is what happened when that
record was checked against the project's commits, issues, CI runs and a mutation
baseline. The record was accurate to the line on what it could count and wrong
in every direction on what it could not see: it documented fewer than half the
days the project shipped code, undersold its own flagship epic by 41%, narrated
two nearly idle months as active, described a three-year, ten-person project as
seven months of one developer and an assistant, never mentioned the tester who
found 92.5% of its bugs, and — through our own earlier revision — claimed twice
the documentation output it produced. None of that was dishonest. It was the
view from one seat.

What the machine records establish stands independently of the journal: test
code outweighed production code 1.69 : 1 in every month; the work landed inside
ordinary hours with zero Saturdays in 716 commits; the cadence has no meaningful
central rate; authorship trailers were a convention adopted on one day and
measure nothing before it; defect discovery was a separate human role with
near-deterministic separation from the engineer; CI failed on half of all runs,
outspent the humans in wall-clock, stayed red in streaks, and did so
independently of how much code a commit changed; and the suite the project was
proud of detects 70% of the semantic changes to code it executes, fully
verifying the money arithmetic and leaving the glue around it exposed.

Three of our own claims did not survive the same treatment — a coin-flip test,
an improvement trend, and a busy-day effect, each significant when runs or
commits were treated as independent and each at p ≈ 0.18 when they were not —
and the mutation score was wrong three times before it was right. We report
these as the most credible part of the paper. A study whose subject is that
agent claims must be verified at 1–2 minutes each has no standing to exempt its
own.

The former title asserted that discipline beat cleverness. The record is
consistent with that and cannot establish it: there is no counterfactual, one
operator, and six models in four months. What the record does establish is
narrower and more useful. **A single actor's account of an AI-assisted project —
however candid — will undersample activity, understate volume, over-report
continuity and omit the actors it cannot see; trailers will tell you when a
convention was adopted, not when the AI arrived; the repository will have
forgotten some of what happened and will not tell you so; the mutation tool may
lie confidently; and the cost that dominates a framework-coupled project can be
shown to be environmental by the correlation that is absent rather than the one
that is present.** Each of those is a claim about how to study this kind of work,
and each was paid for by retracting something we had already written.

The developer's maxim, written in the log after the hardest sprint, is
*"Discipline > cleverness."* We leave it where it belongs: as the hypothesis
this project ran on, which its own records were good enough to test and not
good enough to prove.

---

## Appendix A — Headline numbers (journal claim vs. git-measured)

`A` = journal (self-reported). `B` = git commit record (measured, this
revision). Divergences are the point of the table.

| Claim | Journal (A) | Git (B) | Status |
|---|---|---|---|
| Project span | 2025-11-26 → 2026-07-02 (7 mo) | 2025-10-21 → 2026-08-20 (10 mo) | **B extends A both ends** |
| Total commits | not tracked | 716 (586 + 130) | B only |
| Active days | 47 day-dirs | 143 (105 in A's window) | **A undersamples 2.2×** |
| Commits/active day | "multiple sprints/day" | median 3, mean 5.0, max 35; 18 days ≥10 | **peak ≠ rate** |
| Measured effort | 3 clock-stamped days | 227 sessions ≈140.1 h | B only |
| Weekend work | not tracked | 0 Sat, 1 Sun; 95.9% in 08:00–20:00 | B only |
| S114 commits | 61 | 64 | A low by 3 |
| S114 files | 178 | 183 code (238 w/ docs) | ✅ consistent |
| S114 LOC | +11,204 / −5,876 | +15,844 / −6,075 | **A low ~41%** |
| S114 tests added | +202 | +196 methods | ✅ consistent |
| S114 duration | ≈9.5 h agent compute | 8.2 h sessions / 16.8 h calendar | ✅ same order |
| Unit tests | 852 → ~1,407 (PHPUnit) | 493 → 2,109 methods (different metric) | series not comparable |
| Package-split discontinuity | "most important gotcha", unresolved | conservative: ≤7% methods, ≤1% src LOC | **resolved** |
| Test : source write ratio | asserted TDD | **1.69 : 1** (+150,321 / +88,896) | **B confirms A** |
| Docs volume | 462 files / 113,098 lines | +585,998 `docs` lines (4.4× src) of which the journal is **≈177,600 (≈2.0× src)**; ≈168,200 are pre-journal strategy decks | **our earlier revision over-attributed 2×** |
| Contributors | "single-developer" | 3 humans (87% / 8.8% / 2.7%) + bot | **A retracted** |
| AI-authored share | "primary code author" | trailers on 149/716 (20.8%); 0% pre-May-2026, 86% Aug | **A unverified pre-May** |
| Model generations | Opus 4.7 / 4.8 bylines | 6 distinct strings, May–Aug 2026 | B refines A |
| Findings closed (S114) | 54/54, 0 deferred | not derivable | single-sourced |
| Quality-gate pass | 61/61 green, 0 new suppressions | not derivable | single-sourced |
| Bonus real-money bugs | 4 (cents truncation) | not derivable | single-sourced |
| Security audit | 28 findings (5C/10H/9M/4L) | not derivable | single-sourced |
| Incident catalog | ~75 bugs/CI failures | `ci` category: 288 file-changes | B partially corroborates |
| History integrity | unremarked | mainline squashed 2026-07-02; 491 commits only on LEGACY | **B-only failure** |
| Project age | 7 months (A) / 10 months (B) | Jira issues from **2023-05-30**; 55/156 predate the commit record | **C extends both** |
| Participants | "single-developer" | 3 committers (B); **10 Jira reporters** (C) | **A retracted twice** |
| Bug reporting | assistant + developer triage | **37/40 bugs (92.5%) filed by one dedicated tester**; developer filed **0** | **C-only, reframes the case** |
| Issue → code coverage | not tracked | 61/156 (39%): Story 69%, Bug 42%, Task 8% | C only |
| Fabricated ticket ids | one "unconfirmed ticket number" | **0 of 61** refs fabricated; **1 mislabel** (STRP-138 vs 139) | **C refines A** |
| "Not a bug" reclassification | "a meaningful fraction" | **6/40 (15%)**: 3 `Not a bug` + 3 `Core Bug` | **C confirms A** |
| Lead time | not tracked | median 17 d (n=39, weak) | C only |
| Estimate vs actual | plan/actual pairs in sprint docs | **all Jira time fields empty** | **not recoverable** |
| Journal "sprints" | 1 → 133 | Jira `Sprint` has **2 values** — unrelated concepts | **terminology hazard** |
| CI outcomes | "CI/infra was the largest cluster" | **487 failure / 453 success / 39 cancelled of 979 runs — 49.7%** | **D quantifies A** |
| CI time cost | not tracked | **169.5 h** wall-clock; **90.1 h (53%)** in failing runs; vs ≈140 h human sessions | D only |
| Failure vs commit size | not considered | **no association** — 63% (≥500 ins.) vs 60%; Fisher **p = 0.66**, ρ = −0.024 | **D-only, tested null** |
| CI trend | hardening described | **57% → 46%** across 2026-04-01; nominal p = 0.0014, **p = 0.18** after clustering correction | **D agrees in direction; not significant** |
| Busy days vs CI | "tens of commits/day" on the epic | burst-day commits **72%** vs **56%** failing; Fisher p = 0.0014, **day-permutation p = 0.18** | **D-only; direction, not a result** |
| Time to green | CI "loops" narrated | 74 streaks; median **2 runs / 4.1 h**, 75th pct 28.7 h, max **358 h**; 23 streaks ≥5 runs | **D quantifies A** |
| Sub-sprint → commit mapping | "one phase, one commit" | **9/13 (69%)** span >1 commit, median 5; vs ordinary numbering p = 1.00 | **B: failed on its own terms; comparison underpowered** |
| AI commits vs CI | not claimed | **59% vs 61%** failing (p = 0.88) — confounded null | D only |
| CI provenance | unremarked | **234/979 runs (24%)** on no surviving ref; older runs past retention **gone** | **D-only failure** |
| Test effectiveness | "1,407 tests", TDD asserted | **Covered Code MSI 70%** — 1,592 mutants, 469 escaped, reproducible; **0 escapes** in the three money-arithmetic classes | **E quantifies A** |
| Hollow tests after remediation | "false-positive tests removed" | **`MethodCallRemoval` = 85/469 escapes**, the largest category | **E complicates A** |
| Tooling trustworthiness | not considered | first three measurements non-reproducible (0–1,019 mutants); cause was Infection's random-seeded initial run | **E-only, methodological** |

## Appendix B — Primary artifacts

Journal (Corpus A):

- `20260527/reports/117-final-achievement-summary.md` — the quantified epic.
- `20260527/reports/118-lessons-learned.md` — the collaboration-model reflection.
- `20260527/done/_engineering_requirements.md` — the R-1…R-10 rule set.
- `20260529/done/handoff.md` — log-as-memory / session handoff.
- `2026/02/20260219/reports/01-security-audit-strp99-no-mcp.md` — the AI security audit.
- `2026/02/20260206/reports/02-refund-setstate-bug-analysis.md` — the no-`setState()` invariant + STRP-89.
- `20260622/status.md` — the "committed against instruction" incident.
- `2025/20251128/ARCHITECTURE_REVIEW.md` §12 — the "Hallucination Analysis".
- `architecture/00-overview.md` … `04-webhook-processing.md` + `puml/` — the curated design corpus.

Git (Corpus B), key commits:

- `6e828a242d6b` (2026-07-02) — the mainline squash; 562 files re-added (§6.6).
- `origin/b-7.4.x-LEGACY` — 491 pre-squash commits; the only surviving
  commit-level record of months 1–8.
- `e6a91ee1c821` (2026-01-15) — "STRP-78 Extract paymenmt component", the
  package split (§4.6).
- `f285ea080921`, `b1a27a142f4c` (2025-12-05) — the first two Claude trailers.
- `a5d437cf3d7b` (2026-05-07) — start of routine trailer use (§4.9).

## Appendix C — Dataset

Fifteen CSVs in [`../data/`](../data/), with schema, caveats and reproduction
commands in [`../data/README.md`](../data/README.md), the export scripts
(`fetch_actions.sh`, `build_actions.py`), and `stats.py`, which recomputes every
statistical test cited in this paper (T1–T12):

| File | Grain | Rows |
|---|---|---|
| `commits.csv` | one commit | 716 |
| `commit_loc_by_category.csv` | one commit, LOC split by path category | 716 |
| `daily_activity.csv` | repo × day | 194 |
| `sessions.csv` | work session (>90 min gap boundary) | 227 |
| `test_trajectory.csv` | repo × checkpoint, measured from tree | 27 |
| `author_contribution.csv` | author | 7 |
| `model_generations.csv` | `Co-Authored-By` model string | 6 |
| `hour_histogram.csv` | local hour of day | 24 |
| `jira-stripe.csv` | one Jira issue (raw export, 129 cols) | 156 |
| `jira_issues.csv` | one Jira issue, normalized + joined to commits | 156 |
| `jira_roles.csv` | one Jira reporter × issue type | 10 |
| `actions_runs.csv` | one workflow run, joined to its commit and that commit's LOC | 979 |
| `actions_by_commit.csv` | one commit with ≥1 run: LOC beside run outcomes | 444 |
| `actions_workflows.csv` | repo × workflow | 41 |
| `mutation_escaped.csv` | one escaped mutant: file, line, mutator | 469 |

Every figure in §4 and Appendix A is a direct aggregation over these files, and
every p-value is reproducible with `python3 data/stats.py`. Author email
addresses, Jira account ids, watcher lists and issue description bodies are
deliberately excluded; display names, summaries and actor logins only.
