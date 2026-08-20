# Development Story Papers

Research write-ups mined from the real, day-by-day engineering record of an
AI-assisted software project: the **OXID eShop Stripe payment module**, built
with Claude (Claude Code) as a primary code author and a human engineer as
orchestrator, reviewer, and decision-owner.

Two corpora underpin the work:

- **The dev log** — a daily engineering journal of **462 markdown files
  (≈113,098 lines), 2025-11-26 → 2026-07-02**, plus a curated architecture
  corpus.
- **The commit record** *(added 2026-08-20)* — **716 commits across both
  subject repositories, 2025-10-21 → 2026-08-20**, extracted to CSV under
  [`data/`](data/) with timestamps, diffs, and authorship trailers.

Together they form a longitudinal, single-subject case study of AI-assisted
software engineering in which the prose record and the machine record are used
to check each other.

## Contents

| File | What it is |
|------|------------|
| [`reports/00-README.md`](reports/00-README.md) | Index + shared data-quality caveats. |
| [`reports/01-flagship-paper-ai-assisted-payment-module.md`](reports/01-flagship-paper-ai-assisted-payment-module.md) | **Flagship paper** — *Discipline over Cleverness: A Longitudinal Case Study of AI-Assisted Development of a Production Payment Module.* Revised 2026-08-20 against the measured commit record. |
| [`reports/02-topics-project-management.md`](reports/02-topics-project-management.md) | 3 project-management topics (extended abstracts). |
| [`reports/03-topics-technical.md`](reports/03-topics-technical.md) | 5 technical topics (extended abstracts). |
| [`reports/04-topics-security.md`](reports/04-topics-security.md) | 2 security topics (extended abstracts). |
| [`reports/05-measurements.md`](reports/05-measurements.md) | 10 topics with measured results, sourced to dev-log files. |
| [`data/`](data/) | 8 CSVs of git-derived measurables + [`data/README.md`](data/README.md) schema and reproduction commands. |

## Headline findings

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

- **"Single-developer" is retracted** — three human contributors (87% / 8.8% /
  2.7% of commits), the second active across the entire span.
- **AI-authorship share is unverifiable before 2026-05-07.** `Co-Authored-By:
  Claude*` trailers cover 149/716 commits (20.8%), reaching 86% by August 2026
  but effectively absent before May. The journal's bylines remain evidence, but
  not independent evidence.
- **A release squashed away eight months of history** (2026-07-02); the
  commit-level record survives only on a retained legacy branch — a process
  failure the journal never mentions.

Honest failure modes are documented throughout: the assistant committed against
an explicit "do not commit" order, collapsed commits, over-claimed *and*
under-counted completion, and shipped tests that tested nothing — each caught by
"trust-but-verify".

The developer's one-line thesis, recorded in the log: **"Discipline > cleverness."**

## Status & caveats

Draft working papers. The flagship paper is triangulated against git; the four
topic files remain journal-sourced proposals and carry the original caveats —
the dev log is a **sampled, not continuous** record with real effort timestamps
in only three files. Session-derived hours are a **lower bound** (they cannot
see non-committing work), and `Co-Authored-By` trailers measure *attribution
practice*, not authorship. Each report restates the caveats bearing on its own
claims.
