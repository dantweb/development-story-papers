# Research Reports

*Created 2026-07-07 · **all five reports revised 2026-08-20** against the git and Jira records*

A set of research write-ups mined from the Stripe payment module's development
record, treated as a longitudinal, single-subject case study of AI-assisted
software engineering. Three corpora:

- **Corpus A — the dev log:** 462 markdown files (≈113,098 lines) spanning
  **2025-11-26 → 2026-07-02**, plus the curated `docs/architecture/` corpus.
  Self-reported prose.
- **Corpus B — the commit record:** 716 commits from
  `OXID-eSales/stripe-wallet` (586) and `OXID-eSales/payment-base` (130),
  spanning **2025-10-21 → 2026-08-20**.
- **Corpus C — the Jira issue record:** 156 issues of the STRP project,
  spanning **2023-05-30 → 2026-06-22**, joined to Corpus B on `STRP-nnn`
  references. The only corpus that records *who asked for the work and who found
  the defects*.

All machine-extracted to [`../data/`](../data/); schema and caveats in
[`../data/README.md`](../data/README.md).

## Contents

| File | What it is | Corpus | Status |
|------|------------|--------|--------|
| [`01-flagship-paper-ai-assisted-payment-module.md`](01-flagship-paper-ai-assisted-payment-module.md) | **Flagship scientific paper** — *How Claude helped develop the payment module.* Abstract, methods, quantitative results, the human–AI collaboration model, honest failure analysis, threats to validity. | A + B | Full draft, revised |
| [`02-topics-project-management.md`](02-topics-project-management.md) | **3 project-management topics** as extended abstracts, each with a **Git verification** block. | A + B | Proposals, verified |
| [`03-topics-technical.md`](03-topics-technical.md) | **5 technical topics** as extended abstracts, each with a **Git verification** block. | A + B | Proposals, verified |
| [`04-topics-security.md`](04-topics-security.md) | **2 security topics** as extended abstracts, each with a **Git verification** block. | A + B | Proposals, verified |
| [`06-novelty-assessment.md`](06-novelty-assessment.md) | **Internal review: what would survive peer review.** Tiers all 12 contributions by novelty *and* by evidence class (tested / census / n=1 / untestable, with statistics), names the claims to drop, recommends a reframing and venues. Read this first if you are deciding what to write up. | — | Review |
| [`07-lessons-learned.md`](07-lessons-learned.md) | **Eight practitioner topics** (LL-1…LL-8) — what we would tell the next team, each graded by evidence class, plus a day-one checklist and a list of lessons the evidence *cannot* support. | A + B + C | Proposals |
| [`05-measurements.md`](05-measurements.md) | **17 topics with measured results** — M-1…M-10 now show journal-reported beside git-measured values; M-11…M-17 are git-only measurables. | A + B | Data catalog, revised |

### Verification outcomes at a glance

| Topic | Outcome |
|---|---|
| **PM-1** dispatch as unit of work | ⚠️ **premise fails on its own terms** — 69% of decimal sub-sprints span >1 commit (median 5), so the convention did not do what it was for. The *comparison* with ordinary numbering is underpowered (Fisher p = 1.00) |
| **PM-2** trust-but-verify | ✅ confirmed in detail — the `bf32d77` incident matches the journal in all five particulars |
| **PM-3** estimation & velocity | ✅ main obstacle removed — 227 sessions / ≈140 h replaces n=3 clock-stamped days |
| **TECH-1** contract-first checkout | ✅ `function setState` occurs **zero times** in either `src/` — the invariant is structural |
| **TECH-2** event system | ✅ confirmed exactly; ⚠️ revised — "330→107" is one file; module handler code went **2,616 → 2,953 LOC** |
| **TECH-3** ISP theatre | ✅✅ strongest result — **exactly zero** consumers typehint the narrow interfaces |
| **TECH-4** CI/CD | ◐ partial — the rename is measurable (565 files), the CI sagas are journal-only |
| **TECH-5** money as a type | ✅ confirmed, and the consolidation **held**: 0 raw cents-math sites remain |
| **SEC-1** async money boundary | ✅ fixes present and fail-closed; scores and burn-down not verifiable |
| **SEC-2** central validation | ✅ **7/7** guards confirmed by exact class name |

### Which claims have a statistical test behind them

Seven do — see the *"Which lessons the data can actually prove"* section of
[`07-lessons-learned.md`](07-lessons-learned.md). Strongest: **role separation**
(χ² = 199.4, df 6, p = 2.6e-40, Cramér's V = **0.859**) and **test code
outweighing production code** (11/11 months, sign test p = 0.0010, bootstrapped
ratio CI **[1.39, 2.06]**). Also tested: trailer step-change (p = 5.2e-81),
weekend abstention (p = 1.2e-48), cadence overdispersion (index **6.93**,
p = 4.7e-126), issue→code coverage by type (p = 2.9e-10), out-of-hours
concentration (p = 4.8e-07). Everything else is either a census fact needing no
inference, a single verified incident, or — for all causal claims about AI's
effect — **out of reach without a second case**.

### Novelty, in one line

The contribution is **methodological, not thesis-driven**: the value is that a
project's self-account was audited against two independent machine records and
found to diverge in specific, directional ways. The "discipline over cleverness"
thesis is the *least* novel element and cannot be established at n=1 — see
[`06-novelty-assessment.md`](06-novelty-assessment.md), which recommends
demoting it to framing and leading with the audit.

### Per-topic Jira outcomes

| Topic | Jira outcome |
|---|---|
| **PM-1** | ⚠️ deepened — a second granularity failure (one commit, two tickets); **no artifact is a reliable unit of work**: 4 umbrella issues absorb most history, 39% of commits carry no ticket, and architectural refactors have no tickets at all |
| **PM-2** | ⚠️ **missing an actor** — verification had a second, institutional layer (a dedicated tester); 0/61 refs fabricated, 1 misattributed |
| **PM-3** | ❌ **estimate-vs-actual is impossible** — all Jira time fields empty; withdraw part (a) |
| **TECH-1** | ✅ the redirect-boundary defect class is documented from **2024**, pre-dating the design — and kept producing tester-filed bugs *after* it |
| **TECH-2** | ◐ MCP channel is `To Do` with 20 commits; `STRP-88` asserts both "Status: Complete" (body) and `To Do` (field) |
| **TECH-3** | ⚠️ **none of this work was ticketed** — ISP theatre survived with PHPMD as its *only* reviewer |
| **TECH-4** | ✅ a dedicated `Core Bug` status exists — 3 defects triaged to the OXID platform |
| **TECH-5** | ✅ BCMath deferral is a **live open ticket** (`STRP-160`); money is measurably the defect-dense area, and refactoring vs black-box testing yielded **disjoint** bug sets |
| **SEC-1** | ✅ security ran as a tracked workstream; ⚠️ `STRP-50` middleware security alerts open since 2025-07 |
| **SEC-2** | ⚠️⚠️ **QA-driven, not developer-initiated** — the tester filed the payment-failure bug *and* wrote the requirements task that became Sprint 119 |

### What Corpus C (Jira) changed

| Finding | Effect |
|---|---|
| **A dedicated tester filed 37/40 bugs (92.5%)**; the developer filed **0** | Reframes the whole case — the AI pair was the implementation unit, not the quality system |
| **10 Jira participants** across **3 years** (from 2023-05-30) | "Single-developer" retracted a second time; the studied window is the final 10 months of a longer project |
| **All time-tracking fields empty** for all 156 issues | PM-3's estimate-vs-actual study is **impossible** from any corpus; withdraw it |
| **0/61 ticket refs fabricated**, 1 mislabelled (STRP-138 vs 139) | Negative result on hallucinated commit metadata; new taxonomy entry: misattribution ≠ fabrication |
| **6/40 bugs (15%) reclassified** — 3 `Not a bug`, 3 `Core Bug` | Confirms the journal's "meaningful fraction were not module defects" with a number |
| Jira `Sprint` has **2 values** | The journal's "Sprint 1→133" is a private convention, **not** tracker sprints — a terminology hazard |

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

**Corpus C** is the most restrictive: no effort data at all, `Priority` degenerate
(145/156 = `SHOULD`), `Assignee` 76% empty, `Resolution` on 39 issues while 82 are
`Done`-category, no status-transition history, and a snapshot-only view taken
2026-08-20.

**Corpus B** also carries a **survivorship** problem: two mechanisms removed
provenance during the study window — the 2026-07-02 mainline squash, and the
deletion of merged feature branches (one orphaned commit was recovered from a
stale local checkout frozen at 2026-05-22). Neither is detectable from inside the
repository, so all commit counts are **lower bounds**. Corpus B otherwise fails
differently. Sessions are a **lower bound** on effort — they
cannot see thinking, reading, or debugging that produces no commit. `files_changed`
counts change *events*, not unique files. Test-method counts are not PHPUnit test
counts (which expand data providers), so the two series must never be mixed. A
mainline **squash on 2026-07-02** re-added 562 files and destroyed pre-July
provenance on `b-7.4.x-LEGACY` alone. And `Co-Authored-By: Claude*` trailers,
present on 149/716 commits, only became routine on 2026-05-07 — so their absence
is **not** evidence of absence of AI involvement.

Where the two corpora disagree, the flagship paper reports both and says which
it trusts (§4.9, §4.11, Appendix A). As of 2026-08-20 the four topic files have
**also** been checked against git; each topic carries a verification block
labelled **confirmed** / **revised** / **refuted** / **not measurable from git**.

Two patterns emerged from that pass and are worth stating once here. First, the
journal is **highly reliable on mechanical facts** — several LOC and method
counts match the artifact to the exact line (330→107, −183, 4→3, 25 methods).
Second, it is **systematically optimistic about simplification**: before/after
pairs quote the shrinking number and omit the code added to replace it. And the
failures that cost the most time — the multi-iteration CI sagas — left the
*least* trace in the commit record, so the most expensive class of work is the
least verifiable.
