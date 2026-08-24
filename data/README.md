# Measured dataset — git commits, Jira issues, GitHub Actions runs

Machine-extracted measurables for
[`../reports/01-flagship-paper-ai-assisted-payment-module.md`](../reports/01-flagship-paper-ai-assisted-payment-module.md).
Unlike the dev-log corpus (self-reported prose), every number here is derived
from machine records — **git commit metadata** (timestamps, authorship trailers,
`numstat` diffs), the **Jira issue export**, and the **GitHub Actions run
history** — and is reproducible from the two subject repositories plus the
export.

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

## Files — GitHub Actions

Exported **2026-08-21** via `gh api repos/{owner}/{repo}/actions/runs` (paged,
100 per page) for both repositories, then joined to the commit record on
`head_sha`. This is a **fourth corpus** (D), and the only one that records what
happened *to* each commit after it landed.

| File | Rows | Grain | Notes |
|---|---|---|---|
| `actions_runs.csv` | 979 | one workflow run | repo, run id/number/attempt, workflow name and path, event, conclusion, created-at, duration, branch, actor, `head_sha` — **joined to the commit**: date, author, files changed, insertions, deletions, `src_ins`, `tests_ins`, AI-trailer flag, subject |
| `actions_by_commit.csv` | 444 | one commit with ≥1 run | per-commit LOC (total, `src`, `tests`, `docs`, `ci`) beside run counts: total/success/failure/cancelled, `any_failure`, `all_success`, first and last conclusion, max attempt, total CI seconds, distinct workflows |
| `actions_workflows.csv` | 41 | repo × workflow | runs, success/failure/cancelled, failure-rate %, median and total duration, first/last run date |

**Headline:** 979 runs, **487 failure / 453 success / 39 cancelled — a 49.7%
failure rate**, spanning 2025-10-21 → 2026-08-20 across **40 distinct workflow
names**. Total CI wall-clock **169.5 h**, of which **90.1 h (53%) was spent in
runs that failed**.

### Actions-specific caveats

- **Coverage is partial.** Runs join to **745 of 979** rows (76%); the other 234
  point at `head_sha` values reachable from no ref in either repository —
  **deleted branches and PR merge refs**. Conversely only **444 of 716 commits
  (62%)** have any run, because CI was not configured on every branch for the
  whole period. Per-commit CI figures are therefore a **lower bound on activity,
  not a census of it**.
- **The unresolved 234 rows are further evidence of the survivorship problem**
  documented for Corpus B: CI ran against commits whose branches no longer exist.
- **`duration_seconds` is wall-clock, not billable compute.** It is
  `updated_at − run_started_at`, so it includes queueing and any time a run sat
  waiting on a runner. It is not job-minutes and must not be read as cost.
- **40 workflow names, many of them renames of the same pipeline** (e.g. "Stripe
  full tests OXID CE 7.4" vs "Stripe full tests onm OXID CE 7.4" — the typo is in
  the source). Do not treat distinct names as distinct pipelines without
  inspecting `workflow_path`.
- **`conclusion` is the final state of that attempt.** A commit can carry both a
  failure and a later success (re-runs, fixes on the same `head_sha`), which is
  why `actions_by_commit.csv` reports `first_conclusion` and `last_conclusion`
  separately from the counts.
- **The export is a snapshot** taken 2026-08-21. GitHub retains run history for a
  limited window by default, so **runs older than the retention period are
  already gone** — another provenance loss that is invisible from inside the
  repository.
- Actor logins are retained (they are the same handful of names as in the commit
  record); no tokens, secrets, logs, or job-level detail are exported.

## Files — mutation testing

Produced by an **Infection 0.31.9** run on **2026-08-24** inside the project's
Docker PHP 8.3 container, against the live unit suite (1,509 tests / 3,934
assertions, green).

| File | Rows | Grain | Notes |
|---|---|---|---|
| `mutation_escaped.csv` | 122 | one escaped mutant | source file, line, mutator name |

**Run configuration.** Source scope: `src/Stripe/EventSystem/Handler`,
`src/Stripe/Core`, `src/Stripe/Webhook`, `src/Stripe/Service`. Test scope:
`--testsuite=Unit`. Mutators: `@default` minus `CastInt`/`CastString` (the
project's own `infection.json5` choice). Result: **462 mutants, 340 killed, 122
escaped, Covered Code MSI 73%, mutation code coverage 100%**.

### Reproducing, and the environment caveat that matters

The suite **cannot be run against the developer shop as configured** — eight
modules are active locally and the `mollie → paypal` class-extension chain
aborts the bootstrap. CI activates only `oe_payment_base` and
`oe_payments_stripe_wallet`. To reproduce, match CI's module set:

```bash
docker compose exec php php bin/oe-console oe:module:deactivate oe_payments_mollie
# also: opalreturns, opalsubscription, oe_onepage_checkout, oe_payments_paypal
docker compose exec -w /var/www/extensions/stripe php \
  php -d memory_limit=3G vendor/bin/infection --threads=4 --no-progress
```

This is itself an instance of the local-vs-CI divergence documented in LL-8 —
the run was blocked until the environment matched CI. **The shop configuration
used for this run was snapshotted beforehand and restored bit-for-bit
afterwards** (verified by directory checksum); no module state was left changed.

### Caveats

- **Covered code only.** `--with-uncovered` aborts on shop-coupled classes
  (`ViewConfig` extends the OXID chain). So MSI is over code the unit tests
  already execute, **not** over the module.
- **`stripe` only**, four directories; `payment-base` was not mutated.
- **No equivalent-mutant triage.** Some of the 122 escapes are inevitably
  harmless; Infection says so itself and none were manually classified.
- **Unit suite only** — integration and E2E defences are not credited.

## Statistical tests

`stats.py` recomputes every test cited in
[`../reports/07-lessons-learned.md`](../reports/07-lessons-learned.md) ("Which
lessons the data can actually prove") from the CSVs above, including the
Actions tests (T9). Run it with
`python3 data/stats.py`; it needs only `numpy` (the bootstrap) — Fisher's exact
test, the exact binomial, and the chi-square tail are implemented directly, so
`scipy` is not required. It is seeded, so the bootstrap CI is reproducible.

**Read the p-values correctly.** These corpora are **censuses, not samples**:
every commit and every issue in the window is present. A p-value here rejects a
specific chance-arrangement null (e.g. "reporter is independent of issue type"),
and does **not** license generalisation to AI-assisted development at large —
that needs a second case.

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
- **Survivorship: the corpus is the history that survived, not the history that
  happened.** Comparing against a stale local checkout frozen at 2026-05-22
  (`/home/dtkachev/osc/strp-test-may-21/source/extensions`) surfaced **one commit
  reachable from no ref on the canonical remote**: `ce96dc86085b` (25 files,
  +1,710/−60, subject `test`), the tip of the since-deleted feature branch
  `b-7.4.x-webhook-STRP-144`. `b-7.4.x-fixing-ci` is also gone from the remote.
  The *work* survived — consolidated onto the mainline as `3a50c1c` (61 files,
  +5,431/−1,255, a further-developed version with a different tree) — so the
  orphan is **deliberately excluded** from these CSVs: counting both would
  double-count the same feature. Impact is 1 of 717 known commits (0.14%), which
  changes no aggregate materially. The methodological point stands regardless:
  two mechanisms (a mainline squash and routine branch pruning) removed
  provenance during the study window, neither is detectable from inside the
  repository, and we have no witness for losses before 2026-05-22. **Treat all
  counts as lower bounds.**
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

GitHub Actions:

```bash
gh api "repos/OXID-eSales/stripe-wallet/actions/runs?per_page=100&page=N"
gh api "repos/OXID-eSales/payment-base/actions/runs?per_page=100&page=N"
```
joined to the commit stream on `head_sha`.

Commits:

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
