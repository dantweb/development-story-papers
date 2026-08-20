# Scientific Novelty Assessment

*Written 2026-08-20 · an internal review of what in this corpus of papers would
survive peer review, and what would not*

This document exists because the set had no honest answer to the first question
any reviewer asks: **what is new here?** It assesses the flagship paper and all
ten topic proposals, tiers them by defensible novelty, and names the claims that
should be dropped or demoted.

> **Scope caveat, and it is a real one.** This is an assessment against the
> literature *as known to the author at the time of writing*, without a
> systematic search. A proper related-work pass is the single largest missing
> piece in this programme (§6) and could move items between tiers — most likely
> **downward**. Nothing below should be cited as a novelty claim until that
> search is done.

---

## 1. The headline claim is the weakest part

The flagship paper's thesis is *"the quality of AI-assisted output tracked the
rigidity of the process harness around it"* — the developer's *"Discipline >
cleverness."* It is the paper's title, its abstract's conclusion, and its
emotional centre.

It is also the **least novel thing in the set**, and it cannot be established by
this study.

- **It is close to conventional wisdom by 2026.** "Process discipline matters for
  AI-assisted code quality" is asserted in vendor guidance, practitioner
  writing, and the agentic-SE literature. Restating it with a case study adds
  little.
- **There is no counterfactual.** No non-AI arm, no low-discipline arm. The
  design cannot separate the harness from the operator from the assistant.
- **The treatment is not a constant.** Six model generations appear in four
  months (Opus 4.7 → 4.8 → 5, Sonnet 4.6, Fable 5). "The assistant" is not a
  stable unit of analysis over the study window.
- **n=1, single operator, single framework, single domain.**

The same applies to the **velocity and output figures**. 716 commits, ~140
measured hours, the cadence distribution — these are descriptively interesting
and honestly caveated, but there are randomised controlled trials of AI-assisted
developer productivity in the literature. A single-subject observational study
cannot compete on that ground and should not try. Reported as productivity
evidence, these numbers invite the correct objection: *no control, no baseline,
no causal identification.*

The **failure taxonomy** (instruction violation, granularity collapse,
over-claiming, tests that assert nothing) is likewise largely known and
catalogued in agent-evaluation work. The *specimens* here are unusually
well-verified; the *categories* are not new.

**Recommendation:** demote the thesis to framing and context. Lead with the
measurement contributions in §2. A reviewer who meets "discipline over
cleverness" as the central claim will write "asserted, not shown" — and be right.

---

## 2. Tier 1 — defensible novelty

These are the contributions worth building the papers around.

### N-1. Auditing a project's self-account against its own machine records — and publishing the corrections

**The strongest contribution in the set, and it is a *methods* result.**

Empirical AI-SE leans heavily on self-reported data: developer surveys, diaries,
retrospectives, vendor case studies, and — increasingly — AI-authored completion
reports. Almost nobody publishes what happens when you check such a record
against the artifact, because doing so means retracting your own earlier claims.

This programme did, and the divergences are specific, directional and quantified:

| Divergence | Magnitude |
|---|---|
| Journal undersampled its own active days | **2.2×** (47 documented vs 105 with commits in-window) |
| Flagship epic's insertions understated | **~41%** (+11,204 reported vs +15,844 measured) |
| A narrated-as-active period was measurably idle | **9.1 h across two months** (Mar–Apr 2026) |
| Whole project function omitted | the **QA role** (see N-3) |
| Reported "simplifications" described one file, not the module | 330→107 lines, while module handler code rose 2,616→2,953 |

The generalisable claim: **a high-quality, daily, candid engineering journal
still diverges from the artifact in systematic and predictable directions** —
undersampling activity, over-reporting continuity, understating volume, and
omitting actors outside the author's role. That is a new empirical result about a
data source the field depends on, and it is directly useful to anyone designing
an AI-SE study.

**Why it is novel:** not "we triangulated three corpora" (triangulation is
standard) but "we measured the disagreement and report its direction and size."

### N-2. "Attribution practice ≠ authorship" — with a dated adoption step-change

The most **immediately actionable** finding for other researchers, and the most
underappreciated in the current drafts.

There is a live methodological trend of identifying AI-assisted commits at scale
via `Co-Authored-By: Claude` / Copilot trailers. This corpus shows why that is
hazardous:

- Trailers appear on **149 / 716 commits (20.8%)**.
- **0% through April 2026**, two isolated uses on 2025-12-05, then routine
  adoption from **2026-05-07**, reaching **86% by August 2026**.
- **Six distinct model strings** in four months.

Therefore: **a trailer-derived corpus measures the adoption of a commit
convention, not the incidence of AI involvement.** Any longitudinal trend
computed from trailers — "AI-assisted commits rose over time," "AI-assisted code
has property X" — is confounded by the convention's rollout, and any
model-attributed comparison is confounded by generation churn. Absence of a
trailer is not evidence of absence of AI.

This is a clean, dated, worked counterexample to a technique currently gaining
traction. It is short-paper or methods-note material on its own.

### N-3. The productivity narrative structurally omits the QA labour

The dominant framing in AI-assisted development discourse is the *solo developer
plus agent*. This corpus shows that framing is an artifact of **whose record you
read**.

| Reporter | Story | Task | Bug |
|---|---|---|---|
| the developer (with the assistant) | **52** | 5 | **0** |
| a dedicated tester | 0 | 5 | **37** (92.5% of all bugs) |
| a project manager | 0 | **26** | 0 |

The developer who wrote the code filed **zero** bug reports. An independent human
filed nearly all of them. This function is **invisible in the journal** (a
developer's log) and **invisible in git** (which sees only committers). It
surfaces only in the issue tracker.

The claim to make — carefully — is not "QA explains the outcome." It is: **the
measured quality of an AI-assisted project may be substantially attributable to
human quality-assurance capacity that the productivity framing does not count,
and that the field's usual data sources cannot see.** That is a confound with a
mechanism, and it is under-argued.

**Limits to state plainly:** n=1; roles are inferred from reporting behaviour,
not job titles; there is no work-log to size the tester's effort; and no
counterfactual project without a tester. This is hypothesis-generating.

### N-4. Test-to-source write ratio as an artifact-derived check on a process claim

Test-to-code ratios are an old metric. What is less trodden is using one as a
**falsifiable proxy for a self-reported process discipline** in AI-assisted work.

Measured: **+150,321 lines of test code against +88,896 of production code —
1.69 : 1**, with +196 test methods added during the two-day epic. A project that
asserted TDD while writing tests as an afterthought could not produce that ratio.
It is the one process claim in the corpus that the artifact independently
confirms.

**The tension must be reported alongside it**, and it is what makes the finding
interesting rather than promotional: the *same* project shipped tests that
asserted nothing (`assertTrue(true)` inside `willReturnCallback`) and an
integration suite silently skipping 34% of its cases. So the ratio measures
**effort, not verification quality** — necessary, not sufficient. Stated that
way, it is a contribution; stated as "TDD confirmed," a reviewer will find the
counter-evidence in the same paper.

### N-5. Two discovery mechanisms, disjoint yields (from TECH-5)

On the same subsystem — monetary arithmetic — two defect-detection channels
produced **non-overlapping** yields:

- **DRY-consolidation refactoring** surfaced 4 real-money truncation bugs
  (`(int)(19.99*100) = 1998`), none flagged by the preceding code review.
- **Black-box testing** by the human tester filed 6 *different* amount-related
  bugs (`STRP-103`, `137`, `150`, `125`, `131`, `152`).

This connects to a classic literature — the inspection-versus-testing comparison
experiments of the Basili era — and updates it for the AI-assisted case, where
"inspection" is partly an LLM-driven refactor. **That lineage is what makes it
respectable rather than anecdotal**, and it is the strongest paper any technical
topic in this set can now write.

**Caveat:** the disjointness is observed, not designed; the two channels ran at
different times on different code states, so this is a natural experiment with no
controls.

### N-6. Provenance destruction as a measurement threat

MSR methodology knows about rebases and force-pushes. What this corpus documents
is a complete, dated case with **two independent mechanisms** and a recovered
witness:

1. **A release squash** (2026-07-02) rewrote the mainline, re-adding 562 files;
   eight months of commit history survive only on a retained `b-7.4.x-LEGACY`
   branch (491 commits).
2. **Routine branch pruning** orphaned `ce96dc86085b` (25 files, +1,710/−60,
   subject `test`), detectable *only* by comparing against a stale local checkout
   frozen at 2026-05-22. The commit is now a **dangling object — one `git gc`
   from permanent loss**.

The methodological payload: **neither loss is detectable from inside the
repository**, so commit-mining studies of projects that squash releases and prune
merged branches inherit an **invisible survivorship bias**. All counts are lower
bounds. This is sharpened by the domain — PCI-DSS-obligated payment software,
where per-commit provenance is a compliance artifact rather than a convenience.

Solid methods note. Not a theoretical result, and should not be oversold as one.

---

## 3. Tier 2 — modest or contingent novelty

### N-7. An operational criterion for "fake" interface segregation

*Count the consumers that typehint the narrow interface.* Measured here:
**exactly zero** across four sub-interfaces, while 4 files typehint the wide
composite.

The criterion is obvious once stated — which is a virtue for adoption but a
problem for novelty. The publishable part is the **failure mode**: none of this
work was ticketed, so **a metrics gate (a PHPMD baseline) was the sole reviewer
of an architectural decision**, and it had been silenced. Plus the assistant
later overturning its own earlier architectural claim. Short-paper material.

### N-8. Misattribution ≠ fabrication

Across 436 ticket-bearing commits, **0 of 61** distinct ticket references were
fabricated; exactly one was **mislabelled** (the STRP-138/139 conflation, with a
literal `strp-xxx` placeholder in the agent's own plan file, and STRP-139 never
appearing in any commit message).

A modest but clean addition to the AI-self-report error taxonomy, and a useful
negative result against the common worry that LLMs invent identifiers in commit
metadata.

### N-9. Inverted causality in validation-debt discovery (from SEC-2)

Input-validation debt was discovered as a **payment failure filed by a tester**
(2026-04-01), which produced a **requirements task written by that tester**
(2026-04-20) that became the implementation sprint — then had to be *loosened*
after the allowlist blocked real customers. A transferable observation with a
dated chain, but experience-report material rather than a research result.

### N-10. No artifact is a reliable unit of work (from PM-1)

Sub-sprints did not map to commits (median 5 commits per decimal sub-sprint; 31%
mapped to exactly one, versus 33% for ordinary sprints). Commits often carry no
ticket (39%). Tickets are either umbrellas (`STRP-145`: 64 commits) or absent
entirely for architectural work. Journal "sprints" have **no relation** to Jira
sprints.

A coherent negative finding about AI-assisted project management, and stronger
than the decomposition heuristic PM-1 originally proposed. Its weakness is that
it is a *nothing-works* result without a positive alternative.

---

## 4. Tier 3 — not novel as research

State this plainly rather than letting a reviewer discover it.

| Topic | Assessment |
|---|---|
| **TECH-1** contract-first checkout | Architecturally unremarkable. Redirect-boundary state restoration via a durable server-side aggregate is established practice. The *interesting* part is empirical: the defect class is documented from **2024**, predating the design, and kept producing tester-filed bugs *after* it — i.e. the redesign reduced without eliminating it. Publish that, not the pattern. |
| **TECH-2** event system + translators | PSR-14 dispatch, tagged iterators, template methods, provider translators — all standard. Near-zero CS novelty. |
| **TECH-4** cross-repo CI/CD | Valuable practitioner knowledge, no research contribution. The one interesting observation: **the failures that cost the most time left the least trace in the artifact**, making them the least verifiable class. |
| **SEC-1** async money boundary | The controls are textbook: signature verification, cheapest-first guard chains, atomic idempotency, PII minimisation. Novelty is the **candour** (documenting what was wrong first, what is still open) — a publication-ethics virtue, not a scientific one. **The AI-authored audit being self-scored with no independent tracker record is a liability, not a contribution.** |
| **Velocity / output figures** | No counterfactual, no control, confounded treatment. Descriptive only. |
| **The harness thesis** | See §1. Context, not claim. |

---

## 5. Recommended reframing

The flagship paper is currently *"an AI helped build a payment module, and
discipline was why it worked."* That is the weak version.

The strong version is:

> **What a project's own record gets wrong about itself: auditing an AI-assisted
> development journal against its commit and issue history.**

Under that title:

- **N-1 becomes the contribution** — a methods result for empirical AI-SE.
- The six numbered findings become **evidence**, not the point.
- The **three retractions become credibility**, not embarrassment. A paper that
  withdraws its own "single-developer" claim, withdraws its authorship claim for
  seven of ten months, and corrects a rate by an order of magnitude is *more*
  trustworthy, and reviewers reward that when it is framed as method rather than
  apology.
- The **harness thesis becomes background** — the thing the journal claimed,
  which the audit partially confirms (N-4) and partially cannot reach.

A **second paper** falls out cleanly, and it may be the more citable one:

> **Every corpus is compromised: negative results on measuring AI-assisted
> software engineering.**

Assembling N-2 (trailers measure convention), N-6 (provenance is destroyed and
the loss is invisible), N-10 (no reliable unit of work), the absence of estimate
data in **all three** corpora, and the untracked-architecture blind spot. A
coherent negative-results contribution, and the field currently lacks one.

**Venue fit:** the reframed flagship and the negative-results paper suit
**MSR**, **EMSE**, or **ICSE-SEIP**. The technical and security topics, as
written, suit practitioner venues or industry tracks — not research tracks. TECH-5
(N-5) is the exception and could stand as a research short paper if the
inspection-vs-testing lineage is made explicit.

---

## 6. What is still missing

Ordered by how likely each is to sink the papers.

1. **A related-work section.** Currently deferred in the flagship and absent
   everywhere else. This is the largest gap and the most likely reason for
   rejection. Every Tier-1 claim above needs a search behind it, and some will
   move down.
2. **Explicit renunciation of causal claims.** The papers should state once, up
   front, that no causal attribution is available — not bury it in threats to
   validity.
3. **Corroboration of the role-structure finding (N-3).** The cheapest
   high-value addition available: a two-sentence confirmation from the tester and
   the project manager turns an inference from reporter metadata into
   corroborated fact. Roles are currently *inferred* from what people filed.
4. **A second case.** Every Tier-1 finding is n=1. Even one comparison
   project — another AI-assisted module with a journal, a repo and a tracker —
   would convert "here is a divergence" into "here is a pattern of divergence."
5. **Effort data.** Unrecoverable from all three corpora (Jira's time fields are
   empty for all 156 issues; the journal clock-stamps 3 days). Any future project
   intending to be studied should instrument this prospectively — which is itself
   worth saying as a recommendation.
6. **Independent security assessment.** SEC-1's audit is AI-authored and
   self-scored. Without an external review its findings cannot be reported as
   security results, only as *claims the project made about itself*.

---

## 7. One-paragraph summary

The novelty of this corpus is **not** that an AI helped build a payment module,
nor that discipline mattered — both are unremarkable by 2026 and unprovable at
n=1. It is that the project's own account of itself was **audited against two
independent machine records and found to diverge in specific, measurable,
directional ways**: undersampling its active days 2.2×, understating its flagship
epic by 41%, narrating a measured idle period as active, and omitting the human
QA function that filed 92.5% of its defects. Along the way the audit produced a
dated counterexample to trailer-based AI-commit identification, a documented case
of invisible provenance loss, and an artifact-derived confirmation that the
project's TDD claim was real in *volume* while demonstrably hollow in *places*.
The contribution is methodological, the findings are negative more often than
positive, and the retractions are the most credible part.
