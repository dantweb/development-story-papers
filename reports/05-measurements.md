# Measured Results (22)

*Revised 2026-08-20 — journal-reported values now sit beside git- and
Jira-measured ones.*

Topics where the evidence supports **hard, quantitative results** — not just
narrative. Each entry states the metric, the value(s) recorded, the source, and
what a paper/section can demonstrate with it.

Two provenance classes, kept strictly apart:

- **`[A]` journal-reported** — from the dev-log corpus. Paths relative to
  `docs/dev_logs/daniil_dev_log/` unless prefixed `architecture/`.
- **`[B]` git-measured** — derived from the 716-commit record of both
  repositories, 2025-10-21 → 2026-08-20.
- **`[C]` Jira-measured** — derived from the 156-issue STRP export,
  2023-05-30 → 2026-06-22, joined to the commit record on `STRP-nnn` refs.

Dataset: [`../data/`](../data/); schema and caveats:
[`../data/README.md`](../data/README.md).

> **Read the caveats first.**
> **`[A]`** is a *sampled, not continuous* record: real HH:MM effort timestamps
> in only **3 files**, agent-compute for only **1 epic**, test counts **not
> comparable across the 2026-01-16 package split**, and "done" ≠ "committed" for
> much 2026 work. It is written by the party being studied.
> **`[B]`** fails differently: sessions are a **lower bound** on effort (they
> cannot see non-committing work); `files_changed` counts change *events*, not
> unique files; test-method counts are **not** PHPUnit test counts; a **mainline
> squash on 2026-07-02** re-added 562 files and left pre-July provenance only on
> `b-7.4.x-LEGACY`; and `Co-Authored-By` trailers measure *attribution practice*,
> not authorship.
> **`[C]`** is the most restrictive of the three: **all time-tracking fields are
> empty for all 156 issues**, `Priority` is degenerate (145/156 = `SHOULD`),
> `Assignee` is 76% empty, `Resolution` is set on 39 issues while 82 are
> `Done`-category, there is no status-transition history, and the `Sprint` field
> holds two values — so **Jira sprints are unrelated to the journal's Sprint
> 1→133**. Every measurement below is annotated with the limit that bears on it.

---

## M-1 — Test-suite growth trajectory

**Metric:** test-suite size over time.

**`[A]` Values (PHPUnit-reported):** 852 (2025-11-28, 847 pass) → 1348
(2025-12-15) → **[package split]** 576 stripe / 686 pc (2026-01-16) → 723/1728
assertions (2026-02-27) → 840/1993 (2026-04-16) → 921→1123 (2026-05-27, S114) →
1415 stripe (2026-06-22) → 1397→1407 (2026-07-02).
**Source:** per-day `status.md`; `117-final-achievement-summary.md`.

**`[B]` Values (test *methods*, measured from the tree, both packages summed):**
493 (2025-11-01) → 952 (2025-12-01) → 1,215 (2026-01-01) → **1,130
(2026-01-17, post-split)** → 1,066 (2026-02-01) → 1,203 (03-01) → 1,267 (04-01)
→ 1,326 (05-01) → 1,517 (05-27) → 1,713 (05-29) → 1,995 (07-01) → **2,109
(2026-08-20)**. Alongside: **112 → 481 src files, 6,837 → 39,775 src PHP LOC**.
**Source:** `../data/test_trajectory.csv`.

**Shows:** monotone growth over ten months, with the split annotated. The `[B]`
series is scope-consistent and needs no caveat about mixing suites, so it is the
one to chart.
**Caveat:** the two series measure **different things** and must never be
plotted together — `[A]` expands data providers, `[B]` counts `function test*`
declarations. `[B]` is systematically lower.

## M-2 — Two-day remediation epic: output volume

**Metric:** commits / files / LOC / findings in the Sprint-114 epic (2026-05-27/28).

| | `[A]` reported | `[B]` measured | |
|---|---|---|---|
| Commits | 61 (59 stripe + 2 pb) | **64** (62 + 2) | ⚠️ low by 3 |
| Files | 178 | **183 unique code files** (88 src + 89 tests + 6 pb); 238 incl. docs; 339 change events | ✅ |
| LOC | +11,204 / −5,876 | **+15,844 / −6,075** | ⚠️ **low ~41%** |
| Tests added | +202 | **+196 test methods** | ✅ |
| Findings closed | 54/54, 0 deferred | not derivable | `[A]` only |
| AI-attributed | not stated | **60/64 commits (94%)** carry a Claude trailer | `[B]` only |

**Source:** `117`; `../data/commits.csv`.
**Shows:** peak sustained throughput of reviewed, tested, gate-passing change —
and a worked example of a self-report that **understates** its own output.
**Caveat:** best-instrumented episode; **not** representative of an average day
(see M-11). Reporting it as a rate overstates throughput ~10× (M-12).

## M-3 — Agent-compute distribution across dispatches

**Metric:** wall-clock agent compute per dispatch.
**`[A]` Values:** **≈568 min ≈ 9.5 h** across **15 dispatches**; longest
**165 min** (114.8), shortest **8 min** (114.6). **Source:** `117` §13, §22.
**`[B]` Cross-check:** the same two days measure **8.2 h across 4 commit
sessions**; raw calendar spans are 11.7 h (day 1, 10:28→22:12) and 5.1 h (day 2,
08:58→14:05). Same order of magnitude, independently derived.
**Shows:** a compute-per-dispatch distribution (histogram / box-plot) and
cost-per-finding.
**Caveat:** `[A]` is *agent* wall-clock, not human effort, and is unique to this
epic. `[B]` bounds it from a different direction but cannot decompose it per
dispatch — **the per-dispatch distribution remains single-sourced.**

## M-4 — Quality-gate pass rate & static-analysis debt trend

**Metric:** gate-green commits; new suppressions; PHPMD baseline size.
**`[A]` Values:** **61/61 commits** gate-green (phpcs / PHPStan `--level=max` /
PHPMD / PHPUnit); **0 new suppressions**; PHPMD baseline **4 → 3**.
**Source:** `117` §14 (R-6).
**`[B]` Partial confirmation:** the PHPMD baseline claim is **exact** —
`tests/PhpMd/phpmd.baseline.xml` holds **4 entries before** commit `b23f3de`
(Sprint 114.6) and **3 after**, and still 3 on the current branch. The
gate-green rate itself is **not derivable** from git.
**Shows:** debt going *down* while volume goes up — a rare, quantifiable
"quality did not degrade" claim, with the debt half now independently verified.
**Caveat:** baseline count is small; a trend indicator, not a coverage measure.

## M-5 — Incident catalog: counts by type & severity

**Metric:** bug/CI-failure/regression counts, classified.
**`[A]` Values:** **~75 distinct incidents**; largest cluster **CI/infra &
cross-repo auth**; deepest cluster **contract state-machine × OXID
`finalizeOrder`**; **~10** rated hard/multi-iteration.
**Source:** incident-forensics pass.
**`[C]` Formal bug record:** **40 `Bug`-type issues** (of 156), plus 3 issues
closed **`Not a bug`** and 3 marked **`Core Bug`** (triaged to the OXID platform,
not the module) — **6/40 = 15% reclassified away**. So `[A]`'s ~75 is a
**superset**: it counts CI failures and regressions that never became tickets.
The journal's claim that "a meaningful fraction of reported bugs resolved to
configuration, data, or infrastructure" is **confirmed with a number**.
**`[B]` Directional support:** `ci`-path churn totals **288 file-changes
(+10,074 / −1,894)** and `ci:`-prefixed commit subjects recur across the whole
ten months — the same cross-repo composer-resolution problem is still being
fixed on 2026-08-19. Consistent with "infra > logic," but git **cannot price the
cluster in hours**.
**Shows:** a defect-taxonomy bar chart and a "where the hard time actually went"
argument.
**Caveat:** classification is post-hoc from narrative; severity is effort-based,
not formal (except security items). See M-17 — the expensive failures left the
*least* trace in the commit record.

## M-6 — CI-failure detection & resolution windows

**Metric:** time from last-green to red, and iterations-to-fix.
**`[A]` Values:** unification break — stripe-wallet **7h18m** last-green→red
(2026-04-23 07:21→14:39 UTC); payment-component **~26h25m** green→breaking
force-push; **5 falsified CI iterations**; the rename day spent **~4 h of 7** in
a CI loop with **5 distinct failure modes**.
**Source:** `20260505/reports/01,02-*.md`; `20260508/done/sprint-102-completion-report.md`.
**`[B]` Not measurable.** These windows come from CI/server timestamps, not
commits. What git *does* show for the rename day (2026-05-08) is **565 unique
files across 10 commits** — and that **all 10 commits share one identical
subject line**, so the five failure modes are indistinguishable in history.
**Shows:** MTTR-style windows and an iteration-count metric for environment bugs.
**Caveat:** windows derive from CI logs, not a tracked incident clock, and
**cannot be reconstructed from the artifact** — this metric is journal-dependent
by nature.

## M-7 — Real developer effort per sprint (the 3 timestamped days)

**Metric:** clock-bracketed effort.
**`[A]` Values:** 2026-01-23 **4h43m** for 6 sprints (per-sprint 10–60 min;
S10 = 1 h); 2025-12-03 **~4h15m**; 2026-05-08 **7h17m**.
**Source:** the three status/report files.
**`[B]` Superseded in scope by M-11:** the commit record supplies a lower bound
for **all 143 active days**, not 3. The three `[A]` days remain the only place
*human* effort is bracketed; `[B]` measures commit-bearing spans.
**Shows:** the only genuine "minutes per sprint" data — a sprint is hours, not
days. `[B]` corroborates: median multi-commit session **37 min**.
**Caveat:** n = 3 days for `[A]`; do not extrapolate. Use M-11 for project-wide
statements.

## M-8 — Security audit: findings, severity mix, and burn-down

**Metric:** finding counts by severity and remediation status.
**`[A]` Values:** **28 findings (5 Critical / 10 High / 9 Medium / 4 Low)**;
post-remediation **26/28 done**, all HIGH blockers resolved; standards mapped:
**PCI-DSS v4.0, GDPR, BSI TR-03116-4, OWASP Top 10, PSD2-SCA**; sample CVSS:
TOCTOU idempotency **7.0**, secret-key leak **7.5**.
**Source:** `2026/02/20260219/reports/01-security-audit-strp99-no-mcp.md`.
**`[B]` Fix presence confirmed, scores not.** The remediations are structural and
therefore visible: `isConfigured()` now reads
`!empty(getToken()) && !empty(getWebhookSecret())` (S2, the fail-closed fix);
`UniqueConstraintViolationException` is caught in
`DoctrineWebhookLogRepository` (the atomic-`claimEvent` TOCTOU fix);
`WebhookPayloadSanitizer` exists (H7/GDPR); all four webhook guards and all
**7/7** validation guards exist by exact class name.
**Shows:** a severity-mix pie + burn-down with the 2 deferred items explicit.
**Caveat:** audit and remediation are both **AI-authored and self-scored** — not
an independent assessment. Git confirms a control **exists**; it can never
confirm the control is **sufficient**, nor validate a CVSS score.

## M-9 — DRY / dead-code reduction (before → after)

**Metric:** duplicated-call-site collapse; LOC removed; method-size reduction.
**`[A]` Values:** cents-math **22 call-sites → 1** (`AmountConverter`);
**~2,020 LOC** dead code removed (S114); handler reductions
**CheckoutReturnHandler 144→42**, **`createCheckoutSession()` 81→28**; webhook
dispatch **330→107 lines**; rename touched **~700 PHP files**; cross-module
byte-identity via **SHA-256 over 323 files**.
**Source:** `117` §11/§166; `116-remediation-complete.md`; `sprint-114.4-*`.

**`[B]` Two claims exact, one materially incomplete:**

| Claim | Measured | |
|---|---|---|
| webhook dispatch 330 → 107 | `StripeWebhookProcessor.php`: **330 → 107 lines** | ✅ exact |
| `LazyStripeAdapter` −183 LOC | `b23f3de`: **0 insertions / 183 deletions** | ✅ exact |
| cents-math 22 → 1 | source docblock says "~22"; **0 raw `* 100` sites remain** outside the converter | ✅ and it *held* |
| rename ~700 files | **565 unique files** in the 2 corpus repos (163 + 402) | ✅ consistent |
| "simplification" | ⚠️ same commit added **8 handler classes (+600 src)** and **9 test files (+856)**; module handler code **2,616 → 2,953 LOC**, now **3,147 across 24 files**; commit overall **+1,766/−1,701** (near-neutral) | **one file, not the module** |

**Shows:** quantified simplification with before/after pairs — and, corrected, a
more honest pattern: **these refactors reduced per-unit complexity while
aggregate code held flat or grew.** The largest handler did shrink (the 389-line
capture handler is now 305), and the refactor commit was near LOC-neutral overall,
but the module-level handler total rose by 337 lines. A before/after pair quoting
only the shrinking file overstates the result.
**Caveat:** some LOC figures disagree between a sprint's plan and its completion
report — report ranges. The "~22" is approximate **in the source itself**.

## M-10 — Yield of disciplined refactoring: bonus bugs & test-honesty fixes

**Metric:** defects found as a *side effect* of DRY/refactor; false-green eliminated.
**`[A]` Values:** **7 bonus bugs** fixed during the epic, incl. **4 real-money
truncation bugs** (`(int)(19.99*100)=1998`) absent from the original review;
integration suite **53 of 157 tests silently skipped (~34%) → 0 silent skips**;
false-positive tests (`assertTrue(true)`) removed.
**Source:** `117` §4/§5; `sprint-17-fix-false-positive-tests-report.md`.
**`[B]` The fix is verifiable; the serendipity is not.** `AmountConverter`'s own
docblock records both the bug and the fix verbatim — *"19.99 * 100 = 1998.9999…
→ (int) gives 1998 (WRONG); (int) round(19.99 * 100) → 1999 (CORRECT)"* — and
**zero raw cents-math sites remain** outside it. That the bugs were found *as a
side effect* rather than sought is **not derivable from git**, and it is the
topic's actual contribution.
**Shows:** a measurable argument that DRY consolidation is an effective
*bug-finding* technique, and a "hidden test debt" quantification.
**Caveat:** the 4 bonus bugs are a lower bound. The causal claim rests on `[A]`.

---

# Git-only measurables (new, 2026-08-20)

Seven results that require the commit record. These are the entries with no
journal counterpart, and several are stronger than anything in M-1…M-10 because
nothing about them depends on the project's testimony about itself.

## M-11 — Session-derived active time across the whole project `[B]`

**Metric:** work sessions (commit runs separated by ≤90 min) and their spans.
**Values:** **227 sessions, ≈140.1 h** total (93.5 h inside the journal's own
window); **100 single-commit** sessions (zero measured duration) and **127
multi-commit**; median multi-commit session **37 min**, mean 66, longest **376**
(2025-12-01); median **4.4 commits/hour** in sessions of >2 commits. Per-month
totals in `../data/sessions.csv` show a **measured trough of 9.1 h across
March–April 2026**.
**Shows:** the effort denominator the journal could not supply (M-7 had n=3
days), and the cleanest instance of journal-vs-artifact divergence: the trough
is narrated as active work.
**Caveat:** a **lower bound** — invisible to reading, thinking, and debugging
that produces no commit; bounded at each session's last commit. State as "≥140 h
of commit-bearing activity."

## M-12 — Cadence distribution: the peak is not the rate `[B]`

**Metric:** commits per active day.
**Values:** **143 active days**; median **3**, mean **5.0**, max **35**. Only
**18 days carry ≥10 commits**. Busiest: 2026-01-16 (35, the package split),
05-27 (33), 05-28 (31), 08-19 (26), 2025-11-03 (21), 2026-01-15 (21).
**Shows:** the distribution is **bimodal** — a low modal day punctuated by
structural events. Directly corrects the temptation to read M-2's 30+
commits/day as sustained throughput; peak-as-rate overstates by ~10×.
**Caveat:** commits per day is a proxy for output, not value; the 35-commit day
was a mechanical package split, not 35 features.

## M-13 — Test-to-source write ratio `[B]`

**Metric:** lines of test code written per line of production code (squash
commit excluded).
**Values:** `tests` **+150,321 / −62,008** across 2,429 file-changes; `src`
**+88,896 / −40,888** across 2,918 — a ratio of **1.69 : 1**. Deletions run at
~46% of insertions in `src` (ongoing rewriting, not accretion).
**Shows:** the **only independent confirmation of the project's TDD claims**. A
project that merely asserted TDD while writing tests as an afterthought could not
produce this ratio. Pairs with M-2's +196 test methods in two days.
**Caveat:** volume of test code is **necessary but not sufficient** — M-10
documents this same project shipping tests that asserted nothing. Ratio measures
effort, not verification quality.

## M-14 — Working-hours distribution `[B]`

**Metric:** commits by weekday and local hour.
**Values:** Mon 104 (14.5%), Tue 132 (18.4%), **Wed 181 (25.3%)**, Thu 156
(21.8%), Fri 142 (19.8%), **Sat 0 (0.0%)**, Sun 1 (0.1%). Peak hours 13:00
(110), 16:00 (94), 14:00 (85), 12:00 (76), 17:00 (68). Only **29 commits (4.1%)
fall outside 08:00–20:00**.
**Shows:** the output of M-11/M-12/M-13 was produced **without schedule
compression** — zero Saturdays in ten months. The strongest quantitative support
for the "discipline" thesis, and orthogonal to every journal claim. The lone
exception is legible: the epic's day 1 ran to 22:12, the only such day.
**Caveat:** commit timestamps are when work *landed*, not when it was done;
batched commits could hide evening work. The weekday result is robust to this
(batching does not cross days for 715 of 716 commits).

## M-15 — Contributor distribution `[B]`

**Metric:** commits and LOC per author.
**Values:** Daniil Tkachev **621** commits (920,178 insertions), Bartosz
Sosnowski **61** (66,048), Mario Lorenz **19** (526), `dependabot[bot]` 8,
plus alias/placeholder identities (`dantweb` 3, `Deve L. Oper` 2, `Bartek
Sosnowski` 2). Consolidating aliases: **three human contributors at 87% / 8.8% /
2.7%**, the second active across the entire ten months.
**Shows:** **retracts the flagship paper's "single-developer" confound.** Any
inference to *solo* productivity is unsupported.
**Caveat:** git cannot show how the second contributor's practices differed — an
unmeasured confound, not a resolved one.

## M-16 — AI attribution over time `[B]`

**Metric:** `Co-Authored-By: Claude*` trailers by month and model.
**Values:** **149 / 716 commits (20.8%)**. Monthly share: **0% through April
2026**, then 65% (May), 27% (June), 67% (July), **86% (August)**. Two isolated
trailers on 2025-12-05, then nothing until 2026-05-07. Six model strings: Opus
4.7 (73 commits), Opus 5 (33), Opus 4.8 (31), Sonnet 4.6 (6), unversioned
"Claude" (5), Fable 5 (1) — total +31,838 / −9,996 LOC.
**Shows:** attribution *practice* maturing, and **six model generations across
four months**, each displacing its predecessor within days. Outcomes cannot be
attributed to "a model."
**Caveat:** this measures **attribution, not authorship**. Absence of a trailer
before May 2026 is **not** evidence of absence of AI involvement — so the
"primary code author" claim is **unverifiable for the project's first seven
months**. This is the single largest loss of confidence in the revision.

## M-17 — Provenance and message hygiene `[B]`

**Metric:** integrity of the commit record as an audit trail.
**Values:** **102 distinct commit subjects are reused** across multiple commits
— `"STRP-78 Extract paymenmt component"` **56×** (typo included), `"STRP-135
PaymentComponent -> PaymentBase namespace refactoring"` 10×, `"up"` 10× — and
**33 subjects contain spelling errors**. Only **61% of commits (436/716)** carry
a ticket reference. **11 merges.** On **2026-07-02 the `stripe-wallet` mainline
was squashed** (`6e828a242d6b`, 562 files re-added, +18,417 src / +44,534 tests
/ +19,803 docs); the **491 pre-squash commits survive only on
`b-7.4.x-LEGACY`**. Meanwhile `docs` is the **largest artifact class by volume**:
**+585,998 / −194,375** across 4,005 file-changes — **4.4× the production code**.
**Shows:** two results at once. (a) A **release that destroyed eight months of
per-commit provenance** — a real finding for a PCI-DSS-obligated module, and one
the journal never mentions; this research programme survives only because a
legacy branch was retained. (b) The **"log as memory" practice is, by output
volume, the project's dominant activity** — whether that is admirable discipline
or documentation overproduction is a genuine open question and a candidate for
its own paper.
**Caveat:** reused subjects make it impossible to audit the decomposition
conventions of PM-1 from history; the docs figure includes the dev log itself,
so it measures the *research corpus* as much as the deliverable.

## M-18 — Role separation: who asks, who tests `[C]`

**Metric:** reporter × issue-type cross-tabulation.
**Values:** **Daniil Tkachev 52 Stories / 5 Tasks / 0 Bugs** (57 total, 36.5%);
**Zerfas Razvan 37 Bugs / 5 Tasks / 0 Stories** (42, 26.9%) — **92.5% of all 40
bugs**; **Daniel Paniagua 26 Tasks and nothing else** (16.7%); Mario Lorenz 6
Stories / 4 Tasks / 8 Sub-tasks (11.5%); **10 reporters** in total.
**Source:** `../data/jira_roles.csv`.
**Shows:** the most consequential single result from the Jira corpus. The
developer who wrote the code with the assistant filed **zero bug reports**; an
independent tester supplied nearly all of them. The AI-assisted pair was the
*implementation* unit, not the *quality* system — a structure invisible in both
the journal (a developer's log) and git (which sees only committers).
**Caveat:** roles are inferred from reporting behaviour, not from job titles, and
the export has no work-log to show effort per role.

## M-19 — Issue → code coverage `[B]`+`[C]`

**Metric:** share of Jira issues with at least one commit referencing them.
**Values:** **61/156 (39%)** overall — **Story 40/58 (69%)**, **Bug 17/40
(42%)**, Task 4/50 (8%), Sub-task 0/8. Most-referenced issues: `STRP-145`
"DevLog review" (64 commits), `STRP-78` "Extract Component" (57), `STRP-52`
"Develop Strategy" (33), `STRP-60` "Provider SDK integration" (32).
**Source:** `../data/jira_issues.csv`.
**Shows:** Stories convert to code at 69% while Tasks sit at 8% — Tasks are
coordination, not engineering. Also shows why **tickets are a poor unit of work
here**: a handful of umbrella issues absorb most of the history.
**Caveat:** join is on `STRP-nnn` in commit *subjects* only; work committed
without a reference (39% of commits carry none) is invisible to this metric, so
coverage is a **lower bound**.

## M-20 — Ticket-reference integrity `[B]`+`[C]`

**Metric:** fabricated vs mislabelled ticket references in commit messages.
**Values:** **61/61 distinct refs resolve to real Jira issues — zero
fabricated**, across **436 ticket-bearing commits**. **One mislabel:** `bf32d77`
"STRP-138 AGB complience" contains the `STRP-139` T&C fix, carries `STRP-138`'s
documentation, and has a literal **`strp-xxx` placeholder** in its plan file;
**`STRP-139` appears in no commit message in the corpus.**
**Shows:** a concrete negative result on the most common worry about LLM-authored
commit metadata — no hallucinated identifiers — and a precise taxonomy split:
**misattribution ≠ fabrication**. The mislabel is simultaneously an instance of
granularity collapse against an *externally defined* boundary (two tickets filed
by two different people), which makes it a cleaner specimen than any internal
phase plan.
**Caveat:** the export is a snapshot; a ref could resolve to an issue created
*after* the commit. Spot-checking found no such case, but it is not excluded
systematically.

## M-21 — Project age and prehistory `[C]`

**Metric:** issue creation dates relative to the commit record.
**Values:** Jira spans **2023-05-30 → 2026-06-22**. **55/156 issues (35%) predate
the commit record's start (2025-10-21)** — 44 `Task`, 8 `Sub-task`, 3 `Story`, of
which **44 are `Done`**. Creation peaks in 2026-04 (20), 2026-02 (17), 2026-06
(13), 2026-05 (12).
**Shows:** the STRP project is roughly **three years old**; the AI-assisted
implementation phase this programme studies is its **final ten months**. Every
velocity, effort and output figure here describes a *phase*, not a project, and
the 2023–2025 strategy/evaluation/design effort is a cost none of the corpora
price.
**Caveat:** old `Done` tasks may have been bulk-closed during a tracker cleanup
rather than delivered; creation dates are reliable, closure dates are not.

## M-22 — Lead time, and what Jira cannot measure `[C]`

**Metric:** Created → Resolved interval.
**Values:** **n=39, median 17 days**, mean 28, min 0, max 91.
**Shows:** the only cycle-time signal in existence for this project.
**Caveat:** the weakest number in the catalogue, and reported mainly to document
its weakness. `Resolution` is set on 39 issues while **82** are in status
category `Done`; several 0-day closes are 2023-era tasks. Treat as an order of
magnitude.
**What is absent, and closes off a planned study:** `Original estimate`,
`Remaining Estimate`, `Time Spent`, `Work Ratio` and their `Σ` variants are
**empty for all 156 issues**. Combined with the journal's 3 clock-stamped days,
**planning accuracy for AI-assisted work cannot be measured from any corpus in
this programme** — PM-3's estimate-vs-actual proposal must be withdrawn and
rescoped to its methods contribution.

---

### Suggested figures

1. **Test trajectory** (M-1 `[B]`) — line chart, both packages summed, split
   annotated. Use the git series, not the PHPUnit series.
2. **Cadence histogram** (M-12) — commits/active-day, showing the bimodal shape
   with the 18 high days as a labelled tail.
3. **Weekday × hour heatmap** (M-14) — the empty Saturday column is the figure.
4. **Test-vs-source cumulative LOC** (M-13) — two lines diverging at 1.69:1.
5. **Journal claim vs git measurement** (M-2, M-9) — paired bars with the
   direction of error signed, not absolute.
6. **AI-trailer share by month** (M-16) — step change at 2026-05-07, annotated
   as *convention adopted*, not *AI introduced*.
7. Compute-per-dispatch histogram (M-3) and security severity pie + burn-down
   (M-8) — both `[A]`-only; label them as self-reported in the caption.
8. **Reporter × issue-type matrix** (M-18) — the zero cells are the figure:
   developer/Bugs and tester/Stories are both empty.
9. **Issue→code coverage by type** (M-19) — Story 69% vs Task 8%.
10. **Issue creation timeline** (M-21) with the commit-record window shaded, so
    the three-year prehistory is visible at a glance.

### One-line takeaway for each cluster

Output is large and now **independently** measurable (M-1/2/11/12/13); quality
improved measurably while volume rose, though the refactors grew total code as
they shrank per-unit complexity (M-4/9/10); the hard time went to *environment
not logic* and left the least trace (M-5/6/17); effort is now bounded
project-wide rather than sampled from 3 days (M-7→M-11); the work was done in
ordinary hours by three committers, not one (M-14/15), inside a **10-person
project where a dedicated tester filed 92.5% of the bugs** (M-18); ticket
metadata was **never fabricated but once misattributed** (M-20); the studied
window is the **final ten months of a three-year project** (M-21); the project's
own attribution practice cannot support its authorship claim before May 2026
(M-16); and planning accuracy is **unmeasurable from any corpus** (M-22) — the
honest strength and the honest limit of this dataset, side by side.
