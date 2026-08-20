# Security Research Topics (2)

*Revised 2026-08-20 — each topic now carries a **Git verification** block.*

Extended abstracts. Grounded in the AI-authored security audit, the remediation
sprints, the CI pentest suite, and `architecture/04-webhook-processing.md`.
Paths relative to `docs/dev_logs/daniil_dev_log/` unless prefixed `architecture/`.

**Git and Jira verification.** Named guards, sanitizers, and fail-closed fixes
have been checked against the current tree and commit history of both
repositories, and against the 156-issue Jira export (dataset:
[`../data/`](../data/)). Security claims verified **best of all four topic
files** — the fixes are structural and therefore visible in source. The limit is
inherent and worth stating up front: git can confirm that a control *exists*,
never that it is *sufficient*.

The Jira pass adds one finding that changes SEC-2's framing substantially: **the
validation subsystem was requirements-driven by the project's tester, not
designed on the developers' initiative.**

A meta-point for both topics: **security was run by the AI as a first-class
workstream** — a 28-finding formal audit mapped to PCI-DSS v4.0 / GDPR / BSI
TR-03116-4 / OWASP Top 10 / PSD2-SCA, remediated TDD-first, and later backed by
a CI-runnable black-box pentest harness. The audit even distinguishes findings
the AI *proposed* from those it later *self-corrected* to "already secure."

---

## SEC-1 — Defending the Asynchronous Money Boundary: Webhook Integrity, Idempotency, and Secret Handling

**Thesis.** In a redirect-based PSP integration the browser return is
attacker-controllable, so correctness and security both rest on the asynchronous
webhook. Making that boundary safe requires a *layered* design — signature
verification (fail-closed), a cheapest-first guard chain, atomic idempotency, PII
minimization, and disciplined secret handling — and the project's audit trail
shows each layer, including the ones it got wrong first.

**What the paper shows.**
- **Signature verification, fail-closed** via the Stripe SDK's mandatory
  `Webhook::constructEvent()` (`architecture/04-webhook-processing.md`), and the
  *related real gap* the AI later found: `isConfigured()` had the webhook-secret
  check **commented out** (`return !empty(getToken()) /* && !empty(getWebhookSecret()) */`),
  so the shop could accept payments it could not verify — fixed to fail-closed
  (finding S2, `2026/03/20260324/done/sprint-76-security-fixes-s1-s4.md`).
- **The guard chain** (Chain of Responsibility, ordered cheapest-first):
  `WebhookHttpsGuard` (O(1), returns **400 not 403** — "malformed transport",
  and Stripe retries non-2xx) → `WebhookPayloadSizeGuard` (>64KB, before JSON
  parse) → `WebhookRateLimitGuard` (APCu `apcu_inc`, 100/60s per IP) →
  `WebhookIpAllowlistGuard` (CIDR; **empty = disabled/fail-open**, because PSPs
  publish no stable ranges); failures return **empty body** to deny scanners a
  fingerprint (`2026/02/20260224/reports/sprint-64{a..d}-*.md`, `sprint-67b-*.md`).
- **Idempotency evolution** — a three-stage story: (1) the documented
  `oe_payments_idempotency` table was *dead code*, real dedup ran through
  `oe_payments_webhooklogs`; (2) Sprint 42 revived it (decorator, capture+refund
  only, contract-based keys, 24h TTL) as belt-and-suspenders on Stripe's native
  keys; (3) the audit found a **TOCTOU race** (check-then-insert with "no `SELECT
  FOR UPDATE`, no unique constraint" → two concurrent webhooks both pass → double
  fulfillment/capture, CVSS 7.0), fixed to an **atomic `claimEvent()`** that
  INSERTs and catches `UniqueConstraintViolationException`
  (`2026/02/20260205/reports/03-idempotency-analysis.md`;
  `sprint-42-idempotency-implementation.md`; `sprint-64g-atomic-idempotency.md`).
- **Secret & PII handling:** C1 (CVSS 7.5) — a `_debug` block leaked 12 chars of
  the *secret* key to the browser and logs, removed; S1 — a hardcoded fallback
  `TOKEN_SECRET` made fail-closed; L1 — API keys stored via OXID's ENCODE/DECODE
  ("not true encryption"), accepted-risk with env-var injection offered; H7
  (GDPR 5(1)(c)) — full payloads (email, address, card `last4`/`exp`) persisted
  to the audit table, fixed with a recursive `WebhookPayloadSanitizer`
  (`2026/02/20260219/reports/01-security-audit-strp99-no-mcp.md`;
  `sprint-63a-c1-api-key-exposure.md`; `sprint-69a-h7-webhook-pii-redaction.md`).
- **IDOR on the money path:** H3 — contract-return tokens (HMAC-SHA256) *existed
  and were tested* but `checkoutSuccess()` never called `validateToken()` (the
  "last mile was never wired in"), letting an attacker complete another user's
  payment; token validation is now the first check. H2 —
  `?capture_mode_override=` let any user flip the merchant's capture strategy,
  removed. M9 — the MD5 delivery-address hash was HMAC-bound with constant-time
  compare (`sprint-67-70-security-remediation-plan.md`; `sprint-67a`, `-63b`,
  `-68b`).
- **The AI self-correction sub-story** (H9/H10/M1/M4 downgraded to "already
  secure" on re-examination) and the **honest open items**: C3-replay carried as
  a candid skip, and the CI pentest found the rate-limiter did not engage in the
  test env ("real gap **or** env artifact… needs investigation")
  (`20260623/reports/01-ci-pentest-suite-and-header-hardening.md`).
- **PCI framing:** 3.4 PASS (no card data stored — Stripe tokenization); post-
  remediation "26/28 done, all HIGH blockers resolved," with L1–L4 and C3
  explicitly deferred.

**Method.** Reconstruct the threat model per layer; trace each finding from audit
→ TDD-first remediation → verification (incl. the live pentest run); analyze the
deliberate fail-open vs fail-closed choices and their justifications.

**Contribution.** A layered reference design for the async PSP boundary, notable
for documenting *what was wrong first* and *what is still open* — rare candor in
payment-security literature — and for a comparison against a legacy OXID 6.5
module whose failures (IDOR + session hijack, unauthenticated
`createWebhookEndpoint()`, session tokens in redirect URLs, DOM-XSS) the new
design structurally avoids
(`2026/03/20260324/security_check/security_issues_stripe.md`).

> ### Git verification (2026-08-20) — ✅ **fixes confirmed present and fail-closed**
>
> **Finding S2 — the commented-out webhook-secret check — is confirmed fixed in
> the artifact.** The abstract quotes the broken form
> `return !empty(getToken()) /* && !empty(getWebhookSecret()) */`. Current
> `src/Stripe/Service/ModuleConfigurationService.php` reads:
>
> ```php
> public function isConfigured(): bool
> {
>     return !empty($this->getToken()) && !empty($this->getWebhookSecret());
> }
> ```
>
> The check is live, not commented. This is the single most consequential fix in
> the topic — it is what stopped the shop accepting payments it could not
> verify — and it is now verifiable in three lines of source rather than
> asserted by the party that made it.
>
> All four guard classes and the layered chain exist by name:
> `WebhookHttpsGuard`, `WebhookPayloadSizeGuard`, `WebhookRateLimitGuard`,
> `WebhookIpAllowlistGuard`. The **atomic idempotency fix** is present too —
> `UniqueConstraintViolationException` is caught in
> `src/Repository/DoctrineWebhookLogRepository.php`, which is exactly the
> INSERT-and-catch shape the TOCTOU remediation prescribed (CVSS 7.0), and the
> `oe_payments_idempotency` table has 11 references in `payment-base`,
> confirming the once-dead table is now wired. `WebhookPayloadSanitizer`
> (the GDPR 5(1)(c) / H7 fix) exists in `payment-base`.
>
> **New finding — the work did not stop when the journal did.** Commit `aa7409e`
> (2026-08-19), *"Sprint 133 S13–S14 (F13, F14): mode-scoped webhook secret,
> required shop id"*, extends exactly this control **seven weeks after the
> journal's last entry**. The abstract's picture of webhook-secret handling as a
> closed story is out of date: the secret became *mode-scoped* (test vs live)
> later, which is a real hardening the journal never records. Any paper on this
> topic should extend its window to the git record's end.
>
> **What git cannot verify, and must not be claimed:** the CVSS scores, the
> 28-finding severity mix, the "26/28 done" burn-down, the AI self-corrections
> (H9/H10/M1/M4 downgraded to "already secure"), and the pentest result that the
> rate limiter did not engage in the test environment. Every one of those is
> AI-authored and self-scored. Presence of a control is measurable; adequacy of a
> control is not. The topic's candor — documenting what was wrong first and what
> is still open — remains its strongest feature and its least verifiable one.
>
> ### Jira verification — ✅ **the security workstream is externally corroborated**
>
> The topic's meta-point — that security ran as a **first-class workstream** —
> is confirmed by the tracker rather than only by the audit document:
>
> | Issue | Status | Commits | What it is |
> |---|---|---|---|
> | `STRP-64` | Done | 18 | "[Component] Security & Fraud Prevention" |
> | `STRP-99` | Done | 7 | "[Component][Stripe] Secutiry complience PCI, GDPR" — the audit's parent |
> | `STRP-108` | Done | 0 | "[SECURITY] Create an audit and fix findings" |
> | `STRP-102` | Done | 2 | "[Stripe] PEN/CSRF/brute force abuse test" |
> | `STRP-161` | Release Candidate | 1 | "PEN Test tests on pay1" (created 2026-06-22) |
> | `STRP-89` | Done | 2 | "[Component]Idempotency feature implementation" |
> | `STRP-86` | Passed QA | 3 | "[Stripe] API Keys chaos" |
> | `STRP-146` | Passed QA | 2 | "Hide API keys, add 'show key' icons" |
>
> Two specifics worth citing. `STRP-89` is the idempotency story the topic tells
> in three stages, and its Jira description **links directly to the dev-log file
> on GitHub** — the tracker and the journal cross-reference each other, which is
> useful provenance for any paper quoting both. `STRP-146` is the **L1 API-key
> handling finding** the topic records as "accepted-risk"; it was subsequently
> ticketed and delivered, so the accepted risk was later reduced — an update the
> journal's snapshot does not contain.
>
> **⚠️ One open security item predates the whole AI phase and is still open.**
> `STRP-50` "Fix Security Alerts StripeMiddleWare" (Story, created
> **2025-07-15** by Mario Lorenz, linking to the `stripe-middleware` repository's
> GitHub security page) has status **`To Do`**. It is outside the two modules
> this programme measures, but it belongs in the topic's "honest open items"
> section alongside C3-replay: the *middleware* component carried unresolved
> security alerts throughout the period in which the module was being hardened.
>
> **Still not verifiable from any corpus:** the 28 findings, their severity mix,
> the CVSS scores and the burn-down. Jira does not contain the audit's findings
> as issues — they lived only in the AI-authored report — so the audit remains
> **self-scored with no independent tracker record**, which is the single largest
> caveat on this topic.

---

## SEC-2 — One Hardened Endpoint: A Central Anti-Injection Validation Subsystem for Payment Input

**Thesis.** User input flowing to a PSP and to admin views is an injection
surface that a legacy shop guards with almost nothing (`trim()` + non-empty). A
*single, provider-aware* validation library behind *one* hardened endpoint — with
a character-class allowlist engine, a 7-guard request chain, and a
backend-is-source-of-truth rule — is a better answer than per-provider validators
or a client-side check.

**What the paper shows.**
- **The gap, precisely:** at checkout there was "exactly one rule — `trim()` +
  non-empty" via OXID's `RequiredFieldValidator`; "No format / regex / per-field
  allowlists anywhere on the Stripe boundary," and the module even *bypassed*
  OXID's `validateDeliveryAddress`
  (`20260529/reports/user-data-and-address-validation.md`).
- **The engine** (`ValidationBase` in `payment-base`, Sprint 119): a
  `CharacterClass` grammar with named tokens (`UNICODE_LETTERS = \p{L}`, `LETTERS
  = [A-Za-z]`, `NUMBERS = \p{N}`, `SPACES = U+0020 only, not \s`) plus a
  **universal blocklist applied first** (tabs, CR/LF, null, C0/C1 controls, DEL,
  zero-width/invisible code points) via one PCRE; per-field `allow`/`block`
  grammar in a per-plugin `src/Resources/validation-rules.php`; `RuleSet`,
  `FieldValidationResult` VO with typed codes
  (`20260529/sprints/sprint-119-strp-129-user-address-validation.md`).
- **One central endpoint** `index.php?cl=oepaymentvalidationapi&fnc=validate`
  (owned by `payment-base`, plugin id passed as a parameter) so "only one URL
  needs hardening," fronted by a **7-guard chain** (tagged iterator, first
  failure → 4xx + empty body): `PostOnly`(405) → `PayloadSize`(413, ≤4KiB/≤32
  fields) → `ActiveSession`(401) → `SameOrigin`(403, **no CORS ever**) →
  `CsrfToken`(403, reuses `Session::checkSessionChallenge`) → `RateLimit`(429,
  sliding window keyed by *(pluginModuleId, sessionId)* — **not IP**, so a
  botnet on one harvested session hits a single limit) → `PluginIdAllowlist`(422,
  must be an *activated* module).
- **The explicit threat model and the "what we do NOT do" list:** the endpoint
  reveals a validation routine (enabling flood/fingerprint/valid-char-oracle
  attacks); mitigations chosen and rejected are argued (no viewport-secret token
  — would leak in page source; no IP allowlist — unreliable behind proxies; no
  CORS; POST-only; no dev bypass) (`sprint-119` §4.7).
- **Backend is the source of truth (R-9):** *no JS port* of the engine; the OPC
  widget POSTs raw values and renders the JSON verdict, and deliberately **fails
  open** on HTTP error (releases submit with a `console.warn`) because standard
  checkout re-validates synchronously and the threat is "amplify writes"
  (rate-limited), not "skip validation" (`20260529/done/sprint-119-completion.md`).
- **DRY payoff and a real footgun fix:** extending validation to the admin
  capture-reason (Sprint 120) and admin amount (Sprint 121) needed *zero*
  `payment-base` changes ("adding the entry IS the feature toggle"); Sprint 121
  killed a silent full-capture bug where `parseAmount('12,30 EUR')` returned
  `null` (= full capture) — replaced by a fail-closed `AdminAmountValidator`
  comparing in minor units (`20260605/sprints/sprint-12{0,1}-*.md`).
- **A security-vs-usability self-audit:** six address fields used ASCII-only
  `LETTERS`, blocking `Müllerstraße` / Polish `ł`; the happy-path test had only
  put an umlaut on the `UNICODE_LETTERS` city field, so it "slipped through."
  Fix widened to `UNICODE_LETTERS` with a *documented accepted trade-off* (script
  widens to admit Cyrillic/Greek/CJK homoglyphs, but the universal blocklist and
  per-field `block` lists keep the *injection* surface unchanged) and a flagged
  NFC-normalization follow-up (`20260610/reports/validation-extended-latin-letters-review.md`).

**Method.** Reconstruct the design and its threat model; enumerate the guard
chain and character-class grammar; analyze the fail-open decision and the
security-vs-usability trade-offs; use the admin extensions as evidence of the
architecture's DRY leverage.

**Contribution.** A transferable pattern for centralized, provider-aware input
validation at a payment boundary, with an unusually explicit threat model and a
worked example of the allowlist-too-strict / test-too-narrow failure that
allowlist validation invites.

> ### Git verification (2026-08-20) — ✅ **7/7 guards confirmed by exact class name**
>
> The guard chain is the topic's central artifact and it is present in full, in
> `payment-base/src/Validation/Guard/`, in the order the abstract lists:
>
> | # | Guard claimed | Class measured | Status |
> |---|---|---|---|
> | 1 | `PostOnly` (405) | `PostOnlyGuard.php` | ✅ |
> | 2 | `PayloadSize` (413) | `PayloadSizeGuard.php` | ✅ |
> | 3 | `ActiveSession` (401) | `ActiveSessionGuard.php` | ✅ |
> | 4 | `SameOrigin` (403) | `SameOriginGuard.php` | ✅ |
> | 5 | `CsrfToken` (403) | `CsrfTokenGuard.php` | ✅ |
> | 6 | `RateLimit` (429) | `RateLimitGuard.php` | ✅ |
> | 7 | `PluginIdAllowlist` (422) | `PluginIdAllowlistGuard.php` | ✅ |
>
> Plus the chain's own scaffolding — `ValidationGuardInterface`, `GuardFailure`,
> `ValidationRequestContext` — and `OxidSessionChallengeVerifier`, which confirms
> the specific claim that CSRF protection *reuses OXID's
> `Session::checkSessionChallenge`* rather than rolling its own.
>
> The engine is confirmed and, more importantly, **so is its placement**, which
> is the architectural claim the topic actually rests on:
>
> - `ValidationBase`, `CharacterClass`, `RuleSet`, `FieldValidationResult` — all
>   in **`payment-base`** (the shared engine).
> - `validation-rules.php` — **1 file in `stripe`, 0 in `payment-base`**. Exactly
>   the per-plugin split the design requires: the grammar is shared, the rules
>   are the plugin's. This is what makes the abstract's "adding the entry IS the
>   feature toggle" claim structurally true rather than rhetorical.
> - `AdminAmountValidator` in `stripe` — the Sprint 121 fail-closed replacement
>   for the `parseAmount('12,30 EUR') → null → full capture` footgun.
> - `UNICODE_LETTERS` present (6 references), confirming the documented widening
>   away from ASCII-only `LETTERS` after the `Müllerstraße` / Polish `ł` failure.
>
> **What git cannot verify:** that the widening's accepted trade-off (admitting
> Cyrillic/Greek/CJK homoglyphs while holding the injection surface constant) is
> *sound*; that the fail-open-on-HTTP-error decision in the OPC widget is *safe*;
> and that the threat model's rejected mitigations were rejected for good
> reasons. These are the topic's genuine contributions and they are arguments,
> not artifacts. The NFC-normalization follow-up is likewise unverifiable as
> "flagged" — git shows no NFC normalization in the tree, which is consistent
> with the item still being open, but silence is not evidence.
>
> ### Jira verification — ⚠️⚠️ **the subsystem was QA-driven, not developer-initiated**
>
> This is the most consequential correction in the topic pass. The abstract
> presents the validation subsystem as a design initiative — a considered answer
> to a gap the developers identified ("exactly one rule: `trim()` + non-empty").
> The tracker shows the causal chain ran the other way, and it starts with the
> **tester**:
>
> | Date | Issue | Reporter | What |
> |---|---|---|---|
> | 2026-04-01 | `STRP-116` **Bug** | **Zerfas Razvan (QA)** | "Special characters in account details **block payment completion**" |
> | 2026-04-20 | `STRP-129` **Task** | **Zerfas Razvan (QA)** | "Define Allowed Special Characters for Account / Billing & Shipping Address Fields" — *"Review and enforce input validation rules… Current validation should be updated"* |
> | 2026-06-10 | `STRP-149` Story | Daniil Tkachev | "Validation - non-ascii latin symbols issue" — *"Allowd symbols from national alphabets, not only orthodox Latin"* |
>
> `STRP-129` **is** Sprint 119 — the dev-log file the abstract cites is named
> `sprint-119-strp-129-user-address-validation.md`. So the entire `ValidationBase`
> engine, the character-class grammar, the seven-guard chain and the central
> endpoint were built to satisfy **a requirements task written by the project's
> tester**, filed nineteen days after that tester found the absence of validation
> as a payment-blocking bug.
>
> Three consequences, and they improve the topic rather than damage it:
>
> 1. **The gap was found by black-box testing, not by design review.** The
>    abstract's "the gap, precisely" section reconstructs the missing validation
>    from source reading; in reality a tester hit it from the outside first. That
>    is a cleaner and more transferable finding: *a legacy shop's missing input
>    validation surfaces as a payment failure before it surfaces as a security
>    concern.*
> 2. **The allowlist-too-strict failure was also caught externally.** The abstract
>    reports the `Müllerstraße` / Polish `ł` problem as a **self-audit** that
>    caught a too-narrow happy-path test. Jira's ordering suggests the
>    over-strictness was in the field as `STRP-116` before the widening story
>    `STRP-149` existed. The honest version — *allowlist validation was tightened
>    on QA's instruction and then had to be loosened again after QA found it
>    blocking real customers* — is a better cautionary tale than a self-caught
>    slip, and it is exactly the failure mode allowlist validation invites.
> 3. **Related tester-filed defects confirm the surface.** `STRP-97` "Proper
>    Error Message Is Not Displayed for Invalid Delivery Address", `STRP-148` "A
>    validation message should be displayed when user attempts to proceed…" and
>    `STRP-104` "Maintenance Mode Activated When Attempting to Place an Order with
>    Invalid…" all describe the same boundary from outside.
>
> The DRY-payoff claim survives intact and is now better evidenced: `STRP-129`
> "Define Allowed Special Characters" (4 commits) and the admin extensions needed
> **zero `payment-base` changes**, which is what "adding the entry IS the feature
> toggle" means in practice.
>
> **Recommended reframing.** Retitle the thesis around the discovery path, not
> just the design: a centralized provider-aware validation subsystem is the right
> answer, *and* the requirement for it came from a tester filing a payment-failure
> bug — which is how input-validation debt actually gets discovered in a legacy
> shop. That reframing costs the topic nothing and makes it considerably harder to
> dismiss as a post-hoc architecture story.
