# Research Reports — index

*Created 2026-07-07 · **all seven reports revised 2026-08-21** against the git,
Jira and GitHub Actions records*

Research write-ups mined from the OXID eShop Stripe payment module's development
record, treated as a longitudinal, single-subject case study of AI-assisted
software engineering — with the project's self-account **audited against two
independent machine records** rather than taken at its word.

---

## 1. The four corpora

| | Corpus | Span | Size | What only it can tell you |
|---|---|---|---|---|
| **A** | the dev log | 2025-11-26 → 2026-07-02 | 462 markdown files, ≈113,098 lines, + the curated `architecture/` set | *intent* — why a decision was made, and the process rules |
| **B** | the commit record | 2025-10-21 → 2026-08-20 | 716 commits (`stripe-wallet` 586, `payment-base` 130) | *what actually landed*, and when, to the minute |
| **C** | the Jira issue record | 2023-05-30 → 2026-06-22 | 156 issues of project STRP | *who asked for the work and who found the defects* |
| **D** | the GitHub Actions history | 2025-10-21 → 2026-08-20 | 979 workflow runs, joined to commits on `head_sha` | *what happened to each commit after it landed* |
| **E** | a mutation-testing run | executed 2026-08-24 | Infection 0.31.9 over 462 mutants against the live suite | *whether the tests actually verify anything* |

A is self-reported prose. B, C, D and E are machine records, extracted to
[`../data/`](../data/) — 15 CSVs, a schema and caveats document
([`../data/README.md`](../data/README.md)), and
[`../data/stats.py`](../data/stats.py), which recomputes every statistical test
cited anywhere in these reports.

Each corpus is blind to something the others see. That is the point: the
programme's central method is **using B, C and D to test A**, and reporting the
divergences rather than the agreements.

---

## 2. Where to start

| If you want… | Read |
|---|---|
| the whole argument | [`01-flagship-paper…`](01-flagship-paper-ai-assisted-payment-module.md) |
| to decide **what is worth writing up** | [`06-novelty-assessment.md`](06-novelty-assessment.md) — read this *first* if you are choosing a paper |
| **which published problems we can speak to** | [`08-literature-review.md`](08-literature-review.md) |
| to know **what we would tell the next team** | [`07-lessons-learned.md`](07-lessons-learned.md) |
| a specific number, with its source and caveat | [`05-measurements.md`](05-measurements.md) |
| candidate papers on one theme | [`02`](02-topics-project-management.md) (management), [`03`](03-topics-technical.md) (technical), [`04`](04-topics-security.md) (security) |
| to check the arithmetic | [`../data/README.md`](../data/README.md), then `python3 data/stats.py` |

---

## 3. Contents

| File | What it is | Corpora | Status |
|------|------------|---------|--------|
| [`01-flagship-paper-ai-assisted-payment-module.md`](01-flagship-paper-ai-assisted-payment-module.md) | **Flagship paper** — *Discipline over Cleverness.* Abstract (a concrete spoiler), methods over three corpora, quantitative results §4.1–§4.12, the collaboration model, failure analysis, threats to validity, and an appendix table putting every journal claim beside its measured value. | A+B+C | Full draft, revised |
| [`02-topics-project-management.md`](02-topics-project-management.md) | **3 PM topics** (PM-1…PM-3) as extended abstracts, each with **Git** and **Jira verification** blocks. | A+B+C | Proposals, verified |
| [`03-topics-technical.md`](03-topics-technical.md) | **5 technical topics** (TECH-1…TECH-5), same treatment. | A+B+C | Proposals, verified |
| [`04-topics-security.md`](04-topics-security.md) | **2 security topics** (SEC-1, SEC-2), same treatment. | A+B+C | Proposals, verified |
| [`05-measurements.md`](05-measurements.md) | **30 measured results.** M-1…M-10 show journal-reported beside git-measured values; M-11…M-17 are git-only; M-18…M-22 are Jira-only; M-23…M-27 are Actions-derived. Each carries its metric, source, what it demonstrates, and the caveat that bears on it. | A+B+C | Data catalog |
| [`06-novelty-assessment.md`](06-novelty-assessment.md) | **What would survive peer review.** Tiers all **13** contributions (N-1…N-13) by novelty *and* by evidence class — tested / census / n=1 / mixed / untestable, with statistics. Names the claims to drop, recommends a reframing and research venues. | — | Review |
| [`08-literature-review.md`](08-literature-review.md) | **What published problems this corpus can speak to.** 13 entries against real papers, each graded **instantiates / supports / complicates / counterexample / challenges-us / cannot-address**, plus a consolidated list of where the literature undercuts *us* and six priority searches still outstanding. | — | Review |
| [`07-lessons-learned.md`](07-lessons-learned.md) | **8 practitioner topics** (LL-1…LL-8) — what we would tell the next team. Each graded by evidence class and routed to a **named venue**; plus the full inference grading (Tiers S/D/U/N/X), a 12-item day-one checklist, a submission sequence, three publication gates, and the lessons the evidence **cannot** support. | A+B+C | Proposals |
| [`X-01-five-articles-against-the-literature.md`](X-01-five-articles-against-the-literature.md) | **Five article proposals, each positioned against named published work** — stance (confirms / disproves / enhances), evidence by `N-`/`M-`/`T-` id, reviewer concessions, outstanding work, venue and gate. Opens with a review of reports 00–08 and a corrections queue of stale figures. | — | Proposals |

---

## 4. Headline results

**Tested** — statistic and p-value, all reproducible via `data/stats.py`. These
corpora are **censuses, not samples**, so each test rejects a chance-arrangement
null *within* this project and none licenses generalisation to AI-assisted
development at large.

| Result | Statistic | p |
|---|---|---|
| **Role separation** — the developer filed 52 Stories / **0 Bugs**; a dedicated tester filed **37 of 40 Bugs** / 0 Stories | Fisher on `[[52,0],[0,37]]`; full table **χ² = 199.4**, df 6, **Cramér's V = 0.859** | **6.7e-26** / **2.6e-40** |
| **Test code outweighs production code 1.69 : 1** (+150,321 vs +88,896) | 11/11 months by sign test; bootstrap 95% CI **[1.39, 2.06]** | **0.0010** |
| **AI-trailer adoption is a step change, not a trend** | 2/466 before vs 147/250 after 2026-05-07 | **5.2e-81** |
| **Cadence is bursty — the peak is not the rate** | **dispersion index 6.93** vs Poisson's 1.0 (χ² = 984.4, df 142) | **4.7e-126** |
| **Output without schedule compression** — 0 Saturdays in 716 commits | vs a uniform-7-day null; Mon–Fri itself non-uniform (p = 0.0001) | **1.2e-48** |
| **Issue→code coverage depends on issue type** — Story 69%, Bug 42%, Task 8% | χ² = 47.4, df 3 | **2.9e-10** |
| **Out-of-hours work is concentrated** — 13 of 29 on one day | exact binomial vs uniform over the 11 affected days | **4.8e-07** |
| **CI failure is independent of commit size** — 63% (≥500 ins.) vs 60%; the *null* is the finding | Fisher exact; Spearman **ρ = −0.024** | **0.66** |
| **CI failures cluster** — 85.7% follow another failure (published benchmark >50%); lag-1 ρ = 0.680 | transition rate vs independence | *descriptive + benchmark* |

> **Two claims withdrawn 2026-08-24** after the literature searches in
> [`08`](08-literature-review.md) §7.2: the CI failure rate's "coin flip"
> binomial test (assumed independent runs — invalid) and the 57%→46% CI
> improvement (nominal p = 0.0014 → **p = 0.18** once failure clustering is
> accounted for). Both remain true descriptively; neither is a tested claim.

**Measured by experiment (2026-08-24): Covered Code MSI 70%.** 1,592 mutants,
1,123 killed, **469 escaped**, reproducible across `--threads=1/4/8`. The suite
executes the code and misses **30%** of the semantic changes to it; the largest
escape category is **`MethodCallRemoval` (85/469)** — a call can be deleted with
the suite still green.

**The measurement was wrong three times first, and that is a finding.** The
initial figure (MSI 73%) was published as fact and was not reproducible: seven
runs on unchanged code returned **0–1,019 mutants and 0–73% MSI**. Neither the
coverage driver, the timeout, nor caching was the cause — **Infection's own
generated initial-test run uses a random seed and terminates early at a variable
point**, while PHPUnit's coverage run directly is perfectly deterministic. Fixed
by generating coverage externally and passing `--coverage --skip-initial-tests`.
See M-30.

**Census facts** — complete enumerations needing no inference (attaching a
p-value would be a category error): the journal undersampled its own active days
**2.2×** (47 documented vs 105 with commits); **zero** raw cents-math sites remain
outside the converter; `function setState` occurs **zero** times in either
`src/`; **exactly zero** consumers typehint the narrow adapter sub-interfaces;
**0 of 61** ticket references were fabricated; effort is unrecoverable (Jira time
fields empty for all 156 issues, journal clock-stamps 3 of 143 active days);
**CI failed on 487 of 979 runs (49.7%)** and consumed **169.5 h** of wall-clock —
more than the ≈140 h of measured human session time — with **53% of it in failing
runs**.

**Retractions and corrections** — the most credible part of the set:

| Claim | Outcome |
|---|---|
| "single-developer" | **retracted twice** — 3 committers (87/8.8/2.7%), inside a 10-person, 3-year project |
| "Claude was the primary code author" | **unverifiable before 2026-05-07**; trailers measure convention, not authorship |
| reported "simplifications" | describe **one file, not the module** (330→107 while handler code went 2,616→2,953) |
| PM-1 "premise refuted" | corrected to **underpowered** — the convention failed on its own terms (69% of sub-sprints span >1 commit), but the comparison tests at Fisher **p = 1.00** |
| §4.4 "the only such day" | **false** — 11 days carry out-of-hours commits; the pattern is concentration, not absence |
| rename day "10 commits" | **9** (author date; the earlier figure used committer-date filtering) |

---

## 5. Verification outcomes, per topic

| Topic | vs Git (B) | vs Jira (C) |
|---|---|---|
| **PM-1** dispatch as unit of work | ⚠️ **fails on its own terms** — 69% of decimal sub-sprints span >1 commit (median 5); the comparison with ordinary numbering is underpowered (p = 1.00) | ⚠️ deepened — one commit spanning two tickets; **no artifact is a reliable unit of work** (4 umbrella issues absorb most history, 39% of commits ticketless, refactors untracked) |
| **PM-2** trust-but-verify | ✅ confirmed in detail — `bf32d77` matches the journal in **all five** particulars | ⚠️ **missing an actor** — verification had a second, institutional layer; 0/61 refs fabricated, 1 misattributed |
| **PM-3** estimation & velocity | ✅ main obstacle removed — 227 sessions / ≈140 h replaces n=3 clock-stamped days | ❌ **estimate-vs-actual is impossible** — all time fields empty; withdraw part (a) |
| **TECH-1** contract-first checkout | ✅ `function setState` occurs **zero times** — the invariant is structural | ✅ the defect class is documented from **2024**, predating the design, and kept producing tester-filed bugs *after* it |
| **TECH-2** event system | ✅ exact (330→107); ⚠️ revised — that is one file; module handler code rose **2,616 → 2,953** | ◐ MCP channel is `To Do` with 20 commits; `STRP-88` asserts both "Complete" (body) and `To Do` (field) |
| **TECH-3** ISP theatre | ✅✅ strongest — **exactly zero** consumers typehint the narrow interfaces | ⚠️ **none of this work was ticketed** — PHPMD, with a silenced baseline, was its *only* reviewer |
| **TECH-4** CI/CD | ◐ partial — the rename is measurable (565 files, 9 commits, one shared subject); the CI sagas are journal-only. **✅✅ Corpus D settles the central thesis:** 49.7% failure across 979 runs, and failure **independent of commit size** (p = 0.66, ρ = −0.024) | ✅ a dedicated **`Core Bug`** status exists — 3 defects triaged to the platform |
| **TECH-5** money as a type | ✅ confirmed, and the consolidation **held** — 0 raw cents-math sites remain | ✅ BCMath deferral is a **live open ticket** (`STRP-160`); refactoring and black-box testing yielded **disjoint** defect sets |
| **SEC-1** async money boundary | ✅ fixes present and fail-closed; scores and burn-down not verifiable | ✅ security ran as a tracked workstream; ⚠️ `STRP-50` open since 2025-07 |
| **SEC-2** central validation | ✅ **7/7** guards confirmed by exact class name | ⚠️⚠️ **QA-driven, not developer-initiated** — the tester filed the payment-failure bug *and* wrote the requirements task that became Sprint 119 |

---

## 6. Novelty and where it goes

**In one line:** the contribution is **methodological, not thesis-driven**. The
"discipline over cleverness" thesis is the *least* novel element and cannot be
established at n=1; the value is that a project's self-account was audited
against two machine records and found to diverge in specific, directional ways.
[`06`](06-novelty-assessment.md) recommends retitling the flagship around the
audit and splitting out a negative-results paper.

- **Research venues** — MSR / EMSE / ICSE-SEIP for the reframed flagship and the
  negative-results paper. The engineering and security topics are
  practitioner-grade, not research-grade, and [`06`](06-novelty-assessment.md) §4
  says so plainly.
- **Practitioner venues** — [`07`](07-lessons-learned.md) routes all eight
  lessons: EuroSTAR / TestBash (LL-3, **submit first**), LeadDev (LL-6, LL-5),
  OWASP AppSec (LL-7), QCon / GOTO (LL-1), ACM Queue / IEEE Software (LL-2, LL-4),
  OXID Commons / IPC / phpCE (LL-8).
- **Three gates before anything ships externally**, two of which can stop
  publication outright: employer approval and material classification;
  **named-colleague consent** (LL-6 reports identifiable individuals' work
  patterns and must be anonymised by role); and **security disclosure** (LL-7
  describes real vulnerabilities in a shipped payment module). Detail in
  [`07`](07-lessons-learned.md).

---

## 7. How these were produced

**Corpus A** was mined by five parallel extraction passes — timeline/metrics,
incident forensics, architecture/tech, human–AI collaboration evidence, and
security — then synthesised. Citations are relative to
`docs/dev_logs/daniil_dev_log/` unless prefixed `architecture/`.

**Corpus B** was extracted from *all refs* of both repositories with
`git log --all --numstat`, capturing author and committer timestamps, per-path
diffs split by category (`src`/`tests`/`docs`/`ci`/`assets`/`other`),
`Co-Authored-By` trailers, and sprint/ticket identifiers. Work sessions are
maximal commit runs separated by ≤90 minutes; test-suite sizes are measured
**from the tree** at 15 checkpoints.

**Corpus C** was normalised from a 129-column Jira export and joined to B on
`STRP-\d+` references in commit subjects. Account ids, watcher lists and issue
description bodies are excluded; display names and summaries retained.

**Statistics** are computed by [`../data/stats.py`](../data/stats.py) — exact
Fisher, exact binomial, χ² with an incomplete-gamma tail, and a seeded percentile
bootstrap. It needs only `numpy`.

---

## 8. Data-quality caveats

Read these before quoting any number. Each corpus fails differently, which is
why all three are used.

**Corpus A — self-reported, and sampled.** 47 dated day-dirs across ~7 months,
with real HH:MM effort timestamps in **only three files**. Sprint numbering is
not globally monotonic; test counts are not comparable across the 2026-01-16
package split; "done" ≠ "committed" for much of the mid-2026 work. Written by the
party being studied — candid about failure, which strengthens it, but not an
independent audit. It is also the **only** corpus that records intent, and
therefore irreplaceable for design archaeology.

**Corpus B — a lower bound, twice over.** Sessions cannot see thinking, reading
or debugging that produces no commit, and 100 of 227 sessions are single-commit
and contribute zero duration. `files_changed` counts change *events*, not unique
files. Test-method counts (`function test*`) are **not** PHPUnit test counts,
which expand data providers — the two series must never be mixed. Two mechanisms
destroyed provenance during the study window: the **2026-07-02 mainline squash**
(562 files re-added; 491 commits survive only on `b-7.4.x-LEGACY`) and the
**deletion of merged feature branches** (one orphaned commit recovered from a
stale local checkout frozen at 2026-05-22, now a dangling object). **Neither is
detectable from inside the repository**, so all counts are lower bounds. And
`Co-Authored-By` trailers, on 149/716 commits, became routine only on
2026-05-07 — their absence is **not** evidence of absence of AI involvement.

**Corpus D — partial in both directions.** Runs join to a known commit for
**745/979 (76%)** — the rest point at `head_sha` on deleted branches and PR merge
refs — and only **444/716 commits (62%)** have any run, since CI was not
configured on every branch throughout. `duration_seconds` is **wall-clock
including queueing**, not billable compute. The 40 workflow *names* include
renames of one pipeline (one pair differs only by a typo in the source). A
`failure` conclusion means **friction, not necessarily a broken build** — flaky
E2E, cancelled infrastructure and expired credentials all land there. And the
export is a snapshot subject to GitHub's **run-retention window**, so older runs
are already unrecoverable: a third independent instance of the provenance
problem.

**Corpus C — the most restrictive.** **No effort data at all** (`Original
estimate`, `Time Spent`, `Work Ratio` and their `Σ` variants empty for all 156
issues). `Priority` is degenerate (145/156 = `SHOULD`) and carries no signal;
`Assignee` is 76% empty; `Resolution` is set on 39 issues while 82 are in status
category `Done`, so lead time exists for **n=39 only**, contaminated at the fast
end by 2023-era tasks that look bulk-closed. No status-transition history, and a
snapshot-only view taken 2026-08-20. **Terminology hazard:** the `Sprint` field
holds **two values**, so the journal's "Sprint 1 → 133" is a private convention
with no tracker counterpart — the two notions must never be equated.

**Two patterns from the verification passes**, worth stating once. First, the
journal is **highly reliable on mechanical facts** — several LOC and method counts
match the artifact to the exact line (330→107, −183 LOC, PHPMD 4→3, 25 methods).
Second, it is **systematically optimistic about simplification**: before/after
pairs quote the number that fell and omit the code added to replace it. And the
failures that cost the most time — the multi-iteration CI sagas — left the
*least* trace in the artifact, so the most expensive class of work is the least
verifiable.

Where the corpora disagree, the flagship paper reports both and says which it
trusts (§4.9, §4.11, §4.12, Appendix A).

---

## 9. Revision history

| Date | What changed |
|---|---|
| 2026-07-07 | Initial set: flagship draft + 10 topic proposals, mined from Corpus A alone. |
| 2026-08-20 | **Corpus B added.** Flagship rewritten against the commit record; three retractions; abstract rewritten as a concrete spoiler; §4.11 on incomplete simplifications. All 10 topics given Git verification blocks. `05` grown 10 → 17 entries. |
| 2026-08-20 | **Corpus C added.** Role separation found; flagship §4.12; `05` grown to 22 entries; all 10 topics given Jira verification blocks. Second provenance-loss mechanism recorded from a stale checkout. |
| 2026-08-20 | **`06` novelty assessment** added, then revised with statistics — two findings promoted (N-11, N-12), one downgraded to an observation (N-5). |
| 2026-08-20 | **`07` lessons learned** added: 8 practitioner topics, inference grading (Tiers S/D/U/N/X) backed by `data/stats.py`, day-one checklist, venue routing and publication gates. |
| 2026-08-24 | **Corpus E added** — mutation testing run against the live suite (M-30, flagship §4.14). All six literature searches completed; two of our claims withdrawn or demoted as a result (see §7 of `08`). |
| 2026-08-21 | **Corpus D added** — 979 GitHub Actions runs joined to commits. Flagship §3.4 and §4.13; `05` grown to 27 entries (M-23…M-27); TECH-4's central thesis tested and confirmed; LL-8 rewritten; **N-13** added to `06`; tests T9a–T9c added to `data/stats.py`. Headline: 49.7% CI failure rate, and failure **uncorrelated with commit size**. |
