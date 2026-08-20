# Technical Research Topics (5)

*Revised 2026-08-20 — each topic now carries a **Git verification** block.*

Extended abstracts. Grounded in `architecture/` (the 5 curated design docs + 7
PlantUML diagrams) and the `daniil_dev_log` corpus. Paths are relative to
`docs/dev_logs/daniil_dev_log/` unless prefixed `architecture/`.

**Git verification.** Named classes, method counts, and LOC deltas have been
checked against the trees and diffs of both repositories (dataset:
[`../data/`](../data/)). These abstracts fared **much better than the
project-management ones** — several figures match to the exact line. The one
recurring correction is a pattern the abstracts share: *refactors that reduced
per-unit size while increasing total volume are described only by their
shrinking half.*

---

## TECH-1 — Contract-First Checkout: A Domain State Machine Across a Redirect Boundary

**Thesis.** Modeling "Place Order" as the creation of a `PaymentContract`
aggregate (not an order), with early order creation and a `setState()`-free
state machine, is a principled answer to two hard problems in redirect-based
payments — *state restoration after the customer leaves for a hosted PSP page*
and *pre-payment reconciliation* — but it also *creates* a class of failure
(empty/orphaned orders) that must be engineered against.

**What the paper shows.**
- The lifecycle `DRAFT → NOT_FINISHED → PENDING → AUTHORIZED → READY_TO_COMMIT →
  COMMITTED → FULFILLED` (+ terminal `CANCELLED/EXPIRED/FAILED`), mutated only
  through named methods (`transitionToPending()`, `authorize()`,
  `captureAuthorization()`, `fulfill()`, `cancel($reason)`, …)
  (`architecture/01-architecture-layers.md`; `puml/02-contract-lifecycle.puml`).
- *Why* it exists: `$_REQUEST['sDeliveryAddressMD5']` "will ALWAYS be empty on
  return… we cannot rely on session" — the contract is the durable server-side
  snapshot keyed by a token in the return URL
  (`2025/20251202/done/sprint-1-order-creation-fix.md`); and STRP-74/75 create
  the order *early* in `NOT_FINISHED` so its number can go into PSP metadata
  (`2026/01/20260112/done/sprint-1-state-machine-update.md`).
- The **no-`setState()` invariant** and its motivating crash (STRP-89, refund
  handler called a nonexistent `setState('REFUNDED')`); enforcement in three
  layers (no generic setter; removed PHPStan suppression; hydration guard
  emitting `E_USER_WARNING` rather than throwing, to avoid a data-driven outage)
  (`2026/02/20260206/reports/02-refund-setstate-bug-analysis.md`;
  `sprint-68a-h5-state-machine-guard.md`).
- The **cost side**: early order creation × OXID `finalizeOrder`/`sess_challenge`
  produced empty committed orders (Order 192: three contracts in 36s, last
  committed at 0.00 EUR) — fixed by one-active-`NOT_FINISHED`-order-per-session
  + `sess_challenge` regeneration (`2026/03/20260302/reports/02-empty-orders-on-back-navigation.md`),
  and by *retaining* cancelled orders via native storno to preserve order-number
  sequences for accounting (STRP-123, `2026/04/20260415/done/sprint-88-keep-cancelled-orders.md`).
- A candid **documented-vs-observed gap**: live DB traces show `pending →
  committed` directly; `authorized`/`ready_to_commit` are compressed
  (`20260526/reports/webhook-processing-observations.md`).

**Method.** Design reconstruction from the architecture docs + PUML, validated
against the bug narrative; contrast intended vs observed state transitions.

**Contribution.** A reusable pattern (and its anti-patterns) for redirect-based
PSP integrations, with the honest failure modes most write-ups omit.

> ### Git verification (2026-08-20) — ✅ **invariant confirmed in the tree**
>
> The load-bearing design claim is that the state machine has **no generic
> setter**. Measured on `origin/b-7.4.x`:
>
> - **`function setState` occurs zero times** in `src/` of *either* repository.
>   The invariant is not merely documented, it is absent from the code — the
>   strongest form this claim can take.
> - All named transition methods exist and are in use: `transitionToPending`
>   (2 files), `authorize` (5), `captureAuthorization` (3), `fulfill` (6),
>   `cancel` (6), `expire` (4), `fail` (14).
>
> The STRP-89 crash — a refund handler calling the nonexistent
> `setState('REFUNDED')` — is therefore verifiable as *structurally impossible to
> reintroduce* in the current design, which is a stronger claim than "we fixed
> the bug."
>
> **Not measurable from git:** the live-DB observation that `authorized` /
> `ready_to_commit` are compressed in practice (`pending → committed` directly).
> That rests on runtime traces, not source, and remains the topic's most
> interesting unverified claim — it asserts the *implemented* machine is
> narrower than the *designed* one, which source inspection cannot settle.

---

## TECH-2 — Multi-Channel by Construction: An Event System with Provider Translators

**Thesis.** A thin-controller / fat-handler design over a PSR-14-style dispatcher,
plus a **translator** abstraction, lets one business-logic core serve storefront,
admin, webhook, REST, and MCP channels — and lets a *separate* returns module
trigger PSP refunds without importing a single provider symbol.

**What the paper shows.**
- Two-tier events: agnostic bases in `payment-base` vs concrete
  `Stripe*RequestEvent`s; handlers self-register via the **`payment.event_handler`**
  DI tag consumed as a Symfony `!tagged_iterator`
  (`architecture/02-event-system.md`; `puml/06-event-handler-registration.puml`).
- The **translator** (`oe.payment.event_translator`): `payment-base` emits
  neutral `RefundRequestedEvent`/`CancelAuthorizationRequestedEvent`; each PSP
  registers a translator mapping them to concrete events, so `opalreturns` drives
  Stripe refunds provider-agnostically (`20260506/reports/04,05-*.md`). The
  translator was refactored from an `instanceof` ladder to a data-driven
  `EVENT_MAP` lookup (OCP finding O10, `20260527/done/sprint-114.13-completion.md`).
- **Template-method** `ContractCreationHandler` (fixed algorithm, two provider
  hooks); the SRP "fat handler" refactor (2,330 handler LOC; the 389-line
  capture handler was "the worst offender") into services + immutable Result
  DTOs, with 2 of 6 planned refactors *skipped* as already-thin (no
  overengineering) (`2025/20251209/done/sprint-21-refactor-fat-handlers-report.md`).
- The webhook-handler registry (Sprint 114.4) replacing a 330-line
  `match($event->type)` with a tagged-iterator dispatch (107 lines), after
  discovering *two* disagreeing webhook mechanisms (O1/S1).

**Method.** Trace one checkout dispatch end-to-end through the priority chain
(`architecture/02-event-system.md`, `puml/03`); trace the cross-module refund
chain; quantify the SRP refactor deltas.

**Contribution.** A concrete recipe for multi-channel, multi-provider payment
orchestration with provider isolation enforced by DI, not discipline alone.

> ### Git verification (2026-08-20) — ✅ **confirmed, with one important revision**
>
> The mechanism is all present in the tree: the **`payment.event_handler` DI
> tag** (25 references across both repos), Symfony **`tagged_iterator`** (18
> references), the data-driven **`EVENT_MAP`** that replaced the `instanceof`
> ladder, and the **`oe.payment.event_translator`** (6 references, mostly in
> `payment-base` as the design requires).
>
> The webhook-registry claim is exact:
>
> | Claim | Measured |
> |---|---|
> | dispatch `match($event->type)` 330 → 107 lines | `StripeWebhookProcessor.php`: **330 → 107 lines** ✅ exact |
> | Sprint 114.4, tagged-iterator dispatch | commit `4a0c0b9`, 2026-05-27, "Sprint 114.4b: tagged webhook-handler registry" ✅ |
>
> **⚠️ Revision — "330 → 107" describes one file, not the module.** Commit
> `4a0c0b9` moved the dispatch logic into **8 new handler classes (+600 lines of
> production code)** with **9 test files (+856 lines)**. Module handler code went
> **2,616 → 2,953 LOC** at that commit, and stands at **3,147 LOC across 24
> files** today. The largest individual handler did shrink — the "worst offender"
> capture handler is now **305 lines**, down from the cited 389.
>
> The commit overall was near LOC-neutral (**26 files, +1,766/−1,701**), since it
> deleted the superseded handlers and tests as it added the new ones. So this is
> not a defect in the refactor — distributing a `match` into testable,
> OCP-compliant classes is the right move, and it is what made that epic's +196
> test methods possible. It is a **measurement** issue: a figure that reads as a
> 68% reduction corresponds to +337 lines of handler code at module level. The
> framing the paper should adopt: **these refactors reduced per-unit complexity
> while aggregate code held flat or grew.** A before/after pair quoting only the
> shrinking file overstates the simplification.

---

## TECH-3 — Interface Segregation Theatre: When an ISP "Split" Buys Nothing

**Thesis.** ISP is only real when *consumers* type-hint the narrow interfaces.
This project split a 26+-method Stripe adapter interface into sub-interfaces and
baselined the residue — then discovered years-later-style that the split was
*cosmetic* because no consumer used the narrow types. The most honest ISP paper
is about the fake split.

**What the paper shows.**
- The arc: build-up (agnostic `PaymentAdapterInterface`; a Stripe interface that
  grew to ~26–29 methods; proxies `LazyStripeAdapter`, `IdempotentStripeAdapter`);
  Sprint 46 ISP-splits **and baselines** the PHPMD `TooManyMethods` violations;
  Sprint 114.6 *deletes* `LazyStripeAdapter`; Sprint 132 finds the split fake.
- The verbatim self-correction: *"The adapter interface is already split, but the
  split is fake. No consumer typehints a narrow sub-interface… ISP without
  narrowed consumers buys nothing."* — and the identification of the *real*
  god-interface: `ModuleConfigurationServiceInterface` (25 methods, 21 consumers,
  most using 1–3) (`20260630/sprints/sprint-132-*.md`).
- `LazyStripeAdapter` **built then deleted**: it duplicated the factory's own
  laziness, wasn't Liskov-substitutable, and its caching was a *correctness bug*
  (stale client across operations), not an optimization; 183 LOC deleted, PHPMD
  baseline 4→3 (`20260527/done/sprint-114.6-remove-lazy-stripe-adapter.md`).
- The debt-formalization anti-pattern: inline `@SuppressWarnings` were "doubly
  useless" (PHPMD `--strict` ignores them; PHPStan choked parsing them) and were
  replaced by a baseline file — i.e. debt recorded, not fixed
  (`2026/02/20260206/done/sprint-46-completion-report.md`).
- The **PayPal contrast** (the design lesson inherited by the Mollie sibling
  module): PayPal splits its SDK behind four ≤4-method interfaces aliased to one
  `LazyPayPalAdapter` — the genuinely-segregated shape Stripe only reached
  cosmetically. A **framework constraint** (the factory/dispatcher resolve one
  object implementing the whole interface) blocks naive full segregation.

**Method.** Longitudinal design archaeology across Sprints 19/46/114.6/132;
consumer-usage census of the wide interfaces to demonstrate "fake" segregation.

**Contribution.** A field study of how ISP fails silently under a metrics gate,
and a criterion — *count consumers that use the narrow type* — for detecting it.

> ### Git verification (2026-08-20) — ✅✅ **the strongest-verified topic in the set**
>
> This abstract proposed a criterion — *count consumers that typehint the narrow
> type* — and predicted the answer would be zero. It is **exactly zero**.
>
> | Sub-interface | Total refs in `src/` | Actual consumers |
> |---|---|---|
> | `StripeCheckoutAdapterInterface` | 2 | **0** |
> | `StripeCustomerAdapterInterface` | 2 | **0** |
> | `StripePaymentIntentAdapterInterface` | 2 | **0** |
> | `StripeRefundAdapterInterface` | 2 | **0** |
>
> Every narrow interface is referenced exactly twice: its own definition file,
> and the composite `StripeAdapterInterface` that `extends` it. Meanwhile **4
> files typehint the wide composite**. The split is provably cosmetic — the
> assistant's own verdict (*"the split is fake… ISP without narrowed consumers
> buys nothing"*) is confirmed by measurement rather than accepted on authority.
>
> The source even carries its own archaeology: `StripeAdapterInterface`'s
> docblock reads *"Sprint 19: Route Stripe SDK calls through adapter. Sprint 46:
> ISP split into focused sub-interfaces."* The longitudinal design story the
> abstract proposes to reconstruct is annotated in the artifact.
>
> Three further figures match exactly:
>
> | Claim | Measured |
> |---|---|
> | `LazyStripeAdapter` deleted, **183 LOC** | `b23f3de` (2026-05-27, "Sprint 114.6"): **0 insertions / 183 deletions**, single file ✅ exact |
> | PHPMD baseline **4 → 3** | `tests/PhpMd/phpmd.baseline.xml`: **4 entries → 3** across that commit ✅ exact |
> | the *real* god-interface: `ModuleConfigurationServiceInterface`, **25 methods** | **25 public methods**; referenced by **25 files** ✅ exact |
>
> The consumer count for the god-interface (25 referencing files vs the abstract's
> "21 consumers") differs only because the raw count includes the interface and
> its implementation; the substantive claim — a 25-method interface with ~20+
> consumers most of which use 1–3 methods — stands.
>
> **Not measurable from git:** the PayPal contrast (a sibling module outside this
> corpus) and the claim that the framework's factory/dispatcher *blocks* full
> segregation. The latter is an architectural argument about OXID, testable only
> by attempting the refactor.

---

## TECH-4 — CI/CD in a Cross-Repo, Unified-Namespace, Framework-Coupled World

**Thesis.** The dominant source of hard, multi-iteration failure was not
application logic but the *build/integration environment*: cross-repo private
dependency auth, PHP-version skew, and the OXID unified-namespace generator's
interaction with the Composer install order. These are the failures that
actually cost days.

**What the paper shows.**
- **The unified-namespace break (Sprint 93):** both dependent repos died with
  `Class "OxidEsales\Eshop\Core\ConfigFile" not found in bootstrap.php:184` after
  a `composer.json` `type: composer-plugin → oxideshop-module` flip and the
  deletion of `MigrationPlugin.php`; the install pass interleaved with the
  namespace generator, wiping `generated/`. Documented across **five falsified CI
  iterations**; local never reproduced because `generated/` persisted from a
  pre-unification run (`20260505/reports/01,02-*.md`). Fix + three permanent TDD
  probes.
- **The rename epic (Sprint 102):** ~700 files across 4 modules; the namespace
  string appears in *four* byte-level backslash-escape forms each needing its
  own `sed`; a nested Playwright git repo missed by `git ls-files`; PHPStan
  baseline differs between local PHP 8.3 and CI 8.2; a DI-alias fix unmasked an
  OXID `LoginSecurity` UTC-vs-Berlin timezone bug — **4 of the day's 7 hours were
  this CI loop** (`20260508/done/sprint-102-completion-report.md`).
- **Recurring cross-repo auth pain** (#13/#47/#53 in the incident catalog):
  converged on `actions/checkout` + `path` repo + `ENTERPRISE_GITHUB_TOKEN`, and
  the lesson that a `|| secrets.GITHUB_TOKEN` fallback *masks* a missing token.
- **Local-vs-CI / local-vs-remote divergence** as the top flakiness-triage tool
  (e.g. 34 remote Playwright failures went green locally, isolating one genuine
  a11y bug).

**Method.** Reconstruct each multi-iteration CI saga as a falsification sequence
(hypothesis → CI result → next hypothesis); extract the environment-divergence
taxonomy and the permanent regression guards added.

**Contribution.** A hard-won field guide to CI for framework-coupled, cross-repo
PHP modules — the class of failure most under-documented and most expensive.

> ### Git verification (2026-08-20) — ◐ **partially confirmed; the sagas are journal-only**
>
> **The rename epic is measurable and consistent.** On 2026-05-08 the two
> repositories in this corpus touched **565 unique files** (163 in `stripe`, 402
> in `payment-base`) across **10 commits**, against the abstract's "~700 files
> across 4 modules" — the two modules not in the corpus plausibly supply the
> remainder. Sprint 102's identity is confirmed by the commit subjects
> (`STRP-135 PaymentComponent -> PaymentBase namespace refactoring`).
>
> **An unintended finding, relevant to PM-1.** All 10 of those commits carry the
> **identical subject line**. A day the journal describes as five distinct
> failure modes and a 4-hour CI loop is, in the artifact, ten
> indistinguishable commits. This is the clearest single illustration of the
> thesis that commit history was not being used as the record of increments —
> and it is why the CI-saga reconstruction the abstract proposes **cannot** be
> done from git alone.
>
> **`ci`-category churn corroborates the "environment, not logic" claim** in
> aggregate: 288 `ci`-path file-changes (+10,074/−1,894), with `ci:`-prefixed
> subjects recurring across the whole ten months, e.g. *"ci: fix composer
> resolution — payment-base alias and dev stability"* (2026-08-19) — the same
> cross-repo dependency-resolution problem still being fixed in the final week
> of the record. The abstract's claim that this is the *dominant* cost is
> supported directionally; git cannot price it in hours.
>
> **Not measurable from git:** the five falsified CI iterations, the
> last-green→red windows (those come from CI/server timestamps, not commits), the
> four backslash-escape forms, and the `generated/` interleaving mechanism. This
> topic remains the most journal-dependent of the five, which is worth stating
> plainly in the paper: **the failures that cost the most time left the least
> trace in the artifact.**

---

## TECH-5 — Money as a Type: Float Truncation, Minor-Unit Converters, and Per-Line VAT Reconciliation

**Thesis.** Representing money as IEEE-754 float on the shop side while PSPs
demand integer minor units is a latent, real-money hazard; the durable fix is to
push money behind currency-aware value types and to reconcile per-line VAT to the
charged total *exactly*.

**What the paper shows.**
- **Four real-money truncation bugs** surfaced *as a side effect* of DRY-ing
  duplicated cents math — `(int)(19.99 * 100) = 1998`, charging €19.98 instead of
  €19.99, on createPaymentIntent/authorize/capture/refund — none flagged by the
  preceding review (`20260527/reports/117-final-achievement-summary.md` §4).
- The gold-standard converter: `AmountConverter` uses `(int) round($major *
  $multiplier)` to defeat `19.99*100 = 1998.99…`; cents math collapsed **22 call
  sites → 1** (`117`).
- Currency-awareness: JPY/KRW/BHD bugs from a hardcoded `*100`
  (0-decimal and 3-decimal currencies); `MinorUnitConverter` made canonical and
  currency-aware (`20260622/*`).
- **Per-line VAT** (Sprint 125): ported `TaxableLine`/`VatBreakdown`/
  `PerLineVatCalculator` into `payment-base` because PSPs require per-line
  amounts that reconcile *exactly* to the total — grouped rounding can be off by
  1 cent and get the charge rejected; documented trade-off that per-line@2dp
  over-collects on sub-cent rates, so it ships opt-in default-OFF
  (`20260611/done/sprint-125-completion.md`).
- The deliberate **restraint**: "No BCMath anywhere" — float sites guarded by
  `round()` + a shared `HALF_CENT_EPSILON`; BCMath *deferred* until a concrete
  decimal defect appears (no overengineering) (`20260622/*`; Sprint 129
  extractions `LineItemAmount`/`Money`/`CapturableAmount`).

**Method.** Catalog every monetary defect and its fix; show the before/after
call-site consolidation; analyze the per-line-vs-grouped VAT reconciliation math.

**Contribution.** A concrete, PSP-agnostic pattern for monetary correctness in a
float-based legacy shop, and evidence that *DRY consolidation is an effective
bug-finding technique* for money code.

> ### Git verification (2026-08-20) — ✅ **confirmed; the consolidation is complete**
>
> Every named artifact exists where the abstract says it should, and the
> `payment-base` / `stripe` placement matches the architectural claim:
>
> | Artifact | Location measured |
> |---|---|
> | `AmountConverter` | `stripe` (19 referencing files) |
> | `MinorUnitConverter` | both (canonical in `payment-base`) |
> | `TaxableLine`, `VatBreakdown`, `PerLineVatCalculator` | **`payment-base` only** ✅ as claimed (ported for reuse) |
> | `LineItemAmount`, `HALF_CENT_EPSILON` | `payment-base` |
> | `CapturableAmount`, `AdminAmountValidator` | `stripe` |
>
> **The 22-call-sites-→-1 claim is confirmed, and its provenance is in the
> source.** `AmountConverter`'s own docblock reads: *"Sprint 114.7: centralises
> the ~22 hand-coded `* 100` / `/ 100` sites"* — and records the bug in the same
> comment: *"19.99 * 100 = 1998.9999… → (int) gives 1998 (WRONG); (int) round(19.99
> * 100) → 1999 (CORRECT)"*.
>
> More usefully, the consolidation **held**. A sweep of `src/*.php` on
> `origin/b-7.4.x` finds only 4 matches for raw `* 100` arithmetic: three are
> inside `AmountConverter`'s own explanatory comment, and one is an unrelated
> trust-score scale (`SecurityValidationResult`: *"100 = fully trusted"*).
> **Zero raw cents-math sites remain outside the converter** — the DRY claim is
> not just "we consolidated once" but "it stayed consolidated," which is the
> claim that actually matters and the one self-reports never substantiate.
>
> Note the docblock's own hedge — "~22" — meaning the abstract's precise "22 call
> sites" inherits an approximation from the source. Report it as ~22.
>
> **Not measurable from git:** that the four truncation bugs were *found as a
> side effect* of the DRY refactor rather than sought (the causal claim, and the
> topic's most interesting contribution), and that the preceding review missed
> them. Both rest on `117` §4. The *fix* is verifiable; the *serendipity* is not.

---

*Cross-cutting note.* Every topic above has strong "AI shaped this" evidence —
Claude-authored design docs and reviews, machine-style finding IDs (O1, S1–S7,
O10, A1/A2), R-1…R-10 gate scoring, and sprints where the assistant overturns its
own earlier architectural claim (TECH-3, Sprint 132). Any of these can be framed
either as a pure engineering paper or as an AI-assisted-engineering paper.
