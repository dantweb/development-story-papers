# Literature Review — which published problems this corpus can speak to

*Written 2026-08-21*

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
| Failure share of runs | — | **487/979 = 49.7%** (indistinguishable from a coin flip, p = 0.28) |
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

### 5.2 Defect-reporting and role-separation literature **[secondary]**

**What we found, and did not find.** Searches surfaced work on defect-report
*quality* and on bug-report classification, and an observation that repositories
with testing frameworks and coverage tools report more bugs — but **no paper
directly formulating the question our strongest result answers**: in an
AI-assisted team, *who* generates the defect reports?

**Our result (N-3).** Reporter × issue type in Jira is near-deterministic: the
developer working with the assistant filed **52 Stories and zero Bugs**; a
dedicated tester filed **37 of the project's 40 Bugs (92.5%) and zero Stories**;
a project manager filed **26 of 50 Tasks and nothing else**. Fisher exact on the
2×2 **p = 6.7e-26**; full table **χ² = 199.4, df 6, Cramér's V = 0.859**.

Two consequences for the literature:

1. **The "solo developer + agent" framing that dominates AI-assisted-development
   discourse is an artifact of whose record is read.** This QA function is
   invisible in the developer's journal (Corpus A) and invisible in git (which
   sees only committers). It appears only in the issue tracker. Studies drawing on
   commits or developer self-report will systematically omit it.
2. **Productivity attribution is confounded by unmeasured QA capacity.** Our
   result cannot size that confound — but it can demonstrate that it exists and is
   large in at least one case.

If this gap is real after a proper search, N-3 is the most novel finding in the
programme. If prior work has posed it, our contribution narrows to a quantified
instance. **This is the highest-priority literature question outstanding.**

**Verdict: possibly a GAP; at minimum a quantified instance.** Requires a targeted
search before any novelty claim (§7).

---

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

## 7. Priority searches still outstanding

Ordered by how much a novelty claim depends on them.

1. **Role separation / who files defects in AI-assisted teams** (§5.2). N-3 is our
   strongest result and we have not found the literature that would tell us
   whether it is new. Search: QA role in AI-assisted teams; defect-report
   provenance; issue-tracker reporter analysis.
2. **Self-report vs artifact divergence in engineering journals** (§1.2). METR
   covers perceived productivity; we claim divergence in *documented activity*.
   Search: diary-study validity in SE, developer-log accuracy, experience
   sampling vs repository mining (the EMSE 2021 work on individual differences
   limiting repository-based prediction is a likely anchor).
3. **Test volume vs test honesty** (§2.3). Is over-mocking correlated with or
   orthogonal to test quantity in agent-authored suites?
4. **Agentic-SE field studies** rather than benchmarks. *Agentic Very Much!*
   (arXiv:2606.07448) and *3100 Opinions on Code Review in an AI World*
   (arXiv:2607.07980) both look adjacent and neither has been read.
5. **CI failure rates in industrial closed-source projects.** Our 49.7% needs a
   comparison baseline; most published rates come from open-source CI corpora and
   may not be the right comparison.
6. **PCI-DSS / regulated-domain provenance requirements.** Our §6.6 claim that
   commit provenance is a compliance artifact is asserted, not sourced.

---

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
| 5.2 | Who files defects in AI-assisted teams | Cramér's V = 0.859 role separation; tester filed 92.5% of bugs | **possible GAP** |

**The pattern.** Our strongest contributions are to the **methodology** of studying
AI-assisted engineering (§2) and to the **CI-cost literature** (§3), not to the
productivity-effect literature (§1), where we have nothing a controlled study
does not have more of. That distribution matches
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
- [Agentic Very Much! Adoption of Coding Agent in New GitHub Projects](https://arxiv.org/pdf/2606.07448) — *not yet read*
- [3100 Opinions on Code Review in an AI World](https://arxiv.org/pdf/2607.07980) — *not yet read*
