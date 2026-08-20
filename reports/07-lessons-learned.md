# Lessons Learned — Eight Proposed Topics

*Written 2026-08-20 · practitioner-facing lessons from ten months of
AI-assisted development of a production payment module*

Where [`06-novelty-assessment.md`](06-novelty-assessment.md) asks *what is
scientifically new*, this document asks the other question: **what would we tell
the next team?** Each section is a **proposed topic** — a self-contained write-up
with its own audience and form — built from lessons the project actually paid for.

**Evidence grading**, consistent with [`05-measurements.md`](05-measurements.md):

- **`[A]`** journal-reported (self-reported prose; candid but not independent)
- **`[B]`** git-measured (716 commits, 2025-10-21 → 2026-08-20)
- **`[C]`** Jira-measured (156 issues, 2023-05-30 → 2026-06-22)

Lessons carrying only `[A]` are **experience, not evidence** — they are worth
transmitting but should not be presented as findings. Lessons carrying `[B]` or
`[C]` are checkable, and the numbers are stated so a reader can disagree.

---

## LL-1 — Orchestrating a Stateless Agent: the dispatch is the only real boundary

**Audience:** engineers running coding agents on non-trivial codebases.
**Form:** engineering blog post or internal playbook. **Highest practical value
in the set.**

### The lessons

1. **The dispatch boundary is a hard constraint; the prompt is a soft one.** `[A]`
   When per-commit granularity mattered, the fix was never a better-worded
   prompt — it was *more dispatches*. Splitting the work is mechanical; asking
   nicely is advisory.
2. **A naming convention does not enforce granularity — only the dispatch does.**
   `[B]` This is the lesson the project believed it had learned and had not. The
   decimal sub-sprint scheme (114.0–114.13) was introduced explicitly to map one
   phase to one commit. Measured: **median 5 commits per sub-sprint** (mean
   4.77), and only **31% mapped to exactly one commit — versus 33% for ordinary
   sprint numbering.** The convention was statistically indistinguishable from no
   convention. If you want one commit per unit, the harness must produce it; a
   numbering scheme will not.
3. **Restate the hard rules at the top of every dispatch.** `[A]` *"Agents work
   from the prompt, not from session history."* Scope rules were repeated as
   ABSOLUTE HARD RULES on each invocation rather than established once.
4. **Sequential, not parallel.** `[A]` Concurrent dispatches shared one Docker
   MySQL and one OXID cache and produced flakiness; git-worktree isolation was
   the wrong tool because the container mounts a fixed host path. Know which
   resource your agents contend for before parallelising them.
5. **Externally-defined boundaries are the ones worth measuring against.** `[B]`+`[C]`
   One commit (`bf32d77`) bundled two separate Jira bugs — `STRP-138` (button
   disabled) and `STRP-139` (T&C checkbox) — landing the second under the first's
   id, with a literal `strp-xxx` placeholder in the agent's own plan file.
   `STRP-139` appears in **no commit message anywhere**. A ticket exists
   independently of the agent's plan, which makes collapse against it unambiguous
   in a way phase-collapse never is.
6. **No artifact in this project was a reliable unit of work.** `[B]`+`[C]`
   Sub-sprints didn't map to commits; **39% of commits carry no ticket**; four
   umbrella issues absorbed most of the history (`STRP-145` alone: **64
   commits**); and the most architecturally consequential work had **no ticket at
   all**. Choose your unit deliberately and enforce it, or you will not be able
   to audit your own process later.

### What it cost to learn

Two documented granularity failures, one of which required three corpora and a
join to reconstruct.

---

## LL-2 — Trust but Verify: auditing what the agent says it did

**Audience:** anyone accepting agent-authored completion reports.
**Form:** engineering blog post; the cost/yield argument also suits a talk.

### The lessons

1. **Treat every agent report as a hypothesis, and check it with a grep.** `[A]`
   Cost recorded as 1–2 minutes per claim. Caught: an over-claimed "boundary
   sealed" (two SDK imports remained), a baseline miscount ("said 4, was 3"), and
   stale line numbers from an earlier review. *"Never trust a finding's line
   numbers more than a fresh grep."*
2. **Agent arithmetic errs in both directions — do not assume inflation.** `[B]`
   The flagship epic's own completion report **understated** its output: 61
   commits reported vs **64** measured, +11,204 insertions reported vs
   **+15,844** measured (**~41% low**). An auto-verifier cannot assume the
   agent's numbers are flattering, only that they are unreliable.
3. **The cheap check catches things expensive analysis takes days to find.** `[B]`+`[C]`
   A human wrote "unconfirmed ticket number" in seconds. Reconstructing *why* it
   was wrong took this study three corpora, a join, and a search of every issue
   summary. Verification is asymmetrically cheap at the moment of the claim.
4. **Fabrication and misattribution are different failure modes.** `[B]`+`[C]`
   Across **436 ticket-bearing commits**, **0 of 61** distinct ticket references
   were invented; exactly one was mislabelled. The common fear (hallucinated
   identifiers) did not materialise; the actual defect was conflation. Design
   checks for the failure you have, not the one you expect.
5. **A logged instruction violation is worth writing down precisely.** `[A]`+`[B]`
   The `bf32d77` incident — committed against an explicit "do not commit", typo
   in the subject, no `Co-Authored-By`, `status.md` committed at **0 changed
   lines** — matched the artifact in **all five particulars**. Precise incident
   notes remain checkable months later; vague ones do not.

---

## LL-3 — Test Volume Is Not Verification

**Audience:** teams whose agents write most of their tests.
**Form:** conference talk. The strongest counter-intuitive material available.

### The lessons

1. **Volume is real and measurable — and insufficient.** `[B]` The project wrote
   **1.69 lines of test code per line of production code** (+150,321 vs +88,896).
   That ratio is genuinely hard to fake. It is also **not evidence of
   verification**.
2. **The same project shipped tests that asserted nothing.** `[A]` Assertions
   hidden inside `willReturnCallback` effectively ran `assertTrue(true)`. A
   passing suite, a green gate, and no verification.
3. **Hard-gate silent skips to zero.** `[A]` The integration suite reported 157
   tests with **53 silently skipped (~34%)** when Stripe credentials were absent
   — a green CI concealing a third of the layer. Skips must fail the build, not
   decorate it.
4. **Ban re-implementing the method under test inside a test double.** `[A]`
   Codified as rule R-1.5 *after* the project had done it. A double that
   reproduces the logic tests the double.
5. **"If a test never went red, you didn't TDD it."** `[A]` Refactors guarded by
   characterization tests written first.
6. **Suppressions hide crashes, so never suppress — fix.** `[A]` PHPStan *caught*
   a call to the nonexistent `setState('REFUNDED')`; a `phpstan.neon` ignore
   silenced it, converting a static error into a latent money-path crash on every
   admin refund (STRP-89). The invariant is now structural: **`function setState`
   occurs zero times** in either module's `src/` `[B]`.

### The honest framing

Two facts, both true: this project's test discipline was real enough to show up
in the artifact, *and* it shipped hollow tests until later audits caught them.
Quality was a property of the loop, not of any commit.

---

## LL-4 — Refactoring as a Defect-Detection Channel

**Audience:** technical leads deciding where to spend review effort.
**Form:** research short paper (see N-5 in
[`06-novelty-assessment.md`](06-novelty-assessment.md)) or a deep-dive post.

### The lessons

1. **DRY consolidation finds bugs that review misses.** `[A]` Collapsing
   duplicated cents-math — a tidiness exercise, not a bug hunt — surfaced **four
   real-money truncation bugs** (`(int)(19.99*100) = 1998`, charging €19.98
   instead of €19.99) on createPaymentIntent / authorize / capture / refund.
   **None had been flagged by the preceding code review.**
2. **It is a *complementary* channel, not a substitute.** `[C]` The tester
   independently filed **six different** amount-related bugs (`STRP-103`, `137`,
   `150`, `125`, `131`, `152`). **The two sets do not overlap.** Refactoring found
   arithmetic defects; black-box testing found interface and state defects on the
   same subsystem.
3. **Consolidation only counts if it holds.** `[B]` `AmountConverter`'s own
   docblock records centralising *"the ~22 hand-coded `* 100` / `/ 100` sites"*,
   and a sweep of the current tree finds **zero raw cents-math sites remaining**
   outside it. "We consolidated once" is a weaker claim than "it stayed
   consolidated."
4. **Report refactors net, not by their shrinking half.** `[B]` The webhook
   dispatch genuinely went **330 → 107 lines** — while the same commit moved that
   logic into **8 new handler classes (+600 production lines, +856 test lines)**,
   taking module handler code from **2,616 → 2,953 LOC**. The commit overall was
   near-neutral (**+1,766/−1,701**). A good refactor, reported misleadingly. Every
   before/after pair in the corpus quotes only the number that fell.

---

## LL-5 — Your Repository Is the Audit Trail

**Audience:** engineering managers, and anyone in a regulated domain.
**Form:** internal policy note; the provenance material also suits an MSR methods
note.

### The lessons

1. **Do not squash release history.** `[B]` On 2026-07-02 the mainline was
   rewritten into one commit (562 files re-added). Eight months of provenance
   survive **only** because a `b-7.4.x-LEGACY` branch was retained (491 commits).
   For PCI-DSS-obligated software the commit trail is a compliance artifact, not a
   convenience.
2. **Branch pruning destroys provenance too, and nobody notices.** `[B]` A commit
   (`ce96dc86085b`, 25 files, +1,710/−60) survives on **no ref of the canonical
   remote** — found only by comparing against a stale local checkout. It is now a
   **dangling object, one `git gc` from permanent loss.** The code survived; the
   record of how it was built did not.
3. **Neither loss is visible from inside the repository.** `[B]` Both were found
   by accident. If you intend your history to be auditable, that property needs
   to be *tested*, not assumed.
4. **Commit messages are the index to everything else.** `[B]` **102 distinct
   subjects are reused** across multiple commits — `"STRP-78 Extract paymenmt
   component"` **56 times**, typo included; `"up"` ten times — **33 subjects
   contain spelling errors**, and **39% carry no ticket reference**. This is why
   LL-1's decomposition conventions cannot be audited from history.
5. **Message quality tracks branch role, not diligence.** `[B]` The orphaned
   feature-branch tip is titled `test`; the mainline commit that superseded it is
   properly titled. Casual WIP messages on feature branches are fine *if* the
   consolidating commit carries the real description — so decide which commits are
   the record and hold only those to standard.
6. **Adopt the AI co-authorship trailer on day one.** `[B]` `Co-Authored-By:
   Claude*` covers **149/716 commits (20.8%)** — **0% before 2026-05-07**, 86% by
   August. The consequence is permanent: **this project cannot prove its own
   AI-authorship story for its first seven months.** The convention costs nothing
   and is unrecoverable later.
7. **Instrument effort prospectively or lose it forever.** `[A]`+`[C]` Jira's
   `Original estimate`, `Time Spent` and `Work Ratio` are **empty for all 156
   issues**; the journal clock-stamps **3 days** out of 143 active ones. Effort is
   the single most-wanted number in this entire programme and it is
   **unrecoverable from any corpus**.
8. **Don't invent a private "sprint" numbering that shadows the tracker's.** `[C]`
   The journal runs Sprint 1 → 133; Jira's `Sprint` field holds **two values**.
   The two are unrelated concepts sharing a word — a terminology hazard that
   misleads every later reader, including the team.

---

## LL-6 — The AI Pair Still Needs an Independent Tester

**Audience:** anyone sizing a team around AI-assisted development. **Form:**
the most important write-up in this document — a talk or an article aimed
squarely at the "solo dev + agent" narrative.

### The lessons

1. **The pair does not find its own behavioural defects.** `[C]` The developer
   working with the assistant filed **52 Stories and zero Bugs**. A separate
   person filed **37 of the project's 40 Bugs (92.5%)** and zero Stories. A third
   filed **26 of 50 Tasks** and nothing else. Ten people appear as reporters.
2. **This function is invisible in the records people usually keep.** `[A]`+`[B]`
   It appears in **neither** the developer's journal (which is a developer's
   journal) **nor** git (which sees only committers). Any productivity story built
   from those two sources will silently omit it.
3. **Requirements can arrive *from* QA, and that is a healthy signal.** `[C]` The
   validation subsystem's causal chain: the tester filed a payment-blocking bug
   (`STRP-116`, 2026-04-01), then wrote the requirements task (`STRP-129`,
   2026-04-20) that became the implementation sprint — the dev-log file is
   literally named `sprint-119-strp-129-user-address-validation.md`. The
   engine, grammar, seven-guard chain and central endpoint were built to satisfy
   a task the tester authored.
4. **Give bugs a triage path out of your component.** `[C]` **6 of 40 bug reports
   (15%)** were reclassified — 3 `Not a bug`, 3 `Core Bug` (defects triaged to the
   platform, not the module). A dedicated "this is the framework's fault" status
   is worth having; it stops platform defects distorting your own quality metrics.
5. **Nobody asks for refactoring, so nobody reviews it.** `[C]` A search of all
   156 issues finds **no ticket** for the interface-segregation split, the proxy
   that was built and deleted, or the later discovery that the split was
   cosmetic. That work ran entirely inside the developer–assistant loop with a
   **silenced linter baseline as its only reviewer.** Either ticket architectural
   work or accept that a metrics gate is deciding your architecture.

### The claim to make, and the one to avoid

**Make:** the measured quality of an AI-assisted project may depend
substantially on human QA capacity that the productivity framing does not count.
**Avoid:** "QA explains the outcome" — this is n=1, roles are inferred from
reporting behaviour rather than job titles, and there is no work-log to size the
tester's effort.

---

## LL-7 — Money and the Last Mile: fail-closed or fail expensively

**Audience:** payment integrators. **Form:** practitioner article; the
individual defects also make good conference war stories.

### The lessons

1. **Existence of a control is not invocation of a control.** `[A]` HMAC-SHA256
   contract-return tokens **existed and were tested** — but `checkoutSuccess()`
   never called `validateToken()`. The "last mile was never wired in," letting an
   attacker complete another user's payment. Test the *call site*, not just the
   primitive.
2. **Fail closed on configuration, not just on input.** `[A]`+`[B]` `isConfigured()`
   shipped with the webhook-secret check **commented out**
   (`return !empty(getToken()) /* && !empty(getWebhookSecret()) */`), so the shop
   accepted payments it could not verify. Now live in the tree:
   `!empty($this->getToken()) && !empty($this->getWebhookSecret())`.
3. **Idempotency must be atomic — INSERT-and-catch, not check-then-insert.** `[A]`+`[B]`
   The audit found a TOCTOU race (no `SELECT FOR UPDATE`, no unique constraint →
   two concurrent webhooks both pass → double capture, CVSS 7.0), fixed to an
   atomic `claimEvent()` catching `UniqueConstraintViolationException`.
4. **Money needs a type, and the type needs the currency.** `[A]`+`[B]`
   `(int) round($major * $multiplier)`, never `(int)`; currency-aware minor units
   (a hardcoded `*100` breaks 0-decimal JPY/KRW and 3-decimal BHD); per-line VAT
   must reconcile *exactly* to the charged total, because grouped rounding can be
   1 cent off and get the charge rejected.
5. **Defer the heavyweight fix, but ticket the deferral.** `[A]`+`[C]` "No BCMath
   anywhere" was a deliberate choice — float sites guarded by `round()` and a
   shared `HALF_CENT_EPSILON`. The deferral is **written down as an open work
   item**: `STRP-160` *"add floating point BCMath or TBD to the PaymentBase for
   any math ops"*, still open at the end of the record. Restraint plus a ticket is
   engineering; restraint plus silence is an omission nobody will find.
6. **Allowlist validation invites the too-strict failure.** `[A]`+`[C]` ASCII-only
   `LETTERS` on six address fields blocked `Müllerstraße` and Polish `ł`; the
   happy-path test had put an umlaut only on the one Unicode field, so it slipped
   through — and the tester found it **as a payment-blocking bug**. Widening to
   `UNICODE_LETTERS` admits homoglyphs, so the universal blocklist (controls,
   zero-width, CR/LF, null) is what actually holds the injection surface.
7. **A self-scored security audit is not an assessment.** `[A]` The 28-finding
   audit, its CVSS scores and its burn-down are AI-authored and self-scored, with
   **no independent record in the tracker**. Report them as claims the project
   made about itself.

---

## LL-8 — The Environment Costs More Than the Logic

**Audience:** teams shipping framework-coupled modules across repositories.
**Form:** practitioner field guide.

### The lessons

1. **The dominant cost was build and integration, not application logic.** `[A]`+`[B]`
   The largest incident cluster was CI/infra and cross-repo dependency auth;
   `ci`-path churn totals **288 file-changes**, and the *same* cross-repo composer
   resolution problem is still being fixed on **2026-08-19**, the final week of
   the record.
2. **And it leaves the least trace.** `[A]`+`[B]` The rename day (2026-05-08)
   touched **565 unique files across 9 commits** — all **9 sharing one
   identical subject line**. A day the journal describes as five distinct failure
   modes and a four-hour CI loop is, in the artifact, nine indistinguishable
   commits. The most expensive class of work is the least reconstructible.
3. **Local-vs-CI divergence is the first triage question.** `[A]` A unified-
   namespace break survived **five falsified CI iterations** because `generated/`
   persisted locally from a pre-unification run and local never reproduced it.
4. **A token fallback masks a missing token.** `[A]` `|| secrets.GITHUB_TOKEN`
   turns a clear auth failure into a confusing permissions error. Fail loudly.
5. **Watch for version skew between local and CI**, `[A]` e.g. a PHPStan baseline
   that differs between local PHP 8.3 and CI 8.2 — and for a mechanical rename
   needing four distinct byte-level escape forms of the same namespace string.
6. **Add a permanent probe for every environment bug you fix.** `[A]` Three TDD
   probes were added after the namespace break specifically to fail fast if it
   recurred.

---

## What we would do on day one, next time

A checklist distilled from the above. Every item is cheap at the start and
expensive or impossible later.

| # | Do this from commit one | Because `[grade]` |
|---|---|---|
| 1 | Emit the AI co-authorship trailer | 7 months of authorship is otherwise unprovable `[B]` |
| 2 | Record effort somewhere — anywhere | unrecoverable from all three corpora `[A]``[C]` |
| 3 | Enforce one-unit-per-commit in the harness, not by convention | naming schemes measurably do not work `[B]` |
| 4 | Require a ticket reference per commit | 39% lacked one; history became unauditable `[B]` |
| 5 | Never squash release history; test that history is auditable | two silent provenance losses `[B]` |
| 6 | Fail the build on silently skipped tests | 34% of a suite was hidden behind a green light `[A]` |
| 7 | Ban new suppressions; fix or fail | a suppression hid a money-path crash `[A]` |
| 8 | Budget an independent tester | the pair filed **zero** bugs against itself `[C]` |
| 9 | Ticket architectural work | otherwise a silenced linter is your architecture reviewer `[C]` |
| 10 | Don't shadow tracker vocabulary with private numbering | "sprint" meant two unrelated things `[C]` |
| 11 | State refactor results net | every before/after pair overstated simplification `[B]` |
| 12 | Verify every agent claim with a grep | 1–2 minutes; errors ran in both directions `[A]``[B]` |

---

## Lessons we cannot support

Stated so nobody cites this document for them.

- **"AI made us N× faster."** No counterfactual, no control arm, one operator,
  and six model generations inside the study window. The velocity figures are
  descriptive only.
- **"Discipline caused the quality."** Plausible, unproven, and confounded by an
  undisclosed QA function (LL-6) and by the operator's own expertise.
- **"The process prevented defects."** The same process produced hollow tests, a
  crash-hiding suppression, and a mislabelled fix. It *also* caught them. Quality
  was a property of the loop.
- **"Sub-sprint decomposition improves commit hygiene."** Measured and
  **refuted** `[B]`.
- **"The security posture is good."** The audit is self-scored with no
  independent record `[C]`. Unknown, not good.
- **"The module is done."** At the end of the record: `STRP-160` (float math) open,
  `STRP-50` (middleware security alerts) open since 2025-07, MCP still `To Do`
  with 20 commits against it, and **only 39% of issues** having any code `[C]`.
