# X-03 — Statements and Conclusions Disproved by the Flagship, X-01 and X-02

*Written 2026-09-21 · a ledger of published, practitioner and self-authored
claims that [`01`](01-flagship-paper-ai-assisted-payment-module.md),
[`X-01`](X-01-five-articles-against-the-literature.md) and
[`X-02`](X-02-five-deeper-studies.md) contradict — graded by how strong the
contradiction actually is*

**Statement — what this report claims and concludes.** It claims that three
works of this programme — the audited flagship, the five positioned articles of
X-01 and the five deeper studies of X-02 — contradict a definable set of
statements, and that the contradictions fall into five grades of very unequal
strength. It concludes that the works **disprove two peer-reviewed conclusions
in a bounded sense** — the strong reading of "coding agents supersede human
inspection", by a case in which the agent-assisted pair found none of its own
behavioural defects, and the transferability of churn-based build-failure
prediction, by a setting in which the feature carries no signal — and
**undermine one methodological premise** shared across the agent-mining
literature, that commit trailers index AI involvement. It concludes that the
works supply only **weak counterexamples** to two published trends (rising
off-hours work; the CI-theatre inference), each with an alternative
explanation the works themselves state. And it concludes that **the largest
class of disproved statements is the subject project's own record and this
programme's own earlier drafts**: eleven journal statements false by
enumeration and twelve of our own claims withdrawn, demoted or corrected, none
of which reversed a direction and all of which removed a significance or halved
a magnitude. The report's final claim is about that ratio: an audit of a
self-account that disproves more of itself than of others is behaving as an
audit should, and its credibility rests on the fourth section, not the first.

**Abstract.** Single-subject case studies are routinely read as refuting
general claims they cannot touch. This report enumerates what one such study —
a ten-month, five-corpus audit of an AI-assisted payment module — actually
contradicts, and grades each contradiction: **D1**, a counterexample to a claim
stated or read as universal; **D2**, a published predictor or measurement
premise shown to carry no signal in a documented setting; **D3**, a factual
statement false by complete enumeration; **D4**, an inferential reading
contradicted while its source survives; **D5**, a claim of our own demoted by a
stricter test. Against peer-reviewed work the works yield one D1/D4 pair
(Monperrus's *End of Code Review*: a dedicated tester filed 37 of 40 bugs and
the engineer using the assistant filed none, Cramér's V = 0.859, inside the
paper's own carve-out for regulated systems), one D2 (churn and commit count
predict build failure: ρ = −0.024, p = 0.66 across 444 commits, explained by a
49.7% failure rate double the closed-source baseline and 85.7% failure
clustering), one D2 on a shared premise (trailers as AI involvement: 0.4% →
58.8% on one date, p = 5.2e-81, with journal ground truth for the untrailered
seven months), one weak D1 (*TGIF*: zero Saturdays in 716 commits, with
employment as the alternative explanation), one D4 (CI theatre inferred from
failure rate), and one D2 on reporting practice (single-run mutation scores:
0–1,019 mutants across seven runs of an unchanged suite). Against practitioner
claims it yields ten rows, including that the pair is its own QA, that agents
fabricate identifiers (0 of 61 did), that test volume shows quality (1.69 : 1
and ≈2.3 assertions per test were blind to a 30-point mutation gap), and that
small commits protect the build. Against the subject's own journal it yields
eleven D3 rows, from "single-developer" to a 41% understatement of its flagship
epic. Against our own earlier drafts it yields twelve rows, including a
documentation figure over-attributed by 2×, a mutation score wrong by 70 points,
and three significance claims — the CI trend, the burst-day effect, and a
coin-flip test — that fell to p ≈ 0.18 or invalidity once dependent units were
treated as dependent. Ten further claims these works are sometimes read as
refuting are listed as not disproved, including METR's, which the works confirm.
We conclude that the study's power to disprove is real but narrow, that every
statistical overclaim in the programme came from treating dependent units as
independent and every factual overclaim from reading an aggregate as the thing
it contained, and that the retraction ledger is the most credible product of
the work.

A single-subject study cannot refute a distribution, an effect size or a
survey. It can do four narrower things, and this report does not let the word
"disproved" cover anything else. Every entry below names the claim as stated,
the evidence against it, the grade of the contradiction, and what survives of
the original. The last section lists the claims these works are sometimes read
as disproving and do not.

---

## 0. Grades of contradiction

| Grade | Meaning | What survives of the original |
|---|---|---|
| **D1 — counterexample to a universal or strong claim** | The claim is stated, or commonly read, as holding generally; we supply one fully-instrumented case where it does not. | The claim as a tendency. n = 1 refutes "always", not "usually". |
| **D2 — no signal in a documented setting** | A published predictor, proxy or measurement assumption carries no information in this project, and the reason is identified. | The aggregate finding elsewhere. What falls is the assumption that it transfers. |
| **D3 — factual statement false by enumeration** | A specific count, date or attribution is shown wrong by complete enumeration of the artifact. Needs no inference. | Nothing; the statement is corrected. |
| **D4 — an inferential reading contradicted, the source intact** | A conclusion people draw from a paper is contradicted while the paper's own wording, carve-outs or scope survive. | The paper. What falls is the popular reading. |
| **D5 — a claim of ours demoted by our own later test** | An earlier statement in this programme did not survive a stricter test or a re-measurement. | Usually the direction; never the significance. |

Two constraints inherited from [`08`](08-literature-review.md) §0 apply
throughout. Papers marked **[abstract]** or **[secondary]** there have not been
read in full in this programme, and a contradiction of a claim we have only
seen in an abstract is a contradiction of the abstract. And no entry below is a
causal claim about the assistant.

---

## 1. Published research whose statements these works contradict

### 1.1 Monperrus — *The End of Code Review: Coding Agents Supersede Human Inspection* (arXiv:2606.13175, 2026) — **D1 on the strong form, D4 on the paper**

**Statement contradicted.** That coding agents have crossed a capability
threshold at which human inspection is no longer a necessary part of a quality
pipeline, and that "agents write, humans review" is a dead end.

**Evidence.** In this project the agent-assisted pair did not detect its own
behavioural defects: the engineer using the assistant filed **52 Stories and
zero Bugs**; a dedicated human tester filed **37 of the project's 40 Bugs
(92.5%)** and zero Stories (Fisher p = 6.7e-26; full reporter × type table
χ² = 199.4, Cramér's V = 0.859). Six of the forty bugs were on the money path
(amount, capture, refund). *Flagship §4.12a; X-01 Article 3; X-02 S-3.*

**Grade and what survives.** **D1** against the strong, widely repeated reading:
in at least one regulated production system, the agent-plus-developer unit was
the implementation unit and not the quality system. **D4** against the paper as
written, which reserves a human role for "security-critical paths in regulated
systems" — a PCI-DSS-obligated payment module is exactly that, so the case sits
inside the carve-out. Two caveats we impose on ourselves: the tester performed
**black-box testing of a running shop, not diff review**, so the evidence bears
on "can the pair find its own defects" rather than "is diff review necessary";
and the paper is **[abstract, not yet read]**.

### 1.2 Build-failure prediction on churn and commit-count features (TravisTorrent-era literature, `08` §3.1) — **D2**

**Statement contradicted.** That source churn and the number of commits in a
build are among the most useful pre-execution predictors of build outcome.

**Evidence.** Across 444 commits with CI runs, commits of ≥500 insertions had a
failing run **63%** of the time and smaller commits **60%**: Fisher **p = 0.66**,
Spearman **ρ = −0.024** (p = 0.61), with the threshold and rank framings
disagreeing in *sign*. The feature carries no information here. The mechanism
is supplied by Huang et al. (arXiv:2605.05564): where failures are unrelated to
the patch, size cannot predict them — and this project, at **49.7%** failure
against a published closed-source baseline of 26%, with **85.7%** of failures
following a failure, is the extreme end of that phenomenon. *Flagship §4.13c,
§4.13g; X-01 Article 2.*

**Grade and what survives.** **D2**: the predictive value does not transfer to a
framework-coupled, cross-repository, private-dependency setting — one no
published corpus includes. The direction is not contradicted (ρ is negative,
as reported), and the aggregate finding on public CI corpora stands. What falls
is the assumption that churn features can be adopted without first measuring
the patch-unrelated share.

### 1.3 Trailer-based identification of AI-assisted commits as a measure of AI involvement — **D2**, with ground truth

**Statement contradicted.** The methodological premise, explicit or implicit in
large-scale studies that identify AI-authored commits by `Co-Authored-By`
trailers (e.g. Liu et al., *Debt Behind the AI Boom*, arXiv:2603.28592; the
adoption estimates of *Agentic Much?*, arXiv:2601.18341), that the absence of a
trailer indicates the absence of AI involvement and that a trailer time series
tracks AI adoption.

**Evidence.** Trailers appear on **149 of 716 commits (20.8%)**: **2 of 466
(0.4%)** before 2026-05-07 and **147 of 250 (58.8%)** after (Fisher
**p = 5.2e-81**), reaching 86% by August 2026, with **six model strings in four
months**. The project's own journal documents heavy assistant use throughout
the seven months of near-zero coverage — ground truth an ecosystem-scale study
cannot have. The trailer series records the adoption of a commit convention on
a single date, not the arrival of the assistant. *Flagship §4.9; X-01 Article 4;
X-02 S-2 uses trailers only as a model clock for this reason.*

**Grade and what survives.** **D2** for the premise: in this project, trailer
absence is not evidence of AI absence, and any trend or model-attributed
comparison built on trailers is confounded by rollout and generation churn.
This does **not** disprove Liu et al.'s findings about the commits they *did*
identify — those are AI-authored by construction. It bounds what such corpora
can say about the untrailered remainder and about time.

### 1.4 *TGIF: the evolution of developer commit times* (EMSE 2025) — **D1, weak**

**Statement contradicted.** A consistent rise in the share of night and weekend
commits over time, read as a shift toward always-on, asynchronous work — and
the associated worry that agentic assistance accelerates that shift.

**Evidence.** A 2025–26 agent-assisted project with **zero Saturday commits and
one Sunday commit in 716** (P = 1.2e-48 against uniform days), **95.9%** of
commits inside 08:00–20:00, and out-of-hours work concentrated on one day
(13 of 29 commits; exact binomial p = 4.8e-07). *Flagship §4.4.*

**Grade and what survives.** **D1, weak**: a counterexample to the universality
of a *trend*, which was never a law. The employment context — a paid,
single-team industrial project — is a complete alternative explanation, so the
case cannot be read as evidence that agents *reduce* intensification. It shows
only that agentic work does not *require* it.

### 1.5 The inference "a pipeline red half the time is CI theatre" (from *Continuous Integration Theater*, arXiv:1907.01602) — **D4**

**Statement contradicted.** Not the paper's — the inference commonly drawn from
it, that a persistently failing pipeline indicates CI adopted without the
practices that make it meaningful.

**Evidence.** A **49.7%** failure rate over ten months coexisted with permanent
regression probes added after each environment break, converged dependency
authentication, and a failure rate that fell from 57% to 46% across 2026-04-01.
That improvement is **descriptive only** (nominal p = 0.0014; **p = 0.18** once
failure clustering is modelled). *Flagship §4.13e; `08` §3.3.*

**Grade and what survives.** **D4**: the paper's concern survives intact; the
inference from failure rate alone to "theatre" does not. Note the limit we
impose: because the improvement is not statistically established, this entry
says only that a red pipeline was *tended*, not that the tending worked.

### 1.6 Single-run reporting of industrial mutation scores — **D2 on a practice, not a paper**

**Statement contradicted.** The implicit assumption in industrial mutation-score
reports that one invocation of the tool yields a reproducible figure. We located
no paper reporting a run-to-run stability check, and we name none as wrong.

**Evidence.** The first Infection run on this suite reported 462 mutants and MSI
73% and was published in this programme as a measured result. Seven repeats on
unchanged code returned **0 to 1,019 mutants and 0% to 73% MSI**. The cause was
the tool's own generated initial-test run, which uses a random seed and
terminates at a variable point; PHPUnit's coverage run directly is byte-identical
across runs. The reproducible figure — **1,592 mutants, 469 escaped, MSI 70%**,
identical across `--threads=1/4/8` — required generating coverage externally.
*Flagship §4.14; X-01 Article 5; `06` N-14.*

**Grade and what survives.** **D2** for the assumption, specific to Infection
0.31.9's default workflow: a single confident-looking percentage can be wrong
by 70 points and give no hint of it. Every published MSI obtained the same way
survives unless its authors repeated it; the recommendation is that they say
whether they did.

---

## 2. Practitioner and grey-literature claims these works contradict

Claims in this section circulate in vendor material, talks and blog posts
rather than in peer-reviewed work. They are stated here in their common form.

| # | Claim as commonly stated | Evidence against it | Grade | What survives |
|---|---|---|---|---|
| 2.1 | **"A developer plus a coding agent is a complete unit — the pair can be its own QA."** | The pair filed **0 bugs**; a separate human filed **37 of 40**. The function is invisible in the journal and in git, visible only in the tracker. *Flagship §4.12a, §5.4.* | **D1** | Nothing of the strong form. The pair *fixed* the bugs; it did not find them. |
| 2.2 | **"AI-assisted throughput is N commits per day"** / **"N× faster"** (quoted from peak episodes) | Cadence is overdispersed: median **3** commits per active day, mean 5.0, max 35, **dispersion index 6.93** (p = 4.7e-126); only 18 of 143 days exceed 10. Quoting the epic's 30+ as the rate overstates it ~10×. *Flagship §4.2.* | **D2** | The peak is real. What falls is that a repository like this has a central rate worth quoting. |
| 2.3 | **"LLM agents fabricate ticket identifiers in commit messages."** | **0 of 61** distinct `STRP-nnn` references fabricated across **436** ticket-bearing commits; **1** misattributed (`STRP-138` for `STRP-139`). *Flagship §4.12c, §6.1.* | **D1** | The worry as a possibility. Here the failure that occurred was conflation, not invention. |
| 2.4 | **"Test volume — count, coverage, test-to-code ratio — shows the agent-written suite is good."** | **1.69 : 1** test-to-source and **≈2.3** assertions per test were both compatible with the suite missing **30%** of mutations in code it executes (MSI 70%, `MethodCallRemoval` the top escape at 85/469). The same suite had shipped `assertTrue(true)` tests and a 34% silent-skip rate. *Flagship §4.7, §4.14, §6.5.* | **D2** | Volume as evidence of *effort* (11 of 11 months, p = 0.0010). Not as evidence of verification — which Inozemtseva & Holmes and Zhang & Mesbah already said; we confirm them on one suite at our own expense. |
| 2.5 | **"Keep commits small to protect the build."** | Failure was independent of commit size (p = 0.66, ρ = −0.024) and clustered in streaks (85.7% follow a failure; median 4.1 h, max 358 h to green). Sizing commits addressed a cause the failures did not have. *Flagship §4.13c, §4.13g, §7.4.* | **D2** | Small commits for reviewability and bisectability. Not for build health in an environment-dominated setting. |
| 2.6 | **"A naming or numbering convention makes the agent commit one unit at a time."** (the subject project's own operating belief, `118-lessons-learned.md`) | **9 of 13** decimal sub-sprints (69%) span more than one commit, median 5; the convention failed on its own terms. Whether it beat ordinary numbering is untestable (13 vs 6 groups, p = 1.00). *Flagship §6.2; `07` LL-1.* | **D3** on "it works"; **untestable** on "it helps" | The dispatch boundary as the only hard constraint. |
| 2.7 | **"Agentic development means always-on work."** | 0 Saturdays in 716 commits; 95.9% inside working hours; see §1.4. | **D1, weak** | The worry as a possibility, with employment context as the alternative explanation. |
| 2.8 | **"Agent completion reports inflate what was done."** | The best-instrumented report **understated** its epic by **~41%** on insertions (+11,204 vs +15,844) and by 3 commits; smaller checks found errors in both directions. *Flagship §4.5, §6.3.* | **D1** on "always inflate" | That reports are unreliable. What falls is the direction: unreliability here was not vanity. X-02 S-5 would turn this from two data points into a distribution. |
| 2.9 | **"Squashing release history violates PCI DSS."** (our own earlier wording came close) | PCI DSS 6.4/6.5 requires an auditable change-control record and does not mandate the commit graph. *Flagship §6.6; `08` §7.5.* | **D3** on the general claim | The conditional: where the commit history *is* the change-control evidence, as here, squashing destroys the artifact the audit depends on. |
| 2.10 | **"Changes in the upstream package break the downstream package's build."** (a natural reading of the journal's cross-repo account) | *Pilot only*, X-02 P3: downstream runs within 72 h of an upstream commit failed **45%** against **61%** otherwise — the opposite direction — but the comparison is time-confounded. | **not graded** | Everything; listed so that nobody cites the pilot as a result. The journal blames cross-repo *authentication and resolution*, not upstream code, and the pilot does not touch that. |

---

## 3. Statements of the subject project's own record that the works disprove

The journal (Corpus A) is the object of the audit; these are its claims that
did not survive. All are **D3** — false by enumeration — unless marked.

| Journal statement | Record | Where |
|---|---|---|
| A **single-developer** project | **3** human committers (87 / 8.8 / 2.7% of commits); **10** tracker participants, including a dedicated tester and a project manager | §4.8, §4.12a |
| A **seven-month** project (2025-11-26 → 2026-07-02) | Commits from **2025-10-21**; tracker issues from **2023-05-30**; 35% of issues predate the first commit — a **three-year** project | §3.2, §4.12e |
| **47** active days | **105** days with commits inside the journal's own window; 143 overall | §4.1 |
| March–April 2026 as **active work** | **9.1 h** of commit-bearing activity across the two months | §4.3, §6.4 |
| The flagship epic: **61 commits, +11,204 / −5,876** | **64** commits, **+15,844 / −6,075** | §4.5 |
| Webhook dispatch **"simplified 330 → 107 lines"** | True for one file; the same commit added 8 handler classes and module handler code rose **2,616 → 2,953**; commit near LOC-neutral (+1,766 / −1,701) | §4.11 |
| **"~2,020 LOC of dead code removed"** (unqualified) | No single-figure removal claim in the corpus is stated net of code added to replace it; `src` deletions run at 46% of insertions overall | §4.11 |
| The out-of-hours epic evening as **"the only such day"** | Out-of-hours commits fall on **11** days; the pattern is concentration (13 of 29 on one day), not uniqueness | §4.4 |
| Rename day: **"10 commits"** | **9** (author date) | `00` §4 |
| Decimal sub-sprints map **one phase → one commit** | 9 of 13 span more than one commit (§2.6 above) | §6.2 |
| Bugs triaged by the developer and the assistant | **37 of 40** filed by a tester; **6 of 40** reclassified `Not a bug` / `Core Bug` — confirming the journal's *"meaningful fraction"* claim while relocating who did the triage | §4.12a, §4.12d |

**What the journal said that survived.** The audit is not one-sided, and a ledger
of disproofs should say so. TDD as practice (1.69 : 1 in 11 of 11 months);
every mechanical figure that could be checked (330 → 107, −183 LOC, PHPMD
4 → 3, 25 interface methods, +196 test methods) matched **to the line**; the
`bf32d77` incident matched in all five particulars; all four webhook guards and
all seven validation guards exist by exact class name; and the environmental
account of CI cost was confirmed by Corpus D. The journal was reliable on what
it could count and wrong on what it could not see.

---

## 4. Our own earlier statements that our later work disproved

This is the section a reviewer will assemble anyway, so it is assembled here.
Each row is a statement made in an earlier revision of this programme's own
reports and contradicted by a later measurement or a stricter test.

| Earlier statement (where, when) | Later finding (where, when) | Grade |
|---|---|---|
| *"Discipline over cleverness"* as the flagship's **thesis and title** (01, 2026-07 → 2026-08) | No control arm, one operator, six models in four months: the thesis is consistent with the record and **cannot be established** by it. Retitled; the maxim kept as the hypothesis under audit (01 header, §7.4, §9, 2026-09-21) | **withdrawn as a claim** — not disproved, unsupported |
| **"Single-developer"** listed as a confound (01 first draft, 2026-07-07) | 3 committers; 10 participants (01 §4.8, §4.12, 2026-08-20) | **D3**, retracted twice |
| **"Claude was the primary code author"** (01 first draft) | Unverifiable before 2026-05-07: trailers absent; journal bylines are not independent evidence (01 §4.9, 2026-08-20) | **unverifiable**, reworded to "a primary code author" |
| **"`docs` is 4.4× the production code; the log-as-memory practice is the project's dominant activity"** (01 §4.7, 05 M-17, 2026-08-20) | Decomposed by path: the journal is **≈177,600 lines (≈30%, ≈2.0× src)**; **≈168,200 (≈29%)** are business-strategy decks committed on 2025-10-27 under `STRP-52`, before the journal existed (01 §4.7, 05 M-17, 2026-09-21) | **D3** — over-attributed by ~2× |
| **CI failure rate "indistinguishable from a coin flip", exact binomial p = 0.28** (05 M-23, 2026-08-21) | Runs are autocorrelated (lag-1 0.680); the test assumed independence and is **invalid**. The proportion is a census fact (05 M-23, `08` §7.2, 2026-08-24) | **withdrawn** |
| **"CI hardening measurably worked: 57% → 46%, p = 0.0014"** (01 §4.13e, 05 M-27, 06 §5.3, README, 2026-08-21) | Deflated for autocorrelation: **p = 0.18**. Real as a description, not a tested result (2026-08-24; last stale copies fixed 2026-09-21) | **D5** |
| **"Covered Code MSI 73%, 462 mutants"** published as a measured result (05 M-30, `08` §7.3, 2026-08-24 morning) | Not reproducible: 0–1,019 mutants across seven runs; root cause in the tool's initial test run; corrected to **1,592 / 469 / 70%** (same day) | **D3** — the number was wrong |
| **"`MethodCallRemoval` is the top escaped mutator, 28 of 122"**; weakest files refund handler 27, payment-status 22, checkout-session 22 (`08` §7.3, §8) | **85 of 469**; weakest files capture handler 54, checkout-session handler 36, return-session security 34 (05 M-30; `08` corrected 2026-09-21) | **D3** — stale figures from the retracted run |
| **PM-1's premise "refuted"** (02, 07, 2026-08-20) | 13 vs 6 groups, Fisher **p = 1.00**: no power. Corrected to "failed on its own terms; comparison underpowered" (06 §2.0, 07 Tier U; last stale copy fixed 2026-09-21) | **D5** — an overclaim in the other direction |
| **"The only such day"** for out-of-hours work (01 §4.4 first draft) | 11 days (01 §4.4, 2026-08-20) | **D3** |
| **"Squashing history is a PCI-DSS finding in its own right"** (01 §6.6 first wording) | Narrowed to the conditional claim (01 §6.6, `08` §7.5, 2026-08-24) | **D3** on the general form |
| **"Bursts cost."** — burst-day commits fail CI 72% vs 56%, **p = 0.0014** (X-02 P1 and S-1 as first written, 2026-09-21 morning) | Day-level permutation preserving within-day clustering: **p = 0.18**. Direction holds in both halves of the record; demoted to a direction the same day (`stats.py` T11; X-02 P1, S-1; 01 §4.13h) | **D5** — same error as the CI trend, caught before it left the repository |
| N-3 as **"a possible gap in the literature"** (06 first draft, 2026-08-20) | The question is posed (Garousi) and a falsifiable theory exists (Agarwal et al.); N-3 is the **missing measurement**, not a new question (`08` §5.2, 2026-08-21) | **reframed** — stronger position, different claim |

Three patterns in this table are worth stating once. **Every statistical
overclaim came from treating dependent units as independent** — runs within a
workflow, commits within a day — and every one was caught by testing a published
claim or a stricter null against our own data. **Every factual overclaim came
from reading an aggregate as the thing it contained** — `docs/` as the journal,
one file's shrinkage as the module's, the first tool run as the measurement.
And **none of the corrections reversed a direction**; each removed a
significance or halved a magnitude. That is the honest shape of what audit did
to this programme, and it is the reason the retractions are reported as the most
credible part of the work.

---

## 5. What these works do *not* disprove, and are sometimes read as disproving

Stated so that no one cites this programme for them.

| Claim | Why it is not disproved here | Correct reading |
|---|---|---|
| **METR (2025): AI made experienced developers 19% slower while they felt 20% faster** | We have no clock and no control arm. We **confirm** the self-report-unreliability finding by an independent route and extend it from speed to volume, continuity, scope and actors. | Supported, not contradicted. *X-01 Article 1.* |
| **Peng et al. (2023): Copilot users 55.8% faster** | No counterfactual; our figures are activity descriptions, not productivity measures. | Cannot address. |
| **Liu et al. (2026): >15% of AI commits introduce static issues; 24% survive** | Our instrument (pipeline outcome) cannot see code smells. Our null on AI-trailered commits vs CI (59% vs 61%, p = 0.88) is confounded and coarse. | They challenge *us*; the missing static-analysis pass over our trailered diffs is the cheapest unrun experiment in the programme. |
| **"AI-written code is more (or less) likely to break the build"** | p = 0.88 is a null, n = 49 on one side, trailers cluster in a low-failure period, and trailers are not authorship. | Not tested here in either direction. |
| **Basili & Selby (1987), Juristo et al. (2003): techniques detect different fault classes** | Our disjoint yields (4 refactoring-found vs 6 tester-found amount bugs, zero overlap) cannot be tested without the defect-pool size. | An observation in their lineage; X-02 S-3 would make it a result. |
| **Garousi (2026), Agarwal et al. (2026): oversight is a burden; the team sets the sign** | We supply the measurement they lack. | Enhanced, not contradicted. |
| **Robbes et al. (MSR 2026); Huang et al. (2026); Claes et al. (2018); Hora & Robbes (MSR 2026)** | Instantiated, supported, supported, quantified respectively. | See `08` §8. |
| **"CI hardening worked"** and **"burst-mode work is worse"** | Both are directions with p ≈ 0.18 after dependence is modelled. | Not established; not disproved either. |
| **"The module's security posture is good"** | The audit is AI-authored and self-scored with no independent record. | Unknown. `07` gate 3. |
| **"Discipline caused the quality"** | See §4, row 1. | Unsupported at n = 1; the record is consistent with it. |

---

## 6. Summary by grade

| Grade | Count | Entries |
|---|---|---|
| **D1** counterexample to a strong or universal claim | 6 | Monperrus (strong form); TGIF (weak); "the pair is its own QA"; "agents fabricate ticket ids"; "always-on"; "reports inflate" |
| **D2** no signal in a documented setting | 5 | churn predicts build failure; trailers measure AI involvement; rate quotes from bursty repositories; volume shows test quality; small commits protect the build |
| **D3** factual statement false by enumeration | 14 | eleven journal statements (§3, incl. the sub-sprint convention); the PCI general form; and our own 4.4×, 462/73%, 28/122, "only such day" |
| **D4** inferential reading contradicted, source intact | 2 | Monperrus as written; CI-theatre inference |
| **D5** our own claim demoted by a stricter test | 3 | CI hardening p = 0.0014 → 0.18; PM-1 "refuted" → underpowered; burst days p = 0.0014 → 0.18 |
| **Withdrawn / unverifiable / reframed** | 4 | the "discipline" thesis; "primary code author"; the coin-flip test; N-3 as a gap |
| **Not disproved** | 10 | §5 |

The distribution is the point. These works contradict **two peer-reviewed
conclusions outright** (one strong reading of Monperrus, one predictor family
from the build-failure literature), **undermine one methodological premise** used
across the agent-mining literature (trailers as involvement), **supply weak
counterexamples to two trends**, and **disprove far more of the subject's own
record and of our own earlier drafts than of anyone else's work**. That ratio
is what an audit of a self-account should produce, and it is the reason the
programme's credibility rests on §4 rather than on §1.

---

## 7. References

Read status follows [`08`](08-literature-review.md) §9 and
[`X-02`](X-02-five-deeper-studies.md) §9: **[08]** located and graded there;
**[X-02]** introduced there and **not yet read in full**; **[own]** a report of
this programme. Nothing may be cited from this document.

**Works whose statements are contradicted (§1)**
- Monperrus, M. — *The end of code review: coding agents supersede human inspection*. arXiv:2606.13175, 2026. [08 §7.4 — abstract only, not yet read]
- Build-failure prediction on churn and commit-count features — the TravisTorrent-era literature summarised in `08` §3.1, including *Insights into Continuous Integration Build Failures* (MSR 2017). [08 §3.1, secondary]
- Huang, da Costa, Dick & El Mezouar — *Is this build failure related to my patch? An empirical study of unrelated build failures in continuous integration*. arXiv:2605.05564, 2026. [08 §3.2, full-text] — supplies the mechanism for §1.2
- Liu, Widyasari, Zhao, Irsan & Lo — *Debt behind the AI boom: a large-scale empirical study of AI-generated code in the wild*. arXiv:2603.28592, 2026. [08 §1.3] — affected by §1.3's premise; its own findings are **not** contradicted (§5)
- *Agentic Much? Adoption of coding agents on GitHub*. TOSEM, arXiv:2601.18341; and *Agentic Very Much!*, arXiv:2606.07448, 2026. [08 §5.2.5] — affected by §1.3's premise
- *TGIF: the evolution of developer commit times*. Empirical Software Engineering, 2025. [08 §4.2, secondary]
- *Continuous Integration Theater*. arXiv:1907.01602, 2019. [08 §3.3, secondary] — the inference, not the paper, is contradicted
- Industrial mutation-score reports — no specific paper is named as wrong; the contradicted assumption is single-run reporting (§1.6)

**Works whose statements are confirmed, enhanced or instantiated, and therefore not in §1 (§5)**
- METR — *Measuring the impact of early-2025 AI on experienced open-source developer productivity*. arXiv:2507.09089, 2025. [08 §1.2]
- Peng, Kalliamvakou, Cihon & Demirer — *The impact of AI on developer productivity: evidence from GitHub Copilot*. 2023. [08 §1.1]
- Robbes, Matricon, Degueule, Hora & Zacchiroli — *Promises, perils, and (timely) heuristics for mining coding agent activity*. MSR 2026, arXiv:2601.18345. [08 §2.1]
- *Was it never collected, or rewritten away? A commit-provenance dataset…* arXiv:2607.02774, 2026. [08 §2.2]
- Hora & Robbes — *Are coding agents generating over-mocked tests? An empirical study*. MSR 2026, arXiv:2602.00409. [08 §2.3]
- Agarwal, Miller, Kästner & Vasilescu — *3100 opinions on code review in an AI world: building causal theory from practitioner discourse*. arXiv:2607.07980, 2026. [08 §5.2.2]
- Garousi, V. — *Human oversight and overload: two hidden and costly burdens of AI-assisted software engineering*. arXiv:2606.05770, 2026. [08 §5.2.1]
- Claes, Mäntylä, Kuutila & Adams — *Do programmers work at night or during the weekend?* ICSE 2018. [08 §4.1]
- Basili, V. R. & Selby, R. W. — *Comparing the effectiveness of software testing strategies*. IEEE TSE 13(12), 1987; Juristo, Moreno & Vegas — *Functional testing, structural testing and code reading: what fault type do they each detect?* LNCS 2765, 2003. [08 §5.1]
- Inozemtseva & Holmes — *Coverage is not strongly correlated with test suite effectiveness*. ICSE 2014; Zhang & Mesbah — *Assertions are strongly correlated with test suite effectiveness*. ESEC/FSE 2015. [08 §7.3] — confirmed on one suite (§2.4)
- Just, Jalali, Inozemtseva, Ernst, Holmes & Fraser — *Are mutants a valid substitute for real faults in software testing?* FSE 2014; Papadakis, Shin, Yoo & Bae — *Are mutation scores correlated with real fault detection?* ICSE 2018. [X-02] — the lineage for §1.6 and X-02 S-2/S-3
- PCI Security Standards Council — *PCI DSS v4.0*, Requirements 6.4 and 6.5. [08 §7.5, secondary] — the source of the narrowing in §2.9

**Reports of this programme cited as evidence [own]**
- `01-flagship-paper-ai-assisted-payment-module.md` — *What the Journal Got Wrong* (retitled 2026-09-21); §4.1–§4.14, §6, §7.4, §9 and Appendix A carry every measurement cited above
- `05-measurements.md` — M-1…M-30, the data catalogue; M-17, M-23, M-27 and M-30 carry the corrected entries
- `06-novelty-assessment.md` — N-1…N-14 and the three-paper split
- `07-lessons-learned.md` — the inference grading (Tiers S/D/U/N/X) and the tests T1–T10
- `08-literature-review.md` — the graded literature contacts and the two searches that broke our own results (§7.2, §7.3)
- `X-01-five-articles-against-the-literature.md` — Articles 1–5 and the corrections queue (§1.3)
- `X-02-five-deeper-studies.md` — studies S-1…S-5, pilots P1–P6, and §9 references
- `data/stats.py` — tests T1–T12; T11 (burst days, day-level permutation) and T12 (time-to-green) added 2026-09-21
- `data/README.md` — corpus schema, the mutation-testing determinism note, and the Jira and Actions caveats
