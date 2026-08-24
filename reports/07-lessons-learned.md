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
- **`[D]`** Actions-measured (979 workflow runs, 2025-10-21 → 2026-08-20)

Lessons carrying only `[A]` are **experience, not evidence** — they are worth
transmitting but should not be presented as findings. Lessons carrying `[B]` or
`[C]` are checkable, and the numbers are stated so a reader can disagree.

---

## LL-1 — Orchestrating a Stateless Agent: the dispatch is the only real boundary

**Audience:** engineers running coding agents on non-trivial codebases.
**Venue:** QCon / GOTO AI-assisted-development track; InfoQ as the written form.
**Highest practical value in the set.**

### The lessons

1. **The dispatch boundary is a hard constraint; the prompt is a soft one.** `[A]`
   When per-commit granularity mattered, the fix was never a better-worded
   prompt — it was *more dispatches*. Splitting the work is mechanical; asking
   nicely is advisory.
2. **A naming convention did not enforce granularity — only the dispatch does.**
   `[B]` This is the lesson the project believed it had learned and had not. The
   decimal sub-sprint scheme (114.0–114.13) was introduced explicitly to map one
   phase to one commit. Measured: **9 of 13 sub-sprints (69%) span more than one
   commit, median 5** — so the convention **failed on its own terms**. Note the
   limit precisely, because it is easy to overclaim here (and an earlier draft of
   this document did): whether the scheme was nonetheless *better than* ordinary
   sprint numbering is **untestable** with 13 groups against 6 (31% vs 33%,
   Fisher exact **p = 1.00**). The transferable lesson survives either way: if
   you want one commit per unit, the harness must produce it — do not assume a
   numbering scheme did.
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
**Venue:** ACM Queue or IEEE Software "Practitioner's Digest" — the cost/yield
argument is magazine-column shaped.

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
**Venue:** EuroSTAR, Agile Testing Days, or TestBash. The strongest
counter-intuitive material in the set, and **the one to submit first** — low
effort, no sensitive material, no approval dependency.

### The lessons

1. **Volume is real and measurable — and insufficient.** `[B]` The project wrote
   **1.69 lines of test code per line of production code** (+150,321 vs +88,896).
   That ratio is genuinely hard to fake. It is also **not evidence of
   verification** — and the effectiveness literature is blunter than we were:
   **suite size is a known confounder**, coverage does not track effectiveness
   (Inozemtseva & Holmes, ICSE 2014), and **assertions do** (Zhang & Mesbah,
   FSE 2015). Measured here: **2.28 and 2.33 assertions per test method** across
   the two packages — a better proxy than the ratio, and still not proof. **106
   `willReturnCallback` occurrences remain in the trees**, the exact construct
   that hid the hollow tests. If you want to know whether your agent-written
   suite verifies anything, **run mutation testing**; nothing cheaper answers it.
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
**Venue:** ACM Queue or IEEE Software as practitioner experience *now*; a research
short paper **only after** the designed comparison specified in
[`06-novelty-assessment.md`](06-novelty-assessment.md) §2.5 — the disjointness is
untestable as it stands.

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
**Venue:** split it — LeadDev for the management half, a PCI SSC Community Meeting
or OWASP AppSec for the compliance half, MSR for the provenance methods note.

### The lessons

1. **Do not squash release history.** `[B]` On 2026-07-02 the mainline was
   rewritten into one commit (562 files re-added). Eight months of provenance
   survive **only** because a `b-7.4.x-LEGACY` branch was retained (491 commits).
   **Stated precisely** (PCI DSS 6.4/6.5 requires an auditable change-control
   record with impact documentation, approval, testing and back-out procedures —
   it does *not* mandate that the record be the commit graph): **where your
   change-control evidence *is* your commit history, as it was here, squashing it
   destroys the artifact the audit depends on.** That is a conditional claim about
   practice, not a general claim that squashing breaches the standard.
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

**Audience:** anyone sizing a team around AI-assisted development.
**Venue:** LeadDev primary (its audience makes exactly this decision); EuroSTAR /
TestBash secondary; IEEE Software for the written version. The most important
write-up in this document, aimed squarely at the "solo dev + agent" narrative —
and **gated**: it reports named colleagues' work patterns, so it does not ship
without their agreement and role-level anonymisation (see *Before anything
ships*).

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

**Audience:** payment integrators.
**Venue:** OWASP AppSec (Global or EU); International PHP Conference or SymfonyCon
for the integrator audience; BSides for the war-story cut. **Gated** on security
disclosure — it describes real vulnerabilities in a shipped payment module.

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
**Venue:** OXID Commons, International PHP Conference, phpCE, or DevOpsDays —
niche, but these are the audiences living in the niche. Unblocked; good second
submission after LL-3.

### The lessons

1. **The dominant cost was build and integration, not application logic.** `[A]`+`[B]`+`[D]`
   The largest incident cluster was CI/infra and cross-repo dependency auth;
   `ci`-path churn totals **288 file-changes**, and the *same* cross-repo composer
   resolution problem is still being fixed on **2026-08-19**, the final week of
   the record. **Now measured:** of **979 workflow runs, 487 failed and 453
   succeeded — a 49.7% failure rate**, consuming **169.5 h of CI wall-clock**
   (more than the ≈140 h of measured human session time), **53% of it in failing
   runs**.
2. **Build failure did not scale with change size — so stop sizing commits to
   protect the build.** `[D]`+`[B]` Commits of ≥500 insertions had a failing run
   **63%** of the time; commits under 500, **60%**. Fisher **p = 0.66**, Spearman
   **ρ = −0.024** — no association at all. This is the clearest evidence for the
   whole topic: environmental failures are indifferent to how much code you
   changed, so the mitigation is fixing the environment, not trimming diffs.
3. **CI hardening appears to work — but we cannot prove it here.** `[D]` The
   failure rate fell from **57% to 46%** across 2026-04-01. That is a real
   descriptive change, and it coincides with the permanent regression probes and
   converged dependency auth. It is **not** statistically established: correcting
   for failure clustering (lesson 5 below) leaves **p = 0.18**. Report the
   direction, not a result.
4. **Failures come in runs, so treat build health as a state, not an event.**
   `[D]` **85.7% of failures are immediately preceded by another failure**
   (published benchmark: >50%), transitions occur on only **15.9%** of
   consecutive pairs against 49.9% expected, and lag-1 autocorrelation is
   **0.680**. A broken environment stays broken until someone fixes it — which is
   what an environmental account predicts and a defects-in-changed-code account
   does not. Practically: alert on the **transition** into failure, not on each
   red run, and measure **time-to-green**, not failure count.
5. **Watch the metric's honesty:** a red pipeline is *friction*, not proof of a
   broken build — cancelled runs, flaky E2E and expired credentials all land as
   `failure`. Measure it anyway; just do not call it defect density.
6. **And it leaves the least trace.** `[A]`+`[B]` The rename day (2026-05-08)
   touched **565 unique files across 9 commits** — all **9 sharing one
   identical subject line**. A day the journal describes as five distinct failure
   modes and a four-hour CI loop is, in the artifact, nine indistinguishable
   commits. The most expensive class of work is the least reconstructible.
7. **Local-vs-CI divergence is the first triage question.** `[A]` A unified-
   namespace break survived **five falsified CI iterations** because `generated/`
   persisted locally from a pre-unification run and local never reproduced it.
8. **A token fallback masks a missing token.** `[A]` `|| secrets.GITHUB_TOKEN`
   turns a clear auth failure into a confusing permissions error. Fail loudly.
9. **Watch for version skew between local and CI**, `[A]` e.g. a PHPStan baseline
   that differs between local PHP 8.3 and CI 8.2 — and for a mechanical rename
   needing four distinct byte-level escape forms of the same namespace string.
10. **Add a permanent probe for every environment bug you fix.** `[A]` Three TDD
   probes were added after the namespace break specifically to fail fast if it
   recurred.

---

## Which lessons the data can actually prove

The lessons above are graded by *source* (`[A]`/`[B]`/`[C]`). This section grades
them by **strength of inference** — the distinction that matters if any of this is
written up. Tests were computed from the CSVs in [`../data/`](../data/); the
script is reproducible from the column definitions in
[`../data/README.md`](../data/README.md).

### A note on what a p-value means here

These corpora are **censuses, not samples**: every commit and every issue in the
window is present. So a p-value cannot be read as "generalises to a population of
projects." It answers a narrower and still useful question: *could this pattern
have arisen from a chance arrangement of the labels we observe?* For T2 the null
is "reporter is independent of issue type"; for T4, "commit timing is independent
of weekday"; for T1, "months are exchangeable with respect to which category grew
faster." Each is a real null worth rejecting, and none of them licenses a claim
about AI-assisted development *in general* — that would need the second case this
programme does not have.

All tests are exact or standard, two-sided, and implemented without scipy
(exact Fisher via the hypergeometric, exact binomial, chi-square with an
incomplete-gamma tail, percentile bootstrap at 20,000 resamples).

### Tier S — statistically supported

| # | Lesson | Test | Statistic | p |
|---|---|---|---|---|
| **T1** | Test code outweighs production code (LL-3, LL-4) | sign test over months, + bootstrap CI on the ratio | **11/11 months** test+ > src+; pooled ratio **1.69**, 95% CI **[1.39, 2.06]**, ratio > 1 in **100%** of 20k resamples | **0.0010** |
| **T2** | The pair does not file bugs against itself (LL-6) | Fisher exact on developer×tester / Story×Bug; χ² on the full reporter table | 2×2 = **[[52,0],[0,37]]**; full table **χ² = 199.4**, df 6, **Cramér's V = 0.859** | **6.7e-26** / **2.6e-40** |
| **T3** | Trailer adoption is a step change, not a trend (LL-5) | Fisher exact, pre/post 2026-05-07 | **2/466 (0.4%)** before vs **147/250 (58.8%)** after | **5.2e-81** |
| **T4** | Weekend abstention is real (LL-8) | exact binomial vs uniform-over-7-days; χ² on Mon–Fri | **0/716** Saturdays → P = **1.2e-48**; weekdays **not** uniform (χ² = 22.8, df 4 — Wednesday heavy) | **1.2e-48** / **0.0001** |
| **T5** | Cadence is bursty, not steady (LL-1) | overdispersion vs Poisson | mean 5.01, variance 34.71 → **dispersion index 6.93** (Poisson expects 1.0), χ² = 984.4, df 142 | **4.7e-126** |
| **T6** | Issue→code coverage depends on issue type (LL-6) | χ² independence | Story **69%**, Bug **42%**, Task **8%**, Sub-task **0%**; χ² = 47.4, df 3 | **2.9e-10** |
| **T8** | Out-of-hours work is concentrated, not diffuse (LL-8) | exact binomial vs uniform over the 11 affected days | **13 of 29** out-of-hours commits on 2026-05-27 alone (45%) | **4.8e-07** |
| **T9a** | **CI failure is uncorrelated with commit size** (LL-8) — a *negative* result, and the topic's strongest evidence | Fisher exact on ≥500 vs <500 insertions; Spearman on the same | 63% vs 60%; **ρ = −0.024** | **0.66** ← *null, deliberately* |
| **T10** | **CI failures cluster heavily** (LL-8) | lag-1 autocorrelation; transition rate vs independence | **85.7%** of failures follow a failure (published benchmark >50%); **ρ₁ = 0.680**; transitions 15.9% vs 49.9% expected | *descriptive + benchmark* |
| ~~T9b~~ | ~~CI hardening measurably worked~~ | ~~Fisher, pre/post 2026-04-01~~ | **DEMOTED 2026-08-24**: nominal p = 0.0014, but deflated for T10's autocorrelation (n_eff ≈ 179 of 940) → **p = 0.18** | **not significant** |
| **T9c** | AI-trailered commits are no more CI-fragile (LL-2, LL-8) | Fisher exact | 59% vs 61% — heavily confounded, see M-26 | **0.88** ← *null* |

**On the demotion of T9b, and why it belongs in the record.** Running a published
claim against our data (">50% of failed builds follow a previous failure") to see
whether we corroborated it — we do, at 85.7% — revealed that our own run-level
tests had assumed independent runs. They are not independent: lag-1
autocorrelation is 0.680 and the effective sample size is roughly a fifth of the
nominal. That invalidated a coin-flip test we had reported for the failure rate
(withdrawn) and demoted the CI-improvement trend from p = 0.0014 to **p = 0.18**.
The trend remains a real descriptive change; it is no longer a tested claim. This
is the clearest instance in the programme of the thesis it argues for — that
checking your own numbers against an outside reference finds errors that internal
consistency checks do not.

**On the two deliberate nulls (T9a, T9c).** A p-value of 0.66 normally means
"we learned nothing." Here T9a is the opposite: the hypothesis under test is
*"bigger commits break CI"*, and its failure is the positive evidence for the
environmental account of this project's costs. Absence of a gradient where a
logic-failure model predicts a steep one is a real finding, and it is reported as
such rather than buried. T9c is a genuine null and is confounded (trailered
commits cluster in a period when the failure rate was already falling) — it
rebuts a common assumption without establishing its converse.

These ten are the lessons that can be stated as findings with a test behind
them. **T2 is the strongest result in the entire corpus** — a Cramér's V of 0.859
on a 4×3 table is a near-deterministic association, and it is the finding that
most changes how the case study should be read.

### Tier D — established descriptively, no inference needed

Complete-enumeration facts. These need no statistics because nothing is being
inferred: the population *is* the data. They are not weaker than Tier S, just
different in kind — and citing a p-value for them would be a category error.

| Claim | Value |
|---|---|
| Journal undersampled its own active days (LL-5) | 47 documented vs **105** with commits in-window (**2.2×**) |
| The cents-math consolidation held (LL-4) | **zero** raw `* 100` sites remain outside the converter |
| The no-`setState()` invariant is structural (LL-3) | `function setState` occurs **zero** times in either `src/` |
| CI failed on half of all runs (LL-8) | **487 failure / 453 success / 39 cancelled** of 979 |
| CI wall-clock exceeded human session time (LL-8) | **169.5 h** vs ≈140.1 h; **90.1 h (53%)** in failing runs |
| CI provenance is also lost (LL-5) | **234 of 979 runs (24%)** point at `head_sha` on no surviving ref; older runs past GitHub's retention window are gone |
| The ISP split is cosmetic (LL-1, LL-6) | **exactly zero** consumers typehint any of the 4 narrow sub-interfaces |
| No ticket references were fabricated (LL-2) | **0 of 61** across 436 ticket-bearing commits |
| Provenance was lost twice (LL-5) | 491 commits only on `LEGACY`; 1 commit reachable from **no** remote ref |
| Effort is unrecoverable (LL-5) | Jira time fields empty for **all 156** issues; journal clock-stamps **3** of 143 active days |
| Private "sprint" shadows the tracker (LL-5) | journal Sprint 1→133 vs Jira `Sprint` = **2 values** |
| Commit messages are not an index (LL-5) | **102** reused subjects; one 56×; **39%** carry no ticket |
| All 7 named validation guards exist (LL-7) | **7/7** by exact class name |
| Refactors were reported by their shrinking half (LL-4) | 330→107 in one file, while module handler code went **2,616→2,953** |

### Tier U — underpowered: the direction is visible, the test is not

**This is where my earlier drafts overreached, and the correction matters.**

`02-topics-project-management.md` described PM-1's premise as **refuted** on the
strength of a comparison. That comparison does not survive a test:

| | decimal sub-sprints | ordinary sprints |
|---|---|---|
| groups | 13 | 6 |
| exactly one commit | 4 (31%) | 2 (33%) |

**Fisher exact, two-sided: p = 1.0000.** With 13 groups against 6 there is no
power to detect a difference of any plausible size, so the data are **silent** on
whether decimal numbering helped — that is not the same as showing it did not.

What *is* established, and needs no inference, is the narrower claim: **9 of 13
decimal sub-sprints (69%) span more than one commit, median 5.** The convention's
stated purpose was one phase → one dispatch → one commit, and it demonstrably did
not achieve that. So the honest formulation is:

> The convention **failed on its own terms** (census fact). Whether it was
> nonetheless *better than nothing* is **untestable with this data** (p = 1.00).

Also underpowered or untestable: lead time (n = 39, and `Resolution` is set on 39
issues while 82 are `Done`-category, so the sample is not even well-defined);
and the LL-4 disjointness claim — 4 refactoring-found defects versus 6
tester-found defects with **zero overlap** is striking, but testing it requires
knowing the size of the underlying defect pool, which is unknowable. Report the
disjointness as an observation, not a result.

### Tier N — single-case verified

One instance, checked against the artifact. Not statistics; provenance. Strong
for *existence* claims ("this happened, precisely thus"), useless for frequency.

- The `bf32d77` instruction-violation incident matching the journal in **all five
  particulars**, including `status.md` at 0 changed lines (LL-2).
- The `STRP-138`/`STRP-139` misattribution, with the `strp-xxx` placeholder in the
  agent's own plan file (LL-1, LL-2).
- The flagship epic's self-report understating insertions by **~41%** (LL-2) — a
  single episode, so "agent arithmetic is unreliable in both directions" is
  supported by *two* instances (this and the "said 4, was 3" miscount), which is
  a pattern claim resting on n = 2.
- `isConfigured()` shipping with the webhook-secret check commented out (LL-7).

### Tier X — cannot be supported by any available data

Restating [§ "Lessons we cannot support"](#lessons-we-cannot-support) in
inferential terms: **every causal and comparative claim about the effect of AI
assistance is out of reach**, because there is no counterfactual arm, no control
project, one operator, and six model generations inside the window. No amount of
additional analysis of *these* corpora changes that. It needs a second case.

### What this means for writing it up

- Lead with **T2** (role separation) and **T1** (test-to-source). They are the two
  results with both a strong test and a genuinely counter-narrative message.
- **T3** is the most useful to other researchers and the cheapest to state.
- **T5** should replace every loose use of the word "velocity": the dispersion
  index of 6.93 is the precise way to say "the peak is not the rate."
- Move PM-1 from "refuted" to "failed on its own terms; comparison underpowered."
- Never attach a p-value to a Tier-D claim, and never state a Tier-N incident as
  a frequency.

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

## Where to publish each of these

[`06-novelty-assessment.md`](06-novelty-assessment.md) §5 routes the *research*
contributions (MSR / EMSE / ICSE-SEIP). This section routes the **practitioner**
material, which has a different and much larger set of homes — and a gating
problem the research route does not have (see "Before anything ships" below).

Conference names are the established annual events; **every CFP window and format
needs checking before you plan around it**, and nothing here should be read as a
current call.

### Recommended primary venue per topic

| Topic | Primary venue | Why it fits | Effort |
|---|---|---|---|
| **LL-1** stateless-agent orchestration | **QCon** or **GOTO** (AI-assisted-development track); **InfoQ** article as the written form | The hook is a *negative* result — a naming convention that measurably did not work — which these audiences reward over another "how we use agents" talk | Medium |
| **LL-2** trust but verify | **ACM Queue**, or **IEEE Software** "Practitioner's Digest" | A cost/yield argument with numbers is exactly the magazine-column shape; 1–2 min per claim against a documented catch rate | Medium |
| **LL-3** test volume ≠ verification | **EuroSTAR**, **Agile Testing Days**, or **TestBash** / Ministry of Testing | The strongest testing-community talk in the set: 1.69:1 test-to-source **and** hollow tests plus 34% silent skips *in the same project*. Counter-intuitive, and the audience is professionally invested | **Low — do this first** |
| **LL-4** refactoring as defect detection | **ACM Queue** or **IEEE Software** now; a research short paper only after a designed comparison | Publishable as practitioner experience immediately. As research it needs the controlled study 06 §6 specifies — the disjointness is untestable as it stands | Medium |
| **LL-5** repository as audit trail | Split it: **LeadDev** (the management half) and a **PCI SSC Community Meeting** or **OWASP AppSec** (the compliance half); MSR for the methods note | Two genuinely different audiences. Managers care about instrumenting from day one; compliance people care that a release procedure destroyed an audit trail on PCI-obligated software | Medium |
| **LL-6** the AI pair needs a tester | **LeadDev** primary; **EuroSTAR** / **TestBash** secondary; **IEEE Software** for the written version | The most important topic in the document and the best-evidenced (χ² = 199.4, Cramér's V = 0.859). LeadDev's audience sizes teams, which is exactly the decision this finding informs | High — **gated**, see below |
| **LL-7** money and the last mile | **OWASP AppSec** (Global or EU); **International PHP Conference** / **SymfonyCon** for the integrator audience; **BSides** for the war-story cut | "Existence of a control is not invocation of a control" — HMAC tokens that existed, were tested, and were never called — is a strong AppSec talk on its own | Medium — **gated** |
| **LL-8** environment costs more than logic | **OXID Commons**, **International PHP Conference**, **phpCE**, or **DevOpsDays** | Framework-coupled cross-repo CI is niche, and these are precisely the audiences living in that niche | Low |

### Secondary and opportunistic homes

- **OXID Commons** — the employer's own conference is the natural first home for
  anything module-specific (LL-7, LL-8, and TECH-1's redirect-boundary story).
  Lowest barrier, most directly useful audience, and the approval problem below
  largely evaporates for an internal-facing audience.
- **FOSDEM** PHP/e-commerce devrooms — short slots, good for a single lesson
  rather than a whole topic.
- **Local PHP user groups and BSides chapters** — the right place to rehearse
  LL-7 and LL-8 before a bigger CFP.
- **A single long-form engineering blog post** covering the day-one checklist is
  probably the highest-reach, lowest-effort artifact in this entire programme,
  and it needs no venue at all.

### Suggested sequence

1. **LL-3 to a testing conference.** Lowest effort, strongest counter-intuitive
   hook, no sensitive material, and no dependency on anyone's approval.
2. **LL-8 to OXID Commons / a PHP conference.** Also unblocked, and it rehearses
   the corpus in front of a friendly audience.
3. **The day-one checklist as a blog post.** Cheap, reusable, and it becomes the
   thing everything else links to.
4. **LL-6 to LeadDev — once gated items clear.** This is the one worth real
   effort, and the one that must not be rushed.
5. **LL-7 to OWASP AppSec** after security review (below).
6. **LL-2 / LL-4 / LL-5 as written pieces** on a slower track; magazine lead
   times are long and these lose nothing by waiting.

### Before anything ships: three gates

These are not formalities. Two of them can stop publication outright, and they
are the reason the venue table above marks LL-6 and LL-7 as *gated*.

**1. Employer approval and material classification.** Every corpus here is
internal OXID material: dev logs, an unremediated-at-the-time security audit,
Jira contents, and commit history from private repositories. Nothing external
ships without sign-off, and the security audit in particular (`STRP-99`,
`STRP-108`) should be assumed **not** publishable in detail.

**2. Named-colleague data — the hard one.** LL-6's central finding is a statement
about **identifiable individuals' work patterns**: one person filed 52 Stories and
zero Bugs; another filed 37 of 40 Bugs and zero Stories; a third filed 26 Tasks.
That is performance-adjacent data about named colleagues, derived from a tracker
they did not consent to have analysed. Publishing it externally without their
agreement would be wrong regardless of what the licence on the data says.

Required before LL-6 goes anywhere external:

- ask the tester and the project manager directly, showing them the actual
  numbers and the framing;
- **anonymise by role** ("the tester", "the project manager") in any external
  version — the finding is about *structure*, and loses nothing without names;
- offer them review of the draft, and co-authorship if they want it. 06 §6
  already lists their corroboration as the cheapest high-value addition to the
  research paper; asking permission and asking for corroboration are the same
  conversation.

The same applies, more sharply, to the **`bf32d77` instruction-violation
incident**, which is currently narrated with a commit hash attributable to a
named author. Externally it should be described as a process failure without the
hash, or dropped.

**3. Security disclosure.** LL-7 describes real vulnerabilities in a shipped
payment module: an IDOR on the money path (`validateToken()` never called), a
webhook-secret check shipped commented out, a TOCTOU idempotency race. All are
reported fixed and verified present in the current tree, but external
publication needs confirmation that **released versions** are patched, that
merchants have upgraded, and that nothing still-open is disclosed by
implication — note `STRP-50` (middleware security alerts) has been open since
2025-07-15. Follow OXID's disclosure process, not a conference deadline.

### What not to publish

- **The security audit's findings, scores, or burn-down** as security results.
  They are AI-authored and self-scored with no independent tracker record
  (LL-7 lesson 7). Present them as claims the project made about itself, or not
  at all.
- **Any "N× faster" framing.** Tier X above; there is no counterfactual.
- **Named-colleague statistics** externally, per gate 2.
- **Live commit hashes or ticket ids** in external material, unless the
  repositories are public by then — they are internal references and they date
  the material without adding anything a reader can use.

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
