# Project-Management Research Topics (3)

Extended abstracts. Each is a self-contained paper proposal grounded in the
`daniil_dev_log` corpus (paths relative to `docs/dev_logs/daniil_dev_log/`
unless prefixed `architecture/`). Each states a research question, the evidence
available, a method, expected findings, and the main threat to validity.

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
