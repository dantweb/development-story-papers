# Measured dataset — git commit record

Machine-extracted measurables for
[`../reports/01-flagship-paper-ai-assisted-payment-module.md`](../reports/01-flagship-paper-ai-assisted-payment-module.md).
Unlike the dev-log corpus (self-reported prose), every number here is derived
from **git commit metadata** — timestamps, authorship trailers, and `numstat`
diffs — and is reproducible from the two subject repositories.

## Provenance

| Repo | GitHub | Commits | First | Last |
|---|---|---|---|---|
| `stripe` | `OXID-eSales/stripe-wallet` | 586 | 2025-10-21 | 2026-08-20 |
| `payment-base` | `OXID-eSales/payment-base` | 130 | 2026-01-13 | 2026-08-20 |
| **Total** | | **716** | **2025-10-21** | **2026-08-20** |

Extracted `2026-08-20` from all refs (`git log --all`), so commits on feature
and legacy branches are included, not just the mainline. Timestamps are **author
dates in the committer's local timezone** — this is what makes hour-of-day and
session analysis meaningful.

## Files

| File | Rows | Grain | Notes |
|---|---|---|---|
| `commits.csv` | 716 | one commit | sha, author/committer ISO dates, local hour, weekday, author, merge flag, files, ins/del, AI-trailer flag + model, sprint/ticket refs, subject |
| `commit_loc_by_category.csv` | 716 | one commit | same commits with insertions/deletions/files split by path category: `src`, `tests`, `docs`, `ci`, `assets`, `other` |
| `daily_activity.csv` | 194 | repo × day | commits, files, LOC, AI commits, first/last commit clock time, span |
| `sessions.csv` | 227 | work session | contiguous commit runs, **new session after a >90 min gap**; duration, commits/hour, LOC, repos and authors involved |
| `test_trajectory.csv` | 27 | repo × checkpoint | test methods, test files, src files, src PHP LOC measured **from the tree** at 15 month-end/event checkpoints |
| `author_contribution.csv` | 7 | author | commits, LOC, AI-trailer share, active range |
| `model_generations.csv` | 6 | model | commits and LOC per `Co-Authored-By` model string |
| `hour_histogram.csv` | 24 | hour | commits by local hour of day |

## Definitions and caveats

- **Session** — commits separated by ≤90 min. A proxy for active working time,
  not billed effort: it cannot see thinking or reading between commits, and it
  bounds a session at its last commit. 100 of 227 sessions are single-commit and
  therefore have duration 0; aggregate hours come from the 127 multi-commit
  sessions. Treat session hours as a **lower bound**.
- **`files_changed`** counts file-change *events*, so a file edited in three
  commits counts three times. Unique-file counts are computed separately and
  labelled as such in the paper.
- **Test methods** are `function test*` occurrences under `tests/`. This is
  *not* the same as PHPUnit's reported test count, which expands data
  providers — so these numbers are systematically lower than the counts quoted
  in the dev log, and the two series must not be mixed.
- **The 2026-07-02 squash.** `stripe-wallet`'s mainline was rewritten that day
  (`6e828a242d6b`, "squashed history"): 562 files re-added as new, inflating
  insertions by src +18,417 / tests +44,534 / docs +19,803. It is flagged and
  excluded from LOC aggregates. Pre-July mainline history survives only on
  `origin/b-7.4.x-LEGACY` (491 commits), which is where the early
  `test_trajectory.csv` checkpoints are measured.
- **`docs/` dominates churn** (+605,801 / −194,375 across 4,005 file-changes)
  because the dev log itself lives in the repo. Code-only claims use the
  `src`/`tests` columns.
- **AI-trailer coverage is partial.** `Co-Authored-By: Claude*` appears on 149
  of 716 commits (20.8%), but the convention was only adopted routinely from
  2026-05-07 (two isolated uses on 2025-12-05). Absence of a trailer before
  May 2026 is **not** evidence of absence of AI involvement, so the trailer flag
  measures *attribution practice*, not authorship.
- **Author emails are deliberately excluded** from these CSVs; only display
  names are retained.

## Reproducing

```bash
git -C <repo> fetch --all --tags --prune
git -C <repo> log --all --date-order --numstat \
  --format='@@@C@@@%n%H%n%aI%n%cI%n%an%n%P%n%s%n@@@B@@@%n%B%n@@@E@@@'
```
Session grouping, category split, and trailer parsing are plain aggregations
over that stream; test trajectories use `git grep -hoE 'function test[A-Za-z0-9_]*' <rev> -- tests/`.
