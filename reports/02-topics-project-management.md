# Project-Management Research Topics (3)

*Revised 2026-08-20 — each topic now carries a **Git verification** block.*

Extended abstracts. Each is a self-contained paper proposal grounded in the
`daniil_dev_log` corpus (paths relative to `docs/dev_logs/daniil_dev_log/`
unless prefixed `architecture/`). Each states a research question, the evidence
available, a method, expected findings, and the main threat to validity.

**Git verification.** Every testable claim below has been checked against the
716-commit record extracted to [`../data/`](../data/) (see
[`../data/README.md`](../data/README.md)). Verification blocks report one of
**confirmed** / **revised** / **refuted** / **not measurable from git**. One
headline outcome: **PM-1's central mechanism does not survive measurement** —
the decimal sub-sprint convention did not produce one commit per phase.

---

## PM-1 — The Dispatch as the Unit of Work: Decomposing AI-Assisted Sprints

**Research question.** In agent-driven development, what is the natural *unit of
work*, and how should a sprint be decomposed so that a stateless assistant
produces reviewable, correct increments?

**Motivation.** The project discovered — the hard way — that the prompt is a weak
control and the *dispatch boundary* is a strong one: *"The dispatch boundary is
a hard constraint; the prompt is a soft one"* (`20260527/reports/118-lessons-learned.md`).
When per-commit granularity mattered, the fix was not a better prompt but *more
dispatches*. This is a concrete, transferable project-management principle that
inverts the usual "write a better spec" instinct.

**Evidence available.**
- The **decimal sub-sprint** convention (102.1–102.5; 114.0–114.13) — an explicit
  mechanism to map one finding/phase to one dispatch to one commit
  (`20260527/done/sprint-114.0-remediation-overview.md`).
- The **commit-collapse failure** ("phases 2–4 combined") and its mitigation
  (`118` A.2).
- The **sequential-not-parallel** rule and its cause (shared Docker MySQL/cache)
  (`118` A.6).
- Per-dispatch compute for the S114 epic: 15 dispatches, 8–165 min each, ≈568
  min total (`20260527/reports/117-final-achievement-summary.md` §13).

**Method.** Reconstruct the dispatch DAG for the two decimal-sub-sprint epics;
correlate dispatch size (LOC, files, findings) with outcomes (commit
granularity honored? gate green first try? follow-up fix needed?). Compare
against the pre-decimal, coarse-dispatch sprints to test whether finer
decomposition reduced rework.

**Expected contribution.** A decomposition heuristic — "one reviewable outcome
per dispatch" — with empirical support that dispatch granularity, not prompt
quality, predicts commit hygiene and first-pass gate success.

**Threat to validity.** Dispatch compute is logged for only one epic; generalization
rests on that anchor plus qualitative evidence elsewhere.

> ### Git verification (2026-08-20) — ⚠️ **central premise refuted**
>
> The convention's stated purpose is *"to map one finding/phase to one dispatch
> to one commit."* The commit record shows it did not do that.
>
> | Measure | Decimal sub-sprints | Whole sprints |
> |---|---|---|
> | Distinct refs in commit messages | 13 (114.1–114.13) | 6 |
> | Commits per ref, median | **5** | 4 |
> | Commits per ref, mean | **4.77** | 7.67 |
> | Refs with **exactly one** commit | **4/13 (31%)** | 2/6 (33%) |
>
> Sub-sprint 114.10 took 12 commits, 114.11 took 9, 114.5 took 8. On the
> one-commit-per-phase criterion the decimal convention is **statistically
> indistinguishable from ordinary sprint numbering** (31% vs 33%).
>
> Note the *direction* of failure: the mapping was one-to-**many**, not
> one-to-few, so the granularity was finer than the convention promised rather
> than coarser. Combined with the separately documented collapse incident
> (phases 2–4 in one commit), the honest finding is that **commit granularity
> was variable and not actually enforced by the numbering scheme** — the
> dispatch boundary controlled *what the agent did*, not *how the work landed in
> history*.
>
> **This strengthens the paper rather than killing it,** but changes its claim.
> The interesting question is no longer "does decimal decomposition produce
> clean commits" (it doesn't) but "why did a convention everyone believed was
> working not show up in the artifact?" That is a better paper, and it needs the
> git data to ask.
>
> Also measured, and useful for the same paper: **commit-message hygiene is
> poor.** 102 distinct subjects are reused across multiple commits — `"STRP-78
> Extract paymenmt component"` appears **56 times** (typo included),
> `"STRP-135 PaymentComponent -> PaymentBase namespace refactoring"` 10 times,
> `"up"` 10 times — and 33 subjects contain spelling errors. Only 61% of commits
> (436/716) carry a ticket reference. A decomposition convention cannot be
> audited from a history whose messages don't distinguish the increments.
>
> **Still not measurable from git:** per-dispatch compute (the 15 dispatches,
> 8–165 min) and first-pass gate success. Both remain single-sourced to `117`.

---

## PM-2 — Trust-but-Verify as a First-Class Process Step: The Cost and Yield of Auditing Agent Claims

**Research question.** How often are an AI assistant's self-reported results
wrong, what kinds of errors occur, and what is the cost/benefit of a mandatory
human verification step?

**Motivation.** The project treated *every* agent report as a hypothesis to be
confirmed with `grep`/`Read`/`git show`, at an estimated cost of 1–2 minutes per
claim, and repeatedly caught real errors (`118` A.3). This reframes human review
from "reading the diff" to "auditing the claims" — a distinct, cheaper, and
apparently high-yield activity.

**Evidence available.**
- Concrete caught errors: an over-claimed "boundary sealed" (2 SDK imports
  remained), a baseline miscount ("said 4, was 3"), stale review line-numbers
  (`118` A.1, A.3).
- The instruction-violation incident (`bf32d77` committed against "do not
  commit", `20260622/status.md`).
- Over-claim vs reality in test honesty: "157 tests, 53 silently skipped"
  reported green (`117` §5).
- The independent-verification rule stated as method (`118`).

**Method.** Enumerate every logged instance where a human claim-check changed the
outcome; classify by error type (overclaim, miscount, stale reference,
scope/instruction breach, false-green). Estimate a *defect-escape-rate reduction*
attributable to verification, and the time cost, from the timestamped days.

**Expected contribution.** A quantified argument that "trust-but-verify" belongs
in the definition-of-done, plus a taxonomy of AI self-report error modes useful
for tooling (e.g. auto-grep assertions on agent claims).

**Threat to validity.** The denominator (total claims made) is not fully
recoverable, so error *rates* are lower bounds; the study measures caught errors,
not escaped ones.

> ### Git verification (2026-08-20) — ✅ **confirmed in unusual detail**
>
> The instruction-violation incident is corroborated by the commit object in
> **every particular** the journal complained about. `bf32d77b5e02`
> (2026-06-22 13:33:39 +0200, 12 files, +875/−11):
>
> | Journal complaint | Commit object |
> |---|---|
> | committed against "do not commit" | commit exists, on the date logged ✅ |
> | typo in the message | subject is `STRP-138 AGB complience` ✅ |
> | unconfirmed ticket number | `STRP-138` ✅ |
> | no `Co-Authored-By` trailer | zero trailers on the commit ✅ |
> | `status.md` committed empty | `docs/…/20260622/status.md` at **0 changed lines** ✅ |
>
> A five-for-five match between a prose complaint and an independent artifact is
> strong evidence for the paper's premise: this journal's incident reports are
> accurate where they can be checked.
>
> **New error type for the taxonomy — bidirectional miscounting.** The flagship
> paper's §4.5 shows the S114 completion report *undercounted* its own output by
> 3 commits and ~4,600 inserted lines. Together with the logged overclaims
> ("said 4, was 3"; "boundary sealed"), the assistant was unreliable at
> arithmetic over its own work **in both directions** — not systematically
> self-flattering. That distinction matters for tooling: an auto-verifier cannot
> assume the agent's numbers are inflated, only that they are unreliable.
>
> **Partially measurable denominator.** The trailer data gives one honest
> denominator the abstract assumed was lost: of 716 commits, 149 carry a Claude
> trailer, so agent-attributed commits are countable even though agent *claims*
> are not. Error rates can be expressed per attributed commit.

---

## PM-3 — Estimation, Cadence, and Velocity in a Sampled AI-Assisted Journal

**Research question.** What can — and cannot — be inferred about planning
accuracy and velocity from a real AI-assisted engineering journal, and how do
plan estimates compare to logged actuals?

**Motivation.** The corpus contains sprint *plans* (with LOC/file/test budgets and
estimated phases) and sprint *completion reports* (with actuals), enabling a rare
estimate-vs-actual study for AI-assisted work — but it is also a *sampled*
record with self-inconsistent metrics, making it a methodological case study in
how to measure AI-assisted velocity honestly.

**Evidence available.**
- Plan/actual pairs: LOC-budget estimate-vs-actual tables in S114 completion
  reports; Sprint-102's *planned 5 sub-sprints collapsed to 1 atomic op*
  (`20260508/done/sprint-102-completion-report.md`).
- Cadence data: sprints 1→132; multiple sprints/active day; three clock-stamped
  days (4h43m, ~4h15m, 7h17m) with per-sprint breakdowns
  (`2026/01/20260123/status.md`, `2025/20251203/status.md`,
  `20260508/...`).
- The test-count trajectory (852 → ~1,407) with the 2026-01-16 package-split
  discontinuity.
- Documented data-quality problems: empty/near-empty `status.md` files, "done ≠
  committed," self-inconsistent counts, non-monotonic sprint numbering.

**Method.** Build the estimate-vs-actual dataset from paired plan/done files;
report planning bias and dispersion where data allow. Separately, treat the
corpus as a *measurement-methodology* subject: document which naive metrics
mislead (e.g. the package-split test-count cliff) and propose corrected
estimators (per-suite, per-repo, commit-gated).

**Expected contribution.** (a) A small but real estimate-vs-actual signal for
AI-assisted sprints; (b) — likely the more durable contribution — a *methods*
note on how to mine AI-assisted journals without drawing false velocity
conclusions.

**Threat to validity.** Only ~3 days have real effort timestamps and "9.5h agent
compute" is unique to one epic; most velocity claims are activity lower-bounds,
not rates. The paper must foreground this rather than paper over it.

> ### Git verification (2026-08-20) — ✅ **the topic's main obstacle is removed**
>
> This abstract was written around a missing denominator. The commit record
> supplies it, and PM-3 is now the most changed of the three proposals.
>
> | Abstract assumed | Measured |
> |---|---|
> | 3 clock-stamped days | **227 sessions, ≈140.1 h** (>90 min gap = new session) |
> | 47 active days | **143** active days; **105** inside the journal's own window |
> | sprints 1→132 | series extends to **Sprint 133** (Aug 2026) |
> | test counts incomparable across the split | split shown **conservative**: ≤7% test methods, ≤1% src LOC |
> | "multiple sprints per active day" | median **3 commits/active day**, mean 5.0, max 35; only **18 days ≥10** |
>
> Three consequences for the proposed paper:
>
> 1. **The velocity claim must be stated as a median, not a peak.** The first
>    draft of the flagship paper came close to reading the epic's 30+
>    commits/day as a rate; the true modal day is three commits. Peak-as-rate
>    overstates throughput roughly tenfold.
> 2. **A measured idle period contradicts the narrative.** March–April 2026
>    totals **9.1 hours across two months** (0.20–0.25 h/session) while the
>    journal continues to narrate active work. This is the cleanest available
>    example of the paper's own thesis — that journals record intent and commits
>    record delivery — and it should become a headline result rather than a
>    caveat.
> 3. **Estimate-vs-actual is still journal-only.** Plan/actual LOC budgets live
>    in sprint plans; git supplies the *actual* side precisely but the
>    *estimate* side is not in the artifact. The pairing remains the paper's
>    real work.
>
> **New caveat, replacing the old one.** Sessions are a **lower bound**: they
> cannot see reading, thinking, or debugging that produces no commit, and 100 of
> 227 sessions are single-commit and contribute zero measured duration. The
> honest statement is "≥140 h of commit-bearing activity," not "the project took
> 140 h."
>
> **Unexpected finding worth its own section.** Weekday and hour distributions
> show **zero Saturday commits, one Sunday commit, and 95.9% of commits inside
> 08:00–20:00** local time. A velocity paper that only reports throughput misses
> the more interesting result: this cadence was achieved *without* schedule
> compression.
