# Literature Review — which published problems this corpus can speak to

*Written 2026-08-21 · priority-1 search on role separation run the same day (§5.2)*

[`06-novelty-assessment.md`](06-novelty-assessment.md) §6 names the missing
related-work section as **the single largest gap in this programme** and the most
likely reason for rejection. This document starts closing it: it locates published
work whose stated problems, claims or open questions our four corpora can
**resolve, support, complicate, or contradict** — and, just as importantly, where
the literature **challenges us**.

---

## 0. How to read this, and two honesty constraints

**Verdict taxonomy.** Each entry ends with one of:

| Verdict | Meaning |
|---|---|
| **INSTANTIATES** | The paper formulates a problem as open or hypothetical; we supply a documented, measured case of it. |
| **SUPPORTS** | Our measurement agrees with theirs, independently and by a different route. |
| **COMPLICATES** | Our measurement is compatible in direction but changes the magnitude, scope, or interpretation. |
| **COUNTEREXAMPLE** | We contradict a claim stated or commonly read as general. n=1 cannot refute a distribution — it can refute universality. |
| **CHALLENGES US** | The literature undercuts one of *our* claims, or reframes it less favourably. |
| **CANNOT ADDRESS** | Adjacent and relevant, but our data has nothing to say. Listed to prevent overreach. |

**Constraint 1 — n=1.** This is a single-subject case study with no counterfactual
arm. It cannot refute an RCT, estimate an effect size, or establish a
distribution. What it can do is instantiate an open problem, supply a
counterexample to a universal, and test claims *within* a project (our corpora
are censuses, not samples — see [`07`](07-lessons-learned.md), "A note on what a
p-value means here").

**Constraint 2 — depth of engagement varies, and is marked.** Entries flagged
**[full-text]** were read in substance. Entries flagged **[abstract]** or
**[secondary]** rest on abstracts, publisher metadata, or search summaries and
**must be read in full before citation in a venue draft**. Nothing in this
document should be cited from this document.

---

## 1. AI-assisted productivity: the RCT literature

### 1.1 Peng, Kalliamvakou, Cihon, Demirer — *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot* (2023) **[secondary]**

**Their claim.** In a controlled experiment (recruited developers implementing an
HTTP server in JavaScript), the Copilot treatment group finished **55.8% faster**
than control.

**What we have.** Nothing commensurable — and this is the entry that most needs
stating plainly, because it is the comparison a reviewer will reach for first. We
have no control arm, no task standardisation, and a treatment that changed six
times inside the study window. Our §4.2/§4.3 figures (median 3 commits per active
day, ≈140 h of session time) are **activity descriptions, not productivity
measures**.

Our contribution here is negative and methodological: the **dispersion index of
6.93** (N-11) shows this project's output has *no meaningful central rate*, so any
attempt to extract a "commits/day" or "×faster" figure from a repository like this
one is quoting a distribution that does not have a mean worth quoting. That is a
caution about **generalising RCT-style speedups into field settings via repository
metrics**, not a challenge to the RCT itself.

**Verdict: CANNOT ADDRESS** the speedup claim. **INSTANTIATES** a measurement
hazard in field replication.

### 1.2 METR — *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity* (arXiv:2507.09089, July 2025) **[secondary]**

**Their finding.** 16 experienced open-source developers, 246 tasks in mature
repositories: allowing AI tools made them **19% slower**, while the same
developers estimated afterwards that AI had made them **20% faster**. A ~39-point
gap between measured and perceived effect.

**Why this is the most important paper in this review for us.** METR's headline is
not really about speed; it is about **the unreliability of practitioner
self-report on their own AI-assisted productivity**. That is precisely our N-1,
arrived at by a completely different method — they compared self-report against a
controlled clock; we compared a self-authored journal against the project's own
machine records. Our divergences:

| Our measurement | Divergence |
|---|---|
| Active days | journal documented 47; git shows **105 in-window** (**2.2×** undersample) |
| Flagship epic output | reported +11,204 insertions; measured **+15,844** (**41% understated**) |
| A narrated-as-active period | Mar–Apr 2026 measures **9.1 h** of commit-bearing activity across two months |
| Project scope | journal describes 7 months; Jira shows a **3-year** project, 35% of issues predating the commit record |

Note the **direction** is informative and cuts against a simple
self-flattery story: METR's developers *overestimated* their speed, while our
journal *understated* its own output on the epic. Both are self-report error;
neither is simply vanity. A taxonomy of self-report error in AI-assisted work
should therefore distinguish **optimism about effect** from **imprecision about
volume**, and our case supplies the second.

**What we add that METR cannot.** METR's instrument is a task clock in a
controlled setting. Ours is the artifact trail of an uncontrolled real project
over ten months — so we can show *which kinds* of claims drift (activity
continuity, output volume, project scope, actor inventory) rather than only *that*
perception drifts.

**Verdict: SUPPORTS** strongly, by an independent route — and **extends** the
self-report-unreliability finding from perceived speed to documented volume,
continuity, and scope.

### 1.3 Liu, Widyasari, Zhao, Irsan, Lo — *Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild* (arXiv:2603.28592) **[secondary]**

**Their findings.** 304,362 verified AI-authored commits across 6,275
repositories and five assistants: **code smells are 89.1%** of identified issues,
**>15% of commits from every assistant introduce at least one issue**, and
**24.2% of AI-introduced issues survive** to the latest revision — unresolved AI
debt growing to >110,000 surviving issues by February 2026.

**Where we agree.** Their method — identifying AI commits by attribution — is
exactly the technique our N-2 warns about, and their corpus is subject to the same
adoption confound we document (below, §2.1).

**Where they CHALLENGE US.** Our M-26 reports that **AI-trailered commits were no
more CI-fragile** (59% vs 61% with a failing run, Fisher p = 0.88), and it would
be easy to read that as "AI code was no worse here." Against a large-scale finding
that >15% of AI commits introduce static issues, our null looks like a
**measurement-sensitivity problem rather than a quality result**: CI outcome is a
coarse, noisy proxy that would not detect a code smell at all. Their instrument
(static analysis on the diff) and ours (did the pipeline go red) are not measuring
the same construct.

We already label M-26 as heavily confounded; this literature shows the label is
not cautious enough. **The honest revision is to state that our data cannot speak
to AI code quality, only to AI code's effect on pipeline outcome** — and to add
that a static-analysis pass over our own AI-trailered diffs is a cheap, obvious
follow-up we have not done.

**Verdict: CHALLENGES US.** Action: weaken M-26's framing in
[`05-measurements.md`](05-measurements.md) and note the missing static-analysis
comparison as future work.

---

## 2. Mining AI-agent activity: methodology

### 2.1 Robbes, Matricon, Degueule, Hora, Zacchiroli — *Promises, Perils, and (Timely) Heuristics for Mining Coding Agent Activity*, MSR 2026 (arXiv:2601.18345) **[abstract + venue metadata]**

**Their position.** Coding agents leave traces in repositories that MSR
techniques can study, but those traces come with important caveats: the observed
data is **partial**, comes from **multiple heterogeneous agents**, and is
**rapidly changing**. The paper documents heuristics, promises and perils, and
positions itself as timely guidance for a fast-moving phenomenon.

**This is the closest paper in the literature to our N-2, and we are its worked
single-project case.** Where they catalogue perils at ecosystem scale, we can show
each one biting inside one project with the full artifact available:

| Their peril | Our instance |
|---|---|
| Data is **partial** | `Co-Authored-By: Claude*` on **149/716 commits (20.8%)** |
| Traces appear **over time**, confounding trends | **0% before 2026-05-07**, then 58.8% after (Fisher **p = 5.2e-81**) — a convention being adopted, not a practice emerging |
| **Heterogeneous agents** | **six model strings in four months** (Opus 4.7 → 4.8 → 5, Sonnet 4.6, Fable 5, unversioned) |
| Traces can be **lost** | the 2026-07-02 squash; deleted feature branches; **24% of CI runs** pointing at `head_sha` on no surviving ref |

The step-change result is the sharpest thing we can contribute: because we have
the *whole* project including its pre-convention period, we can show that the
trailer series is **uninformative as a time series of AI involvement** — the
journal independently documents heavy AI use throughout a period with 0% trailer
coverage. An ecosystem-scale study cannot demonstrate that, because it has no
ground truth for the untrailered commits. We do, in Corpus A.

**Verdict: INSTANTIATES** their perils with a documented ground-truth case, and
**SUPPORTS** their caution with a quantified step-change. This is the single
strongest venue fit in the review: our Paper 2
([`06`](06-novelty-assessment.md) §5.2) is a companion piece to theirs.

### 2.2 *Was It Never Collected, or Rewritten Away? A Commit-Provenance Dataset Separating Ingestion Gaps from Upstream History Edits across the World of Code* (arXiv:2607.02774) **[secondary]**

**Their problem.** A commit can be missing from a mined corpus for two very
different reasons: the upstream project **rewrote history** (force-push, rebase,
squash, filter) so the commit no longer exists anywhere and its absence is
correct; or the mirror **never ingested it**, a genuine collection gap that bounds
what any study on that corpus can observe. They build a dataset to separate the
two.

**Our contribution.** We are a **primary-source case study of the first
mechanism**, with the rare property that we caught it from *outside* the
repository. Three losses, three mechanisms:

1. **Release squash** (2026-07-02): mainline rewritten, 562 files re-added; 491
   pre-squash commits survive only on a retained `b-7.4.x-LEGACY` branch.
2. **Branch pruning:** commit `ce96dc86085b` (25 files, +1,710/−60, subject
   `test`) reachable from **no ref on the canonical remote** — recovered only by
   comparing against a stale local checkout frozen at 2026-05-22, and now a
   **dangling object one `git gc` from permanent loss**.
3. **CI retention:** 234 of 979 workflow runs (24%) reference `head_sha` values on
   no surviving ref, and GitHub's run-retention window silently discards older
   runs.

The methodological point their framing invites and we can supply: **none of the
three is detectable from inside the repository.** We found the second only by
accident of a stale checkout existing on the same machine. So a study cannot
generally distinguish "rewritten away" from "never happened" *even with full
access to the repository* — the distinction may require artifacts outside version
control entirely.

Domain matters here too: this is **PCI-DSS-obligated payment software**, where
per-commit provenance is a compliance artifact rather than a convenience, and the
loss went unremarked in a daily engineering journal.

**Verdict: INSTANTIATES**, with a recovered witness and a third mechanism (CI
retention) their two-way framing does not cover.

### 2.3 Hora & Robbes — *Are Coding Agents Generating Over-Mocked Tests? An Empirical Study*, MSR 2026 (arXiv:2602.00409) **[full-text attempted; abstract-level]**

**Their question.** Whether coding agents produce excessive mocking — tests that
appear complete but "pass without actually testing the intended behavior" —
targeting mock overuse, assertion quality, and test-double appropriateness.

**Our case is an unusually direct instance, from both sides.** Corpus A documents
this project committing precisely that defect and then banning it:

- **False-positive tests:** assertions hidden inside `willReturnCallback` that
  effectively executed `assertTrue(true)`.
- **A codified rule against it:** R-1.5 forbids re-implementing the
  method-under-test inside a test double — written *after* the project had done
  it.
- **Silent skips:** an integration suite reporting 157 tests with **53 silently
  skipped (~34%)** when credentials were absent — a green pipeline concealing a
  third of a layer, later hard-gated to zero.

And we contribute the tension that makes it interesting: this same project wrote
**1.69 lines of test code per line of production code** (+150,321 vs +88,896;
11/11 months, sign test p = 0.0010, bootstrap CI [1.39, 2.06]). So **test volume
and test honesty were independent** here. A study measuring agent test *quantity*
would have rated this project excellent; the hollow tests were found by human
audit.

That suggests a research question their framing sets up and our case sharpens:
**is over-mocking correlated with test volume, or orthogonal to it?** If
orthogonal, quantity metrics are actively misleading for agent-authored suites.

**Verdict: INSTANTIATES** their phenomenon, and **contributes** a
volume-vs-honesty independence observation plus a concrete anti-pattern rule
(R-1.5) drawn from a real remediation.

---

## 3. CI and build failure — where our sharpest result lands

### 3.1 The build-failure prediction literature (TravisTorrent-era; churn and commit-count features) **[secondary]**

**Their claims, as reported in survey and empirical work.** Build complexity —
usually measured by **number of build commits** — and **source-code churn**
(changed lines/files) are **negatively correlated with build failures**, and the
number of commits in a build is often reported as *the* most important factor for
build outcome. The TravisTorrent dataset (2.64M builds, 31 pre-execution features)
underpins much of this.

**Our result (N-13).** Joining 979 Actions runs to per-commit diffs (n = 444
commits with CI): commits with **≥500 insertions had a failing run 63%** of the
time; those under 500, **60%**. Fisher exact **p = 0.66**; Spearman
**ρ = −0.024** (p = 0.61).

**An internal-consistency point I want to state before claiming anything.** Our
two framings disagree in *sign*: the threshold split leans very slightly toward
*more* failure for bigger commits (+3 points), while the rank correlation leans
very slightly *negative* (ρ = −0.024). Both are null. Their disagreement in sign
is itself evidence that neither direction is real here, and it is why we describe
this as **no association** rather than as a negative one. It also means we are
**directionally compatible** with the literature's negative-correlation claim
while finding **essentially zero magnitude**.

So the honest verdict is not "we contradict them." It is:

- Their *direction* (more churn ⇏ more failures) is **not contradicted** — if
  anything our ρ agrees in sign.
- Their *usefulness claim* — that churn and commit-count features carry
  predictive signal for build outcome — **does not hold in this project**. A
  predictor with ρ = −0.024 predicts nothing here.
- The interesting question becomes **why**, and §3.2 supplies the mechanism.

**Verdict: COMPLICATES.** Directionally consistent, magnitude ≈ 0, predictive
value absent. A case where a well-supported feature family fails, and the failure
is explicable.

### 3.2 Huang, da Costa, Dick, El Mezouar — *Is this Build Failure Related to my Patch? An Empirical Study of Unrelated Build Failures in Continuous Integration* (arXiv:2605.05564, May 2026) **[full-text]**

**Their findings.** Across seven Apache projects, **13.33% of CI build failures
(10,316/77,354)** are *potentially* unrelated to the triggering patch (371
manually confirmed). Developers' stated reasons: unspecified 34.86%, unrelated
tests 20.00%, external interference (dependency updates, unavailable resources)
19.73%, non-reproducible/transient 17.03%, concurrent commits 3.24%, environment
2.43%, configuration 2.43%. Developers spend a **median of 4 hours** determining
whether a failure relates to their patch, motivating automated relatedness
prediction.

**This is the paper that explains our null, and the pairing is the strongest
argument in our Paper 3.** If a meaningful share of failures is unrelated to the
patch, then failure probability need not scale with the patch's size — and in the
limit, where *most* failures are patch-unrelated, the correlation vanishes.
That is our observation exactly: **ρ = −0.024**.

Our project appears to be a far more extreme instance of their phenomenon than
their 13.33%:

| Measure | Their corpus | Ours |
|---|---|---|
| Failure share of runs | — | **487/979 = 49.7%** — roughly **2×** the 26% closed-source baseline (§7.1) |
| Failures unrelated to the patch | **13.33%** potentially | not directly measured, but implied high by ρ ≈ 0 |
| Time cost | median **4 h** per relatedness decision | **169.5 h** total CI wall-clock, **90.1 h (53%)** in failing runs |

Their cause taxonomy also maps cleanly onto what Corpus A narrates
independently — external interference ≈ our cross-repo dependency-auth failures;
environment ≈ our PHP 8.2/8.3 skew and namespace-generation ordering;
non-reproducible ≈ our flaky E2E and the five falsified CI iterations where local
never reproduced the break.

**A method they suggest and we should adopt.** They *manually confirm*
relatedness. We infer it from an absent correlation. The rigorous version of our
Paper 3 would sample failing runs, classify relatedness by hand against their
taxonomy, and report the share directly — converting our indirect inference into a
measured quantity. **That is the single most valuable addition to Paper 3 this
review identifies.**

**Verdict: SUPPORTS** each other bidirectionally — they supply our mechanism, we
supply an extreme case and a size-independence result their framing predicts. Also
**CHALLENGES US** on method: relatedness should be measured, not inferred.

### 3.3 *Continuous Integration Theater* (arXiv:1907.01602) **[secondary]**

**Their concern.** Projects adopt CI tooling without the practices that make CI
meaningful.

**Our relevance.** We have both halves of the tension. On one side, a **49.7%
failure rate** over ten months, and 40 workflow "names" that include renames of
one pipeline — a pipeline red half the time is not functioning as a gate. On the
other, a **measured 11-point improvement** (57% → 46% across 2026-04-01, Fisher
**p = 0.0014**) and permanent regression probes added after each environment
break — the project was actively repairing the practice, not merely displaying it.

**Verdict: COMPLICATES.** A high failure rate is not sufficient evidence of
theatre; the trend matters, and ours improves. We can offer a case where a badly
failing CI was nonetheless a live, tended practice.

---

## 4. Work rhythms

### 4.1 Claes, Mäntylä, Kuutila, Adams — *Do programmers work at night or during the weekend?* ICSE 2018 **[secondary]**

**Their findings.** From commit timestamps across 86 large open-source projects:
**two-thirds of developers mainly follow typical office hours** (empirically
established as **10h–18h**) and do not usually work nights or weekends, with large
variation between projects and individuals; hired developers work more within
office hours.

**Our measurement (N-12).** **Zero Saturday commits and one Sunday commit in
716** — P(zero Saturdays | uniform over 7 days) = **1.2e-48** — with **95.9% of
commits inside 08:00–20:00**, peaks at 13:00/16:00/14:00, and out-of-hours work
**concentrated** rather than diffuse (13 of 29 out-of-hours commits on one day,
the hardest sprint; exact binomial p = 4.8e-07).

Our case sits at the **extreme end of their office-hours group** — an industrial,
paid, single-team project, consistent with their "hired developers" observation.
The contribution is what it is paired with: this schedule coexisted with the
output described in §4.2/§4.7 of the flagship, including a 1.69:1 test-to-source
write ratio and a two-day, 64-commit remediation epic.

**Verdict: SUPPORTS** their office-hours finding, and **extends** it to the
AI-assisted setting where intensification is a live worry.

### 4.2 *TGIF: the evolution of developer commit times*, EMSE 2025 **[secondary]**

**Their finding.** A subtle but consistent **increase** in the proportion of
nighttime and weekend commits over time, especially early-morning hours —
interpreted as a shift toward more flexible, asynchronous work.

**Our case runs the other way.** A 2025–2026 project, in the period their trend
covers, with **0.14% weekend commits** and 4.1% outside 08:00–20:00.

The worthwhile question this raises: **does agentic assistance push toward
intensification or away from it?** A plausible mechanism cuts against the
always-on worry — if an agent compresses a task from an evening's work into a
40-minute dispatch (our median multi-commit session is **37 min**), the work fits
inside the working day. Our data is consistent with that and **cannot establish
it**: n=1, one operator, no baseline, and an employment context that supplies an
obvious alternative explanation.

**Verdict: COUNTEREXAMPLE** to universality of the trend (it is a trend, not a
law, so this is a weak claim), and **INSTANTIATES** a research question worth a
designed study.

---

## 5. Defect detection

### 5.1 Basili & Selby — *Comparing the Effectiveness of Software Testing Strategies*; and the replication literature **[secondary]**

**Their findings.** Comparing code reading by stepwise abstraction, functional
testing, and structural testing across 32 professional programmers and 42
advanced students on four unit-sized programs: **code reading and functional
testing were equal and both better than structural testing** for defect
detection, and — crucially for us — **effectiveness varies by fault class**
(functional better for faults of omission; structural better or equal for faults
of commission). Replications conclude relative effectiveness **depends on program
and fault type**.

**Our observation (N-5).** On one subsystem — monetary arithmetic — two channels
produced **non-overlapping** yields:

- **DRY-consolidation refactoring** (a reading-and-restructuring activity)
  surfaced **4 real-money truncation bugs** (`(int)(19.99*100) = 1998`), none
  flagged by the preceding code review.
- **Black-box testing by the human tester** filed **6 different**
  amount-related defects (`STRP-103`, `137`, `150`, `125`, `131`, `152`).

Zero overlap. Their "different techniques detect different fault classes" is
**exactly the lineage this observation needs**, and citing it converts our
anecdote from a curiosity into a modern instance of an established result — with
a new channel (LLM-assisted refactoring) standing in for code reading.

**What they also do is show us how weak our version is.** Their design is a
fractional-factorial controlled experiment with assigned techniques and a known
fault inventory. Ours is two uncontrolled activities at different times on
different code states, with an unknowable defect pool — which is why
[`06`](06-novelty-assessment.md) §2.5 downgrades N-5 to an **observation** and
specifies the designed comparison needed to make it a result. This literature is
the template for that design.

**Verdict: SUPPORTS**, and supplies both the lineage and the experimental template
we lack. Also **CHALLENGES US** on rigour.

### 5.2 Who files the defects in an AI-assisted team — **priority-1 search, run 2026-08-21**

This was flagged as the outstanding search that determines whether N-3 — our
strongest result — is a genuine gap or a quantified instance. It has now been run
across four angles: QA role in AI-assisted teams; issue-tracker reporter analysis;
who finds bugs in AI-generated code; and oversight-burden measurement.

**Result: N-3 is *not* an unexplored question — and that is a better outcome than
a gap.** The question is posed, and a falsifiable theory about it exists. What
does not exist is the **measurement**. N-3 is that measurement.

#### 5.2.1 Garousi — *Human Oversight and Overload: Two Hidden and Costly Burdens of AI-Assisted Software Engineering* (arXiv:2606.05770, June 2026) **[abstract]**

**Their position.** Two overlooked burdens of AI-assisted SE: (1) "the constant
need for human oversight and inspection of AI-generated artifacts," and (2)
cognitive overload from the volume of AI suggestions. Oversight is framed as
non-optional — "engineers must review, validate, and sometimes rework what AI
produces." Related practitioner work defines **oversight burden** as the
cumulative effort to review, validate, repair and integrate AI-generated
artifacts, including inspection time, debugging of subtle errors, and the
cognitive effort of verifying correctness.

**What the paper is and is not.** It synthesises "recent opinions from
practitioners" and states its aim as opening a conversation. It contains **no
measurement**, **no role-separation analysis**, and **no issue-tracker data**. It
does not ask *who* performs the oversight.

**Our contribution against it.** N-3 answers the unasked half of their question
with a measurement: in this project the oversight was performed by **someone
other than the engineer who used the AI**. The developer working with the
assistant filed **52 Stories and zero Bugs**; a dedicated tester filed **37 of 40
Bugs (92.5%) and zero Stories** (Fisher **p = 6.7e-26**; full reporter×type table
**χ² = 199.4, df 6, Cramér's V = 0.859**). Their burden was not merely large — it
was **borne by a distinct role**, which changes what mitigating it means. "Teams
should handle oversight" and "teams need a person whose job is oversight" are
different recommendations, and only the second follows from measurement.

**Verdict: INSTANTIATES and sharpens.** We supply the missing quantitative case
for a burden they characterise qualitatively, and add the role dimension they do
not raise.

#### 5.2.2 Agarwal, Miller, Kästner, Vasilescu — *3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse* (arXiv:2607.07980, July 2026) **[abstract, verbatim]**

**This is the most important paper found in the entire review, and it changes
N-3's framing.**

Their method: 38,709 grey-literature documents filtered to those substantively
about code review, a stratified random sample of **3,100** coded via an
LLM-assisted pipeline, yielding a causal model of **26 constructs and 67
relationships** (64 directed, 3 contested). Their organizing claim, verbatim:

> "review is the control point through which a coding agent's effect on software
> is decided, and that AI does not fix the sign of that effect: the team sets it,
> through the expertise its humans bring and how it structures the review
> process."

They explicitly turn "AI is changing code review" into **falsifiable propositions
with named constructs and moderators**.

**Three points of contact, and one of them is uncanny.**

1. **N-3 is a measured data point on their central proposition.** They claim the
   team sets the sign through how it structures review. Our team structured it with
   a dedicated tester who filed 92.5% of the defect reports, and the association is
   near-deterministic (V = 0.859). That is exactly the kind of evidence a
   falsifiable proposition needs and that discourse synthesis cannot supply.
2. **They state our own methodological problem before we did.** Their motivating
   observational analysis finds agent-authored PRs "reviewed less often, merged
   several times faster, and discussed less" — *"yet the direction of these trends
   flips under different but equally defensible analysis choices, so the traces
   establish what is changing without explaining why."* We independently hit the
   same wall: our two framings of N-13 **disagree in sign** (threshold split +3
   points; Spearman ρ = −0.024), which is why we report it as *no association*
   rather than picking the flattering direction. Their observation is the general
   statement of our specific experience, and it retroactively validates reporting
   both framings.
3. **Their diagnosis of repository mining is our diagnosis of the journal.** They
   say traces show *what* changes without explaining *why*, and turn to
   practitioner discourse for mechanism. Our programme does the mirror image: we
   have the mechanism (Corpus A, a daily journal) and add machine records for the
   *what*. **The two papers are methodologically complementary halves** — theory
   from discourse at scale, versus measurement plus mechanism on one project.
   That is a strong framing for a citation and for a venue pitch.

**Verdict: SUPPORTS bidirectionally, and reframes N-3** from "novel question" to
"missing measurement for a named published proposition" — which is more citable,
not less, because it enters an active conversation with a specific theory to test.

#### 5.2.3 Reporter-type analysis pre-dates AI, but asks a different question **[secondary]**

Huo et al. compared bug reports written by **developers versus users** and found
differences significant enough to affect prediction models; related work
(Bettenburg, Zimmermann and others) studies gaps between what reports contain and
what developers need. Reporter *reputation*, severity and blocker status are
established determinants of fix time.

So reporter-type analysis is a recognised dimension of issue-tracker mining — but
the contrast is **developer vs end user**, the outcome of interest is **report
quality or fix-time prediction**, and the setting is **pre-agentic**. Our contrast
is *developer-who-used-the-AI vs dedicated tester*, and our outcome is **which
role generates defect discovery at all**. Adjacent lineage, different question.

**Verdict: adjacent — supplies precedent for the method, not for the finding.**

#### 5.2.4 Practitioner and grey-literature evidence on the burden's size **[secondary — treat with care]**

Widely circulated non-peer-reviewed analyses report that AI-authored PRs carry
**~10.83 issues each vs 6.45** for human PRs, **1.4× more critical** and **1.7×
more major** issues, PRs ~18% larger, and review-time increases as high as
**441%**. These are vendor or blog analyses, not peer-reviewed studies, and should
be cited only as practitioner discourse — which is precisely how §5.2.2 treats
such material, and a reason to prefer their coded synthesis over the raw claims.

If even directionally right, they **strengthen our N-3 narrative** (oversight is
heavy) while **underscoring our limit**: we cannot size the tester's effort,
because Jira's time-tracking fields are empty for all 156 issues.

#### 5.2.5 Adoption-rate context for N-2 **[secondary]**

*Agentic Much? Adoption of Coding Agents on GitHub* (TOSEM; arXiv:2601.18341)
estimates **22.20%–28.66%** agent adoption as of 21 February 2026, and its
companion *Agentic Very Much!* (arXiv:2606.07448) finds adoption more than twice
as high, and more intensive, in newly created projects. Useful calibration: our
project's trailer coverage (20.8% overall, 86% by August 2026) sits far above
ecosystem adoption in its late period — consistent with a mature single-project
convention rather than a representative sample, which is one more reason our
trailer series cannot be read as an adoption curve.

#### 5.2.6 Revised status of N-3

| Before this search | After |
|---|---|
| "Possibly a gap; requires targeted search before any novelty claim." | **Not a gap.** The oversight-burden question is posed (§5.2.1) and a falsifiable causal theory about team structure exists (§5.2.2). |
| Novelty claim: unverified | Novelty claim: **the measurement**, not the question. N-3 supplies quantitative, artifact-derived evidence for a proposition that currently rests on practitioner discourse. |
| Risk | The risk is no longer "someone already found this." It is **n=1**: one team's structure cannot confirm a proposition about team structure in general. |

**What to do with it.** Cite §5.2.2 as the theoretical frame and position N-3 as a
test case rather than a discovery. Drop any claim that the question is unexplored.
And note in the paper what would raise this from a data point to a result: the
same reporter×type analysis across several AI-assisted projects with differing QA
staffing — a cheap multi-case study, since it needs only issue-tracker exports.

## 6. Where the literature challenges us — consolidated

Worth reading as a list, because it is the part a reviewer will assemble anyway.

| Our claim | Challenge | Our response |
|---|---|---|
| M-26: AI commits no more CI-fragile (p = 0.88) | *Debt Behind the AI Boom*: >15% of AI commits introduce static issues; 24.2% survive | Our instrument (pipeline outcome) cannot see code smells. **Weaken the claim**; add a static-analysis pass over our AI-trailered diffs. |
| N-13: failure ⟂ change size | Build-failure literature reports churn features as predictive | Directionally compatible; magnitude ≈ 0. Reframe as "these features carry no signal *here*", with §3.2 as mechanism. |
| N-13's inference | Huang et al. *measure* patch-relatedness manually | Our inference is indirect. **Sample and hand-classify failing runs** against their taxonomy. |
| N-5: disjoint yields | Basili & Selby ran a controlled factorial design | Ours is uncontrolled with an unknown defect pool. Already downgraded to an observation. |
| Velocity/output figures | Peng et al., METR — both controlled | We have no control arm. Report as activity description only. |
| N-12: no intensification | *TGIF* finds the opposite trend; our employment context explains it | State the alternative explanation; claim a counterexample to universality, nothing more. |

---

## 7. The outstanding searches — all run 2026-08-24

All six searches from the first revision have now been run. Priority 1 is in
§5.2; the remaining five are below. **Two of them changed our results**, one of
them by exposing a statistical error of our own.

### 7.1 CI failure-rate baselines — **our 49.7% is an outlier, not a norm** **[secondary]**

**What the literature reports.** Published build-failure rates:

| Setting | Failure rate |
|---|---|
| Closed-source projects (initial study of CI bad practices) | **26%** |
| Large, long-lived projects | **19%** |
| Java OSS CI workflows (empirical analysis) | **>38%** |
| Industrial systems with hardware-in-the-loop | **1,414 / 11,731 ≈ 12%** |
| **This project** | **49.7%** (487/979; 51.8% of decided runs) |

Causes reported elsewhere: compilation **47%**, testing **36%**, checkout **12%**;
dependency-related errors are the largest category in build-log analysis.

**Why this matters, and it cuts against how we framed M-23.** We presented 49.7%
as evidence that CI failure was "the modal outcome half the time" — true, but the
implicit reading was that this is simply what CI is like. It is not. Our rate is
roughly **double the closed-source baseline** and above every figure we found.
That makes it a **property of this project**, not a general fact, and it
strengthens rather than weakens the environmental account: a project with an
unusually fragile build environment is exactly where you would expect
patch-unrelated failures to dominate (§3.2) and where size-independence (N-13)
should appear most clearly.

**It also demands a caveat we had not made.** A high failure rate in a
*framework-coupled, cross-repo, private-dependency* setting may be normal *for
that setting*, and none of the baselines above share it. The honest claim is
"unusually high against published baselines, which do not include a comparable
setting."

**Verdict: CHALLENGES US** (on framing), and **strengthens N-13** (on mechanism).

### 7.2 Failure clustering — a published claim we could test, which exposed an error in T9 **[secondary → own analysis]**

**Their claim.** In multi-project build analyses, *"for 10 projects, more than 50%
of failed builds follow a previous build failure."* Overall stability of recent
build history is reported as the strongest single influence on build outcome.

**Our test (new, T10 in [`../data/stats.py`](../data/stats.py)).** Grouping runs
by repository × workflow and walking them in time order:

- **409 of 477 failures (85.7%) are immediately preceded by another failure** —
  far above their >50% threshold.
- Outcome **transitions occur on only 15.9%** of consecutive pairs, against
  **49.9% expected** under independence.
- **Lag-1 autocorrelation = 0.680.**

**This confirms their claim and extends it — and then it broke one of our own
results.** An AR(1) deflation gives an **effective sample size of ~179 against a
nominal 940**. Two consequences, both corrections:

1. **M-23's "indistinguishable from a coin flip (exact binomial p = 0.28)" is
   withdrawn.** That test assumed independent runs. It is invalid, it has been
   removed from `stats.py`, and the failure proportion now stands as a **census
   fact requiring no test** — which is what it always should have been.
2. **M-27 / T9b — the 57% → 46% improvement — is demoted.** Nominal Fisher
   p = 0.0014; deflated to n_eff, **p = 0.18**. The improvement **does not survive
   as a statistically significant result.** It remains a real descriptive change
   in the observed proportions, and the qualitative account (permanent regression
   probes, converged dependency auth) is unaffected — but it can no longer be
   listed among the tested claims.

**What is *not* affected.** T9a (failure ⟂ commit size) and T9c (AI-trailered vs
not) are **per-commit** rather than per-run, where autocorrelation is weaker
(lag-1 = 0.429), and both are **nulls**. Autocorrelation inflates false positives;
a null that survives it is conservative. **N-13 stands.**

**Verdict: SUPPORTS their claim strongly (85.7% vs >50%) and CHALLENGES US —
the most valuable single outcome of this search round, because it caught a real
statistical error in our own work.**

### 7.3 Test size versus test quality — **the literature says our headline metric is the wrong one** **[secondary]**

**What the literature establishes.**

- **Assertions, not size, track effectiveness.** Zhang & Mesbah (FSE 2015),
  across 6,700 constructed suites and ~24,000 assertions in five real-world Java
  projects: *assertion count is strongly correlated with test-suite
  effectiveness.*
- **Coverage is not.** Inozemtseva & Holmes (ICSE 2014): coverage is **not**
  strongly correlated with effectiveness.
- **Size is a confounder.** A TOSEM (2025) analysis finds mutation-score↔fault-
  detection correlations are strong when suite size is *uncontrolled* but fall to
  roughly **0.05–0.20 when size is controlled** — most of the apparent
  association is a size effect.
- **And specifically for LLM-generated suites**, a 2026 replicability study
  (arXiv:2607.22880) finds *little evidence that suite size is a dominant
  confounder*, with size correlating only **weakly** with mutation score and
  real-bug detection.

**This is a direct challenge to how N-4 is stated.** Our **1.69:1 test-to-source
write ratio** is a **size** metric. The literature's consensus is that size is
precisely the wrong proxy for effectiveness, and it names the right one —
assertions — which is also exactly the axis on which this project's documented
failure occurred (`assertTrue(true)` hidden inside `willReturnCallback`).

**So we computed the better metric.** Measured on `origin/b-7.4.x`:

| Repo | Test methods | Assertions | Assertions/test | Mock creations/test | `willReturnCallback` |
|---|---|---|---|---|---|
| `stripe` | 1,194 | 2,722 | **2.28** | 0.55 | 87 |
| `payment-base` | 915 | 2,128 | **2.33** | 0.24 | 19 |

Two readings, and we should publish both. **Charitable:** ~2.3 assertions per test
method is a substantive density, consistent across two independently developed
packages — so the suite is not merely voluminous. **Sceptical:** 106
`willReturnCallback` occurrences remain in the trees, the exact construct that
concealed the project's hollow tests, and assertion *count* still says nothing
about assertion *strength*.

**Consequence for the claims.** N-4 should be restated as: *test-writing effort
was real and sustained (a size fact), and assertion density is moderate (a better
proxy) — but neither establishes effectiveness, which this corpus cannot measure
without mutation testing.* Running a mutation-testing pass over this suite is
now the single most valuable technical follow-up available, and it is feasible:
the code, the tests and the harness all still exist.

**Verdict: CHALLENGES US**, productively — and yields a new measurement and a
concrete follow-up.

### 7.4 Agentic-SE field studies — and the position directly opposed to ours **[abstract]**

**Monperrus, *The End of Code Review: Coding Agents Supersede Human Inspection*
(arXiv:2606.13175, June 2026).** Argues coding agents have crossed a capability
threshold at which human code review is no longer a necessary part of a quality
pipeline: every stated goal of review — defect detection, style, knowledge
transfer, team awareness — can be met by agents at lower cost and higher
throughput, and the "agents write, humans must review" arrangement is a dead end
that neither assures quality nor scales.

**This is the strongest published counter-position to our N-3**, and the paper
set is better for engaging it head-on rather than citing only the agreeable
Agarwal et al. (§5.2.2).

Three honest observations:

1. **Our case is a counterexample to the strong form.** In this project the
   agent-assisted pair did not detect its own behavioural defects: **a human
   filed 37 of 40 bugs**, and the developer using the AI filed **zero**. If agents
   could supersede human inspection here, that distribution should not look the
   way it does.
2. **But we must not overstate it, because the constructs differ.** Monperrus
   argues about *code review* — inspection of a diff. Our tester performed
   *black-box testing* against a running system. Those are different activities,
   and his argument does not obviously extend to the second. Our evidence bears on
   "can the agent-plus-developer pair find its own defects", not on "is diff
   review necessary".
3. **We fall inside his own carve-out.** He reserves a continuing human role for
   *"security-critical paths in regulated systems"* and changes whose correctness
   depends on requirements the agent was never given. A PCI-DSS-obligated payment
   module is exactly that. So our case is consistent with his position as stated,
   and only contradicts the loose popular reading of it.

**Verdict: COUNTEREXAMPLE to the strong/popular form; CONSISTENT with the paper
as written.** Cite it as the opposing pole and state the carve-out.

Also located but not yet read: *Early Adoption of Agentic Coding Tools by GitHub
Projects* (arXiv:2607.14037) and *Code Review Agent Benchmark* (arXiv:2603.23448).

### 7.5 PCI-DSS provenance — **our compliance claim is now sourced, and it is narrower than we wrote** **[secondary]**

**What we asserted.** In §6.6 of the flagship, that for a PCI-DSS-obligated
module "per-commit provenance is not a nicety" and a release procedure that
discards it is a finding in its own right. This was unsourced.

**What the standard actually requires.** PCI DSS **Requirement 6.4/6.5** governs
change control and requires, for each change: documentation of impact,
documented **approval by authorised parties**, **testing** of functionality, and
**back-out procedures** — with change-control records providing an **audit trail
of changes for accountability**. Requirement 6 also mandates secure SDLC
practice, code review and version control for policies and procedures.

**The honest correction.** The standard requires an **auditable change-control
record**; it does **not** specify that the record must be the git commit graph.
An organisation could satisfy 6.4/6.5 through a change-management system while
squashing its VCS history. So our claim must be narrowed to something we can
actually defend:

> Where a project's change-control evidence *is* its commit history — as it was
> here, with the dev log and commit trail serving as the only record of what
> changed, why, and with what testing — destroying that history at release
> removes the artifact the audit trail depends on.

That is a **conditional** claim about this project's practice, not a general claim
that squashing violates PCI DSS. We should not imply the latter, and §6.6
currently comes close to doing so.

**Verdict: CHALLENGES US.** Sourced, but narrower than asserted. Requires a
wording fix in the flagship §6.6 and in LL-5.

## 8. Summary

| # | Published problem | Our evidence | Verdict |
|---|---|---|---|
| 2.1 | Perils of mining coding-agent activity (MSR 2026) | trailers 0% → 86%, p = 5.2e-81; six models in four months; ground truth in Corpus A | **INSTANTIATES + SUPPORTS** |
| 1.2 | Self-report unreliable on AI-assisted productivity (METR) | journal undersampled 2.2×; epic understated 41%; idle period narrated as active | **SUPPORTS + EXTENDS** |
| 3.2 | Build failures unrelated to the patch (13.33%) | 49.7% failure rate; failure ⟂ change size (ρ = −0.024) | **SUPPORTS bidirectionally** |
| 2.2 | Rewritten-away vs never-collected provenance gaps | three loss mechanisms, one orphan recovered from a stale checkout | **INSTANTIATES** |
| 5.1 | Techniques detect different fault classes (Basili & Selby) | 4 refactoring-found vs 6 tester-found amount defects, zero overlap | **SUPPORTS (lineage)** |
| 2.3 | Agent-generated over-mocked tests (MSR 2026) | `assertTrue(true)` tests, 34% silent skips, rule R-1.5 — alongside a 1.69:1 write ratio | **INSTANTIATES + contributes** |
| 3.1 | Churn/commit-count predict build outcome | ρ = −0.024, Fisher p = 0.66 — no predictive value here | **COMPLICATES** |
| 4.1 | Two-thirds of developers keep office hours (ICSE 2018) | 0 Saturdays / 716, P = 1.2e-48; 95.9% in 08:00–20:00 | **SUPPORTS + extends** |
| 4.2 | Rising night/weekend commits (TGIF, EMSE 2025) | 0.14% weekend commits in 2025–26 | **COUNTEREXAMPLE (weak)** |
| 3.3 | CI theatre | 49.7% failure but a measured 11-point improvement | **COMPLICATES** |
| 1.3 | AI code introduces surviving debt | our CI-based null cannot see code smells | **CHALLENGES US** |
| 1.1 | Copilot RCT 55.8% faster | no control arm; dispersion 6.93 means no central rate to quote | **CANNOT ADDRESS** |
| 5.2.1 | Oversight burden characterised, never measured (Garousi) | V = 0.859 role separation; the tester, not the AI's user, bore it | **INSTANTIATES + sharpens** |
| 5.2.2 | "The team sets the sign, through how it structures review" — falsifiable proposition (Agarwal et al.) | one measured team; and they state our sign-flip problem independently | **SUPPORTS bidirectionally** |
| 5.2.5 | Ecosystem agent-adoption 22–29% (Feb 2026) | our 20.8% overall / 86% late is a project convention, not an adoption curve | **calibrates N-2** |

**The pattern.** Our strongest contributions are to the **methodology** of studying
AI-assisted engineering (§2), to the **CI-cost literature** (§3), and — after the
priority-1 search — as the **missing measurement** for an existing causal theory
of how team structure decides an agent's effect (§5.2). Not to the
productivity-effect literature (§1), where we have nothing a controlled study does
not have more of. That distribution matches
[`06-novelty-assessment.md`](06-novelty-assessment.md) §5's three-paper split
independently, which is mild evidence the split is right.

**Sources** are linked inline in §9.

---

## 9. Sources

- [The Impact of AI on Developer Productivity: Evidence from GitHub Copilot](https://www.microsoft.com/en-us/research/publication/the-impact-of-ai-on-developer-productivity-evidence-from-github-copilot/) — Peng, Kalliamvakou, Cihon, Demirer
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://arxiv.org/abs/2507.09089) — METR ([blog](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/))
- [Promises, Perils, and (Timely) Heuristics for Mining Coding Agent Activity](https://arxiv.org/abs/2601.18345) — MSR 2026 ([ACM](https://dl.acm.org/doi/10.1145/3793302.3793375), [artifacts](https://github.com/labri-progress/agent-mining))
- [Are Coding Agents Generating Over-Mocked Tests? An Empirical Study](https://arxiv.org/pdf/2602.00409) — Hora & Robbes, MSR 2026
- [Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild](https://arxiv.org/html/2603.28592v1) — Liu, Widyasari, Zhao, Irsan, Lo
- [Is this Build Failure Related to my Patch?](https://arxiv.org/html/2605.05564) — Huang, da Costa, Dick, El Mezouar
- [Was It Never Collected, or Rewritten Away?](https://arxiv.org/pdf/2607.02774)
- [Do programmers work at night or during the weekend?](https://dl.acm.org/doi/10.1145/3180155.3180193) — ICSE 2018
- [TGIF: the evolution of developer commit times](https://link.springer.com/article/10.1007/s10664-025-10767-2) — EMSE 2025
- [Comparing the Effectiveness of Software Testing Strategies](https://www.semanticscholar.org/paper/Comparing-the-Effectiveness-of-Software-Testing-Basili-Selby/3953558e92b1397c778cd450b4ca58da45932bcc) — Basili & Selby
- [Functional Testing, Structural Testing and Code Reading: What Fault Type Do They Each Detect?](https://link.springer.com/chapter/10.1007/978-3-540-45143-3_12)
- [Insights into Continuous Integration Build Failures](https://www.researchgate.net/publication/318124591_Insights_into_Continuous_Integration_Build_Failures)
- [Continuous Integration Theater](https://arxiv.org/pdf/1907.01602)
- [Individual differences limit predicting well-being and productivity using software repositories](https://link.springer.com/article/10.1007/s10664-021-09977-1) — EMSE 2021
- [Human Oversight and Overload: Two Hidden and Costly Burdens of AI-Assisted Software Engineering](https://arxiv.org/abs/2606.05770) — Garousi, June 2026
- [3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse](https://arxiv.org/abs/2607.07980) — Agarwal, Miller, Kästner, Vasilescu, July 2026
- [Agentic Much? Adoption of Coding Agents on GitHub](https://arxiv.org/abs/2601.18341) — TOSEM ([ACM](https://dl.acm.org/doi/abs/10.1145/3822180))
- [Agentic Very Much! Adoption of Coding Agent in New GitHub Projects](https://arxiv.org/abs/2606.07448)
- [Early Adoption of Agentic Coding Tools by GitHub Projects](https://arxiv.org/abs/2607.14037) — *not yet read*
- [Mining Issue Trackers: Concepts and Techniques](https://arxiv.org/html/2403.05716v1) — for the reporter-type lineage (Huo et al., Bettenburg et al., Zimmermann et al.)
- [The End of Code Review: Coding Agents Supersede Human Inspection](https://arxiv.org/html/2606.13175) — *not yet read; states the opposing position to §5.2.2*
