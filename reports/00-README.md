# Research Reports

*Created 2026-07-07 · flagship paper revised 2026-08-20 against the git record*

A set of research write-ups mined from the Stripe payment module's development
record, treated as a longitudinal, single-subject case study of AI-assisted
software engineering. Two corpora:

- **Corpus A — the dev log:** 462 markdown files (≈113,098 lines) spanning
  **2025-11-26 → 2026-07-02**, plus the curated `docs/architecture/` corpus.
  Self-reported prose.
- **Corpus B — the commit record:** 716 commits from
  `OXID-eSales/stripe-wallet` (586) and `OXID-eSales/payment-base` (130),
  spanning **2025-10-21 → 2026-08-20**. Machine-extracted to
  [`../data/`](../data/); schema in [`../data/README.md`](../data/README.md).

## Contents

| File | What it is | Corpus | Status |
|------|------------|--------|--------|
| [`01-flagship-paper-ai-assisted-payment-module.md`](01-flagship-paper-ai-assisted-payment-module.md) | **Flagship scientific paper** — *How Claude helped develop the payment module.* Abstract, methods, quantitative results, the human–AI collaboration model, honest failure analysis, threats to validity. | A + B | Full draft, revised |
| [`02-topics-project-management.md`](02-topics-project-management.md) | **3 project-management topics** as extended abstracts. | A | Proposals |
| [`03-topics-technical.md`](03-topics-technical.md) | **5 technical topics** as extended abstracts. | A | Proposals |
| [`04-topics-security.md`](04-topics-security.md) | **2 security topics** as extended abstracts. | A | Proposals |
| [`05-measurements.md`](05-measurements.md) | **10 topics with measured results** — metric, recorded value(s), source file, what it demonstrates, suggested figures. | A | Data catalog |

## How these were produced

Corpus A was mined by five parallel extraction passes (timeline/metrics,
incident forensics, architecture/tech, human–AI collaboration evidence,
security), then synthesized. Citations use paths relative to
`docs/dev_logs/daniil_dev_log/` unless prefixed with `architecture/`.

Corpus B was extracted from all refs of both repositories with `git log --all
--numstat`, capturing author/committer timestamps, per-path diffs,
`Co-Authored-By` trailers, and sprint/ticket identifiers; work sessions are
maximal commit runs separated by ≤90 minutes, and test-suite sizes are measured
from the tree at 15 checkpoints.

## Data-quality note

**Corpus A** is a **sampled, not continuous** record: 47 dated day-dirs across
~7 months, with real HH:MM developer-effort timestamps in **only three files**.
Sprint numbering is not globally monotonic, test counts are not comparable
across the 2026-01-16 package split, and "done" ≠ "committed" for much of the
mid-2026 work. It is also written by the party being studied.

**Corpus B** fails differently. Sessions are a **lower bound** on effort — they
cannot see thinking, reading, or debugging that produces no commit. `files_changed`
counts change *events*, not unique files. Test-method counts are not PHPUnit test
counts (which expand data providers), so the two series must never be mixed. A
mainline **squash on 2026-07-02** re-added 562 files and destroyed pre-July
provenance on `b-7.4.x-LEGACY` alone. And `Co-Authored-By: Claude*` trailers,
present on 149/716 commits, only became routine on 2026-05-07 — so their absence
is **not** evidence of absence of AI involvement.

Where the two corpora disagree, the flagship paper reports both and says which
it trusts (§4.9, Appendix A). The four topic files are still Corpus-A-only and
have **not** been revised against git; their quantitative claims should be read
with the same scepticism the flagship paper's first draft earned.
