# Research Reports — 2026-07-07

A set of research write-ups mined from the Stripe payment module's development
record: **462 markdown dev-log files (≈113,098 lines) spanning 2025-11-26 →
2026-07-02**, plus the curated `docs/architecture/` corpus. The material is
treated as a longitudinal, single-subject case study of AI-assisted software
engineering.

## Contents

| File | What it is | Status |
|------|------------|--------|
| [`01-flagship-paper-ai-assisted-payment-module.md`](01-flagship-paper-ai-assisted-payment-module.md) | **Flagship scientific paper** — *How Claude helped develop the payment module.* A full draft: abstract, methods (log-mining), quantitative results (velocity, incidents, quality gates), the human–AI collaboration model, honest failure analysis, threats to validity. | Full draft |
| [`02-topics-project-management.md`](02-topics-project-management.md) | **3 project-management topics** as extended abstracts, each ready to grow into its own paper. | Proposals |
| [`03-topics-technical.md`](03-topics-technical.md) | **5 technical topics** as extended abstracts. | Proposals |
| [`04-topics-security.md`](04-topics-security.md) | **2 security topics** as extended abstracts. | Proposals |

## How these were produced

The corpus was mined by five parallel extraction passes (timeline/metrics,
incident forensics, architecture/tech, human–AI collaboration evidence,
security), then synthesized. Every quantitative claim traces to a dated
dev-log file; citations use paths **relative to
`docs/dev_logs/daniil_dev_log/`** unless prefixed with `architecture/`.

## Data-quality note (applies to every report here)

The dev log is a **sampled, not continuous** record: only 47 dated day-dirs
across ~7 months, with real HH:MM developer-effort timestamps present in **only
three files**. Sprint numbering is not globally monotonic, test counts are not
comparable across the 2026-01-16 package split, and "done" ≠ "committed" for
much of the mid-2026 work. Each report restates the caveats that bear on its
specific claims. These are the honest limits of a case study built on a working
engineer's journal rather than an instrumented experiment.
