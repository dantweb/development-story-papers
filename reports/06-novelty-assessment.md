# Scientific Novelty Assessment

*Written 2026-08-20 · an internal review of what in this corpus of papers would
survive peer review, and what would not*

This document exists because the set had no honest answer to the first question
any reviewer asks: **what is new here?** It assesses the flagship paper and all
ten topic proposals, tiers them by defensible novelty, and names the claims that
should be dropped or demoted.

**Revised 2026-08-20 (statistics pass).** Every item now carries an **evidence
class** — *tested*, *census*, *n=1*, *mixed*, or *untestable* — with the statistic
where one exists (§2.0). That pass changed three verdicts: two findings previously
dismissed as "descriptive" turned out to be statistically established and were
promoted (**N-11**, **N-12**); **N-5** was downgraded to an observation once it
became clear no test of it is possible; and **N-10**'s "refuted" was corrected to
*underpowered*. Item numbers are stable identifiers cited from the other reports,
so N-11 and N-12 sit at the end of Tier 1 rather than being renumbered into it.

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

The same applies to the **velocity and output figures as productivity claims**.
716 commits, ~140 measured hours — descriptively interesting and honestly
caveated, but there are randomised controlled trials of AI-assisted developer
productivity in the literature. A single-subject observational study cannot
compete on that ground and should not try. Reported as productivity evidence,
these numbers invite the correct objection: *no control, no baseline, no causal
identification.*

**One distinction rescues part of this material, and it is worth drawing
carefully.** *Rate* claims ("N commits/day," "N× faster") are unsupported here for
the reasons above. *Distributional* claims about the same data are a different
matter and are testable: that the cadence is overdispersed (dispersion index
**6.93**, p = 4.7e-126) and that the work avoided weekends (P = **1.2e-48**) are
statistically established, non-obvious, and counter-narrative. They are promoted
to **N-11** and **N-12** in §2. What cannot be claimed is that AI *caused* either
pattern.

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

### 2.0 Evidence strength, item by item

Novelty and evidential strength are **different axes**, and conflating them is
how a case study oversells itself. A finding can be conceptually new and weakly
evidenced (N-5), or unremarkable in kind but near-unassailable in support (N-3).
The tests below are computed by [`../data/stats.py`](../data/stats.py); the full
grading of every claim in the programme is in
[`07-lessons-learned.md`](07-lessons-learned.md).

| Item | Evidence class | Statistic | p |
|---|---|---|---|
| **N-3** QA labour omitted *(measurement for an existing theory — see 08 §5.2)* | **tested** | Fisher on `[[52,0],[0,37]]`; full table **χ² = 199.4**, df 6, **Cramér's V = 0.859** | **6.7e-26** / **2.6e-40** |
| **N-2** trailers ≠ authorship | **tested** | 2/466 vs 147/250 across 2026-05-07, Fisher exact | **5.2e-81** |
| **N-4** test-to-source ratio *(+ assertion density M-29, + mutation score M-30)* | **tested** | 11/11 months by sign test; CI **[1.39, 2.06]**; **MSI 70%**, 469/1,592 escaped, reproducible | **0.0010** |
| **N-14** MSI measurements need a reproducibility check *(new)* | **census + demonstration** | same tool, same code: 0–1,019 mutants across runs before the fix; 1,592 every time after | *n/a* |
| **N-11** peak ≠ rate *(new, §2.7)* | **tested** | **dispersion index 6.93** vs Poisson 1.0; χ² = 984.4, df 142 | **4.7e-126** |
| **N-12** intensity without crunch *(new, §2.8)* | **tested** | 0/716 Saturdays under a uniform-7-day null; Mon–Fri also non-uniform (χ² = 22.8, df 4, p = 0.0001) | **1.2e-48** |
| **N-13** CI failure ⟂ commit size *(new, §2.9)* | **tested (null)** | 63% vs 60%; Spearman **ρ = −0.024**; 49.7% failure — roughly **2× published closed-source baselines** — and 85.7% failure clustering | **0.66** *(the null is the finding)* |
| **N-1** self-account vs machine record | **census** | 2.2× undersampling; 41% understatement; a measured 9.1 h over two narrated-as-active months | *n/a — complete enumeration* |
| **N-6** provenance destruction | **census** | 2 mechanisms; 491 commits only on `LEGACY`; 1 commit on no remote ref | *n/a* |
| **N-7** ISP criterion | **census** | **exactly 0** consumers typehint the narrow interfaces | *n/a* |
| **N-8** misattribution ≠ fabrication | **census + n=1** | 0/61 fabricated; **1** mislabel | *frequency untestable* |
| **N-10** no reliable unit of work | **mixed** | 39% of commits ticketless (census); sub-sprint comparison **underpowered** | **1.0000** ← *no power* |
| **N-9** inverted causality (SEC-2) | **n=1, dated** | one three-step chain | *n/a* |
| **N-5** disjoint yields | **untestable** | 4 vs 6 defects, zero overlap — needs the defect-pool size | *not computable* |

Three consequences for how the papers should be written.

1. **Two items are stronger than their prose suggested.** The cadence
   overdispersion and the weekend result were buried inside material §1 dismisses
   as "descriptive only." They are tested, counter-narrative, and belong in the
   contribution list — promoted to **N-11** and **N-12** below.
2. **A fourth corpus arrived after this assessment was first written** and added
   **N-13**, whose evidence is a *deliberate null*. Nulls are usually
   unpublishable; this one is the point, because the absent correlation is what
   discriminates between an environmental and a logical account of the project's
   costs.
3. **N-1 and N-6 are census-strength, not test-strength.** That is not a
   weakness — a complete enumeration needs no inference, and attaching a p-value
   to "zero raw cents-math sites remain" would be a category error. But the
   papers must not *imply* statistical support where the support is enumerative.
4. **N-5 is the weakest Tier-1 item and should be labelled as an observation.**
   See §2.5.

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

Split at the adoption date the change is categorical rather than gradual —
**2/466 (0.4%)** before versus **147/250 (58.8%)** after, Fisher exact
**p = 5.2e-81**. That distinction is the whole point: a trend line fitted through
this data would describe a convention being adopted, not a practice emerging.

This is a clean, dated, worked, and *tested* counterexample to a technique
currently gaining traction. It is short-paper or methods-note material on its
own.

### N-3. The productivity narrative structurally omits the QA labour

> **Reframed 2026-08-21 after the priority-1 literature search**
> ([`08-literature-review.md`](08-literature-review.md) §5.2). This is **not an
> unexplored question**. The oversight burden is already characterised
> qualitatively (Garousi, arXiv:2606.05770 — but with no measurement, no
> role-separation analysis and no tracker data), and a **falsifiable causal
> theory** already claims that *"the team sets the sign, through the expertise its
> humans bring and how it structures the review process"* (Agarwal, Miller,
> Kästner, Vasilescu, arXiv:2607.07980, from 3,100 coded practitioner documents).
> N-3's contribution is therefore **the measurement, not the question** — the
> artifact-derived evidence those papers lack. That is a *stronger* position than
> a gap: it enters an active conversation with a named proposition to test. The
> residual risk shifts accordingly, from "someone already found this" to **n=1 —
> one team's structure cannot settle a proposition about team structure.**

The dominant framing in AI-assisted development discourse is the *solo developer
plus agent*. This corpus shows that framing is an artifact of **whose record you
read**.

| Reporter | Story | Task | Bug |
|---|---|---|---|
| the developer (with the assistant) | **52** | 5 | **0** |
| a dedicated tester | 0 | 5 | **37** (92.5% of all bugs) |
| a project manager | 0 | **26** | 0 |

The association is near-deterministic: Fisher exact on the developer×tester /
Story×Bug 2×2 gives **p = 6.7e-26**, and the full reporter×type table gives
**χ² = 199.4, df 6, p = 2.6e-40, Cramér's V = 0.859**. This is the most
statistically robust result in the corpus.

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
not job titles; there is no work-log to size the tester's effort (Jira's time
fields are empty for all 156 issues); and no counterfactual project without a
tester. Given §5.2.2's theory already exists, this is best positioned as
**hypothesis-testing on a single case**, not hypothesis-generating — and the cheap
upgrade is the same reporter×type analysis across several AI-assisted projects
with differing QA staffing, which needs only issue-tracker exports.

### N-4. Test-to-source write ratio as an artifact-derived check on a process claim

Test-to-code ratios are an old metric. What is less trodden is using one as a
**falsifiable proxy for a self-reported process discipline** in AI-assisted work.

Measured: **+150,321 lines of test code against +88,896 of production code —
1.69 : 1**, with +196 test methods added during the two-day epic. A project that
asserted TDD while writing tests as an afterthought could not produce that ratio.
It is the one process claim in the corpus that the artifact independently
confirms.

**The effectiveness literature challenges the metric itself,** and this should be
conceded up front rather than defended: suite **size** is a known confounder of
effectiveness measures, coverage does not track effectiveness (Inozemtseva &
Holmes, ICSE 2014), and **assertions do** (Zhang & Mesbah, FSE 2015). Our 1.69:1
is a size metric. We therefore also measured the better proxy — **2.28 and 2.33
assertions per test method** across the two packages (M-29) — and then **ran the
mutation-testing pass** that would settle it. After three non-reproducible attempts and a root-cause fix, the
measurement is **stable**: **Covered Code MSI 70%** (1,592 mutants, 469 escaped),
identical across thread counts (M-30). N-4 is therefore a three-metric claim in
which the third — and only the third — speaks to effectiveness, and it says the
suite misses **30%** of the semantic changes to code it executes. The largest
escape category is `MethodCallRemoval` (85/469), a measured instance of the
over-mocking phenomenon rather than an anecdote.

**A methodological by-product worth its own mention (N-14).** The first three
measurements were wrong and each looked authoritative; the instability came from
Infection's own random-seeded initial test run, not from the coverage driver or
the suite. No paper we located that reports an industrial MSI reports having
checked run-to-run stability. That is a cheap, generalisable caution.

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

**Caveat — and it is the binding one.** The disjointness is **not testable with
this data**. Computing the probability of zero overlap between a 4-defect set and
a 6-defect set requires the size of the underlying population of amount-related
defects, which is unknowable; without it there is no null to reject. The two
channels also ran at different times against different code states, so this is an
uncontrolled natural experiment.

**Therefore: label this an observation, not a result.** It is the most
conceptually interesting item in Tier 1 and the least defensible one, which is an
uncomfortable combination and the reason it is stated last. What would make it a
result: a designed comparison — hold a subsystem fixed, run a refactoring pass
and an independent testing pass against the same code state, and compare yields
against an agreed defect inventory. That is a follow-up study, not a
reinterpretation of this data.

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

Solid methods note, resting on **complete enumeration rather than inference** —
there is nothing here to test, and nothing that needs testing. Not a theoretical
result, and should not be oversold as one.

---

### N-11. "The peak is not the rate": a statistical correction to how AI-assisted throughput gets quoted

**Promoted from material §1 dismisses as descriptive.** The *rate* claim remains
unsupported; the *distributional* claim is tested, and they are different claims.

Commits per active day: mean 5.01, **variance 34.71**, median 3, max 35. The
**dispersion index is 6.93** where a steady (Poisson) process gives 1.0 —
overdispersion χ² = 984.4, df = 142, **p = 4.7e-126**. Only 18 of 143 active days
exceed 10 commits.

Why this is a contribution rather than a statistic: **AI-assisted throughput is
routinely quoted from peak episodes.** This project's own completion report
invited exactly that reading, and the first draft of the flagship paper came close
to taking it — the epic's 30+ commits/day against a modal day of three, an
overstatement of roughly tenfold. The dispersion index is a one-number, testable
way to say "this distribution has no meaningful central rate," and it is
applicable to any repository. Anyone reporting AI-assisted velocity should be
required to report dispersion alongside the mean, and this gives them the
instrument and a worked example.

**Limit:** commits/day is a proxy for output, not value — the 35-commit day was a
mechanical package split, not 35 features. The result establishes burstiness, not
productivity.

### N-12. Sustained AI-assisted output without schedule compression

**Also promoted.** Across ten months: **zero Saturday commits** and one Sunday
commit in 716; **95.9% of commits inside 08:00–20:00** local time. Under a null of
commits distributed uniformly across seven days, P(zero Saturdays) =
**1.2e-48**. Within Mon–Fri the distribution is itself non-uniform (χ² = 22.8,
df = 4, **p = 0.0001**, Wednesday heavy). Out-of-hours work exists but is
**concentrated**: 13 of the 29 out-of-hours commits fall on one day, the hardest
sprint in the record (exact binomial **p = 4.8e-07**).

Why it matters: a recurring worry about agentic development is that it enables or
demands intensification — always-on work, because the agent is always available.
This case is a counterexample with a hard test behind it, and it is orthogonal to
everything the journal claims about itself.

**Limit, and it is worth stating in the paper rather than being caught on it:**
commit timestamps record when work *landed*, not when it was done, so batching
could in principle hide evening effort. The weekday result is robust to that
(batching does not cross day boundaries for 715 of 716 commits); the hour-of-day
result is weaker for exactly this reason. And n=1 operator — this is one person's
working pattern, not a property of AI-assisted development.

### N-13. A measured non-association: build failure is independent of change size

**Added with Corpus D (GitHub Actions, 979 runs).** The claim that
infrastructure, not application logic, dominates the cost of framework-coupled
cross-repo work is practitioner folklore and appears throughout this corpus as
narrative (TECH-4, LL-8, M-5/M-6). Corpus D lets it be tested, and the test that
matters is a **null**:

| Commit size | Commits with ≥1 failing run |
|---|---|
| ≥500 insertions | 77/123 (**63%**) |
| <500 insertions | 193/321 (**60%**) |

Fisher exact **p = 0.66**; Spearman **ρ = −0.024**. Alongside: **49.7% of 979
runs failed**, CI consumed **169.5 h** of wall-clock against ≈140 h of human
session time, and **53% of CI time went to failing runs**.

**Why the null is the contribution.** A logic-failure model predicts that failure
scales with the volume of changed logic; the data show no gradient at all. So the
folklore claim is supported not by a correlation but by the *conspicuous absence*
of the one a competing explanation requires. That is a cleaner argument than any
amount of saga-telling, and — being a joined-corpus result — it is not available
to a study of commits alone or of CI alone.

**Secondary, and now only descriptive:** the failure rate fell **57% → 46%**
across 2026-04-01 (nominal p = 0.0014). **Corrected for failure clustering
(lag-1 autocorrelation 0.680, n_eff ≈ 179 of 940) this becomes p = 0.18 and is
withdrawn as a tested claim** — see [`08`](08-literature-review.md) §7.2. The
direction stands; the significance does not.

**A third element, added 2026-08-24 and arguably the best part of the paper:**
failures are **strongly clustered** — 85.7% of failures immediately follow
another failure, against a published multi-project benchmark of >50%. This is
independent evidence for the same mechanism (a broken environment persists until
repaired, unlike defects in changed logic), and it is a corroboration of an
existing published claim rather than a bare assertion.

**Limits.** `failure` conflates broken builds with flaky E2E, cancelled
infrastructure and expired credentials — it measures friction, not defect
density. Coverage is 62% of commits and 76% of runs. The 2026-04-01 split is
chosen, not derived, and workflow composition changed across it. Run-level
outcomes are **autocorrelated (ρ₁ = 0.680)**, so any run-level test must model
the dependence — the per-commit tests behind N-13 are less affected and, being
nulls, conservative under it. And this remains one project: the non-association is
established *here*, not in general — and against an **outlier failure rate**, which
is itself part of why it appears so cleanly.

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
| **TECH-4** cross-repo CI/CD | **Upgraded by Corpus D.** As engineering advice, still practitioner knowledge with no research contribution. But its central thesis is now *tested* — see **N-13**: 49.7% CI failure across 979 runs, and failure independent of commit size (p = 0.66, ρ = −0.024). The measured non-association is publishable; the field guide is not. The standing observation also holds: **the failures that cost the most time left the least trace in the artifact.** |
| **SEC-1** async money boundary | The controls are textbook: signature verification, cheapest-first guard chains, atomic idempotency, PII minimisation. Novelty is the **candour** (documenting what was wrong first, what is still open) — a publication-ethics virtue, not a scientific one. **The AI-authored audit being self-scored with no independent tracker record is a liability, not a contribution.** |
| **Velocity / output figures** | No counterfactual, no control, confounded treatment. Descriptive only. |
| **The harness thesis** | See §1. Context, not claim. |

---

## 5. Recommended reframing

The flagship paper is currently *"an AI helped build a payment module, and
discipline was why it worked."* That is the weak version. Three papers fall out
of this corpus, and the allocation matters — two of them are about *measurement*
and one is about the *phenomenon*, which is a distinction §5.3 turns on.

### 5.1 Paper 1 — the audit (the reframed flagship)

> **What a project's own record gets wrong about itself: auditing an AI-assisted
> development journal against its commit, issue and CI history.**

- **N-1 becomes the contribution** — a methods result for empirical AI-SE, and
  its strength is **enumerative**: it does not need a p-value and should not
  claim one.
- The **tested** results become the paper's hard evidence — **N-3** (Cramér's
  V = 0.859, the one finding no reviewer can wave away), then **N-2**, **N-4**,
  **N-11**, **N-12**, **N-13**.
- The six numbered findings become **evidence**, not the point.
- The **retractions become credibility**, not embarrassment. A paper that
  withdraws its own "single-developer" claim, withdraws its authorship claim for
  seven of ten months, corrects a rate by an order of magnitude, and downgrades
  its own "refuted" to *underpowered* after running the test is **more**
  trustworthy — and reviewers reward that when it is framed as method rather than
  apology.
- The **harness thesis becomes background** — the thing the journal claimed,
  which the audit partially confirms (N-4) and partially cannot reach.

**On N-13's placement here:** the flagship should *report* it (§4.13 already
does) as one more instance of the journal's account being testable against
machine records — the journal asserted an environmental cost story, and the CI
data confirms it by a route the journal never had. But the flagship should not
*develop* it, because its subject is the audit method, not payment-module CI. The
development belongs in Paper 3.

### 5.2 Paper 2 — the negative results (measurement)

> **Every corpus is compromised: negative results on measuring AI-assisted
> software engineering.**

Assembling **N-2** (trailers measure convention adoption, not AI involvement),
**N-6** (provenance is destroyed by at least three mechanisms and the loss is
invisible from inside the repository), **N-10** (no artifact is a reliable unit of
work), the absence of estimate data in **all four** corpora, and the
untracked-architecture blind spot. A coherent negative-results contribution, and
the field currently lacks one.

Corpus D strengthens this paper without changing its shape: it supplies a
**third, independent provenance-loss mechanism** (24% of runs point at
`head_sha` values on deleted branches, and GitHub's retention window silently
discards older runs), and a fourth corpus with **no effort data** — so "instrument
effort prospectively or lose it" is now supported four ways rather than three.

### 5.3 Paper 3 — where the cost actually goes (new, and N-13 anchors it)

> **Environmental, not logical: build failure is independent of change size in a
> framework-coupled AI-assisted project.**

**This is the paper N-13 should carry, and it is a different kind of paper from
the other two.** Papers 1 and 2 are about how badly software engineering *measures
itself*. This one makes a claim about the *engineering*, and it is the only
Tier-1 result that does.

The spine:

| Element | Evidence |
|---|---|
| CI failure is the modal outcome | **487/979 runs failed (49.7%)** across 40 workflow names over ten months |
| The machine outspends the humans | **169.5 h** CI wall-clock vs ≈140 h measured human session time; **90.1 h (53%)** in failing runs |
| **The central result — a measured non-association** | ≥500 insertions fail **63%**, <500 fail **60%**; Fisher **p = 0.66**, Spearman **ρ = −0.024** |
| Hardening appears to work — descriptively | **57% → 46%** failure across 2026-04-01; nominal p = 0.0014, **p = 0.18** after clustering correction (§2 N-13, `08` §7.2) — a direction, not a result |
| Supporting qualitative account | the namespace-generation break (five falsified CI iterations), cross-repo dependency auth, PHP 8.2/8.3 skew — `03-topics-technical.md` TECH-4 |
| Companion result | **N-5**, disjoint defect yields from refactoring vs black-box testing on the same subsystem |

**Why the null is the argument, and how to write it so a reviewer sees that.**
State the competing hypothesis first and commit to its prediction: if these
failures were defects in changed logic, failure probability must rise with the
volume of changed logic. Then show there is no gradient at all — not a weak one,
ρ = −0.024. The environmental account survives *because* the logical account made
a falsifiable prediction that failed. Framed that way it is a hypothesis test, not
an absence of evidence; framed carelessly ("we found no correlation") it reads as
a failed analysis. That framing choice is the difference between publishable and
rejected.

**What this paper must concede.** `failure` conflates broken builds with flaky
E2E, cancelled infrastructure and expired credentials, so it measures *friction*
rather than defect density — and a critic will say the non-association is
therefore unsurprising. The honest answer is that this is the point: half of all
pipeline outcomes were friction of a kind indifferent to the code, which is
itself the finding. Also: 62% commit coverage, a chosen split point for the trend,
changing workflow composition across it, and n=1 project.

**Feasibility note.** This is the cheapest of the three papers to write. The data
is already exported and joined (`../data/actions_runs.csv`,
`../data/actions_by_commit.csv`), the tests are already implemented
(`../data/stats.py` T9a–T9c), and — unlike Papers 1 and 2 — it needs **no
named-colleague consent** and touches no security material, so it clears the
publication gates in `07-lessons-learned.md` immediately.

### 5.4 Venue fit

- **Papers 1 and 2** — **MSR**, **EMSE**, or **ICSE-SEIP**. Paper 1 should cite
  Agarwal et al. (arXiv:2607.07980) as its theoretical frame for N-3 and position
  the result as a test case; the two works are methodologically complementary
  halves — theory from discourse at scale, versus measurement plus mechanism on
  one project.
- **Paper 3** — **MSR** is the natural home (it is a repository-mining result);
  **ICSE-SEIP** or **ESEM** also fit, and ESEM arguably best, since the
  contribution is an empirical hypothesis test rather than a mining technique.
- The technical and security topics as written suit practitioner venues or
  industry tracks — not research tracks. **TECH-5 (N-5)** is the exception and
  could stand as a research short paper if the inspection-versus-testing lineage
  is made explicit; it is also the natural companion result inside Paper 3.
- Practitioner routing for all eight lessons is in
  [`07-lessons-learned.md`](07-lessons-learned.md).

### 5.5 Suggested order

1. **Paper 3** first — cheapest, ungated, self-contained, and it establishes the
   corpus in a venue before the more argumentative papers arrive.
2. **Paper 2** second — negative results are easier to land once the data is
   already cited, and it needs no consent work either.
3. **Paper 1** last — the most valuable and the most gated: it depends on
   named-colleague consent for N-3 (see `07-lessons-learned.md`, "Before anything
   ships") and on the related-work search in §6 below.

---

## 6. What is still missing

Ordered by how likely each is to sink the papers.

1. **A related-work section — now partly closed, and one Tier-1 item is at
   risk.** [`08-literature-review.md`](08-literature-review.md) locates published
   work for most Tier-1 claims and grades each as instantiates / supports /
   complicates / counterexample / challenges-us. Net effect on this assessment:
   **N-2 gains its strongest venue fit** (it is a single-project ground-truth case
   for the perils catalogued by *Promises, Perils, and (Timely) Heuristics for
   Mining Coding Agent Activity*, MSR 2026); **N-13 must be reframed** —
   the build-failure literature reports churn features as predictive, so our
   claim is "no predictive value *here*", with *Is this Build Failure Related to
   my Patch?* (13.33% patch-unrelated failures) supplying the mechanism; **N-5
   gains a lineage and an experimental template** (Basili & Selby: techniques
   detect different fault classes); and **M-26 is challenged outright** by
   *Debt Behind the AI Boom* — our CI-based null cannot see the static issues
   they measure. Still outstanding: the targeted search for §5.2 of that review,
   which determines whether **N-3 is a genuine gap or a quantified instance**.
   **That search was run on 2026-08-21** (§5.2 of the review): N-3 is **not** a
   gap — it is the missing measurement for an existing falsifiable theory, which
   is a better position but a different claim, and N-3 above is reframed
   accordingly.
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
6. **Effort data.** Unrecoverable from all three corpora (Jira's time fields are
   empty for all 156 issues; the journal clock-stamps 3 days). Any future project
   intending to be studied should instrument this prospectively — which is itself
   worth saying as a recommendation.
7. **Independent security assessment.** SEC-1's audit is AI-authored and
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
QA function that filed 92.5% of its defects — a role separation so sharp it tests
at **χ² = 199.4, Cramér's V = 0.859, p = 2.6e-40**. Along the way the audit
produced a *tested* counterexample to trailer-based AI-commit identification
(**p = 5.2e-81**), an artifact-derived confirmation that the TDD claim was real in
volume (**11/11 months, ratio CI [1.39, 2.06]**) while demonstrably hollow in
places, a one-number instrument for the peak-versus-rate error that AI-throughput
reporting keeps making (**dispersion 6.93**), evidence of sustained output without
schedule compression (**zero Saturdays, P = 1.2e-48**), and a documented case of
invisible provenance loss. Five of those carry a statistical test; the rest are
complete enumerations that need none; **every causal claim about AI's effect
remains out of reach**, and the honest correction of one earlier overclaim — a
"refuted" that a test showed to be merely underpowered — is as much a part of the
contribution as anything confirmed. The contribution is methodological, the
findings are negative more often than positive, and the retractions are the most
credible part.
