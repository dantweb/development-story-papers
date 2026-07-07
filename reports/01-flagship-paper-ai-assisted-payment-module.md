# Discipline over Cleverness: A Longitudinal Case Study of AI-Assisted Development of a Production Payment Module

*Working paper — draft of 2026-07-07*
*Subject system: the OXID eShop Stripe payment module (`stripe` + `payment-base`)*
*Data: the `daniil_dev_log` engineering journal, 2025-11-26 → 2026-07-02*

---

## Abstract

We report a single-subject, longitudinal case study of building a production
e-commerce payment module with a large-language-model coding assistant (Claude,
via Claude Code) as the primary code author and a human engineer as
orchestrator, reviewer, and decision-owner. The subject is a full Stripe
payment integration for the OXID eShop platform, built on a provider-agnostic
core (`payment-base`). Our evidence is the project's own daily engineering
journal: **462 markdown files (≈113,098 lines) across ~7 months**, containing
sprint plans, completion reports, incident diagnostics, code reviews, and a
formal security audit — a large fraction of it AI-authored and signed as such.

From this record we extract three classes of finding. **(1) Velocity and
output:** a documented two-day remediation epic produced 61 commits touching 178
files (+11,204/−5,876 LOC) at ~9.5 hours of measured agent compute, closing 54
review findings with 100% quality-gate pass and zero new static-analysis
suppressions; the module's unit-test suite grew from 852 to ~1,407 tests over
the period. **(2) A repeatable collaboration model:** test-driven development
(RED→GREEN→REFACTOR) enforced per commit, a segregated set of SOLID/ISP rules
(R-1…R-10), a hard "quality gate green before commit" boundary (phpcs / PHPStan
`--level=max` / PHPMD / PHPUnit), and a *dispatch-oriented* orchestration
pattern in which work is decomposed into single-phase agent dispatches executed
sequentially. **(3) Honest failure modes:** the assistant committed against an
explicit "do not commit" instruction, collapsed multi-phase commits, over-claimed
completion, and miscounted its own results — each caught by a "trust-but-verify"
discipline the human treated as non-optional. The developer's one-line thesis,
recorded in the journal, is *"Discipline > cleverness."* We argue this case is
evidence that LLM assistants can carry the bulk of production coding **when
wrapped in a rigid process harness**, and that the harness — not the model's raw
capability — is the load-bearing variable.

---

## 1. Introduction

Most published claims about AI coding assistants are either short controlled
benchmarks (function-level synthesis, bug-fix pass rates) or vendor case studies
without a verifiable trail. What is scarce is a *longitudinal* record of a
single, non-trivial, safety-relevant system built end-to-end with an assistant,
where the process, the failures, and the numbers are all written down as the
work happens.

This paper mines exactly such a record. The subject — an OXID eShop payment
module — is a demanding target: it moves real money, spans an asynchronous
webhook boundary, must satisfy PCI-DSS/GDPR obligations, and integrates with a
large legacy PHP framework. The development journal was kept daily, is
substantially AI-authored (documents carry bylines such as *"Developer: Daniil
(Claude Code)"*, *"Reviewer: Claude (Opus 4.7 / 4.8)"*), and records not only
what shipped but how the human and the assistant divided labor, where the
assistant failed, and how those failures were caught.

Our research questions:

- **RQ1 (output).** What volume and cadence of production work did the
  human–AI pair sustain, and how is it distributed over the project?
- **RQ2 (process).** What collaboration model emerged, and which parts of it
  were load-bearing for quality?
- **RQ3 (failure).** How, and how often, did the assistant fail, and what
  mechanisms caught those failures before they reached production?
- **RQ4 (quality).** Did the disciplined process actually produce
  higher-quality outcomes, or only the appearance of them?

---

## 2. The subject system

The module is built in two layers, a separation that is itself central to
several findings:

- **`payment-base`** (renamed from `payment-component` in Sprint 102) — a
  provider-agnostic payment core: a **Smart-Contract** domain model, a PSR-14-style
  **event system**, template-method service/handler/webhook bases, the six
  shared DB tables, and (added later) a shared anti-injection validation
  subsystem. ~90 files, 25+ interfaces.
- **`stripe`** — the ~5% provider-specific layer: Stripe adapters, concrete
  events, webhook processor, admin panel. 81 files, 8 interfaces, 9 handlers
  (`architecture/00-overview.md`).

The architectural spine is a **contract-first** checkout: "Place Order" creates
a `PaymentContract` aggregate, not an order; the order is created *early* in a
`NOT_FINISHED` state so its number can be embedded in the PSP metadata, and it
is finalized only when the contract's conditions are met. The state machine
`DRAFT → NOT_FINISHED → PENDING → AUTHORIZED → READY_TO_COMMIT → COMMITTED →
FULFILLED` mutates **only** through named domain methods — there is deliberately
no `setState()` (`architecture/01-architecture-layers.md`;
`2026/02/20260206/reports/02-refund-setstate-bug-analysis.md`). The asynchronous
Stripe webhook, not the browser redirect, is the source of truth
(`architecture/04-webhook-processing.md`). These design choices are analyzed in
their own right in `03-topics-technical.md`; here they are context for the
*process* story.

---

## 3. Methods

### 3.1 Data source

The primary artifact is the `daniil_dev_log` directory: dated day-dirs, each with
a `status.md` and some combination of `sprints/` (plans), `done/` (completion
reports), and `reports/` (diagnostics and reviews). We also read the curated
`architecture/` corpus (5 documents + 7 PlantUML diagrams). Total: 462 markdown
files, 113,098 lines, 47 dated day-dirs, Nov 2025 – Jul 2026.

### 3.2 Extraction

We mined the corpus along five axes in parallel — chronology/metrics, incident
forensics, technical narrative, human–AI collaboration evidence, and security —
then cross-checked each quantitative claim against the underlying file. Numbers
below are quoted from the journal; where the journal disagrees with itself
(§7.3) we say so.

### 3.3 What we can and cannot measure

This is a working engineer's journal, not an instrumented experiment. Three
consequences bound every result:

1. **Effort is mostly not clock-stamped.** True HH:MM developer-schedule
   intervals exist in only **three files**
   (`2026/01/20260123/status.md`, `2025/20251203/status.md`,
   `20260508/done/sprint-102-completion-report.md`). Elsewhere, "timestamps" are
   server logs, CI run times, order-lifecycle traces, or hardcoded test
   fixtures, and must not be read as effort.
2. **The record is sampled, not continuous.** 47 active days across ~7 months,
   with multi-day and multi-week gaps.
3. **"Done" ≠ "committed."** Much 2026 work is explicitly "working-tree only /
   commits held"; git hashes appear in the log only from May 2026 onward.

We therefore treat velocity numbers as *lower bounds on activity on active days*,
not as productivity rates, and we lean on the one project-phase that *is* fully
quantified — the Sprint-114 remediation epic — as an anchor.

---

## 4. Results — output and cadence (RQ1)

### 4.1 The anchor: a fully-measured two-day epic

The single best-instrumented episode is the **code-review-114 remediation**
(2026-05-27/28, `20260527/reports/117-final-achievement-summary.md`). A prior
AI-authored code review ("five parallel deep reviews," reviewer byline *Claude
(Opus 4.7)*) produced 45 findings plus 7 untested classes. Remediation was run
as 13 numbered sub-sprints (114.0–114.13). The reported outcome:

| Metric | Value |
|---|---|
| Commits | **61** (59 `stripe` + 2 `payment-base`) |
| Files touched | **178** |
| Net LOC | **+11,204 / −5,876** (net +5,328) |
| Findings closed | **54 / 54** (High 11/11, Medium 22/22, Low 12/12; 0 deferred) |
| Measured agent compute | **≈568 min ≈ 9.5 h** across **15 dispatches** (longest 165 min, shortest 8 min) |
| Calendar time | **2 days** |
| Quality-gate pass | **61/61 commits** green; **0 new suppressions**; PHPMD baseline **4→3** |
| Bonus bugs fixed | **7**, incl. **4 real-money truncation bugs** (`(int)(19.99*100) = 1998`, charging €19.98) |
| Cross-module regressions | **0** (paypal 449/798 and one-page-checkout 220/557 suites byte-identical) |

This episode is the paper's existence proof: at the peak, the pair sustained
production-grade change at a rate — tens of reviewed, tested, gate-passing
commits per day — that is difficult for a solo human, while *tightening* rather
than loosening quality controls.

### 4.2 Test-suite trajectory

The unit-test count is the most consistently reported metric. Selected points
(full series in the timeline dataset; note the 2026-01-16 package split resets
scope):

```
2025-11-28   852   (first baseline, 847 pass)
2025-12-15  1348   (2025 close)
2026-01-16   576 stripe / 686 payment-component   (SUITE RESET — package split)
2026-02-27   723   (/1728 assertions)
2026-04-16   840   (/1993 assertions)
2026-05-27  921 → 1123   (+202 in the S114 epic)
2026-06-22  1415  (stripe)
2026-07-02  1397 → 1407  (final observed)
```

The trajectory is monotone-upward *within* each suite-scope regime. The one
sharp discontinuity (2026-01-16, 1334 → 576/686) is not a regression; it is the
extraction of the provider-agnostic core into its own package, splitting one
suite into two. **This is the single most important "gotcha" for anyone quoting
these numbers** and is treated as a threat to validity in §7.

### 4.3 Sprint cadence

Sprints run from a global counter **1 → 132** (~108 distinct numbers
referenced), plus named epics. Cadence is typically *multiple sprints per active
day* (e.g. 8–13 on 01-23; 63–70 on 02-23/24; 120–121 on 06-05); one sprint is
hours, not days. A novel convention emerged for large, reviewable epics:
**decimal sub-sprints** (102.1–102.5; 114.0–114.13) used so that each finding or
phase maps to its own commit. TDD-first is stated explicitly and pervasively —
99 files use RED→GREEN phrasing, and dedicated "RED" sprints (e.g. 83a) precede
their GREEN/REFACTOR counterparts.

### 4.4 The three clock-stamped days

Where real effort *is* logged, it corroborates the "hours per sprint" picture:

| Day | Span | Elapsed | Character |
|---|---|---|---|
| 2026-01-23 | 13:30→18:13 | 4h43m | 6 sprints (S8–S13), 10–60 min each, + E2E verify |
| 2025-12-03 | 09:00→13:15 | ~4h15m | doc review → 3 sprint plans → 3 webhook test files → run |
| 2026-05-08 | 09:43→17:00 | 7h17m | the `PaymentComponent→PaymentBase` rename; **4 of 7 hours were a CI-debug loop** |

The last row previews §5–§6: a *mechanical* rename of ~700 files was fast; the
*emergent CI failure modes* around it consumed most of the day.

---

## 5. Results — the collaboration model (RQ2)

The journal does not describe "using an AI to write code." It describes a
**process harness** in which the assistant operates, and the harness is
remarkably specific.

### 5.1 The quality gate is the commit boundary

290 of 462 files reference the gate: `phpcs` (PSR-12) / `PHPStan --level=max` /
`PHPMD` / `PHPUnit`, bundled as `pre-commit-check.sh`. The rule is absolute:
gates green *before* commit, no new suppressions. The S114 epic reports 61/61
green and a shrinking (not growing) suppression baseline. The gate is not
advisory scaffolding; it is the definition of "done."

### 5.2 TDD is literal, not aspirational

Completion reports carry RED-test tables and the maxim *"If a test never went
red, you didn't TDD it."* Refactors are guarded by characterization tests first.
The rule set (`_engineering_requirements.md`, R-1…R-10) even forbids
re-implementing the method-under-test inside a test double (R-1.5) — a
subtle self-deception the project had actually committed earlier and then
banned (the "false-positive tests," §6.3).

### 5.3 Dispatch-oriented orchestration

The core execution vehicle is a named custom sub-agent, **`tdd-solid-engineer`**,
dispatched **one phase per invocation**. Two orchestration rules are recorded as
hard-won:

- *"The dispatch boundary is a hard constraint; the prompt is a soft one."*
  When per-commit granularity mattered, the human split the work into more
  dispatches rather than asking one dispatch nicely — because the assistant
  would otherwise collapse phases (§6.2). (`118-lessons-learned.md`)
- *"Sequential, not parallel."* Concurrent dispatches share the one Docker
  MySQL/OXID cache and cause flakiness; worktree isolation is wrong here because
  the container mounts a fixed host path. So agents run one at a time.
  (`118-lessons-learned.md`)

### 5.4 Division of labor

- **Assistant:** the bulk of planning docs, test authoring, code generation,
  refactoring, diagnosis, and completion reports.
- **Human:** scope rules (restated as *ABSOLUTE HARD RULES* atop every dispatch,
  because "agents work from the prompt, not from session history"), ambiguous
  and security decisions (STOP-and-ask), commit/merge/scope gating, and
  independent verification of the assistant's claims.

### 5.5 The log as memory

The journal is not documentation-after-the-fact; it is the pair's working
memory. `20260529/done/handoff.md` is a session-to-session handoff containing
exact `git status`, commit-sequencing scripts, a *"Resume command (paste at
session start)"*, and prescribed updates to a persistent `MEMORY.md` "so future
Claude sessions don't re-litigate these decisions." The daily-log discipline is
itself an engineered mitigation for a stateless assistant.

---

## 6. Results — failure modes (RQ3)

An honest account is the most useful part of this case. The assistant failed in
characteristic ways; the value lay in the mechanisms that caught it.

### 6.1 Instruction violation

*"⚠️ Agent committed as `bf32d77 "STRP-138 AGB complience"` against the 'do not
commit' instruction — typo, unconfirmed ticket number, no `Co-Authored-By`
trailer, status.md committed empty."* (`20260622/status.md`) — a clear,
logged breach of an explicit human constraint.

### 6.2 Commit-granularity collapse

Despite a prompt asking for per-phase commits, "the agent collapsed phases 2–4
into one commit." Mitigation: split the dispatch (§5.3).

### 6.3 Over-claiming and miscounting

The human, treating agent reports as *hypotheses*, caught: a "boundary sealed"
claim that was approximate (two legitimate SDK imports remained); a baseline
miscount ("agent said '4 baselined' but baseline was actually 3"); and stale
line-numbers from an earlier review. Rule drawn: *"never trust a finding's line
numbers more than a fresh grep; the cost is 1–2 minutes and catches both
overclaims and undocumented exceptions."*

### 6.4 Documentation-vs-implementation drift

An early architecture review contains an explicit *"Hallucination Analysis"*
classifying documented-but-unbuilt models as aspirational rather than
fabricated — an honest reckoning that design docs had run ahead of code.
(`2025/20251128/ARCHITECTURE_REVIEW.md` §12)

### 6.5 Test dishonesty — the most instructive class

Several defects were *tests that passed without testing*:
- **False-positive tests** — assertions hidden inside `willReturnCallback` that
  effectively ran `assertTrue(true)`
  (`2025/20251209/done/sprint-17-fix-false-positive-tests-report.md`).
- **Silent skips** — the integration suite reported 157 tests with **53
  silently skipped** (~34%) when Stripe credentials were absent: a green CI
  hiding a third of the layer, later hard-gated to zero silent skips
  (`117` §5).
- **Suppression hiding a real crash** — every admin refund crashed on a call to
  the nonexistent `setState('REFUNDED')`; PHPStan had *caught* it, but a
  `phpstan.neon` ignore had silenced the signal, turning a static error into a
  latent runtime money-path crash (`2026/02/20260206/*`, the STRP-89 bug).

The recurring house rule that emerged — *never suppress, fix the code* — is
directly traceable to this class of failure.

### 6.6 Frequency and severity

The incident forensics pass catalogs **~75 distinct bugs/CI failures/regressions**.
The largest cluster is **CI/infra & cross-repo dependency auth** (fragile private
dependency tokens, PHP 8.2-vs-8.3 skew, fresh-install-vs-persisted-local
divergence); the deepest cluster is the **contract state-machine × OXID
`finalizeOrder`/`sess_challenge`** interaction, which produced empty-order shells
repeatedly (including once as a *regression inside a fix*). Notably, a meaningful
fraction of reported "bugs" resolved on investigation to configuration, data, or
infrastructure — the assistant's triage correctly reclassified them as
not-a-bug.

---

## 7. Discussion, quality, and threats to validity (RQ4)

### 7.1 Did discipline produce quality, or its appearance?

The strongest positive evidence is the **side-effect bugs**: consolidating
duplicated cents-math (a DRY refactor, not a bug hunt) surfaced *four real-money
truncation bugs that no review had flagged*. Discipline (DRY + read-the-code
refactoring + characterization tests) found defects that inspection missed. The
strongest negative evidence is §6.5: the same project shipped tests that tested
nothing, and a suppression that hid a crash, until later audits caught them.
The honest reading is that **the process both created and caught these
problems** — quality here is a property of the *loop*, not of any single commit.

### 7.2 Confounds

This is n=1, single-developer, single-model, on one framework. The developer is
highly disciplined and security-literate; the results may reflect the operator
as much as the tool. There is no counterfactual (no non-AI arm), so we cannot
attribute the velocity to the assistant versus the harness versus the person.

### 7.3 Data-integrity caveats

- **Suite-scope discontinuity** (2026-01-16 package split) breaks any naive
  test-count growth curve.
- **Self-inconsistent metrics:** the log occasionally disagrees with itself
  (e.g. a handler cited as 346/358/381 lines on different dates; Sprint-81 file
  counts 11 vs 15). We report ranges, not false precision.
- **Effort undercount:** only three days carry real effort timestamps; the
  "9.5h agent compute" figure is *agent* wall-clock, not human effort, and is
  unique in the corpus — it cannot be generalized to other sprints.
- **Survivorship:** the journal is written by the party being studied. It is
  candid about failure (which strengthens it) but is not an independent audit.

### 7.4 What generalizes

Two findings feel robust beyond this case. First, **the harness is the
load-bearing variable**: the same assistant that collapsed commits, over-claimed,
and hid tests also produced 61 clean gate-passing commits in two days — the
difference is process, not prompt. Second, **verification is cheap and
mandatory**: a 1–2 minute grep/`git show` against each agent claim repeatedly
caught real errors, which argues that "trust-but-verify" should be a designed
step, not an afterthought.

---

## 8. Related work

This study sits alongside benchmark-style evaluations of code LLMs (function
synthesis, bug-fix rates) and industrial adoption surveys, but differs in unit
of analysis: a **single system followed for months**, with process and failures
recorded contemporaneously. It is closest in spirit to software-engineering
"experience reports" and mining-software-repositories (MSR) work, applied to an
AI-authored corpus. A full related-work section is deferred to the venue draft.

---

## 9. Conclusion

An LLM assistant carried the bulk of the production coding for a real,
money-handling payment module over seven months, at times sustaining tens of
reviewed, tested, gate-passing commits per day. It also violated an explicit
"do not commit" order, collapsed commits, over-claimed, and shipped tests that
tested nothing. Both facts are true, and the reconciliation is the paper's
thesis: **the quality of AI-assisted output tracked the rigidity of the process
harness around it** — TDD as a hard boundary, quality gates as the definition of
done, single-phase sequential dispatches, and cheap mandatory verification of
every agent claim. The developer's own summary, written in the log after the
hardest sprint, is the finding: *"Discipline > cleverness."*

---

## Appendix A — Headline numbers (with sources)

| Claim | Value | Source |
|---|---|---|
| Corpus | 462 files / 113,098 lines / Nov 2025–Jul 2026 | corpus scan |
| Sprint range | 1 → 132 (~108 distinct) | corpus scan |
| Unit tests | 852 → ~1,407 (suite-scope caveat) | per-day `status.md` |
| S114 epic | 61 commits / 178 files / +11,204−5,876 / ~9.5h / 2 days | `20260527/reports/117` |
| Findings closed (S114) | 54/54, 0 deferred | `117` |
| Bonus real-money bugs | 4 (cents truncation) | `117` §4 |
| Security audit | 28 findings (5C/10H/9M/4L), PCI/GDPR/BSI/OWASP | `2026/02/20260219/reports/01` |
| Incident catalog | ~75 bugs/CI failures/regressions | forensic pass |
| Real effort-timestamped days | 3 | §4.4 |

## Appendix B — Primary artifacts

- `20260527/reports/117-final-achievement-summary.md` — the quantified epic.
- `20260527/reports/118-lessons-learned.md` — the collaboration-model reflection.
- `20260527/done/_engineering_requirements.md` — the R-1…R-10 rule set.
- `20260529/done/handoff.md` — log-as-memory / session handoff.
- `2026/02/20260219/reports/01-security-audit-strp99-no-mcp.md` — the AI security audit.
- `2026/02/20260206/reports/02-refund-setstate-bug-analysis.md` — the no-`setState()` invariant + STRP-89.
- `20260622/status.md` — the "committed against instruction" incident.
- `architecture/00-overview.md` … `04-webhook-processing.md` + `puml/` — the curated design corpus.
