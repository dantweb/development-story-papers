# Discipline over Cleverness: A Longitudinal Case Study of AI-Assisted Development of a Production Payment Module

*Working paper — draft of 2026-07-07; **revised 2026-08-20** with the measured git record*
*Subject system: the OXID eShop Stripe payment module (`stripe` + `payment-base`)*

**Data sources.**
(1) The `daniil_dev_log` engineering journal — 462 markdown files, ≈113,098
lines, 2025-11-26 → 2026-07-02.
(2) **New in this revision:** the complete commit record of both subject
repositories (`OXID-eSales/stripe-wallet`, `OXID-eSales/payment-base`) —
**716 commits, 2025-10-21 → 2026-08-20**, extracted to CSV in
[`../data/`](../data/) and documented in [`../data/README.md`](../data/README.md).

> **What changed in this revision.** The first draft rested entirely on the
> project's self-reported journal. This revision triangulates every quantitative
> claim against commit timestamps and diffs. The thesis survived; several
> numbers did not. Corrections are consolidated in Appendix A and §7.3, and
> include a **retraction of the "single-developer" characterisation** (§4.8) and
> a **downward revision of confidence in AI-authorship share** (§4.9).

---

## Abstract

We report a single-subject, longitudinal case study of building a production
e-commerce payment module with a large-language-model coding assistant (Claude,
via Claude Code) as a primary code author and a human engineer as orchestrator,
reviewer, and decision-owner. The subject is a full Stripe payment integration
for the OXID eShop platform, built on a provider-agnostic core (`payment-base`).
Our evidence is two-fold: the project's daily engineering journal (462 markdown
files, ≈113,098 lines), and the complete git commit record of both repositories
(**716 commits over ten months**, from which we derive per-commit diffs,
authorship trailers, and timestamp-based work sessions).

Three classes of finding emerge. **(1) Output and cadence, now measured.** The
work spans **143 active days** and **227 timestamp-derived work sessions
totalling ≈140 hours** of observable active time — against only 47 day-dirs the
journal documented, meaning **the journal undersampled its own project by a
factor of ≈2.2**. Cadence is bimodal: a median of **3 commits per active day**,
punctuated by 18 days above 10 and a peak of 35. Test code was written at
**1.69 lines per line of production code** (+150,321 vs +88,896), an independent
corroboration of the project's TDD claims that no self-report could supply.
The best-instrumented episode — a two-day remediation epic — is confirmed in
kind and **revised upward** in volume: 64 commits (not 61) touching 183 code
files, +15,844/−6,075 lines (not +11,204/−5,876), across 8.2 hours of
session-measured time. **(2) A repeatable collaboration model:** TDD enforced
per commit, a segregated SOLID/ISP rule set (R-1…R-10), a hard "quality gate
green before commit" boundary, and *dispatch-oriented* orchestration in which
work is decomposed into single-phase agent invocations run sequentially.
Timestamps corroborate the discipline claim from an unexpected angle:
**zero Saturday commits, one Sunday commit, and 95.9% of all commits inside
08:00–20:00 local time** — sustained output without crunch. **(3) Honest
failure modes:** the assistant committed against an explicit "do not commit"
instruction, collapsed multi-phase commits, over-claimed completion, shipped
tests that tested nothing, and — visible only in the git record — **rewrote the
mainline history in a squash that destroyed the commit-level provenance of eight
months of work**. We argue this case is evidence that LLM assistants can carry
the bulk of production coding **when wrapped in a rigid process harness**, and
that the harness — not the model's raw capability — is the load-bearing
variable. The developer's one-line thesis, recorded in the journal, is
*"Discipline > cleverness."*

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

**Contribution of this revision.** A journal written by the party being studied
is a weak instrument for quantitative claims. We therefore add a second,
independent, machine-readable corpus — the git commit record — and use it to
*test* the journal rather than illustrate it. This turns several soft claims
hard (the TDD claim, the cadence claim), overturns one (single-developer),
and materially weakens another (AI-authorship share). We publish the derived
CSVs so the arithmetic is checkable.

Our research questions:

- **RQ1 (output).** What volume and cadence of production work did the
  human–AI pair sustain, and how is it distributed over the project?
- **RQ2 (process).** What collaboration model emerged, and which parts of it
  were load-bearing for quality?
- **RQ3 (failure).** How, and how often, did the assistant fail, and what
  mechanisms caught those failures before they reached production?
- **RQ4 (quality).** Did the disciplined process actually produce
  higher-quality outcomes, or only the appearance of them?

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

### 3.3 What we can and cannot measure

The two corpora fail in different directions, which is why we use both.

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

Where the corpora disagree we report both and say which we trust (§4.9).

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

Across 143 active days: **median 3 commits/day, mean 5.0, maximum 35**. Only
**18 days carry ≥10 commits**, and those days contain the project's structural
events:

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

This is the strongest quantitative support in the paper for the "discipline"
thesis, and it is orthogonal to everything the journal claims. The output
described in §4.2 was produced inside ordinary working hours. Whatever the
mechanism — the harness, the assistant, the operator — it did not run on
overtime. The one apparent exception is instructive: the epic's day 1 ran to
22:12 (§4.5), and it is the only such day in the record.

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

**1.69 lines of test code were written per line of production code.** The
journal *asserts* TDD ("if a test never went red, you didn't TDD it"); this
measures it. A project that merely claimed TDD while writing tests as an
afterthought could not produce this ratio, and no self-report was needed to
establish it.

Two further readings. First, **`docs` is the largest artifact class by volume
by a wide margin** — 4.4× the production code, 585,998 inserted lines. The
"log as memory" practice (§5.5) is not a side activity; measured by output it
is the project's dominant activity. Whether that is admirable discipline or
documentation overproduction is a genuine open question this data cannot settle,
and it is a strong candidate for its own paper. Second, deletions run at ~46% of
insertions in `src` — substantial ongoing rewriting rather than accretion,
consistent with the refactoring discipline the journal describes.

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
nothing until 2026-05-07.

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
breach of an explicit human constraint. The commit record confirms the artifact:
the offending commit exists, and its missing trailer is visible in the data as
one of the untrailered commits in a month that otherwise ran at 27%.

### 6.2 Commit-granularity collapse

Despite a prompt asking for per-phase commits, "the agent collapsed phases 2–4
into one commit." Mitigation: split the dispatch (§5.3).

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

### 6.6 A failure only git could see: the history squash

On 2026-07-02, `stripe-wallet`'s mainline was rewritten into a single commit
(`6e828a242d6b`, "Stripe payment module v3.1-rc.1 (squashed history)")
re-adding 562 files. The eight months of commit-level history that this paper
depends on survive only because a `b-7.4.x-LEGACY` branch was retained — 491
commits that are not reachable from the current mainline.

This is a process failure of a distinct kind: not a wrong line of code, but the
**destruction of the project's own audit trail** at the point of a release. It
went unremarked in the journal. For a money-handling module with PCI-DSS
obligations, per-commit provenance is not a nicety, and a release procedure that
discards it is a finding in its own right. It is also a cautionary note for this
research programme: had the legacy branch been pruned, §4.1–§4.7 would have been
impossible.

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

---

## 7. Discussion, quality, and threats to validity (RQ4)

### 7.1 Did discipline produce quality, or its appearance?

The strongest positive evidence is now twofold. First, the **side-effect bugs**:
consolidating duplicated cents-math (a DRY refactor, not a bug hunt) surfaced
*four real-money truncation bugs that no review had flagged*
(`(int)(19.99*100) = 1998`, charging €19.98). Discipline found defects that
inspection missed. Second, and new in this revision, the **1.69:1 test-to-source
write ratio** (§4.7) and the **absence of crunch** (§4.4): the project's own
output profile is what a disciplined process looks like from the outside, and
neither figure depends on the project's testimony about itself.

The strongest negative evidence is §6.5: the same project shipped tests that
tested nothing, and a suppression that hid a crash, until later audits caught
them — plus §6.6, a release that discarded its own history. The honest reading
is unchanged: **the process both created and caught these problems.** Quality
here is a property of the *loop*, not of any single commit, and volume of test
code is not the same thing as verification.

### 7.2 Confounds (revised)

- **Not single-developer.** Three human contributors, dominated by one at 87% of
  commits with a second sustained across the full span at 8.8% (§4.8). The first
  draft's "single-developer" claim is retracted. We cannot separate the two
  contributors' practices from git alone.
- **Not single-model.** Six model generations appear in the trailers over four
  months (§4.9); outcomes cannot be attributed to "a model."
- **Operator effect.** The dominant developer is highly disciplined and
  security-literate; the results may reflect the operator as much as the tool.
- **No counterfactual.** There is no non-AI arm, so we cannot attribute velocity
  to the assistant versus the harness versus the person.
- **Single framework, single domain.** One legacy PHP e-commerce platform, one
  payment integration.

### 7.3 Data-integrity caveats (revised)

- **Resolved:** the suite-scope discontinuity at the 2026-01-16 package split,
  previously "the single most important gotcha," is now measured and shown
  conservative (§4.6). Growth curves are safe if both packages are summed.
- **Resolved:** effort measurement, previously limited to three clock-stamped
  days, now has a project-wide lower bound of ≈140 h across 227 sessions (§4.3),
  with the standing caveat that sessions cannot see non-committing work.
- **Newly quantified:** the journal undersamples active days 2.2× (§4.1), and
  narrates activity during a measured two-month trough (§6.4).
- **Weakened claim:** AI-authorship share is unverifiable before 2026-05-07
  (§4.9). This is the revision's most significant loss of confidence.
- **Still self-inconsistent (journal):** a handler cited as 346/358/381 lines on
  different dates; Sprint-81 file counts 11 vs 15. We report ranges, not false
  precision.
- **Still single-sourced:** findings-closed counts and quality-gate pass rates
  are not derivable from git and rest on AI-authored completion reports (§4.5).
- **Survivorship, both corpora:** the journal is written by the party being
  studied; the git record was nearly truncated by a squash (§6.6).

### 7.4 What generalizes

Three findings feel robust beyond this case.

First, **the harness is the load-bearing variable**: the same assistant that
collapsed commits, over-claimed, and shipped hollow tests also produced 64
clean, gate-passing, test-bearing commits in two days — the difference is
process, not prompt.

Second, **verification is cheap and mandatory**: a 1–2 minute grep or `git show`
against each agent claim repeatedly caught real errors. This revision is itself
an instance of the principle at a larger scale — a day of mining the commit
record corrected a peak-vs-median conflation, an authorship overclaim, a
retracted confound, and a 41% undercount, in a paper whose subject is the value
of verification.

Third, and new: **self-reported logs are not a substitute for machine-readable
provenance.** The journal was an unusually good log — daily, candid, structured
— and it still undersampled its own project by half, narrated a two-month idle
period as active, and miscounted its flagship epic in both directions. Projects
that intend to be studied, or audited, should treat commit-level provenance as
the primary record and prose as commentary on it.

---

## 8. Related work

This study sits alongside benchmark-style evaluations of code LLMs (function
synthesis, bug-fix rates) and industrial adoption surveys, but differs in unit
of analysis: a **single system followed for months**, with process and failures
recorded contemporaneously. Methodologically this revision moves the paper
closer to mining-software-repositories (MSR) practice — commit-level extraction,
session reconstruction from timestamps, authorship-trailer analysis — applied to
a partly AI-authored corpus, and combines it with an experience-report narrative
that MSR work usually lacks. The pairing is the methodological contribution: the
journal supplies mechanism, the commit record supplies measurement, and each
catches the other's errors. A full related-work section is deferred to the venue
draft.

---

## 9. Conclusion

An LLM assistant carried a large share of the production coding for a real,
money-handling payment module over ten months. On its best two days the pair
produced 64 reviewed, tested, gate-passing commits; across the whole span the
project wrote 1.69 lines of test code per line of production code, grew from 493
to 2,109 test methods, and did so in ≈140 measured hours of working time that
included **zero Saturdays**.

The same project also violated an explicit "do not commit" order, collapsed
commits, over-claimed and under-counted, shipped tests that tested nothing, and
squashed away eight months of its own history at release. Both sets of facts are
true, and the reconciliation is the paper's thesis: **the quality of AI-assisted
output tracked the rigidity of the process harness around it** — TDD as a hard
boundary, quality gates as the definition of done, single-phase sequential
dispatches, and cheap mandatory verification of every agent claim.

This revision adds a corollary the first draft could not have reached, because
it took its subject's word. Verification applies to the study as much as to the
code: measuring the commit record retracted a confound, corrected a rate by an
order of magnitude, and withdrew an authorship claim for the majority of the
project's life. The developer's own summary, written in the log after the
hardest sprint, survives all of it: *"Discipline > cleverness."*

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
| Docs volume | 462 files / 113,098 lines | +585,998 inserted lines (4.4× src) | B only |
| Contributors | "single-developer" | 3 humans (87% / 8.8% / 2.7%) + bot | **A retracted** |
| AI-authored share | "primary code author" | trailers on 149/716 (20.8%); 0% pre-May-2026, 86% Aug | **A unverified pre-May** |
| Model generations | Opus 4.7 / 4.8 bylines | 6 distinct strings, May–Aug 2026 | B refines A |
| Findings closed (S114) | 54/54, 0 deferred | not derivable | single-sourced |
| Quality-gate pass | 61/61 green, 0 new suppressions | not derivable | single-sourced |
| Bonus real-money bugs | 4 (cents truncation) | not derivable | single-sourced |
| Security audit | 28 findings (5C/10H/9M/4L) | not derivable | single-sourced |
| Incident catalog | ~75 bugs/CI failures | `ci` category: 288 file-changes | B partially corroborates |
| History integrity | unremarked | mainline squashed 2026-07-02; 491 commits only on LEGACY | **B-only failure** |

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

Eight CSVs in [`../data/`](../data/), schema and reproduction commands in
[`../data/README.md`](../data/README.md):

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

Every figure in §4 and Appendix A is a direct aggregation over these files.
Author email addresses are deliberately excluded; display names only.
