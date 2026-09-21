# X-01 — Five Articles That Confirm, Disprove or Extend Published Research

*Written 2026-09-21 · a review of reports 00–08 and the `data/` corpus, followed
by five concrete article proposals, each positioned against named published work*

The eight reports before this one did three things in sequence: they mined a
self-account ([`01`](01-flagship-paper-ai-assisted-payment-module.md),
[`02`](02-topics-project-management.md)–[`05`](05-measurements.md)), audited it
against four machine records and published the corrections
([`05`](05-measurements.md), [`06`](06-novelty-assessment.md),
[`07`](07-lessons-learned.md)), and then located the published work each result
speaks to ([`08`](08-literature-review.md)). What the set still lacks is the
step a reviewer or an editor actually needs: **which articles to write, against
which papers, taking which position.** This report supplies that. It offers
**five articles**, each with a declared stance toward specific published
research — **CONFIRMS**, **DISPROVES**, or **ENHANCES** — the evidence it rests
on (by stable `N-` / `M-` / `T-` identifier), the concession a reviewer will
demand, the work still outstanding, and the gate it must clear.

---

## 0. How to read this

### 0.1 Three stances, and what each can mean at n = 1

[`08`](08-literature-review.md) §0 grades every contact with the literature on
a six-way scale. For article proposals three coarser stances are more useful,
and each has a precise meaning in a single-subject study:

| Stance | Meaning here | What it can never mean |
|---|---|---|
| **CONFIRMS** | We reach the same conclusion as a published study **by an independent route** — different instrument, different setting, same direction. | A replication. One project cannot re-estimate an effect size or reproduce a distribution. |
| **DISPROVES** | We supply a **counterexample to a claim read as universal**, or show a published **predictor carries no signal in a documented setting**. | A refutation of an RCT or a survey. n = 1 refutes universality, not tendency. |
| **ENHANCES** | We supply what the published work states it lacks: **the measurement** for a qualitative claim, **the mechanism** for an observed correlation, **the ground truth** for an inferred label, or **a witness** for a hypothesised loss. | A generalisation. What we add is a documented instance, fully instrumented. |

A single article can take more than one stance toward more than one paper.
Each proposal below states all of them, and states the primary one first.

### 0.2 Evidence classes carried over

Every number cited below already exists in [`05`](05-measurements.md) or
[`07`](07-lessons-learned.md) and is recomputed by
[`../data/stats.py`](../data/stats.py). Grading is inherited unchanged:

- **Tier S** — a statistic and a p-value (T1–T10 in `07`).
- **Tier D** — a complete enumeration needing no inference.
- **Tier N** — one incident, verified against the artifact.
- **Tier U / X** — underpowered or unsupportable; **excluded** from every
  proposal here as evidence, permitted only as explicitly labelled context.

### 0.3 Two constraints inherited from `08`

1. **Nothing below may be cited from this document.** Several of the papers
   engaged are marked **[abstract]** or **[secondary]** in
   [`08`](08-literature-review.md) §9 and must be read in full before a venue
   draft names them. The "Still to do" block of each proposal lists which.
2. **No causal claim about AI's effect.** No control arm, one operator, six
   model generations inside the window. Every proposal is an observational
   case that confirms, contradicts or instruments a published claim; none
   attributes an outcome to the assistant.

---

## 1. Review of the previous work

### 1.1 What the eight reports established

The programme's method is stable and worth stating once: **use corpora B, C, D
and E to test corpus A**, and publish the divergences. Its outcomes fall into
four groups, and the five articles draw from all four.

| Group | Contents | Where |
|---|---|---|
| **Tested results** (Tier S) | role separation V = 0.859; test/source 1.69:1 with CI [1.39, 2.06]; trailer step-change p = 5.2e-81; dispersion 6.93; zero Saturdays P = 1.2e-48; issue→code by type p = 2.9e-10; CI failure ⟂ commit size p = 0.66; failure clustering 85.7% | `07` "Tier S", `06` §2.0 |
| **Census facts** (Tier D) | 2.2× undersampling; 0/61 fabricated refs; 491 commits only on `LEGACY`; 234/979 runs on no surviving ref; 49.7% CI failure; 169.5 h CI wall-clock; **MSI 70%** (1,592 / 1,123 / 469) | `05` M-11, M-17, M-20, M-23, M-24, M-30 |
| **Retractions** | "single-developer" (twice); AI authorship before 2026-05-07; PM-1 "refuted" → underpowered; M-23 coin-flip test; M-27 trend p = 0.0014 → 0.18; the first three mutation scores | `00` §4, `05` M-27, M-30, `08` §7.2 |
| **Literature contacts** | 16 graded entries, incl. two that broke our own results (`08` §7.2, §7.3) and one search that reframed our strongest finding from "gap" to "missing measurement" (`08` §5.2) | `08` §8 |

Two features of this record matter for what follows. First, **the strongest
results are methodological**, and [`06`](06-novelty-assessment.md) §5 already
splits them into three papers — an audit paper, a negative-results paper, and a
CI-cost paper. Second, **the corrections are the most credible part**, and the
articles below keep them in the text rather than in a footnote.

### 1.2 What this review re-verified

Two claims from the first, retracted mutation run were carried into `08` §7.3
and never re-checked against the corrected 1,592-mutant data. This review
checked them against `../data/mutation_escaped.csv` (469 rows):

| Claim (from the 462-mutant run) | On the corrected run | Status |
|---|---|---|
| `AmountConverter`, `MinorUnitConverter`, `CapturableAmount` have zero escaped mutants | **0 of 469 rows** name any of the three files | ✅ **holds** — and is now stated on a set 3.4× larger |
| Weakest files: `StripeRefundRequestHandler` 27, `StripePaymentStatusHandler` 22, `CheckoutSessionService` 22 | `StripeCaptureRequestHandler` **54**, `StripeCheckoutSessionHandler` **36**, `ReturnSessionSecurityService` **34**, `CaptureService` 27, `StripeReturnResolver` 23 | ⚠️ **superseded** — the refund handler fell to 8 after Sprint 135 (M-30) |
| Top escaped mutator `MethodCallRemoval` 28 of 122 | `MethodCallRemoval` **85 of 469**, then `ArrayItem` 78, `ArrayItemRemoval` 70, `ReturnRemoval` 27, `Coalesce` 25 | ✅ direction holds; **numbers stale** in `08` |

The first row is the one that matters for Article 5: the positive half of the
mutation result — that consolidating money arithmetic into value objects made
it fully verified — **survives the re-measurement**, and can now be stated
without the caveat that it came from a truncated draw.

### 1.3 Corrections queue — stale figures found in this review

Three re-measurements in August 2026 (M-30's determinism fix, M-27's
demotion, M-23's withdrawn test) were propagated to `05`, `06` §2 and `07`'s
Tier S table but **not everywhere**. The following are stale and should be
fixed before any article below is drafted, because each is the kind of
internal inconsistency a reviewer will find first. **None has been applied by
this review**; the list is the deliverable.

| File : line | Stale text | Should read |
|---|---|---|
| `README.md` : 25 | "Infection over **462 mutants**" | 1,592 mutants (462 was the retracted first run) |
| `README.md` : 75–76 | "CI hardening **measurably worked** … (**p = 0.0014**)" | descriptive 57% → 46%; **p = 0.18** after autocorrelation correction; not a tested claim |
| `reports/00-README.md` : 21 | corpus E "over **462 mutants**" | 1,592 |
| `reports/01-…flagship…` : 1385, 1514 | "p = 0.0014" as the CI-trend result; Appendix A row "D confirms A" | p = 0.18 (demoted); "D **describes** the same direction; not significant" |
| `reports/01-…flagship…` : 1568 | Appendix C — `mutation_escaped.csv` "**122**" rows | 469 |
| `reports/03-topics-technical.md` : 411, 420 | TECH-4 verification block cites the trend at p = 0.0014 as a gain for the topic | demote to descriptive, cite `08` §7.2 |
| `reports/06-novelty-assessment.md` : 556 | Paper-3 spine table "Hardening works, measurably … p = 0.0014" | contradicts `06` §2 N-13 two pages earlier; demote |
| `reports/08-literature-review.md` : 333 | §3.3 cites the 11-point improvement at p = 0.0014 as evidence against "CI theatre" | descriptive only |
| `reports/08-literature-review.md` : 737, 829 | "`MethodCallRemoval` **28 of 122**" (§7.3 item 2 and §8 summary row 2.3); §7.3 item 1's file list | 85 of 469; file list per §1.2 above |
| `reports/07-lessons-learned.md` : 729 | "Sub-sprint decomposition … **Measured and refuted**" | contradicts Tier U (same file, line 521–545) and line 582; should read "failed on its own terms; comparison underpowered (p = 1.00)" |
| `reports/07-lessons-learned.md` : 131–165 | LL-3 has **two items numbered 2b and two numbered 5**, and lesson 3 contains two overlapping sentences with different file lists (the old run's and the new run's) | renumber; keep the corrected list only |

Everything else spot-checked in this review — the T-table in `07`, `06` §2.0,
`05` M-28…M-30, and `data/README.md` — is consistent with the corrected
figures.

---

## 2. How the five were chosen

Sixteen literature contacts in [`08`](08-literature-review.md) §8 reduce to
five articles under four filters, applied in order:

1. **A named published claim must be engaged.** Not "the literature says" —
   a specific paper, with a specific proposition we confirm, contradict or
   instrument.
2. **The evidence must be Tier S or Tier D.** Tier U and Tier X material is
   out. This alone removes N-5 (disjoint defect yields) as a lead result.
3. **The stance must be defensible at n = 1** under §0.1 — so no article
   claims to refute an effect-size estimate or to generalise a rate.
4. **Each article must be separable from the others** on venue, gate, or
   theory engaged, so that a delay on one does not block the rest.

The result maps onto [`06`](06-novelty-assessment.md) §5's three-paper split
with two changes: **N-3 is pulled out of the audit paper** into its own article
(Article 3), because it engages a distinct published theory and carries the one
gate — named-colleague consent — that would otherwise hold the audit paper
hostage; and **the mutation result is pulled out of LL-3** into its own article
(Article 5), because its literature engagement is with the test-effectiveness
lineage and with a tool-reproducibility question that the testing-conference
talk cannot carry.

| Article | Primary stance | Toward | `06` paper | Gate |
|---|---|---|---|---|
| **1** | CONFIRMS + ENHANCES | METR (self-report vs measured) | Paper 1 (the audit) | employer |
| **2** | DISPROVES (in setting) + CONFIRMS | build-failure prediction; Huang et al.; clustering benchmark | Paper 3 (CI cost) | **none** |
| **3** | ENHANCES + DISPROVES (strong form) | Agarwal et al.; Garousi; Monperrus | split from Paper 1 | **named-colleague consent** |
| **4** | ENHANCES | Robbes et al.; the commit-provenance dataset | Paper 2 (negative results) | employer |
| **5** | CONFIRMS (against ourselves) + ENHANCES | Zhang & Mesbah; Inozemtseva & Holmes; Hora & Robbes; MSI reporting practice | split from LL-3 | **none** |

---

## 3. The five articles

Each proposal has the same eight blocks: working title; stances; the published
claims engaged; our evidence; the argument; what we add that the cited work
cannot have; what a reviewer will say and how we concede it; still to do,
venue, gate, effort.

---

### Article 1 — *Imprecise about volume, not only optimistic about speed: auditing a daily AI-assisted engineering journal against its own commit, issue and CI records*

**Stances.** **CONFIRMS** METR's central finding by an independent route;
**ENHANCES** it with a taxonomy of self-report error that METR's instrument
cannot produce; **CONFIRMS** Claes et al. (ICSE 2018) on office-hours work at
the extreme; **ENHANCES** Agarwal et al.'s diagnosis of trace mining by
supplying its mirror image.

**Published claims engaged.**

| Paper | Claim | Read status (`08`) |
|---|---|---|
| METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity* (arXiv:2507.09089) | 16 developers, 246 tasks: AI made them **19% slower** while they estimated **20% faster** — practitioner self-report about AI-assisted work is unreliable | [secondary] |
| Claes, Mäntylä, Kuutila, Adams, *Do programmers work at night or during the weekend?* (ICSE 2018) | two-thirds of developers keep office hours; hired developers more so | [secondary] |
| Agarwal, Miller, Kästner, Vasilescu (arXiv:2607.07980) | repository traces "establish what is changing without explaining why" | [abstract, verbatim] |

**Our evidence** — all Tier D (complete enumeration) unless marked:

| Divergence between journal and record | Magnitude | Id |
|---|---|---|
| Active days documented vs active days with commits | 47 vs **105** in-window — **2.2×** undersampled | N-1, M-11 |
| Flagship epic insertions | +11,204 reported vs **+15,844** measured — **41% understated** | M-2 |
| March–April 2026, narrated as active | **9.1 h** of commit-bearing activity in two months | M-11 |
| "Simplification" 330 → 107 lines | one file; module handler code **2,616 → 2,953** in the same commit | M-9, §4.11 |
| Actor inventory | journal: one developer + assistant; Jira: **10 reporters**, a tester filing 92.5% of bugs *(Tier S, see Article 3)* | M-18 |
| Project scope | journal: 7 months; Jira: **3 years**, 35% of issues predating the commit record | M-21 |
| Work rhythm *(Tier S)* | 0 Saturdays / 716, P = 1.2e-48; 95.9% inside 08:00–20:00 | T4, M-14 |

**The argument.** METR showed that developers' *perception of AI's effect on
their speed* was wrong by about 39 points against a task clock. This article
shows that a **candid, daily, artifact-linked engineering journal** — the best
case for self-report, written by an engineer who documented failures as
carefully as successes — still diverged from the project's own machine records
in **five directions at once**: it undersampled activity, understated volume,
over-reported continuity, omitted actors outside the author's role, and framed
a three-year project as a seven-month one. The direction is informative: METR's
subjects were *optimistic about effect*; our journal was *imprecise about
volume* — it **understated** its own flagship output. Self-report error in
AI-assisted work therefore has at least two independent components, and a study
correcting for one does not correct for the other.

**What we add that METR cannot have.** METR's instrument is a clock in a
controlled task. Ours is the full artifact trail of an uncontrolled ten-month
project, so we can say *which kinds* of claim drift and *in which direction*,
not only *that* perception drifts. And we have the piece Agarwal et al. say
trace mining lacks — the *why*, in the journal — sitting next to the machine
record of the *what*. The two papers are complementary halves and should be
cited as such.

**What a reviewer will say, and the concession.**
- *"This is one journal by one person."* Yes; the claim is existence, not
  frequency: a journal of this quality can still diverge this much. State it
  as a lower bound on the problem.
- *"Discipline over cleverness is asserted, not shown."* Agreed, and it is
  removed as the thesis. [`06`](06-novelty-assessment.md) §1 already makes
  this call; the article leads with the audit and demotes the harness account
  to background.
- *"The office-hours result has an obvious alternative explanation."*
  Employment context. Stated up front; claimed only as a confirmation of Claes
  et al.'s hired-developer observation, and a weak counterexample to the *TGIF*
  intensification trend (EMSE 2025), not as a property of AI assistance.

**Still to do.** Read METR and Claes et al. in full. Rewrite the flagship
under the new title with `06` §5.1's allocation: N-1 as the contribution, the
Tier S results as evidence, the retractions in the body. Apply the corrections
queue (§1.3) first — a paper about auditing self-reports cannot carry a stale
p-value. Decide whether N-3 appears here as one row of the divergence table
(role-anonymised, numbers only) or is held for Article 3; recommended: **one
row, anonymised**, with the full development in Article 3.

**Venue.** EMSE or ICSE-SEIP (a methods result about a data source the field
depends on). MSR as fallback. **Gate:** employer approval; the security audit
material is excluded entirely. **Effort:** medium — the flagship is most of the
text; the work is cutting, not writing.

---

### Article 2 — *Churn predicts nothing here: build failure independent of change size in a framework-coupled, cross-repository project*

**Stances.** **DISPROVES**, within a documented setting, the predictive
usefulness of churn and commit-count features from the build-failure
prediction literature; **CONFIRMS** Huang et al.'s mechanism (patch-unrelated
failures) and supplies an extreme case of it; **CONFIRMS and extends** the
published failure-clustering benchmark; **COMPLICATES** *Continuous Integration
Theater*.

**Published claims engaged.**

| Paper | Claim | Read status |
|---|---|---|
| TravisTorrent-era build-failure prediction (survey and empirical work, `08` §3.1) | churn and number of commits per build are among **the most important predictors** of build outcome | [secondary] |
| Huang, da Costa, Dick, El Mezouar, *Is this Build Failure Related to my Patch?* (arXiv:2605.05564) | **13.33%** of failures across seven Apache projects are potentially unrelated to the patch; developers spend a median **4 h** deciding | **[full-text]** |
| Multi-project build analyses (`08` §7.2) | for 10 projects, **>50%** of failed builds follow a previous failure; recent history is the strongest single predictor | [secondary] |
| Published failure-rate baselines (`08` §7.1) | closed-source **26%**, large long-lived **19%**, Java OSS **>38%**, hardware-in-the-loop **~12%** | [secondary] |
| *Continuous Integration Theater* (arXiv:1907.01602) | CI adopted without the practices that make it meaningful | [secondary] |

**Our evidence** — Corpus D joined to B, all reproducible via `stats.py`
T9a, T9c, T10:

| Result | Value | Tier | Id |
|---|---|---|---|
| Failure ⟂ commit size | ≥500 insertions: **63%** fail; <500: **60%**; Fisher **p = 0.66**; Spearman **ρ = −0.024** | S (null) | N-13, T9a, M-25 |
| Failure clustering | **85.7%** of failures follow a failure (benchmark >50%); transitions 15.9% vs 49.9% expected; lag-1 **ρ₁ = 0.680** | S | T10, M-28 |
| Failure rate | **487 / 979 = 49.7%**, roughly **2×** the closed-source baseline and above every published figure found | D | M-23 |
| Cost | **169.5 h** CI wall-clock vs ≈140 h human session time; **90.1 h (53%)** in failing runs | D | M-24 |
| AI-trailered commits no more fragile | 59% vs 61%, p = 0.88 — **confounded null, reported as such only** | S (null) | T9c, M-26 |
| Hardening trend | 57% → 46% across 2026-04-01 — **descriptive only; p = 0.18 after autocorrelation correction** | withdrawn | M-27 |

**The argument.** Write it as a hypothesis test, not an absence of evidence.
The competing account — that these failures were defects in changed logic —
makes a falsifiable prediction: failure probability rises with the volume of
changed logic. Across 444 commits with CI it does not rise at all;
ρ = −0.024, and the two framings (threshold split, rank correlation) disagree
in *sign*, which is itself evidence that neither direction is real. The
environmental account survives *because* the logical account's prediction
failed. Huang et al. supply the mechanism: where failures are unrelated to the
patch, size cannot predict them; in the limit, as the unrelated share grows,
the correlation vanishes. Our project — with a failure rate double the
closed-source baseline and failures arriving in runs of 0.68 autocorrelation —
is that limit approached. The clustering result then does double duty:
substantively it is what a broken-environment account predicts and a
defects-in-code account does not; methodologically it is what **invalidated
two of our own earlier tests** (`08` §7.2), and the article says so.

**What we add that the cited work cannot have.** Huang et al. *measure*
relatedness by hand on Apache projects with failure rates far below ours; we
supply the extreme end of their phenomenon, a size-independence result their
framing predicts but does not test, and the cost side (machine time exceeding
human time) that a relatedness study does not compute. The prediction
literature reports churn as predictive on aggregate; we document a setting —
framework-coupled, cross-repository, private-dependency — that none of its
corpora include and in which the feature family carries no signal.

**What a reviewer will say, and the concession.**
- *"`failure` is friction, not defect density."* Correct, and it is the
  point: half of all pipeline outcomes were friction indifferent to the code.
  Say so in the abstract.
- *"You infer patch-unrelatedness from an absent correlation; Huang et al.
  measure it."* Correct. **The article must include a hand-classified sample
  of failing runs against Huang et al.'s cause taxonomy** — this is the single
  most valuable addition `08` §3.2 identifies, and without it the paper is
  weaker than its companion.
- *"Your improvement claim is not significant."* Already withdrawn; report
  57% → 46% as direction only, with the p = 0.18 in the text.
- *"49.7% might be normal for your setting."* Conceded: the baselines do not
  include a comparable setting. Claim "unusually high against published
  baselines, none of which share this setting."
- *"One project."* The non-association is established *here*, and appears so
  cleanly partly *because* the failure rate is an outlier.

**Still to do.** (1) **Hand-classify a random sample of failing runs**
(target: 100 of 487) against Huang et al.'s taxonomy — unrelated tests,
external interference, environment, non-reproducible, concurrent commits,
configuration — from run logs. **Risk:** GitHub's run-retention window
(`data/README.md`) may already have discarded the logs for older runs; check
availability *first* and, if a large share is gone, report that as a fourth
provenance-loss instance rather than silently sampling survivors. (2) Replace
the AR(1) deflation with a mixed model with workflow random effects (M-28's
own caveat). (3) Read the prediction-literature sources and the clustering
source in full. (4) Decide whether N-5 (disjoint defect yields) appears as a
labelled *observation* in the discussion; recommended yes, one paragraph,
Basili & Selby cited as lineage, no test claimed.

**Venue.** MSR (repository-mining result) or ESEM (empirical hypothesis test;
arguably the better fit). ICSE-SEIP as fallback. **Gate:** none — no named
individuals, no security material; **this is the ungated article and should
go first.** **Effort:** low to medium; data, joins and tests exist. The
hand-classification is the only new measurement.

---

### Article 3 — *The team set the sign: a measured case of role-separated oversight in an AI-assisted project*

**Stances.** **ENHANCES** Agarwal et al. by supplying artifact-derived
measurement for a proposition that rests on practitioner discourse;
**ENHANCES** Garousi by answering the question the oversight-burden framing
does not ask — *who* bears it; **DISPROVES** the strong, popular reading of
Monperrus's *End of Code Review* while remaining **consistent** with the paper
as written.

**Published claims engaged.**

| Paper | Claim | Read status |
|---|---|---|
| Agarwal, Miller, Kästner, Vasilescu, *3100 Opinions on Code Review in an AI World* (arXiv:2607.07980) | 26 constructs, 67 relationships from 3,100 coded documents; verbatim: *"review is the control point through which a coding agent's effect on software is decided, and … AI does not fix the sign of that effect: the team sets it, through the expertise its humans bring and how it structures the review process."* | [abstract, verbatim] |
| Garousi, *Human Oversight and Overload* (arXiv:2606.05770) | oversight of AI-generated artifacts is a hidden, costly, non-optional burden — characterised qualitatively, **no measurement, no role analysis** | [abstract] |
| Monperrus, *The End of Code Review: Coding Agents Supersede Human Inspection* (arXiv:2606.13175) | human code review is no longer necessary; reserves a role for "security-critical paths in regulated systems" | [abstract] — **not yet read** |
| Reporter-type issue mining (Huo et al.; Bettenburg; Zimmermann — `08` §5.2.3) | developer-vs-user reports differ; reporter attributes predict fix time | [secondary] |

**Our evidence:**

| Result | Value | Tier | Id |
|---|---|---|---|
| Reporter × issue type | developer: **52 Stories / 0 Bugs**; tester: **0 Stories / 37 Bugs** (92.5% of 40); PM: 26 Tasks only | S | N-3, T2, M-18 |
| Strength | Fisher on `[[52,0],[0,37]]` **p = 6.7e-26**; full table **χ² = 199.4**, df 6, **p = 2.6e-40**, **Cramér's V = 0.859** | S | T2 |
| Issue → code conversion by type | Story **69%**, Bug **42%**, Task **8%**; χ² = 47.4, **p = 2.9e-10** | S | T6, M-19 |
| Requirements arriving *from* QA | tester filed payment-blocking bug `STRP-116` (2026-04-01) → wrote requirements task `STRP-129` (2026-04-20) → became the validation sprint | N (dated chain) | N-9, LL-6 |
| Triage path out of the component | 6 of 40 bugs reclassified (3 `Not a bug`, 3 `Core Bug`) | D | M-5 |
| Invisibility in the usual sources | the tester appears in **neither** the journal **nor** git | D | N-3 |

**The argument.** Agarwal et al. turned "AI is changing code review" into
falsifiable propositions and named the moderator: how the team structures
review. Their evidence is discourse at scale; they say themselves that
repository traces show *what* changes without *why*, and that trends flip under
equally defensible analysis choices. We have one team, fully instrumented, and
the structure it chose is measurable to near-determinism: the engineer using the
assistant produced requirements and code and filed **zero** defects against the
result; a separate human produced almost all defect discovery. That is a
measured data point on their central proposition. It also answers the half of
Garousi's question he does not ask — the burden was not merely large, it was
**borne by a distinct role**, which changes what mitigating it means: "teams
should handle oversight" and "teams need a person whose job is oversight" are
different recommendations, and only the second follows from this measurement.
Against Monperrus, the case is a counterexample to the *strong* reading — here
the agent-plus-developer pair did **not** find its own behavioural defects —
while sitting squarely inside his own carve-out for regulated, security-critical
systems, which a PCI-DSS-obligated payment module is.

**What we add that the cited work cannot have.** A near-deterministic
association (V = 0.859) from a tracker export, sitting beside the journal that
explains the mechanism — the two halves Agarwal et al. say cannot be had from
one source. And a construct distinction the debate needs: our tester performed
**black-box testing of a running system**, not diff review; Monperrus's argument
is about diff review. Our evidence bears on "can the pair find its own
behavioural defects," not on "is diff review necessary," and the article says
so rather than letting the reader conflate them.

**What a reviewer will say, and the concession.**
- *"One team's structure cannot test a proposition about team structure."*
  Correct. Position as **hypothesis-testing on a single case** with a named
  theory, not as discovery; and specify the cheap multi-case replication (§
  "Still to do").
- *"Roles are inferred from what people filed, not from job titles."*
  Conceded; corroboration from the two people concerned turns inference into
  fact and costs two sentences (`06` §6 item 3).
- *"You cannot size the burden."* Correct — Jira time fields are empty for all
  156 issues. Report the *distribution* of oversight, not its *cost*.
- *"The reporter-type lineage already exists."* Yes, for developer-vs-user
  and for fix-time prediction. Cite it as precedent for the method; the
  contrast (AI's user vs dedicated tester) and the outcome (who generates
  defect discovery at all) are different.

**Still to do.** (1) **Consent and corroboration in one conversation**: show
the tester and the project manager the numbers and the framing; ask for a
two-sentence confirmation of roles; offer draft review and co-authorship.
(2) **Anonymise by role** in every external version — the finding is about
structure and loses nothing without names. (3) Read Agarwal et al. and
Monperrus in full; the latter is currently unread and is engaged only through
its abstract. (4) Write the replication design: reporter × issue-type on
several AI-assisted projects with differing QA staffing — needs only tracker
exports, and turns a data point into a result.

**Venue.** ICSE-SEIP or EMSE for the research version; LeadDev for the
practitioner version (LL-6), which sizes teams and is exactly the decision this
informs. **Gate:** **named-colleague consent** (hard), plus employer
approval. **Effort:** high — the writing is moderate, the gate is the work.
Do not rush it.

---

### Article 4 — *Ground truth for the perils: a single-project case for what commit traces of coding agents can and cannot show*

**Stances.** **ENHANCES** Robbes et al.'s catalogue of perils with a
fully-instrumented single-project instance of each; **ENHANCES** the
commit-provenance dataset's two-way framing with a recovered witness and a
third loss mechanism it does not cover; **calibrates** against the *Agentic
Much?* adoption estimates; supplies a small **negative result** on identifier
fabrication.

**Published claims engaged.**

| Paper | Claim | Read status |
|---|---|---|
| Robbes, Matricon, Degueule, Hora, Zacchiroli, *Promises, Perils, and (Timely) Heuristics for Mining Coding Agent Activity*, MSR 2026 (arXiv:2601.18345) | agent traces in repositories are **partial**, from **heterogeneous** agents, **rapidly changing**, and can be **lost** | [abstract + venue metadata] |
| *Was It Never Collected, or Rewritten Away?* (arXiv:2607.02774) | a missing commit is either rewritten away upstream or never ingested; a dataset to separate the two | [secondary] |
| *Agentic Much?* (TOSEM, arXiv:2601.18341) and *Agentic Very Much!* (arXiv:2606.07448) | ecosystem agent adoption **22.20%–28.66%** as of 2026-02-21; higher in new projects | [secondary] |

**Our evidence:**

| Their peril | Our instrumented instance | Tier | Id |
|---|---|---|---|
| Data is **partial** | `Co-Authored-By: Claude*` on **149 / 716 (20.8%)** | D | M-16 |
| Traces appear **over time** | **2/466 (0.4%)** before 2026-05-07 vs **147/250 (58.8%)** after; Fisher **p = 5.2e-81** — a convention adopted, not a practice emerging; the journal independently documents heavy AI use throughout the 0% period | S + A | N-2, T3 |
| **Heterogeneous** agents | **six model strings in four months** (Opus 4.7 → 4.8 → 5, Sonnet 4.6, Fable 5, unversioned) | D | M-16 |
| Traces are **lost** — mechanism 1 | 2026-07-02 release squash; 562 files re-added; **491 commits** survive only on `b-7.4.x-LEGACY` | D | N-6, M-17 |
| Lost — mechanism 2 | merged branches pruned; `ce96dc86085b` (25 files, +1,710/−60) on **no remote ref**, recovered only from a stale checkout; now a dangling object | D + N | N-6, M-17 |
| Lost — mechanism 3 (**not in their framing**) | **234 / 979 CI runs (24%)** point at `head_sha` on no surviving ref; GitHub's retention window silently discards older runs | D | `data/README.md`, `08` §2.2 |
| Identifier fabrication | **0 of 61** distinct ticket refs fabricated across 436 ticket-bearing commits; **1** misattributed (`STRP-138`/`139`) | D + N | N-8, M-20 |
| Adoption calibration | 20.8% overall, **86%** by August 2026 — far above the 22–29% ecosystem estimate for the period, i.e. a project convention, not an adoption curve | D | `08` §5.2.5 |

**The argument.** Robbes et al. catalogue perils at ecosystem scale and cannot,
by construction, have ground truth for untrailered commits. We have it: a daily
journal that documents heavy assistant use through seven months in which trailer
coverage was **0%**. So we can show something an ecosystem study cannot — that
the trailer series is **uninformative as a time series of AI involvement**, and
that a trend line fitted through it describes a convention being rolled out.
On loss, the provenance dataset separates "rewritten away" from "never
collected"; we are a primary-source case of the first with a **recovered
witness**, plus a mechanism their two-way framing does not cover: CI history
that outlives its commits and then expires on a retention schedule. The
methodological payload is uncomfortable and worth stating plainly: **none of the
three losses is detectable from inside the repository**, and the second was
found only because a stale checkout happened to exist on the same machine. A
study cannot in general distinguish "rewritten away" from "never happened" even
with full repository access.

**What we add that the cited work cannot have.** Ground truth for the
untrailered period (from Corpus A); a *dated* adoption step with a test behind
it; a recovered orphan commit as physical evidence of routine branch-pruning
loss; and a third loss channel outside version control. Plus the small negative
result: the commonly feared failure (hallucinated identifiers) did not occur in
436 ticket-bearing commits; the failure that did occur was conflation.

**What a reviewer will say, and the concession.**
- *"These are known perils."* Yes — the paper is a companion case, not a new
  catalogue. Its value is that each peril is shown biting inside one project
  with the whole artifact available, and quantified.
- *"One orphan commit is 0.14% of the record."* Conceded and stated; the
  point is not magnitude but **detectability** — the loss was invisible from
  inside, and there is no witness for losses before 2026-05-22.
- *"The PCI-DSS angle overreaches."* Already narrowed in `08` §7.5: the
  standard requires an auditable change-control record, not the commit graph.
  State the conditional form only — *where the commit history is the
  change-control evidence, as here, squashing destroys the artifact the audit
  depends on.*

**Still to do.** (1) Read Robbes et al. in full and consult their public
artifacts (`labri-progress/agent-mining`) — if their heuristics can be run on
our repositories, do it and report agreement with the journal's ground truth
per period. (2) Read the provenance dataset paper in full; check whether CI
retention is genuinely outside its framing or merely outside its abstract.
(3) Fold in `06` §5.2's remaining negative results — no reliable unit of work
(N-10: 39% of commits ticketless, umbrella issues), and **effort data absent
from all five corpora** — as further instances of "every corpus is
compromised." (4) Externally, describe commits by role and size, not by hash
(`07` gate 2).

**Venue.** MSR — the natural companion to Robbes et al.; the negative-results
or "data showcase" framing fits. EMSE as fallback. **Gate:** employer approval
only. **Effort:** medium; the material is complete and scattered across `05`,
`06` §5.2 and `08` §2.

---

### Article 5 — *Size, assertions, and the 30% neither could see: mutation testing an agent-written suite, and why the first three scores were wrong*

**Stances.** **CONFIRMS**, on our own data and at the expense of our own
headline metric, the test-effectiveness literature's position that suite size
is the wrong proxy and assertions the better one — and then shows that neither
saw a 30% gap; **ENHANCES** Hora & Robbes by converting their over-mocking
phenomenon from an anecdote in our corpus into a measured escape category;
**ENHANCES** mutation-testing reporting practice with a documented,
root-caused non-determinism in a widely used tool and a reproducibility check
no located industrial MSI paper reports.

**Published claims engaged.**

| Paper | Claim | Read status |
|---|---|---|
| Zhang & Mesbah (FSE 2015) | assertion count is strongly correlated with suite effectiveness | [secondary] |
| Inozemtseva & Holmes (ICSE 2014) | coverage is **not** strongly correlated with effectiveness | [secondary] |
| TOSEM 2025 analysis (`08` §7.3) | mutation-score ↔ fault-detection correlations fall to **0.05–0.20** once suite size is controlled — most of the association is a size effect | [secondary] |
| 2026 replicability study on LLM-generated suites (arXiv:2607.22880) | little evidence that size dominates; size correlates only **weakly** with mutation score | [secondary] |
| Hora & Robbes, *Are Coding Agents Generating Over-Mocked Tests?*, MSR 2026 (arXiv:2602.00409) | agent-written tests may pass "without actually testing the intended behavior" | [abstract-level] |

**Our evidence:**

| Metric | Value | What it can and cannot show | Tier | Id |
|---|---|---|---|---|
| Size | **1.69 : 1** test-to-source write ratio (+150,321 vs +88,896); 11/11 months; CI [1.39, 2.06] | effort was real and sustained; **blind to effectiveness** | S | T1, M-13 |
| Assertions | **2.28 / 2.33** assertions per test method across the two packages; **106 `willReturnCallback`** remain — the construct that hid the hollow tests | a better proxy; **still blind** | D | M-29 |
| Effectiveness | **Covered Code MSI 70%**: 1,592 mutants, 1,123 killed, **469 escaped**; identical across `--threads=1/4/8`, three runs each | the suite misses **30%** of semantic changes to code it executes | D (experiment) | M-30, N-4 |
| Over-mocking signature | **`MethodCallRemoval` 85 / 469** is the largest escape category — a call can be deleted with the suite green | Hora & Robbes' phenomenon, measured | D | M-30 |
| Where escapes cluster | `StripeCaptureRequestHandler` 54, `StripeCheckoutSessionHandler` 36, `ReturnSessionSecurityService` 34, `CaptureService` 27 — **orchestration**, not domain logic | consolidation into collaborators moved the gaps to the glue | D | M-30, LL-3 |
| Where they do not | **0 escaped mutants** in `AmountConverter`, `MinorUnitConverter`, `CapturableAmount` — **re-verified on the corrected 469-row set (§1.2)** | the money path is fully verified at the strongest available evidence level | D | `08` §7.3, this report |
| Targeted work moves it | 13 tests → **25 escapes closed**, MSI **68% → 70%**; refund handler 27 → 8 | the number is actionable | D | M-30 |
| Reproducibility | first score (462 mutants, MSI 73%) **not reproducible**; seven runs on unchanged code: **0–1,019 mutants, 0–73% MSI**; root cause: Infection's generated initial-test run uses a **random seed and terminates early**; PHPUnit's own coverage byte-identical across runs; fix: `--coverage=<dir> --skip-initial-tests` | a confident-looking percentage from one run can be wrong; the instability is invisible without repeats | D (demonstration) | N-14, M-30 |
| Hollow tests, documented | `assertTrue(true)` inside `willReturnCallback`; integration suite with **53 of 157 (34%)** silently skipped; rule R-1.5 written *after* the fact | the phenomenon existed here before it was measured | A | LL-3 |

**The argument.** We came to the literature with a size metric and the
literature told us it was the wrong one. So we measured the metric it prefers,
and then ran the experiment that settles it. The result is a clean confirmation
of the effectiveness lineage *against ourselves*: the size metric (1.69 : 1)
and the assertion metric (≈2.3 per test) were both **compatible with the suite
missing 30% of the semantic changes to code it executes, and neither could
reveal it**. The largest escape category is the over-mocking signature Hora &
Robbes study — so their phenomenon is now measured in an agent-assisted suite
that any quantity metric would have rated excellent. The positive half matters
too: the classes this project consolidated money arithmetic into have **zero
escapes**, so mutation testing shows both where consolidation worked and where
the untested glue around it sits. And the measurement itself is a finding:
**three authoritative-looking wrong answers** preceded the right one, the cause
was in the tool's own default workflow, and a single invocation gives no hint.

**What we add that the cited work cannot have.** A single project in which the
size metric, the assertion metric and the mutation score were all computed on
the same suite, with the hollow-test history documented independently in the
journal — so the divergence between proxies and effectiveness is shown, not
inferred across projects. A measured value for an over-mocking signature in an
agent-assisted suite. And a reproducibility caution with a root cause and a
fix, for a tool the PHP ecosystem uses widely.

**What a reviewer will say, and the concession.**
- *"MSI over covered code only, one package, unit suite only, no
  equivalent-mutant triage."* All conceded in M-30; at least one escape is a
  known equivalent (`CustomerDataSanitizer:28`), so **100% is not a coherent
  target** and the article says so.
- *"n = 1 suite; the proxies-vs-effectiveness literature is about
  correlations across many suites."* Correct; the claim is that the
  divergence they predict occurred here at a magnitude (30 points) that
  neither proxy could see. Not a correlation, a worked instance.
- *"The non-determinism is a tool bug, not a research result."* Partly. The
  research-relevant part is that **no located industrial MSI paper reports a
  run-to-run stability check**, and this case shows why one is needed.
- *"Attributing over-mocking to the agent is unsupported."* Agreed — the
  tests are of mixed authorship and trailer coverage is 20.8% (Article 4).
  The claim is about the *suite*, not about who wrote it.

**Still to do.** (1) **Mutate `payment-base`** — it has no baseline, and a
second package is the cheapest widening available. (2) **Triage a random
sample of the 469 escapes** (target: 100) for equivalence, so the 30% has a
stated upper bound on how much of it is real. (3) **Search Infection's issue
tracker** for the initial-test-run seed behaviour; file it upstream if absent,
and cite the issue. (4) Read Zhang & Mesbah, Inozemtseva & Holmes, the TOSEM
2025 paper, the 2026 replicability study and Hora & Robbes in full — all are
currently [secondary] or abstract-level. (5) Optionally re-measure MSI at two
or three historical checkpoints from `test_trajectory.csv` to show whether the
score moved with the size metric or independently of it — the one addition
that would let the article speak to the *correlation* literature rather than
only instance it.

**Venue.** Research: ESEM or ICST short paper; MSR if positioned as a
companion to Hora & Robbes. Practitioner: EuroSTAR / TestBash as LL-3, which
[`07`](07-lessons-learned.md) already recommends submitting first. **Gate:**
none — no named individuals, no security material, and the project's own
`docs/for_developer/mutation-testing.md` already documents the recipe.
**Effort:** low to medium; the experiment is done and reproducible, the
outstanding items are triage and reading.

---

## 4. Considered and not offered

Stated so the omissions are deliberate rather than oversights.

| Candidate | Published work | Why not an article |
|---|---|---|
| **Disjoint defect yields** (N-5) | Basili & Selby; the inspection-vs-testing replications | **Untestable** — zero overlap between a 4-set and a 6-set has no null without the defect-pool size (`06` §2.5, `07` Tier U). Offered as a labelled *observation* inside Article 2 or 5; a designed comparison would make it an article. |
| **Work rhythm as counterexample** (N-12) | *TGIF* (EMSE 2025) intensification trend | Tier S, but the employment context is a complete alternative explanation, and a trend is not a law. Folded into Article 1 as one confirming row (Claes et al.) and one weak counterexample. |
| **Copilot RCT** | Peng et al. (2023) | **CANNOT ADDRESS** — no control arm; our activity figures are not productivity measures. The one usable point (dispersion 6.93 → no central rate to quote) belongs in Article 1's discussion. |
| **AI code debt** | Liu et al., *Debt Behind the AI Boom* (arXiv:2603.28592) | **Challenges us**, and our instrument (pipeline outcome) cannot see what theirs (static analysis) measures. Becomes an article only after a static-analysis pass over our trailered diffs — the cheapest **new** experiment in the programme, and recommended, but not yet run. |
| **PCI-DSS provenance** | PCI DSS Req. 6.4/6.5 | Narrowed to a conditional claim in `08` §7.5; practitioner material (LL-5), one paragraph in Article 4. |
| **Security topics** (SEC-1, SEC-2) | OWASP, PCI | Self-scored AI-authored audit; **not publishable as security results** (`06` §4, `07` gate 3). |
| **CI theatre** | arXiv:1907.01602 | One paragraph in Article 2; the demotion of the improvement trend weakens our side of it. |

---

## 5. Order, dependencies and gates

| # | Article | Gate | Blocking new work | Order |
|---|---|---|---|---|
| 2 | Churn predicts nothing here | none | hand-classify ~100 failing runs (check log retention first) | **1st** |
| 5 | Size, assertions, and the 30% | none | mutate `payment-base`; triage ~100 escapes; upstream Infection issue | **2nd** |
| 4 | Ground truth for the perils | employer | full-text reads; optionally run Robbes et al.'s heuristics | 3rd |
| 1 | Imprecise about volume | employer | apply §1.3 corrections; retitle and cut the flagship | 4th |
| 3 | The team set the sign | **named-colleague consent** + employer | consent conversation; role anonymisation; replication design | **last** |

Two dependencies run across articles. Article 1 should cite Articles 2 and 5
for the CI and mutation results rather than re-develop them, which is why it
goes after them. Article 3 shares its evidence table with one anonymised row of
Article 1; if consent is refused, Article 1 keeps the anonymised row and
Article 3 is not written.

**Before any of them:** apply the corrections queue in §1.3. Every article
above cites a number that at least one earlier report currently states wrong.

---

## 6. Summary

| # | Working title | Confirms | Disproves | Enhances |
|---|---|---|---|---|
| **1** | Imprecise about volume, not only optimistic about speed | METR (self-report unreliable); Claes et al. (office hours) | — (weak counterexample to *TGIF*) | METR — a two-component taxonomy of self-report error; Agarwal et al. — the *why* beside the *what* |
| **2** | Churn predicts nothing here | Huang et al. (patch-unrelated failures); clustering benchmark (85.7% vs >50%) | churn/commit-count as build-outcome predictors — no signal in this setting | Huang et al. — an extreme case and a size-independence result their framing predicts |
| **3** | The team set the sign | — | Monperrus, strong form (the pair did not find its own defects) | Agarwal et al. — the missing measurement (V = 0.859); Garousi — *who* bears the burden |
| **4** | Ground truth for the perils | Robbes et al. (partial, heterogeneous, changing, lost) | the assumption that trailers index AI involvement (p = 5.2e-81 step change with journal ground truth) | provenance dataset — a recovered witness and a third loss mechanism; fabrication fear — 0/61 |
| **5** | Size, assertions, and the 30% | Zhang & Mesbah; Inozemtseva & Holmes; the size-confounder result — on our own suite | — | Hora & Robbes — over-mocking measured (85/469); MSI reporting — a reproducibility check with root cause |

Two of the five clear every gate today. All five rest on Tier S or Tier D
evidence already in `data/`, and none makes a causal claim about the assistant.

---

## 7. Sources

Reused from [`08`](08-literature-review.md) §9; read status as marked there.

- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://arxiv.org/abs/2507.09089) — METR
- [Do programmers work at night or during the weekend?](https://dl.acm.org/doi/10.1145/3180155.3180193) — Claes, Mäntylä, Kuutila, Adams, ICSE 2018
- [TGIF: the evolution of developer commit times](https://link.springer.com/article/10.1007/s10664-025-10767-2) — EMSE 2025
- [Is this Build Failure Related to my Patch?](https://arxiv.org/html/2605.05564) — Huang, da Costa, Dick, El Mezouar
- [Insights into Continuous Integration Build Failures](https://www.researchgate.net/publication/318124591_Insights_into_Continuous_Integration_Build_Failures)
- [Continuous Integration Theater](https://arxiv.org/pdf/1907.01602)
- [3100 Opinions on Code Review in an AI World](https://arxiv.org/abs/2607.07980) — Agarwal, Miller, Kästner, Vasilescu
- [Human Oversight and Overload](https://arxiv.org/abs/2606.05770) — Garousi
- [The End of Code Review: Coding Agents Supersede Human Inspection](https://arxiv.org/html/2606.13175) — Monperrus, *not yet read*
- [Mining Issue Trackers: Concepts and Techniques](https://arxiv.org/html/2403.05716v1) — reporter-type lineage
- [Promises, Perils, and (Timely) Heuristics for Mining Coding Agent Activity](https://arxiv.org/abs/2601.18345) — Robbes, Matricon, Degueule, Hora, Zacchiroli, MSR 2026 ([artifacts](https://github.com/labri-progress/agent-mining))
- [Was It Never Collected, or Rewritten Away?](https://arxiv.org/pdf/2607.02774)
- [Agentic Much? Adoption of Coding Agents on GitHub](https://arxiv.org/abs/2601.18341) — TOSEM; [Agentic Very Much!](https://arxiv.org/abs/2606.07448)
- [Are Coding Agents Generating Over-Mocked Tests?](https://arxiv.org/pdf/2602.00409) — Hora & Robbes, MSR 2026
- Zhang & Mesbah, *Assertions are strongly correlated with test suite effectiveness*, FSE 2015; Inozemtseva & Holmes, *Coverage is not strongly correlated with test suite effectiveness*, ICSE 2014 — cited in `08` §7.3 from secondary sources
- [Debt Behind the AI Boom](https://arxiv.org/html/2603.28592v1) — Liu, Widyasari, Zhao, Irsan, Lo — *considered, not offered*
- [The Impact of AI on Developer Productivity: Evidence from GitHub Copilot](https://www.microsoft.com/en-us/research/publication/the-impact-of-ai-on-developer-productivity-evidence-from-github-copilot/) — Peng et al. — *considered, not offered*
