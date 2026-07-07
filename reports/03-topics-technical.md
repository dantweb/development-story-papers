# Technical Research Topics (5)

Extended abstracts. Grounded in `architecture/` (the 5 curated design docs + 7
PlantUML diagrams) and the `daniil_dev_log` corpus. Paths are relative to
`docs/dev_logs/daniil_dev_log/` unless prefixed `architecture/`.

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

---

*Cross-cutting note.* Every topic above has strong "AI shaped this" evidence —
Claude-authored design docs and reviews, machine-style finding IDs (O1, S1–S7,
O10, A1/A2), R-1…R-10 gate scoring, and sprints where the assistant overturns its
own earlier architectural claim (TECH-3, Sprint 132). Any of these can be framed
either as a pure engineering paper or as an AI-assisted-engineering paper.
