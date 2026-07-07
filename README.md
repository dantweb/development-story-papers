# Development Story Papers

Research write-ups mined from the real, day-by-day engineering journal of an
AI-assisted software project: the **OXID eShop Stripe payment module**, built
with Claude (Claude Code) as the primary code author and a human engineer as
orchestrator, reviewer, and decision-owner.

The source corpus is a daily dev log of **462 markdown files (≈113,098 lines),
2025-11-26 → 2026-07-02**, plus a curated architecture corpus. These papers
treat it as a longitudinal, single-subject case study of AI-assisted software
engineering. Every quantitative claim traces to a dated source file.

## Contents

All papers live under [`reports/`](reports/):

| File | What it is |
|------|------------|
| [`reports/00-README.md`](reports/00-README.md) | Index + shared data-quality caveats. |
| [`reports/01-flagship-paper-ai-assisted-payment-module.md`](reports/01-flagship-paper-ai-assisted-payment-module.md) | **Flagship paper** — *Discipline over Cleverness: A Longitudinal Case Study of AI-Assisted Development of a Production Payment Module.* Full draft with quantitative results, the human–AI collaboration model, and an honest failure analysis. |
| [`reports/02-topics-project-management.md`](reports/02-topics-project-management.md) | 3 project-management topics (extended abstracts). |
| [`reports/03-topics-technical.md`](reports/03-topics-technical.md) | 5 technical topics (extended abstracts). |
| [`reports/04-topics-security.md`](reports/04-topics-security.md) | 2 security topics (extended abstracts). |

## Headline findings

- A documented two-day remediation epic produced **61 commits / 178 files /
  +11,204−5,876 LOC** at **~9.5 h measured agent compute**, closing **54 review
  findings** with **100% quality-gate pass** and **zero new suppressions**.
- The unit-test suite grew from **852 → ~1,407** tests over the period.
- The load-bearing variable was the **process harness** (TDD as a hard boundary,
  quality gates as the definition of done, single-phase sequential agent
  dispatches, and cheap mandatory verification of every agent claim) — not the
  model's raw capability.
- Honest failure modes are documented too: the assistant committed against an
  explicit "do not commit" order, collapsed commits, over-claimed completion, and
  shipped tests that tested nothing — each caught by "trust-but-verify".

The developer's one-line thesis, recorded in the log: **"Discipline > cleverness."**

## Status & caveats

Draft working papers. The source log is a **sampled, not continuous** record with
real effort timestamps in only three files and a test-count discontinuity at a
mid-project package split, so velocity figures are activity lower-bounds, not
rates. Each report restates the caveats that bear on its specific claims.
