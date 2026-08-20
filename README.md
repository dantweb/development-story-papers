# Development Story Papers

Research write-ups mined from the real, day-by-day engineering record of an
AI-assisted software project: the **OXID eShop Stripe payment module**, built
with Claude (Claude Code) as a primary code author and a human engineer as
orchestrator, reviewer, and decision-owner.

Three corpora underpin the work:

- **The dev log** — a daily engineering journal of **462 markdown files
  (≈113,098 lines), 2025-11-26 → 2026-07-02**, plus a curated architecture
  corpus.
- **The commit record** *(added 2026-08-20)* — **716 commits across both
  subject repositories, 2025-10-21 → 2026-08-20**, with timestamps, diffs, and
  authorship trailers.
- **The Jira issue record** *(added 2026-08-20)* — **156 issues of the STRP
  project, 2023-05-30 → 2026-06-22**, joined to the commits on `STRP-nnn`
  references. The only corpus that records who asked for the work and who found
  the defects.

All extracted to CSV under [`data/`](data/). Together they form a longitudinal,
single-subject case study of AI-assisted software engineering in which the prose
record and the machine records are used to check each other.

## Contents

| File | What it is |
|------|------------|
| [`reports/00-README.md`](reports/00-README.md) | Index + shared data-quality caveats. |
| [`reports/01-flagship-paper-ai-assisted-payment-module.md`](reports/01-flagship-paper-ai-assisted-payment-module.md) | **Flagship paper** — *Discipline over Cleverness: A Longitudinal Case Study of AI-Assisted Development of a Production Payment Module.* Revised 2026-08-20 against the measured commit record. |
| [`reports/02-topics-project-management.md`](reports/02-topics-project-management.md) | 3 project-management topics (extended abstracts). |
| [`reports/03-topics-technical.md`](reports/03-topics-technical.md) | 5 technical topics (extended abstracts). |
| [`reports/04-topics-security.md`](reports/04-topics-security.md) | 2 security topics (extended abstracts). |
| [`reports/05-measurements.md`](reports/05-measurements.md) | 10 topics with measured results, sourced to dev-log files. |
| [`reports/06-novelty-assessment.md`](reports/06-novelty-assessment.md) | **Internal review of scientific novelty** — what would survive peer review, what to drop, recommended reframing and venue fit. |
| [`reports/07-lessons-learned.md`](reports/07-lessons-learned.md) | **Eight practitioner topics** — orchestrating a stateless agent, trust-but-verify, test volume vs verification, refactoring as defect detection, the repo as audit trail, why the AI pair still needs a tester, fail-closed money, and why the environment costs more than the logic. Includes a day-one checklist and the lessons the evidence cannot support. |
| [`data/`](data/) | 11 files of git- and Jira-derived measurables + [`data/README.md`](data/README.md) schema and reproduction commands. |

## Headline findings

Measured from the Jira record:

- **A dedicated human tester filed 37 of the project's 40 bugs (92.5%) and zero
  stories; the developer filed 52 stories and zero bugs.** The AI-assisted pair
  was the *implementation* unit, not the *quality* system — a structure invisible
  in both the journal and the commit history.
- **10 participants across 3 years** (issues from 2023-05-30). The AI-assisted
  phase studied here is the project's final ten months, not the project.
- **Zero of 61 ticket references were fabricated** across 436 ticket-bearing
  commits — one was misattributed (STRP-138 vs STRP-139). Misattribution and
  fabrication are different failure modes.
- **All Jira time-tracking fields are empty**, so planning accuracy for
  AI-assisted work is unmeasurable from any corpus here.

Measured from the commit record:

- **1.69 lines of test code per line of production code** (+150,321 vs +88,896)
  — an independent confirmation of the project's TDD claims that no self-report
  could supply.
- **Zero Saturday commits and one Sunday commit in ten months**, with 95.9% of
  all commits inside 08:00–20:00 local time. Sustained output without crunch.
- **143 active days** and **227 timestamp-derived work sessions ≈140 hours**,
  against the 47 day-dirs the journal documented — the journal undersampled its
  own project by ≈2.2×.
- Cadence is **bimodal**: median 3 commits/active day, but 18 days above 10 and
  a peak of 35. Quoting the peak as the rate overstates throughput ~10×.
- The flagship two-day remediation epic is **confirmed and revised upward**:
  64 commits (reported: 61), +15,844/−6,075 LOC (reported: +11,204/−5,876),
  183 code files, +196 test methods, 8.2 h of session time.
- Test suite grew **493 → 2,109 test methods**; the 2026-01-16 package split is
  shown to have been **conservative** (≤7% methods, ≤1% source LOC), resolving
  the first draft's biggest open caveat.

What the commit record took away:

- **"Single-developer" is retracted twice** — three human contributors committed
  code (87% / 8.8% / 2.7%), inside a ten-person project with a dedicated QA
  function.
- **AI-authorship share is unverifiable before 2026-05-07.** `Co-Authored-By:
  Claude*` trailers cover 149/716 commits (20.8%), reaching 86% by August 2026
  but effectively absent before May. The journal's bylines remain evidence, but
  not independent evidence.
- **A release squashed away eight months of history** (2026-07-02); the
  commit-level record survives only on a retained legacy branch — a process
  failure the journal never mentions. A **second** mechanism was found later:
  merged feature branches were deleted from the remote, orphaning a commit that
  survives only in a stale local checkout. Neither loss is detectable from inside
  the repository, so every commit count here is a **lower bound**.

Honest failure modes are documented throughout: the assistant committed against
an explicit "do not commit" order, collapsed commits, over-claimed *and*
under-counted completion, and shipped tests that tested nothing — each caught by
"trust-but-verify".

The developer's one-line thesis, recorded in the log: **"Discipline > cleverness."**

## What is actually new here

Assessed in [`reports/06-novelty-assessment.md`](reports/06-novelty-assessment.md).
Short version: **the headline thesis is the weakest part.** "Discipline >
cleverness" is close to conventional wisdom by 2026 and cannot be established
from n=1 with no counterfactual and six model generations inside the study
window. The defensible contributions are methodological:

1. **Auditing a self-account against machine records — and publishing the
   corrections.** A candid daily journal still diverged systematically:
   undersampled its active days 2.2×, understated its flagship epic by 41%,
   narrated a measured idle period as active, omitted the QA function entirely.
2. **`Co-Authored-By` trailers measure convention adoption, not AI involvement** —
   0% before 2026-05-07, 86% by August, six model strings in four months. A dated
   counterexample to a technique currently gaining traction.
3. **The productivity narrative structurally omits QA labour** — invisible in both
   the journal and git, visible only in the tracker.
4. **Test-to-source write ratio as a falsifiable proxy** for a self-reported
   process claim — real in volume, demonstrably hollow in places.
5. **Refactoring and black-box testing yielded disjoint defect sets** on the same
   subsystem, connecting to the classic inspection-vs-testing literature.
6. **Provenance loss is invisible from inside a repository** — two mechanisms, one
   orphan recovered from a stale checkout, all counts therefore lower bounds.

The engineering and security topics are practitioner-grade, not research-grade,
and the assessment says so.

## Status & caveats

Draft working papers. All five reports are now triangulated against git and
Jira; each topic carries a verification block labelled confirmed / revised /
refuted / not measurable. Caveats that bear on every claim: the dev log is a
**sampled, not continuous** record with real effort timestamps in only three
files; session-derived hours are a **lower bound** (they cannot see
non-committing work); `Co-Authored-By` trailers measure *attribution practice*,
not authorship, and are absent before May 2026; and the Jira export has **no
effort data**, a degenerate `Priority` field, and no status-transition history.
One terminology hazard: the journal's "Sprint 1 → 133" is a private convention
with **no relation** to Jira sprints.
