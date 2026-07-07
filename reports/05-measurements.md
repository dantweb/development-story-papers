# Measured Results (10)

Ten topics where the dev-log corpus supports **hard, quantitative results** —
not just narrative. Each entry states the metric, the measured value(s) actually
recorded in the log, the source file, and what a paper/section can demonstrate
with it. Paths are relative to `docs/dev_logs/daniil_dev_log/` unless prefixed
`architecture/`.

> **Read the caveats first.** The log is a *sampled, not continuous* record.
> Real HH:MM developer-effort timestamps exist in only **3 files**; agent-compute
> is measured for only **1 epic**; test counts are **not comparable across the
> 2026-01-16 package split**; and "done" ≠ "committed" for much 2026 work. Every
> measurement below is annotated with the limit that bears on it.

---

## M-1 — Test-suite growth trajectory (852 → ~1,407)

**Metric:** unit-test count over time. **Values (selected):** 852 (2025-11-28,
847 pass) → 1348 (2025-12-15) → **[package split]** 576 stripe / 686 pc
(2026-01-16) → 723/1728 assertions (2026-02-27) → 840/1993 (2026-04-16) → 921→1123
(2026-05-27, S114) → 1415 stripe (2026-06-22) → 1397→1407 (2026-07-02).
**Source:** per-day `status.md`; `20260527/reports/117-final-achievement-summary.md`.
**Shows:** monotone growth *within* each suite-scope regime; a chart with the
package-split break annotated. **Caveat:** the 2026-01-16 discontinuity is a
scope reset, not a regression — mandatory annotation.

## M-2 — Two-day remediation epic: output volume

**Metric:** commits / files / LOC / findings in the Sprint-114 epic.
**Values:** **61 commits** (59 stripe + 2 payment-base), **178 files**,
**+11,204 / −5,876 LOC** (net +5,328), **54/54 findings closed (0 deferred)** in
**2 calendar days**. **Source:** `20260527/reports/117-final-achievement-summary.md`.
**Shows:** peak sustained throughput of reviewed, tested, gate-passing change.
**Caveat:** this is the best-instrumented episode; not representative of an
average day.

## M-3 — Agent-compute distribution across dispatches

**Metric:** wall-clock agent compute per dispatch. **Values:** **≈568 min ≈ 9.5 h**
across **15 dispatches**; longest sub-sprint **165 min** (114.8), shortest
**8 min** (114.6). **Source:** `117` §13, §22. **Shows:** a compute-per-dispatch
distribution (histogram / box-plot) and cost-per-finding. **Caveat:** *agent*
wall-clock, not human effort; unique to this epic — the only place in the corpus
agent-compute is measured.

## M-4 — Quality-gate pass rate & static-analysis debt trend

**Metric:** gate-green commits; new suppressions; PHPMD baseline size.
**Values:** **61/61 commits** gate-green (phpcs / PHPStan `--level=max` / PHPMD /
PHPUnit); **0 new suppressions**; PHPMD baseline **4 → 3** (shrank).
**Source:** `117` §14 (R-6). **Shows:** debt going *down* while volume goes up —
a rare, quantifiable "quality did not degrade" claim. **Caveat:** baseline count
is small; treat as a trend indicator, not a coverage measure.

## M-5 — Incident catalog: counts by type & severity

**Metric:** bug/CI-failure/regression counts, classified. **Values:** **~75
distinct incidents** catalogued; largest cluster **CI/infra & cross-repo auth**;
deepest cluster **contract state-machine × OXID `finalizeOrder`** (empty-order
shells recurred, once as a regression-in-a-fix); **~10** rated hard/multi-iteration.
**Source:** incident-forensics pass (per-incident file citations therein).
**Shows:** a defect-taxonomy bar chart and a "where the hard time actually went"
argument (infra > logic). **Caveat:** classification is post-hoc from narrative;
severity is effort-based, not a formal CVSS-style scale (except security items).

## M-6 — CI-failure detection & resolution windows

**Metric:** time from last-green to red, and iterations-to-fix. **Values:**
unification break — stripe-wallet **7h18m** last-green→red (2026-04-23
07:21→14:39 UTC); payment-component **~26h25m** green→breaking force-push;
diagnosed over **5 falsified CI iterations**; the rename day spent **~4 h of 7**
in a CI loop with **5 distinct failure modes**. **Source:**
`20260505/reports/01,02-*.md`; `20260508/done/sprint-102-completion-report.md`.
**Shows:** MTTR-style windows and an iteration-count metric for environment bugs.
**Caveat:** windows are derived from CI/server timestamps, not a tracked
incident clock.

## M-7 — Real developer effort per sprint (the 3 timestamped days)

**Metric:** clock-bracketed effort. **Values:** 2026-01-23 **4h43m** for 6
sprints (per-sprint 10–60 min; S10 = 1 h); 2025-12-03 **~4h15m**; 2026-05-08
**7h17m**. **Source:** `2026/01/20260123/status.md`, `2025/20251203/status.md`,
`20260508/done/sprint-102-completion-report.md`. **Shows:** the only genuine
"minutes per sprint" data — a sprint is hours, not days. **Caveat:** n = 3 days;
do not extrapolate to a project-wide rate.

## M-8 — Security audit: findings, severity mix, and burn-down

**Metric:** finding counts by severity and remediation status. **Values:** **28
findings (5 Critical / 10 High / 9 Medium / 4 Low)**; post-remediation **26/28
done**, all HIGH blockers resolved; standards mapped: **PCI-DSS v4.0, GDPR, BSI
TR-03116-4, OWASP Top 10, PSD2-SCA**; sample CVSS: TOCTOU idempotency **7.0**,
secret-key leak **7.5**. **Source:**
`2026/02/20260219/reports/01-security-audit-strp99-no-mcp.md`;
`sprint-67-70-security-remediation-plan.md`. **Shows:** a severity-mix pie + a
burn-down chart with the 2 deferred items (C3-replay, L-series) explicit.
**Caveat:** audit and remediation are both AI-authored/self-scored — not an
independent third-party assessment.

## M-9 — DRY / dead-code reduction (before → after)

**Metric:** duplicated-call-site collapse; LOC removed; method-size reduction.
**Values:** cents-math **22 call-sites → 1** (`AmountConverter`); **~2,020 LOC**
dead code removed (S114); handler reductions **CheckoutReturnHandler 144→42**,
**`createCheckoutSession()` 81→28**; webhook dispatch **330→107 lines**; rename
touched **~700 PHP files**; cross-module byte-identity verified via **SHA-256 over
323 files**. **Source:** `117` §11/§166; `116-remediation-complete.md`;
`20260527/done/sprint-114.4-*`; `20260529/done/sprint-119-completion.md`.
**Shows:** quantified simplification with before/after pairs. **Caveat:** a few
LOC/method-size figures disagree between a sprint's plan and its completion
report (§7.3 of the flagship) — report ranges.

## M-10 — Yield of disciplined refactoring: bonus bugs & test-honesty fixes

**Metric:** defects found as a *side effect* of DRY/refactor, and false-green
eliminated. **Values:** **7 bonus bugs** fixed during the epic, incl. **4
real-money truncation bugs** (`(int)(19.99*100)=1998`) none of which were in the
original review; integration suite **53 of 157 tests silently skipped (~34%) → 0
silent skips**; false-positive tests (`assertTrue(true)`) removed.
**Source:** `117` §4/§5; `2025/20251209/done/sprint-17-fix-false-positive-tests-report.md`.
**Shows:** a measurable argument that DRY consolidation is an effective
*bug-finding* technique, and a "hidden test debt" quantification. **Caveat:**
the 4 bonus bugs are a lower bound (found incidentally, not by exhaustive search).

---

### Suggested figures

1. Test-count line chart (M-1) with the package-split break annotated.
2. Compute-per-dispatch histogram + cost-per-finding (M-3).
3. Incident taxonomy stacked bar by type × severity (M-5).
4. Security-finding severity pie + remediation burn-down (M-8).
5. DRY before/after paired-bar for the collapse metrics (M-9).

### One-line takeaway for each cluster

Output is large and *measurable* (M-1/2/3), quality *improved measurably* while
volume rose (M-4/9/10), the hard time went to *environment not logic* (M-5/6),
and effort-per-unit is small but *only weakly sampled* (M-7) — the honest
strength and the honest limit of this dataset, side by side.
