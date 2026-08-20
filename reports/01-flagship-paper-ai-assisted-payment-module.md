# Discipline over Cleverness: A Longitudinal Case Study of AI-Assisted Development of a Production Payment Module

*Working paper — draft of 2026-07-07; **revised 2026-08-20** with the measured git and Jira records*
*Subject system: the OXID eShop Stripe payment module (`stripe` + `payment-base`)*

**Data sources.**
(1) The `daniil_dev_log` engineering journal — 462 markdown files, ≈113,098
lines, 2025-11-26 → 2026-07-02.
(2) **New in this revision:** the complete commit record of both subject
repositories (`OXID-eSales/stripe-wallet`, `OXID-eSales/payment-base`) —
**716 commits, 2025-10-21 → 2026-08-20**.
(3) **Also new:** the **Jira issue record** of the STRP project — **156 issues,
2023-05-30 → 2026-06-22** — the only corpus that records *who asked for the
work*. All extracted to CSV in [`../data/`](../data/) and documented in
[`../data/README.md`](../data/README.md).

> **What changed in this revision.** The first draft rested entirely on the
> project's self-reported journal. This revision triangulates every quantitative
> claim against commit timestamps and diffs. The thesis survived; several
> numbers did not. Corrections are consolidated in Appendix A and §7.3, and
> include a **retraction of the "single-developer" characterisation** (§4.8,
> further overturned by the Jira record in §4.12) and a **downward revision of
> confidence in AI-authorship share** (§4.9). The Jira corpus adds the finding
> that most reframes the case: **an independent human QA function filed 92.5% of
> the project's bugs** (§4.12).

---

## Abstract

**In one line:** an LLM assistant helped build a production payment module over
ten months; we measured the result against its own git history, and found that
the project's *process* claims held up, its *volume* claims were understated, and
its *authorship* claims cannot be verified for the first seven months.

**The subject.** A full Stripe payment integration for the OXID eShop platform,
built on a provider-agnostic core (`payment-base`), with Claude (via Claude Code)
as a primary code author and a human engineer as orchestrator, reviewer, and
decision-owner. It moves real money, spans an asynchronous webhook boundary,
carries PCI-DSS/GDPR obligations, and integrates with a large legacy PHP
framework.

**What we measured.** Three corpora, deliberately chosen to fail in different
directions. **(A)** The project's daily engineering journal — 462 markdown files,
≈113,098 lines, 2025-11-26 → 2026-07-02 — candid but self-reported. **(B)** The
complete git record of both repositories — **716 commits, 2025-10-21 →
2026-08-20** — from which we derive per-commit diffs split by path category,
authorship trailers, work sessions reconstructed from timestamps (≤90 min gap),
and test-suite sizes measured from the tree at 15 checkpoints. **(C)** The Jira
issue record — **156 issues, 2023-05-30 → 2026-06-22** — the only corpus that
records who requested the work and who found the defects. We use (B) and (C) to
*test* (A) rather than to illustrate it, and publish the derived CSVs so the
arithmetic is checkable.

**What we found — six concrete results.**

1. **Test code outweighed production code 1.69 : 1** (+150,321 vs +88,896 lines).
   This is the only independent confirmation of the project's TDD claims; a
   project merely asserting TDD could not produce this ratio.
2. **The work was done in ordinary hours: zero Saturday commits, one Sunday
   commit, and 95.9% of all commits inside 08:00–20:00 local time.** Whatever
   produced the output, it was not overtime.
3. **Cadence is bimodal, and the peak is not the rate.** Median **3 commits per
   active day** (mean 5.0, max 35) across **143 active days**; only 18 days
   exceed 10 commits. Reading the best days as sustained throughput — which the
   first draft came close to doing — overstates it roughly tenfold.
4. **Effort is now bounded project-wide, not sampled from three days.** 227
   sessions totalling **≈140 hours** of commit-bearing activity, replacing a
   journal that clock-stamped only 3 of its days. The same data exposes a
   **measured two-month trough (9.1 h across March–April 2026)** that the journal
   narrates as active work.
5. **The flagship two-day remediation epic is confirmed and revised upward:** 64
   commits (reported: 61), +15,844/−6,075 lines (reported: +11,204/−5,876), 183
   code files, +196 test methods, 8.2 h of session time. The self-report
   *understated* its own output by ~41% on insertions.
6. **The test suite grew 493 → 2,109 test methods**, and the 2026-01-16 package
   split — the first draft's largest unresolved caveat — is shown to have been
   **conservative** (≤7% of methods, ≤1% of source LOC), so growth curves are
   safe if both packages are summed.
7. **The AI-assisted pair was not the whole quality system.** Jira shows a
   **strict role separation across 10 participants**: the developer filed 52
   Stories and **zero Bugs**, while a separate tester filed **37 of the
   project's 40 Bugs (92.5%)** and zero Stories, and a third person filed 26 of
   the 50 Tasks. An independent human QA function, invisible in both the journal
   and the commit record, was supplying the defects the pair then fixed.
8. **Zero fabricated ticket references.** All **61** distinct `STRP-nnn` ids
   appearing in commit messages resolve to real Jira issues — though one is
   *mislabelled*, and that single case is the paper's sharpest micro-study
   (§6.1).

**What we retracted.** Measurement cost us three claims, and the Jira record
deepens the first of them: the project ran on a **10-person Jira participant
base over three years** (2023-05 → 2026-06), so the AI-assisted implementation
phase studied here is one stage of a much longer effort, not the project. **(i)** "Single-developer"
is **withdrawn**: there were three human contributors (87% / 8.8% / 2.7% of
commits), the second active across the full span. **(ii)** "Claude was the primary
code author" is **unverifiable before 2026-05-07**: `Co-Authored-By` trailers
cover only 149/716 commits (20.8%), are absent before May 2026, and reach 86% by
August — they measure attribution *practice*, not authorship. **(iii)** Reported
"simplifications" describe **one file, not the module**: the webhook refactor
genuinely cut its dispatch method 330 → 107 lines, but moved that logic into 8
new handler classes (+600 lines of production code, +856 of tests), taking
module handler code from 2,616 to 2,953 LOC. Per-unit complexity fell while
aggregate code rose; only the shrinking half was reported.

**Failure modes, including one only git could see.** The assistant committed
against an explicit "do not commit" instruction (verified: commit `bf32d77`
matches the journal's complaint in all five particulars, including a `status.md`
committed at zero changed lines), collapsed multi-phase commits, over-claimed
*and* under-counted its own results, and shipped tests that asserted nothing.
Additionally, **a release on 2026-07-02 squashed the mainline and destroyed eight
months of per-commit provenance** — a process failure the journal never mentions,
and one this study survives only because a legacy branch was retained.

**Conclusion.** LLM assistants can carry the bulk of production coding on a
money-handling system **when wrapped in a rigid process harness** — TDD as a hard
boundary, quality gates as the definition of done, single-phase sequential agent
dispatches, and cheap mandatory verification of every agent claim. The harness,
not the model's raw capability, is the load-bearing variable: the same assistant
that collapsed commits and hid hollow tests also produced 64 clean, gate-passing,
test-bearing commits in two days. A third finding generalises beyond the case:
**self-reported logs are not a substitute for machine-readable provenance.** This
was an unusually good log, and it still undersampled its own project by 2.2×,
narrated an idle period as active, and miscounted its flagship epic in both
directions. The developer's one-line thesis, recorded in the journal, survives
all of it: *"Discipline > cleverness."*

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

### 3.4 What we can and cannot measure

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

**Corpus C (Jira) limitations** are set out in §3.3 and are the most restrictive
of the three: no effort data, no severity signal, no transition history, and a
snapshot-only view.

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

Fourth, and the strongest methodological lesson of this revision: **a single
actor's record cannot describe a multi-actor system.** The journal is a
developer's log, so it documents the developer's process in fine detail and omits
the tester entirely — yet an independent human filing 92.5% of the defect reports
is plainly part of how this project achieved quality (§4.12a). Nothing in the
journal is false; the omission is structural, and no amount of candour inside one
person's log would have surfaced it. Case studies of AI-assisted engineering
should sample the issue tracker as a matter of course, precisely because it
records the actors a developer's log cannot see.

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
commits, over-claimed and under-counted, shipped tests that tested nothing,
mislabelled a fix under a neighbouring ticket, and squashed away eight months of
its own history at release. Both sets of facts are true, and the reconciliation
is the paper's thesis: **the quality of AI-assisted output tracked the rigidity
of the process harness around it** — TDD as a hard boundary, quality gates as the
definition of done, single-phase sequential dispatches, and cheap mandatory
verification of every agent claim.

One qualification belongs in the conclusion rather than a footnote. The harness
was not the whole apparatus: an independent human tester filed 92.5% of this
project's bug reports, a fact absent from the developer's journal and visible
only in the issue tracker. The defensible claim is therefore narrower and more
useful than "an AI built a payment module": **an AI, a disciplined developer, a
dedicated tester and a project manager built it, and the AI carried the bulk of
the typing under a process that assumed it would be wrong.**

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
| Project age | 7 months (A) / 10 months (B) | Jira issues from **2023-05-30**; 55/156 predate the commit record | **C extends both** |
| Participants | "single-developer" | 3 committers (B); **10 Jira reporters** (C) | **A retracted twice** |
| Bug reporting | assistant + developer triage | **37/40 bugs (92.5%) filed by one dedicated tester**; developer filed **0** | **C-only, reframes the case** |
| Issue → code coverage | not tracked | 61/156 (39%): Story 69%, Bug 42%, Task 8% | C only |
| Fabricated ticket ids | one "unconfirmed ticket number" | **0 of 61** refs fabricated; **1 mislabel** (STRP-138 vs 139) | **C refines A** |
| "Not a bug" reclassification | "a meaningful fraction" | **6/40 (15%)**: 3 `Not a bug` + 3 `Core Bug` | **C confirms A** |
| Lead time | not tracked | median 17 d (n=39, weak) | C only |
| Estimate vs actual | plan/actual pairs in sprint docs | **all Jira time fields empty** | **not recoverable** |
| Journal "sprints" | 1 → 133 | Jira `Sprint` has **2 values** — unrelated concepts | **terminology hazard** |

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
| `jira-stripe.csv` | one Jira issue (raw export, 129 cols) | 156 |
| `jira_issues.csv` | one Jira issue, normalized + joined to commits | 156 |
| `jira_roles.csv` | one Jira reporter × issue type | 10 |

Every figure in §4 and Appendix A is a direct aggregation over these files.
Author email addresses, Jira account ids, watcher lists and issue description
bodies are deliberately excluded; display names and summaries only.
