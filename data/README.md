# Measured dataset — git commit record + Jira issue record

Machine-extracted measurables for
[`../reports/01-flagship-paper-ai-assisted-payment-module.md`](../reports/01-flagship-paper-ai-assisted-payment-module.md).
Unlike the dev-log corpus (self-reported prose), every number here is derived
from machine records — **git commit metadata** (timestamps, authorship trailers,
`numstat` diffs) and the **Jira issue export** — and is reproducible from the two
subject repositories plus the export.

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

## Files — git

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

## Files — Jira

Source: `jira-stripe.csv`, a 156-issue / 129-column export of the **STRP**
project (OXID's Jira), covering **2023-05-30 → 2026-06-22**. This is a *third*
corpus, independent of both the dev log and git, and it is the only one that
records **who asked for the work**.

| File | Rows | Grain | Notes |
|---|---|---|---|
| `jira-stripe.csv` | 156 | one issue | the raw export, as received (129 columns, most empty) |
| `jira_issues.csv` | 156 | one issue | normalized + **joined to the commit record**: type, status, category, priority, urgency, reporter, assignee, created/resolved, lead time, commit count, first/last commit date, `has_code`, summary |
| `jira_roles.csv` | 10 | one reporter | reporter × issue-type matrix — the role-separation result |

### Jira-specific caveats — read before quoting

- **No time tracking whatsoever.** `Original estimate`, `Remaining Estimate`,
  `Time Spent`, `Work Ratio` and their `Σ` variants are **empty for all 156
  issues**. The estimate-vs-actual study the papers hoped for is *not*
  recoverable from this corpus either.
- **Priority is degenerate and carries no signal:** 145/156 issues are
  `SHOULD` (93%). `Urgency` is likewise `Medium` (107) or empty (49). Do not
  build severity analyses on these fields.
- **`Assignee` is 76% empty** (119/156). Assignment was not used as a workflow
  mechanism; `Reporter` is the informative actor field.
- **`Resolution` disagrees with `Status`.** Only 39 issues carry a `Resolution`,
  but 82 are in status category `Done`. Prefer `status_category`; treat
  `resolved` / `lead_time_days` as available for **n=39 only**.
- **Jira sprints are NOT the dev log's sprints.** The `Sprint` field holds just
  two values — `STRIPE Wallet` and `STRIPE All Tickets Sprint`. The journal's
  "Sprint 1 → 133" numbering is a **private convention with no counterpart in
  Jira**, so the two sprint notions must never be equated.
- **Lead time is contaminated at the fast end.** Several 0-day resolutions are
  2023-era `Task` issues that look bulk-closed, not delivered in a day.
- **The export is a snapshot** taken 2026-08-20 and reflects status *as of then*,
  not status at any earlier point; there is no status-transition history.
- Account IDs, watcher lists, and issue `Description` bodies are **excluded**
  from the derived CSVs; summaries are retained.

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

The Jira join keys on `STRP-\d+` occurrences in commit **subjects** (case
insensitive, de-duplicated per commit). All **61** distinct references found in
the commit record resolve to real issues in the export — there are **no
fabricated ticket numbers**.
