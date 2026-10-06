# Initial critique of `IFN_LOW_NETWORK_PLAN.md`

**Date:** 2026-10-06
**Reviewer:** Claude (AI assistant), for Pascal Antwi and Dr Tyler Grimes
**Scope:** the whole plan, with priority on (a) understanding it, (b) extending its scope, (c) methodological problems.
**Supporting code:** `reviews/2026-10-06_appendixA_checks.py` (numerical checks quoted in Section 2.3 and Appendix R1).

> **Important caveat on verification.** This session's network policy blocked NCBI (PubMed, E-utilities, GEO), Europe PMC and bioRxiv. I could only use a general web search. So **every new reference and GEO fact in this review that isn't already in the plan is marked *(web search only; not checked against NCBI)***. Following `CLAUDE.md`, check those against NCBI before citing them. Appendix R2 gives the list. I didn't re-check the PMIDs and accessions already in the plan; the plan says they were verified on 2026-10-01.

---

## Contents

- [The short version](#the-short-version)
- [1. Plain-language explanation of the study](#1-plain-language-explanation-of-the-study)
- [2. Motivation and novelty](#2-motivation-and-novelty)
- [3. Strengths and weaknesses](#3-strengths-and-weaknesses)
- [4. Extending the scope (priority)](#4-extending-the-scope-priority)
- [5. Feasibility](#5-feasibility)
- [6. Methodological issues](#6-methodological-issues)
- [7. Open decisions D1–D12](#7-open-decisions-d1d12)
- [8. Questions to ask Tyler](#8-questions-to-ask-tyler)
- [Appendix R1. Numerical checks](#appendix-r1-numerical-checks)
- [Appendix R2. Sources and verification status](#appendix-r2-sources-and-verification-status)

---

## The short version

**What the plan does well.** It's unusually careful. It thinks hard about leakage, confounding (sex, batch, treatment), a symmetric LIONESS reference, and "boring" baselines that could explain away a network result. The Appendix A derivation is **correct** (I re-derived it and checked it numerically), and it's a real insight. The simulation study is the right idea.

**The main problems:**
1. **The headline question is too narrow and too likely to give an uninterpretable null.** "Does LIONESS-partial beat WGCNA at telling IFN-low SLE from healthy people?" has no clinical use. In practice the answer will probably be driven by treatment, blood cell composition, or IFN signal left over below the cutoff. Two cohorts at most, likely only one, can't carry a methods paper on their own.
2. **Appendix A implies more than the plan draws from it.** Each LIONESS-partial edge is (almost exactly) a **quadratic function of the patient's own expression**. So an elastic net on LIONESS edges is essentially a **regularised quadratic classifier**, and every LIONESS feature is a function of information the baselines already have. "L2 beats M5 and M7, therefore it's a genuine network effect" doesn't follow as written (Section 2.4). The right way to show a co-regulation change is a **direct two-group test of the covariance structure**, which Tyler's own `dnapath` framework does. Classifier AUC is the wrong tool for that.
3. **The IFN-low cutoff leaves residual IFN signal.** Even if IFN-low patients were truly identical to controls, the tail of the IFN-high group that falls below the cutoff gives the leftover IFN score an AUC of about 0.6. If IFN-low patients are slightly raised, it reaches about 0.7–0.8 (Section 6.1). That's the size of effect the plan hopes to find.
4. **Several smaller technical issues:** shrinkage with pathways of 150 genes and about 130 training samples makes partial and Pearson LIONESS nearly identical; residual-based baselines need the same leave-one-out treatment as LIONESS; random-effects meta-analysis with 2 cohorts doesn't work; naive CV-based tests overstate certainty; and the stacking design is heavier than the sample sizes can support.

**Recommended extended scope** (Section 4). Turn the paper into:

> **"What do single-sample co-expression networks actually measure? A unifying quadratic theory, and a benchmark across autoimmune contrasts, with interferon-low lupus as the hardest case."**

It has three pillars:
- **(A) Method and theory.** Generalise Appendix A into a unifying result for LIONESS (Pearson and partial), SSN, P-SSN, SWEET and BONOBO. Use it to derive what each method can and can't detect, and test that in the simulation.
- **(B) A graded benchmark of real contrasts.** Run the comparison from strong to weak signal: IFN-high SLE vs healthy → IFN-low SLE vs healthy → **IFN-low SLE vs RA** (same-study controls in GSE110169) → **within SLE: disease activity, lupus nephritis**. Optionally add other autoimmune diseases (Sjögren's; PRECISESADS if access is granted).
- **(C) Biology of IFN-low SLE, done properly.** Use direct per-pathway tests of mean, dispersion and covariance differences (dnapath-style), adjusted for blood cell composition and the glucocorticoid score.

An optional fourth pillar, if the GEO annotations allow: **(D)** per-patient network change in the randomised tabalumab trials (GSE88885/GSE88886) or the longitudinal paediatric cohort (GSE65391).

**The 5 changes I'd prioritise:**
1. **Reframe the contribution** as theory plus benchmark plus biology (above). Make "LIONESS-partial vs WGCNA in IFN-low SLE vs HC" one contrast among several, not the whole paper.
2. **Add the direct population-level tests** (mean / dispersion / covariance per pathway, with permutation) as the mechanism analysis. Add a **regularised quadratic classifier** (QDA-type) as a baseline, since the theory says LIONESS edges live in that space.
3. **Fix the IFN-low definition.** Use a stricter primary cutoff, IFN-score matching between groups, and residual-IFN models as a mandatory comparator. Make **cell-composition estimates** a core confounder control, not an option.
4. **Simplify the machinery.** Cap pathways at about 50 genes for the primary analysis, cut the model list to about 8, use a lighter aggregation than two-level stacking, use fixed-effect or per-cohort reporting instead of random effects with k = 2, and use CV-aware inference.
5. **Do the data feasibility check first, and widen it.** In the next 2–3 weeks, count female IFN-low patients and controls in GSE88884, GSE319130 and GSE110169. Measure how big the *linear* IFN-low vs HC signal really is (the plan assumes it's tiny; whole blood may disagree). Start a PRECISESADS data-access request in parallel.

---

## 1. Plain-language explanation of the study

### 1.1 The question in one paragraph

Most people with lupus (SLE) have a strong **type I interferon (IFN) signature**: dozens of IFN-stimulated genes are switched on in their blood. That signature is so strong that almost any classifier can tell SLE from healthy blood, with published AUCs of 0.85–1.0. But roughly 13–35% of patients are **IFN-low**: their IFN genes look normal. In those patients, ordinary "which genes go up or down?" analyses find very little. The plan asks: if we stop looking at *levels* of genes and instead look at *relationships between genes within each patient*, using per-patient networks from LIONESS, can we see a difference that level-based methods miss? It then asks *why* any difference appears: is it really changed gene–gene wiring, or something simpler?

### 1.2 IFN-low SLE

- **Type I interferons** (IFN-α, IFN-β and others) are antiviral signalling proteins. When cells see them, they switch on a stereotyped set of "IFN-stimulated genes" (ISGs), such as IFI27, IFI44L and RSAD2. An **IFN score** averages these genes (after standardising each one), so a high score means lots of IFN activity.
- In SLE, the IFN score is high in most patients, and it's linked to more severe disease. The anti-IFN drug **anifrolumab** was developed on this basis.
- **IFN-low patients** still have SLE: they meet the classification criteria and often have active disease. But the main molecular hallmark is missing, so what drives their disease is less clear. That's the biological reason to care.
- The plan cites Panwar 2021: in sorted classical monocytes, IFN-negative SLE showed only 5 differentially expressed genes (DEGs) vs controls. Note that this was in **sorted cells**. In **whole blood** (what the plan's cohorts measure), shifts in cell composition and treatment effects add signal. For example, an AstraZeneca analysis of IFN-gene-signature-"test-low" patients reported distinct eosinophil, IFN-γ, and T-cell and B-cell signatures (PMID 31660791, *web search only*). So the premise that IFN-low patients look "almost like healthy people" in whole blood should be **measured, not assumed** (Section 5.4).

### 1.3 LIONESS, and how the partial-correlation version differs from your Pearson version

**The basic idea of LIONESS** (Kuijjer 2019). You have N samples. You can build one *aggregate* network from all of them, for example the Pearson correlation between every pair of genes. LIONESS asks what each sample *contributed* to that network:

> e_q = N · ρ(all N samples) − (N − 1) · ρ(all samples except q)

In words: build the network with everyone, build it again without patient q, and scale up the difference. The difference tells you how patient q pushed the network. Multiplying by N − 1 turns that small push into an edge weight on the same scale as the aggregate network. Averaged over all patients, the e_q values give back the aggregate network (approximately).

**In your osteosarcoma pilot** (`lionessR`), ρ was the **Pearson correlation**: how strongly two genes rise and fall together across patients, *ignoring all other genes*.

**In this plan**, ρ is the **partial correlation**: how strongly two genes rise and fall together *after removing the part of each that the other genes in the pathway explain*. Why does that matter?
- In whole blood, many genes correlate simply because the share of a cell type (say neutrophils) varies between people. All neutrophil genes then rise and fall together. Pearson correlation calls them all "connected".
- Partial correlation asks whether gene A and gene B are still related once we know all the other genes. That removes many **indirect** links (A↔C↔B looks like A↔B under Pearson, but not under partial correlation).
- Mathematically, partial correlations come from the **inverse** of the covariance matrix, called the **precision matrix** Ω: ρ_ij = −Ω_ij / √(Ω_ii Ω_jj).

**The catch: inverting a covariance matrix needs many samples.** With G genes you estimate about G²/2 covariances. If G is close to N (say a 150-gene pathway and 130 training samples), the plain sample covariance can't be inverted at all. So the plan uses **shrinkage** (Schäfer–Strimmer, `corpcor`):
- Blend the sample covariance with a simple target (here: no correlations, i.e. a diagonal matrix): Σ_λ = (1 − λ)S + λ·diag(S).
- λ between 0 and 1 controls how much you trust the data. Larger λ means more stable but more "pulled towards zero".
- The plan estimates λ once per training fold and then **holds it fixed** while doing LIONESS. That's sensible: otherwise removing one patient would also change λ and add noise.

**What's new compared with your pilot:**
- (1) partial instead of Pearson correlation
- (2) networks built **within Reactome pathways** (15–150 genes each) instead of one big network of the most variable genes
- (3) networks turned into **topology features** (node strength, clustering and so on) used for prediction, instead of limma tests on edges
- (4) everything done **inside cross-validation**, so nothing leaks from test patients into training

### 1.4 Appendix A, step by step

The goal of Appendix A is to find a simple formula for the LIONESS-partial edge, so we can see what it measures. Here's the argument, with what each step means.

**Step 0: notation.**
- Σ is the reference covariance matrix of the pathway's genes (divisor N), and Ω = Σ⁻¹ is the precision matrix.
- d is patient q's deviation from the reference mean (their expression minus the average).
- a = 1/(N − 1), a small number.

**Step 1: how does removing one patient change the covariance?**
- Patient q contributes d dᵀ/N to the covariance (an "outer product": a G × G matrix whose (i, j) entry is d_i·d_j).
- Removing q and re-averaging gives, to first order in a: Σ₋q ≈ Σ − a(d dᵀ − Σ).
- Intuition: if patient q's outer product d dᵀ is "bigger" than average (Σ), removing them shrinks the covariance in that direction.
- I checked this, including the change in the mean when q is removed. The exact result is Σ₋q = Σ − a[(N/(N−1)) d dᵀ − Σ], so the first-order version is right.

**Step 2: how does the precision matrix change?**
- For a small change δΣ, the inverse changes by approximately −Ω δΣ Ω (the matrix version of d(1/x) = −dx/x²).
- So Ω₋q ≈ Ω + a(Ω d dᵀ Ω − Ω Σ Ω) = Ω + a(u uᵀ − Ω), where **u = Ω d**.
- **What is u?** For each gene i, u_i/Ω_ii is the residual you get when you regress gene i on all the other pathway genes, evaluated at patient q. So u is "patient q's deviation, after removing what the other genes predict".
- **Scaled residual:** ũ_i = u_i/√Ω_ii is that residual divided by its standard deviation. Across a population, each ũ_i has variance 1.
- A subtle fact the plan states correctly: Cov(ũ_i, ũ_j) = **−ρ_ij**. The two genes' residuals are *negatively* correlated when their partial correlation is positive. That's a known property of regression residuals.

**Step 3: how does the partial correlation change?**
- ρ_ij depends on Ω_ij, Ω_ii and Ω_jj. Differentiating gives ρ − ρ₋q ≈ a[ũ_i ũ_j + ρ_ij (ũ_i² + ũ_j²)/2].
- I re-derived this. The "−a ρ" and "+a ρ" pieces cancel exactly, which is why the result is so clean.

**Step 4: plug into LIONESS.** e_q = ρ + (N − 1)(ρ − ρ₋q). The factor N − 1 cancels a = 1/(N − 1), leaving:

> **e_q ≈ ũ_i ũ_j + ρ_ij · (1 + (ũ_i² + ũ_j²)/2)**

**Step 5: sanity check.** Averaged over patients, E[ũ_i ũ_j] = −ρ and E[ũ²] = 1, so E[e_q] = −ρ + ρ(1 + 1) = ρ. The single-sample networks average back to the aggregate network, as LIONESS requires. ✔

**What the two terms mean:**
- **ũ_i ũ_j (the product term).** If, *for this patient*, genes i and j both deviate from what the rest of the pathway predicts, in the same direction, the edge goes up. In opposite directions, it goes down. This is "joint deviation". The baseline **M5** uses exactly these products.
- **ρ_ij (ũ_i² + ũ_j²)/2 (the squared terms).** If this patient is unusual for gene i or gene j *in either direction*, the reference edge ρ_ij gets **amplified**. Squares ignore direction, so patients who deviate in *different* directions (one up, one down) still look alike here. That's the "heterogeneity" argument. The baseline **M7** (distance from health) captures this.
- **Contrast with Pearson LIONESS** (your pilot): e_q ≈ z_i z_j + r_ij (1 − (z_i² + z_j²)/2). There the squared terms have a **minus** sign, so unusual patients get their edges *shrunk* towards zero. The two methods respond to outliers in **opposite** directions. That's worth a sentence in the paper.

### 1.5 What Appendix A implies, including some things the plan doesn't say

1. **Each LIONESS-partial edge is a fixed quadratic function of the patient's own expression.**
   - ũ = D⁻¹ᐟ² Ω d is a *linear* function of the patient's expression d. Ω and ρ come from the reference, so they're the same for everyone.
   - So e_q is quadratic in d. All the patient-specific information in a LIONESS network is the patient's expression vector (within that pathway), re-expressed.
   - That's not a flaw, since every single-sample feature is a function of the sample's expression. But it means **"network" features can't contain information that expression doesn't**. They can only present it in a form that a particular classifier finds easier to use.
2. **A linear model on edges is a quadratic classifier.**
   - An elastic net on all LIONESS edges of a pathway (model L1) computes Σ β_ij e_ij. That's a quadratic form ũᵀBũ plus a constant: a **quadratic discriminant**.
   - The optimal (Bayes) classifier for two Gaussian groups with different covariances is also a quadratic discriminant (QDA). So L1 is a cleverly parameterised, regularised QDA.
   - **A regularised QDA or quadratic-logistic baseline belongs in the comparison** (Section 6.6).
3. **Node strength is almost a simple function of the residuals.**
   - Node strength s_i = Σ_j e_ij ≈ ũ_i·(Σ_{j≠i} ũ_j) + Σ_j ρ_ij(1 + (ũ_i² + ũ_j²)/2).
   - That's "this gene's residual × the pathway's total residual" plus squared-residual terms. So the L2 strength features are close relatives of M4 (residuals) and M7 (sums of squared residuals).
4. **The squared terms also carry ordinary mean differences.**
   - If cases have a shifted mean, their ũ are shifted, so ũ² and ũ_iũ_j are larger on average.
   - So LIONESS edges also respond to plain differential expression. That matches Deschildre 2024 and Kuijjer, De Marzio & Glass 2026, who found LIONESS edges partly encode differential expression.
   - So in simulation scenario S1 (mean shift), L1 and L2 may do nearly as well as M2 and M4. The "expected winner" column should allow for that.
5. **‖W − P‖_F (one of the pathway-level features) is essentially a dispersion score.**
   - The distance between the patient's network and the reference network is a function of the ũ_ij products and squares.
   - So it's close to M7 by construction. Fine to keep, but it doesn't count as a "network" feature when interpreting results.

### 1.6 The baselines, in plain words

The plan's logic: if LIONESS wins, we must rule out every simpler explanation. Each baseline stands for one explanation.

| ID | What it is | The question it answers |
|---|---|---|
| **M0a** | The IFN score itself, within the IFN-low range | Is there leftover IFN signal below the cutoff? (Section 6.1 says probably yes.) |
| **M0b** | Glucocorticoid-response score (Hu 2018 genes) | Is the separation just steroid treatment? |
| **M1** | Elastic net or random forest on all genes | The standard "throw everything in" approach |
| **M2** | Pathway-by-pathway expression, then stacked | Same aggregation as LIONESS, but linear features. Is it the pathways, not the networks, that help? |
| **M3** | One score per pathway (singscore, mean z, PC1) | Classic "pathway activity" approach |
| **M4** | Conditional residuals ũ per pathway | The *linear* building block of LIONESS-partial. Does conditioning on other genes help on its own? |
| **M5** | Products ũ_i ũ_j, with the same topology metrics as L2 | LIONESS without the reference network. Is it just joint deviations? |
| **M6** | Non-linear models (boosting, kernel SVM) on pathway expression | Generic interactions, without network structure |
| **M7** | Distance from health per pathway (Σũ², or Mahalanobis distance) | Do patients simply scatter further from the healthy centre? |
| **W1** | A typical published WGCNA + hub-gene pipeline, done without leakage | What the SLE literature usually does |
| **W2** | WGCNA module eigengenes fitted inside each training fold | The primary "established network method" comparator |
| **L1** | LIONESS-partial edges | Edge-level network features |
| **L2** | LIONESS-partial topology (strength, clustering, …) | **The main model** |
| **L2-P** | Same, with Pearson LIONESS | Does *partial* correlation matter? |
| **L3** | L2 plus M2 | Does the network add anything over expression? |

### 1.7 Stacking

There are about 100 pathways, each giving dozens of features. Fitting one model to thousands of features from about 130 patients would overfit. **Stacking** does it in two levels:
1. **Level 1.** For each pathway, fit a small model (elastic net) that predicts SLE vs control from that pathway's features alone. Use inner cross-validation, so each training patient's prediction comes from a model that didn't see them ("out-of-fold" predictions).
2. **Level 2.** Treat each pathway's predicted probability as a new feature, and fit a second model (non-negative elastic net) that combines them. Its weights say which pathways matter ("pathway attribution").

The benefit is interpretability, plus the same aggregation for every feature type. The cost is complexity and variance (Section 6.5).

### 1.8 Nested cross-validation

- **Ordinary cross-validation (CV):** split the data into 5 folds, train on 4, test on 1, and rotate.
- **Nested CV:** every choice made from data (tuning λ, selecting features, picking the IFN cutoff, fitting WGCNA, fitting the stacker) is made *only from the training folds*, using a second, inner CV inside them. The outer test fold is touched only once, for the final evaluation.
- The plan repeats the whole thing 10 times with different random splits (10 × 5) to reduce the luck of a particular split.
- **Why it matters:** this is exactly the leakage problem from paper 1. If any choice sees the test patients, the AUC is inflated.

### 1.9 The simulation study

Real data can't tell you *why* a model wins. In a simulation you create data where you know the truth, then check whether your pipeline recovers it. The plan simulates:

| Scenario | What differs between groups |
|---|---|
| S0 | Nothing (the null) |
| S1 | Mean shift |
| S2a | Bigger variance in every direction |
| S2b | Hidden subtypes pushed in different directions |
| S3 | Genuinely rewired partial correlations |
| S4 | A treatment effect in some cases |

In each scenario the effect size is set so that the *best possible* classifier (the "oracle", which knows the true distributions) reaches an AUC of 0.6, 0.7 or 0.8. Every model is then compared with that ceiling. The result is a "reading guide": "if M7 wins and L2 doesn't beat it, the likely mechanism is dispersion", and so on. This is a strong part of the plan, and it becomes even more central under the extended scope (Section 4).

---

## 2. Motivation and novelty

### 2.1 Is the gap real? What the literature search found

I searched with a general web search engine (NCBI and Europe PMC were blocked; see the caveat at the top).

| Claim in the plan | What I found | Verdict |
|---|---|---|
| No application of LIONESS, SSN, SWEET, CSN, iENA or BONOBO to SLE | No SLE application turned up. LIONESS + PANDA has been applied to **rheumatoid arthritis synovium** (cell-specific regulatory networks; PMC10793435 / PMC11330812, *web search only*). Banchereau 2016 used **per-patient WGCNA** on longitudinal data, which is a different idea (each patient's own time series). | **Holds for SLE.** Not true for "autoimmune disease" in general, so word it as "SLE". |
| No LIONESS + partial correlation | Nothing found. The closest matches are P-SSN (Huang 2021, already cited), and partial-correlation individual networks in neuroimaging, which use **repeated measurements per person**, not LIONESS (Gregorich 2022 scoping review, PMC8898441, *web search only*). | **Holds**, as far as a web search can tell. Worth one more targeted PubMed search when access allows. |
| No classifier reports performance separately for IFN-low SLE | None found. But the IFN-low group has been **characterised**: AstraZeneca "IFNGS test-low vs high" signatures (PMID 31660791); Hopkins "IFN-independent endotypes" (Gómez-Bañuelos 2024, PMC11148857), which reports that dysregulated IFNs don't explain the IFN signature in 64% of patients; paediatric IFN-low endotype, 35% of 74 cSLE, PBMC RNA-seq (Cross et al. *Ann Rheum Dis* 2026, PMID 41539892); PRECISESADS cross-disease clusters including a "healthy-like" group (Barturen 2021). All *web search only*. | **The narrow gap holds**, but the plan's background should cite these papers. Otherwise reviewers will say "IFN-low SLE has been characterised". The novelty is the *method* and the *mechanism decomposition*, not the existence of the group. |
| Evidence that single-sample networks help prediction is thin | Consistent with Gregorich 2022: most studies are "proof of concept that network characteristics can in principle be useful", and few predict outcomes for new individuals. BONOBO (Saha et al. *Genome Res* 2024, PMC11529861) is published; it isn't a bioRxiv-only method any more. | **Holds.** It strengthens the case for the theory-plus-benchmark framing in Section 4. |
| SWEET | Chen et al. *Brief Bioinform* 2023, 24(2):bbad032 (*web search only*). It's in the target journal, so it's a natural comparator. | Add the citation. |

**Has anyone already shown that single-sample networks are quadratic in expression?**
- For **Pearson** LIONESS and SSN, the first-order formula is essentially in Liu 2016 (Eq. 4, as the plan notes). Kuijjer 2019 (*iScience*) also discusses the Pearson case.
- I found **no** paper that (a) derives the partial-correlation version, (b) treats the shrinkage case, or (c) uses the quadratic form to *unify* several single-sample methods and turn the result into testable predictions about what each can detect.
- That's the most defensible novelty in the project, and the core of my proposal A (Section 4). It still needs a proper PubMed and arXiv search before you claim it. Search terms to try: "single-sample network" AND (quadratic OR "first-order approximation" OR "influence function"), and "jackknife" AND "partial correlation".

### 2.2 Tyler's own work is directly relevant and should be cited

Tyler's **dnapath** (Grimes, Potter & Datta, *Sci Rep* 2019, *web search only*; R package on CRAN) does **pathway-based differential network analysis between two groups**, with permutation tests and any association measure, including partial correlation. That's exactly the population-level test the plan is missing for its mechanism question (Section 6.2). Using it:
- makes the analysis stronger
- plays to the supervisor's expertise
- makes "pathway-wise networks" a natural continuation of the lab's work, not an add-on

SeqNet (already cited) is the natural simulation engine.

### 2.3 Checking the Appendix A derivation

**Result: the derivation is correct.** I re-derived every step (Section 1.4) and re-ran the numerical check.

| Setting | cor(exact, plan's formula), plan | Same, my re-run |
|---|---|---|
| N = 100, G = 12, unshrunk | 0.9984 | 0.9986 |
| N = 300, G = 12, unshrunk | 0.9998 | 0.9999 |
| N = 100, G = 40, unshrunk | 0.9930 | 0.9918 |
| N = 100, G = 40, λ = 0.2 | 0.9953 | 0.9948 |
| N = 300, G = 12, λ = 0.2 | 0.9989 | 0.9983 |

(The small differences come from different random covariance structures.) The Pearson analogue is also correct: I re-derived it the same way.

**Three issues and one improvement:**

1. **Improvement: the shrinkage case can be derived, not just checked numerically.**
   - The plan says the shrinkage version is "supported empirically, not derived". But with λ held fixed, the shrinkage covariance Σ_λ = (1 − λ)S + λ·diag(S) is a **linear** function of S. So the same first-order argument goes through.
   - Removing patient q changes Σ_λ by −a[L(d dᵀ) − Σ_λ], where L(M) = (1 − λ)M + λ·diag(M).
   - Following Steps 2–4 with M = (1 − λ) u uᵀ + λ Ω diag(d²) Ω (scaled by √(Ω_ii Ω_jj) to give M̃) gives:

     > **e_q ≈ ρ + M̃_ij + ρ_ij (M̃_ii + M̃_jj)/2**

     which equals
     > ρ + (1 − λ)[ũ_iũ_j + ρ(ũ_i² + ũ_j²)/2] + λ[w_ij + ρ(w_ii + w_jj)/2], where w = Ω diag(d²) Ω scaled the same way.

   - It's still a quadratic form in d. Its expectation is still exactly ρ, because E[M] = Ω Σ_λ Ω = Ω.
   - Numerically it fits better than the plan's formula once λ is large (Appendix R1, Check 1): for example 0.9987 vs 0.9955 at N = 130, G = 150, λ = 0.7.
   - This handles one of the *Statistics in Medicine* "additions" in Section 7 of the plan. It assumes the variance part of the target is also held fixed. `corpcor` also shrinks the variances by a separate λ_var, which would need fixing too, or the same argument extended.
2. **"Exact" and "Sherman–Morrison".**
   - With a shrinkage target that depends on the sample variances, removing a sample changes diag(S) as well. The update is then not rank-one, so the Sherman–Morrison formula isn't exact.
   - Either hold the target fixed at the full-fold values (then it *is* rank-one, but it's a slightly different estimator), or just invert directly.
   - Direct inversion of a ≤ 150 × 150 matrix, N times per fold, takes seconds. **Recommendation:** drop Sherman–Morrison and invert directly; it's simpler and easier to unit-test.
3. **Training and test features: the exchangeability claim holds for exact LIONESS, but not for the residual baselines.**
   - I checked that exact leave-one-out (training) and exact add-one-in (test) LIONESS edges have the same spread: ratio 0.98–1.03 (Appendix R1, Check 3). The plan's symmetry argument is right.
   - **However**, if M5 and M7a compute residuals ũ from a reference that *includes* the training patient, the training residuals come out much smaller than test residuals. The ratio of mean Σũ² (test/train) was **1.4–1.9** (Check 2). In-sample points always look closer to the centre.
   - A classifier trained on the small training values would then be miscalibrated on test patients, unfairly handicapping those baselines.
   - **Fix:** compute ũ for each training patient from a leave-one-out mean and precision, exactly as LIONESS does implicitly.
4. **Accuracy at the extremes.**
   - The approximation is excellent on average, but max |difference| reaches about 7 at G = 40, N = 100 unshrunk.
   - The error grows with ũ⁴ terms, so it's worst for the most unusual patients. Those are the ones that matter for a dispersion story.
   - Keep the winsorising or rank transform, and report accuracy in the tails, not just the overall correlation.

### 2.4 The logical gap: "L2 beats M7 and M5 ⇒ genuine network effect"

This is the most important conceptual point in the review.
- From Section 1.5: L1 is (to first order) a linear combination of M5's products ũ_iũ_j and the squares ũ_i². L2 is a set of non-linear summaries of the same quantities.
- So if L2 beats M5 and M7, it means "a particular non-linear summary of residual products and squares classifies better at this sample size". It doesn't, by itself, mean "the gene–gene wiring differs between groups".
- Conversely, real rewiring (scenario S3) shows up directly in M5, and in M7's Mahalanobis version, as the plan notes. So L2 may *tie* with them even when rewiring is real.

**What's needed instead.** Separate two questions:
- **(i) Mechanism (population level):** do IFN-low SLE and healthy controls differ, per pathway, in **mean**, **dispersion** (overall variance) or **covariance / partial-correlation structure**? Answer this with direct two-sample tests (permutation tests on mean vectors, on total variance, and on the partial-correlation matrix, as in dnapath), adjusted for cell composition. No classifier is needed. The simulation can check the tests' power.
- **(ii) Prediction:** given the mechanism, which single-sample representation turns it into the best classifier at realistic N? This is where LIONESS vs M5/M7/QDA belongs, and the theory predicts the answer.

That separation also makes a null prediction result interpretable: "pathway X differs in covariance (test (i)), but no single-sample representation can exploit it at N ≈ 150 (test (ii))" is a clean, publishable statement.

---

## 3. Strengths and weaknesses

### 3.1 Strengths

1. **Leakage awareness is excellent.** The IFN cutoff inside folds, the symmetric reference, one sample per patient, the overlap catalog and the permutation check are all well ahead of the SLE literature, and consistent with paper 1.
2. **The "mechanism-aware baselines" idea is genuinely good.** Most single-sample-network papers compare against nothing, or against WGCNA. Building M5 and M7 from the method's own algebra is the right instinct.
3. **The Appendix A result is correct and useful**, and it can be generalised (Section 4, proposal A).
4. **Honest expected outcome.** The plan says a modest or confounded result is likely, and designs for it.
5. **The simulation study** with an oracle ceiling is the right way to make results interpretable.
6. **Confounding is taken seriously:** female-only primary analysis, Y-chromosome sex inference (not XIST, for a good reason), and batch eligibility.

### 3.2 Weaknesses (candidly)

1. **The scientific question is narrow, and its answer may not matter to anyone.**
   - Nobody needs to diagnose SLE vs health from blood in IFN-low patients. Doctors use clinical criteria and autoantibodies.
   - So the result only matters as (a) evidence about the *method*, or (b) evidence about the *biology* of IFN-low SLE.
   - As written, the plan is weak on both. With 1–2 cohorts and one contrast, it's not a convincing methods benchmark. And a classifier comparison is a poor way to learn biology (Section 2.4).
   - Tyler's "needs to be more substantial" is fair.
2. **The probability of a confounded or null result is high.** My rough, subjective estimate:
   - About 60–70% that L2 doesn't significantly beat the best simple baseline (M7, M2 or residual IFN).
   - About 50% that much of the separation tracks treatment, cell composition or residual IFN.
   - Reasons: the residual IFN signal (Section 6.1); the glucocorticoid score correlating with neutrophil counts and lymphocyte percentages (Hu 2018 reported this, *web search only*), so it partly measures composition; small samples; and the many-model comparison.
3. **Is a null publishable?**
   - *In the current scope, in Briefings in Bioinformatics:* unlikely, in my judgement. A single-cohort, single-contrast null with a heavy pipeline reads as a negative application, not a methods advance.
   - *Under the extended scope:* yes. A unifying theory, a simulation-validated reading guide and a multi-contrast benchmark are publishable whichever way the IFN-low result goes, because the paper's claim no longer depends on LIONESS "winning".
4. **The data may support only one cohort.**
   - GSE88884 has 60 controls in total. Female-only could leave fewer than 40, failing the go criterion.
   - So the likely real design is a single primary cohort (GSE319130) plus weak replication. That undermines "pooled across cohorts", and makes random-effects meta-analysis impossible (Section 6.4).
5. **Too many moving parts for the sample size.**
   - About 15 models × about 100 pathways × several topology metrics × two-level stacking × 10 × 5 nested CV × sensitivity analyses, on about 130 training patients.
   - The variance of the comparisons will be large, and the number of researcher choices ("forking paths") is high, even with Holm correction on H1–H3.
6. **The primary comparator is a low bar.**
   - H1 is "L2 beats WGCNA eigengenes". WGCNA eigengenes are a weak predictive baseline (one summary per module, built for description, not prediction).
   - Beating W2 says little. The informative comparisons are L2 vs M2, M7 and a quadratic baseline (H2, H3), and L3 vs M2 (added value). Section 6.7 suggests a re-ordering.
7. **Large pathways defeat the purpose of partial correlation.** With G = 150 and about 130 training samples, λ will be large. Then partial correlations become nearly proportional to marginal correlations. In my check, the per-edge across-patient correlation between LIONESS-partial and LIONESS-Pearson rose from 0.62 (G = 15) to 0.94 (G = 150, λ = 0.8; Appendix R1, Check 4). So L2 vs L2-P is uninformative for large pathways.

---

## 4. Extending the scope (priority)

Each proposal gives the question, the data, the extra work and the risk. They're ranked by value-for-effort, given Tyler's expertise and *Briefings in Bioinformatics*.

### Proposal A (rank 1): a unifying theory of single-sample co-expression networks, with a mechanism-based benchmark

**Question.** What do single-sample network methods actually measure, and under which data-generating mechanisms can they beat simple expression-based features?

**Content:**
1. Generalise Appendix A into a **unifying first-order result**:
   - LIONESS-Pearson, LIONESS-partial (with shrinkage; Section 2.3) and SSN (Liu 2016; essentially LIONESS without the N scaling) are all fixed quadratic forms in the sample's standardised (or conditionally standardised) deviation.
   - The same probably holds for P-SSN, SWEET (a sample-weighted SSN) and BONOBO (posterior covariance = prior + sample outer product, so plausibly quadratic). These need checking one by one.
   - CSN-type methods (local density counts) are the non-quadratic exception. That makes them a useful contrast.
2. **Derive predictions** from the theory. For example:
   - Edges respond to mean shifts through squared terms.
   - Partial and Pearson versions respond to dispersion with **opposite signs**.
   - A linear model on edges spans the same space as a regularised quadratic discriminant, so it can't beat a well-tuned QDA-type model asymptotically. It may still win at small N because of its regularisation structure, and that's testable.
3. **Test the predictions** in the simulation (already planned; expand it to the extra methods and add a QDA baseline). Then test them in the real contrasts of proposal B.

**Data.** Simulation (SeqNet; real control covariances) plus the cohorts already in the plan.

**Extra work.**
- About 1–2 months of derivation and code.
- SSN, SWEET and BONOBO have public implementations (BONOBO is in netZooPy/netZooR *(unverified)*), and SSN is a few lines of code.
- The derivations need careful checking (D11). Tyler or a statistician colleague is the right person.

**Risk.**
- Medium-low for the theory: the Pearson and partial cases are done; others may need approximations.
- The main risk is prior art for the unification idea. Do a thorough search before committing (Section 2.1).

**Why rank 1.** It makes the paper's contribution independent of whether LIONESS wins in SLE. It fits the target journal (methods-centred; SWEET and P-SSN were published there). And it builds directly on work you've already done.

### Proposal B (rank 2): a graded set of clinically meaningful contrasts

**Question.** How does the value of network features change as the linear signal weakens, and do they help in contrasts that matter clinically?

**Contrasts, from strongest to weakest expected signal:**

| Contrast | Clinical relevance | Candidate data | Feasibility notes |
|---|---|---|---|
| IFN-high SLE vs HC | Positive control | All cohorts | Already planned |
| IFN-low SLE vs HC | The original question | GSE319130, GSE88884 | Go/no-go check |
| **IFN-low SLE vs RA** | Differential diagnosis: both are inflammatory arthritides with autoantibodies | **GSE110169**: 82 SLE, 84 RA, 77 HC in one study and platform, with batch and glucocorticoid annotations (plan Table 3.1). GSE45291 (493 RA, 292 SLE; but the 20 controls are shared with the Hopkins series). | GSE110169 is the cleanest: same study, same platform, steroid status recorded. But IFN-low SLE may be only about 11–29 patients. GSE45291 has many more SLE and RA patients and the same platform, but it's a different patient population (Hopkins). |
| IFN-low SLE vs other systemic autoimmune diseases | Mechanistic: is IFN-low SLE molecularly "SLE" or "generic autoimmunity"? | **PRECISESADS** (Barturen 2021): whole blood from 955 patients with 7 diseases (SLE, RA, Sjögren's, SSc, MCTD, PAPS, UCTD) plus 267 HC, one platform. **Controlled access via ELIXIR Luxembourg** (*web search only*). GSE51092 (Sjögren's, 190 patients + 32 HC, Illumina GPL6884, *web search only*) has no SLE in the same study. | PRECISESADS is the ideal dataset. Access needs an application and a data-access agreement; allow 2–4+ months. **Apply now** if Tyler agrees. Cross-study contrasts (GSE51092 vs an SLE cohort) are confounded by batch and should be avoided. |
| Within SLE: disease activity (SLEDAI), high vs low | Clinically useful (monitoring) | GSE65391 (paediatric; SLEDAI per visit, *web search only*); GSE88884 (trial entrants: moderate-to-severe activity; is a per-patient SLEDAI in the supplement? *(unverified)*); Hopkins series (SLEDAI, *(unverified)*) | Activity contrasts are within SLE, so **no healthy controls are needed**. That removes the binding constraint of the whole plan. |
| Within SLE: lupus nephritis vs not | Clinically important | GSE99967 (29 LN + 16 HC plus non-LN SLE, Affymetrix Human Gene 2.0, *web search only*); GSE88884 (renal involvement, *(unverified)*) | Small, but again needs no controls if done as LN vs non-LN |

**Extra work.**
- Each extra contrast reuses the pipeline. The marginal cost is mostly data wrangling: about 1–2 weeks per cohort, plus the confounding audit.
- Within-SLE contrasts avoid the female-control bottleneck.

**Risk.**
- Low for the pipeline.
- Medium for the data: annotation availability, and small IFN-low counts in GSE110169.
- Higher for PRECISESADS (access may be refused or slow).

**Why rank 2.** It directly addresses "not clinically relevant" and "too few cohorts", and it turns Fig. 5 ("advantage vs signal strength") into the paper's main empirical result.

### Proposal C (rank 3): population-level biology of IFN-low SLE (mean vs dispersion vs covariance), adjusted for composition and treatment

**Question.** In IFN-low SLE, which pathways differ from health in mean, in dispersion, and in partial-correlation structure? Does any of this survive adjustment for blood cell composition and glucocorticoid exposure?

**Content.**
- Per-pathway permutation tests on three statistics: mean (e.g. Hotelling-type or a sum of t-statistics), dispersion (trace of the covariance, or mean squared Mahalanobis distance), and covariance or partial-correlation difference (dnapath-style).
- Run them on residuals after regressing out deconvolved cell proportions and the glucocorticoid score.
- Use the simulation to check power.

**Data.** The same cohorts as the main analysis, plus **cell-type deconvolution** (CIBERSORTx-type, or marker-gene scores). Whole-blood SLE studies show composition matters: adjusting for estimated proportions cut SLE-vs-HC DEGs by 76% in one study (PMC10311871, *web search only*).

**Extra work.** About 1 month. dnapath already exists, and deconvolution is standard.

**Risk.** Low to medium. The tests may find little, but "little beyond composition and treatment" is itself an answer to a real biological question.

**Why rank 3.** It replaces the weakest inferential step in the plan (classifier AUC as evidence of mechanism) with the right tool. It uses Tyler's method, and it's needed anyway to interpret proposals A and B.

### Proposal D (rank 4): per-patient network change over time, or under randomised treatment

**Question.** Do within-patient changes in pathway networks track changes in disease activity, or respond to a drug, beyond what expression changes show?

**Data:**
- **GSE88885 / GSE88886** (ILLUMINATE-1/-2, tabalumab, a BAFF-blocking antibody, vs placebo): blood at baseline, week 16 and week 52, HTA 2.0 (*web search only*). If treatment arm is annotated in GEO *(unverified; must check)*, this gives a **randomised** contrast: drug vs placebo change in network features, free of the confounding that dogs everything else.
- **GSE65391** (paediatric, 158 patients, 924 visits, SLEDAI per visit): within-patient association between change in network features and change in SLEDAI. A patient's own visits act as their controls.

**Extra work.**
- Longitudinal LIONESS needs a careful reference: one visit per patient in the reference, applied to all visits of held-out patients.
- Plus mixed models. About 1.5–2 months.

**Risk.**
- Medium-high. Arm labels may not be in GEO.
- Within-patient changes in IFN-low patients may be small.
- It adds a second paper's worth of analysis.

**Why rank 4.** High value if the annotations exist (randomisation is the cleanest causal design available). But it's a stretch for the timeline. It's a good **follow-up paper** if not included.

### Proposal E (rank 5): data-driven IFN-low endotypes from networks

**Question.** Are there reproducible subgroups among IFN-low patients, defined by pathway network features?

**Data.** The same cohorts. It needs ≥ 2 cohorts to show reproducibility.

**Extra work.** Small (clustering and stability analysis), about 2–3 weeks.

**Risk.** **High** for a meaningful result. Clustering always returns clusters, and with about 100–200 IFN-low patients, network-feature clusters may reflect treatment or composition. Hubbard 2023 and PRECISESADS already report endotypes.

**Recommendation.** Keep it as a descriptive supplementary analysis, with a pre-specified stability criterion (e.g. clusters reproduce across cohorts with adjusted Rand index > 0.5). Don't make it a pillar.

### Not separate proposals, but required anyway

- **Cell-type deconvolution:** a core confounder control (Section 6.3). It isn't an extension; the paper isn't credible without it.
- **Comparison with other single-sample methods (SSN, SWEET, BONOBO, CSN):** folded into proposal A, where the theory gives the comparison a purpose. Without the theory, a "we ran five methods" benchmark adds bulk but little insight.

### Recommended combination

**A + B + C as the paper; D as an optional extension or follow-up; E as a supplementary analysis.**

Suggested revised aims:
1. **Theory.** Derive the first-order (quadratic) representation of major single-sample co-expression methods, including the new LIONESS-partial with shrinkage, and state the predictions it implies.
2. **Simulation.** Test those predictions and build a reading guide, including the power of the population-level tests.
3. **Benchmark.** Compare single-sample network features with mechanism-matched baselines across a graded set of autoimmune contrasts: IFN-high vs HC → IFN-low vs HC → IFN-low SLE vs RA → activity / nephritis within SLE.
4. **Biology.** Characterise how IFN-low SLE differs from health (mean / dispersion / covariance per pathway), adjusted for composition and treatment.

Suggested title: *"What do single-sample co-expression networks measure? A quadratic theory and a benchmark across autoimmune contrasts, with interferon-low lupus as a stress test."*

**Trim to pay for it:**
- Drop W1, the literature-style pipeline; it belongs in paper 1.
- Drop M1-random-forest and M6-kernel-SVM; keep boosting.
- Shrink the Tier 2 simulation.
- Use pathways of ≤ 50 genes for the primary analysis (fewer, smaller, faster).

---

## 5. Feasibility

### 5.1 Data access

| Cohort | Access issue | What to do |
|---|---|---|
| GSE88884 | Expression is in supplementary files (HTA 2.0). The processed matrix may be large; raw CEL files would need RMA/SST-RMA. Controls are split across trial batches. | Download the supplementary processed matrix first. Check its normalisation, and whether controls and patients were normalised together. |
| GSE319130 | RNA-seq counts in supplementary files; only SLE/HC in the GEO matrix; sex must be inferred. Eli Lilly cohort; trial origin unknown. | Download counts; infer sex from Y-chromosome genes; check whether the controls could overlap any other Lilly cohort (e.g. GSE88884 controls). It's a different platform, but the same donors are possible. |
| GSE110169 | Affymetrix; batch and glucocorticoid status present | Quick win for the RA contrast and the steroid checks |
| PRECISESADS | Controlled access (ELIXIR Luxembourg) | Data-access application: needs Tyler as PI, an institutional agreement, and possibly ethics review. Start now; it may take months. |
| GSE88885/6 | Longitudinal; need arm labels | Check the GSM characteristics for treatment arm |

**Practical tip.** For supplementary-file cohorts, write a small download-and-parse script per cohort that saves a standard `SummarizedExperiment` (or a matrix plus a sample table). Commit the script, not the data. This is also part of the go/no-go check.

### 5.2 Compute

Cheap overall:
- LIONESS-partial on a ≤ 150-gene pathway is about 130 matrix inversions per fold. That's under a second per pathway per fold in R, so about 100 pathways × 50 outer fits × inner CV takes minutes to hours, not days.
- **The expensive parts** are the WGCNA fits inside each fold, gradient boosting with inner tuning, and the Tier 2 simulation (100 replicates × full nested pipeline × scenarios × sample sizes).
- **Estimate:** Tier 2 could be several CPU-days. A university cluster or a laptop running overnight in parallel is fine. Do the planned timing run early.

### 5.3 Timeline

- The plan's 10–11 months assumes paper 1 runs first or in parallel. Paper 1 is itself 5–6 months of intensive work (systematic review, double coding, re-runs, AI-analyst audits). **For one student, running both at once is the real feasibility risk**, more than compute or data.
- With the extended scope (A + B + C), I'd estimate **12–14 months** realistically, or 10–11 months if the trims in Section 4 are adopted and proposal D is deferred.
- A suggested sequence:

| Month | Work |
|---|---|
| 0–0.5 | Go/no-go check (expanded, Section 5.4); PRECISESADS application; prior-art search for the unification |
| 0.5–2 | Theory (proposal A) written up and checked by Tyler; LIONESS-partial code with unit tests; small-pathway pilot on GSE319130 controls only (no SLE labels touched) |
| 2–3.5 | Simulation Tier 1 with all methods plus QDA; population-level tests; reading guide; **register on OSF** |
| 3.5–6 | Real-data contrasts (B), primary cohort first |
| 6–7.5 | Biology (C); deconvolution-adjusted analyses; sensitivity analyses |
| 7.5–9 | Remaining contrasts / replication cohort; Tier 2 simulation (reduced) |
| 9–11 | Writing, code release, submission |

### 5.4 The go/no-go check: keep it, widen it

Add these items to Section 0:
1. **Measure the linear signal.** In each cohort, run a quick, leakage-safe, cross-validated elastic net on all genes (model M1) for IFN-low SLE vs HC. Also count DEGs (limma, FDR 5%).
   - If M1 already reaches AUC ≥ 0.85, the "hard case" premise is false, and the paper's story changes.
   - This uses outcome labels, so treat it as part of the feasibility stage and declare it in the registration.
2. **Residual-IFN check.** Compute the AUC of the IFN score alone *within* the IFN-low range (M0a). If it's ≥ 0.65, the IFN-low definition needs tightening (Section 6.1).
3. **Glucocorticoid score and composition.** The AUC of the glucocorticoid score alone, and of the estimated neutrophil and lymphocyte proportions alone.
4. **Female control counts** in GSE88884 (the most likely failure point).
5. **Contrast feasibility:** IFN-low SLE count in GSE110169 (vs RA); SLEDAI and LN annotations in GSE88884 and GSE65391; treatment arm in GSE88885/6.
6. **Revised go criterion:** see D1 (Section 7).

### 5.5 What to do first (next 2–3 weeks)

1. **Talk to Tyler** about the reframing (Section 8 questions), before investing in code.
2. **Run the expanded go/no-go check** on GSE319130, GSE88884 and GSE110169. Script the downloads and keep the outputs in a short report in `reviews/` or a new `feasibility/` folder.
3. **Learning exercise that also builds the code.** Take your osteosarcoma data. Implement LIONESS-partial (with fixed-λ shrinkage) alongside your existing Pearson LIONESS. Check numerically that the Appendix A formula matches on real data. This gives you the core function, unit tests and an intuition for the method, without touching SLE labels.
4. **Prior-art search** for the unification idea (Section 2.1), via PubMed/arXiv once you have access.
5. **If Tyler agrees, start the PRECISESADS access request.**

---

## 6. Methodological issues

### 6.1 The leakage-safe IFN-low definition is leakage-free but not confounding-free

- The cutoff is fitted inside folds and applied to both groups: correct, and clever.
- **The problem is truncation.** IFN-low SLE patients are those whose score falls below the cutoff. They include (a) truly IFN-normal patients and (b) the lower tail of patients whose IFN activity is mildly raised.
  - The controls below the cutoff are a nearly complete healthy distribution.
  - So *within* the IFN-low range, SLE patients sit higher on average. Any gene correlated with IFN activity (including genes outside the panel and outside the Reactome IFN pathways) carries that signal.
- **Illustration** (made-up but plausible numbers): controls N(0, 1); SLE = 25% "low" component plus 75% IFN-high N(4, 1.5); cutoff at control mean + 2 SD.

  | IFN-low component mean | Share of SLE called IFN-low | AUC of the residual IFN score |
  |---|---|---|
  | 0 (identical to controls) | 31% | **0.59** |
  | 0.5 | 30% | **0.68** |
  | 1.0 | 28% | **0.77** |

  The first row is the key: even with **no real difference** in the IFN-low component, the spill-over from the IFN-high tail gives AUC about 0.6.

**Recommendations:**
- (a) **Primary: a stricter cutoff**, e.g. IFN score ≤ control mean + 1 SD, or ≤ control 90th percentile. Report + 2 SD as sensitivity. Fewer patients, but a cleaner question.
- (b) **IFN-score matching:** within the IFN-low range, weight or match controls and patients on IFN score (e.g. by IFN-score bins), so the residual IFN score has AUC ≈ 0.5 by construction. Do it inside folds.
- (c) **Always report M0a**, and add **"L3-IFN" = L2 + residual IFN score vs residual IFN score alone**. The question becomes "does the network add anything beyond leftover IFN?".
- (d) Exclude the whole Reactome IFN subtree in the primary analysis (D4).

### 6.2 Mechanism inference

See Section 2.4. Add direct population-level tests (proposal C). Re-word Aim 3, and the risk-table row "Distance-from-health baseline matches LIONESS", in terms of those tests.

### 6.3 Cell composition and treatment

- **Whole-blood co-expression is dominated by cell composition.** Many "edges" will reflect variation in neutrophil, lymphocyte, B-cell or plasmablast proportions. Glucocorticoids shift composition (neutrophilia, lymphopenia), and the Hu 2018 signature correlates with neutrophil counts (*web search only*). So M0b partly measures composition.
- **Recommendations:**
  - Add **M0c: estimated cell proportions alone** (deconvolution or marker-gene scores) as a baseline.
  - Run an analysis on **composition-adjusted expression** (residuals after regressing out proportions inside folds).
  - Run the D7 sensitivity analysis with composition proxies in the partial-correlation conditioning set. Partial correlation is the natural tool for "co-expression *beyond* composition", and that's a nice selling point.
- **Hu 2018 details to check against the paper** (*web search only*): it reportedly identified **64 up-regulated and 18 down-regulated** genes. Decide whether the score uses both. The plan mentions only the 64.

### 6.4 Pooling, testing and power

1. **Random-effects meta-analysis with 2 cohorts doesn't work.** The between-cohort variance can't be estimated meaningfully from k = 2. Use a fixed-effect (inverse-variance) pooled estimate with an explicit heterogeneity statement, or simply report each cohort and require the same sign in both.
2. **CV-based tests overstate certainty.**
   - DeLong tests on out-of-fold predictions treat them as independent test-set predictions. They aren't: the models share training data across folds and repeats.
   - Repeated CV reduces split noise but doesn't create new information.
   - Use the nested-CV standard error of Bates, Hastie & Tibshirani (*JASA* 2023 / arXiv 2104.00673, *(unverified citation details)*), a corrected resampled t-test (Nadeau–Bengio), or a bootstrap of the whole pipeline (expensive).
   - Then **validate the testing procedure in the S0 simulation** (false-positive rate ≈ 5%). The plan already has the machinery.
3. **Power is limited.**
   - With about 90 vs 77 patients, an AUC near 0.7 has SE ≈ 0.04.
   - For two models whose predictions correlate at about 0.7, the paired difference has SE ≈ 0.03. So the **smallest reliably detectable difference is about 0.08–0.09** (80% power, two-sided 5%), and more after Holm.
   - Differences between closely related models (L2 vs M5 or M7) will usually be smaller than that. Report **estimates with intervals** as primary, and treat the hypothesis tests as secondary. The simulation should confirm these numbers.
4. **Number of models.**
   - About 15 models plus about 6 sensitivity analyses gives a large space of possible "findings".
   - Holm on H1–H3 controls the formal tests, but readers will look at everything.
   - Cut to about 8 models (suggestion: M0a, M0b, M0c, M2, M4, M7, QDA-type, W2, L2, L2-P, L3). Pre-register which comparisons are confirmatory, and label the rest exploratory.

### 6.5 Is the stacking design overkill?

Mostly yes, for these sample sizes.
- Two-level stacking with inner CV inside 10 × 5 outer CV, for about 100 pathways and about 10 models, gives long run times, high variance, and many tuning choices.
- **Simpler alternatives** with the same "same aggregation for every feature type" property:
  - **(a)** Per-pathway out-of-fold scores, then a non-negative ridge or plain average. This is stacking with a fixed, simple second level.
  - **(b)** A **group lasso** with pathways as groups: one model, built-in pathway selection.
  - **(c)** Pre-specify about 20–30 pathways from the immune subtree (fewer, smaller, less redundant).
- Keep full stacking as a sensitivity analysis if you like. Attribution from stacking weights is unstable with correlated pathways anyway; report how often each pathway gets a weight across repeats, not one set of weights.

### 6.6 Missing baselines

- **Regularised quadratic discriminant (QDA-type) per pathway:** e.g. shrinkage QDA, or logistic regression on ũ and the products ũ_iũ_j with a ridge penalty. By the theory this is the "closest strong competitor" to L1 (Section 1.5).
- **M0c composition baseline** (Section 6.3).
- **M7 with a leave-one-out reference** (Section 2.3, issue 3), and the same for M5 and M4.

### 6.7 Hypothesis ordering

Suggested confirmatory set:
- **H1:** L3 (L2 + M2) beats M2. Does the network add anything over expression? This is the most interpretable question.
- **H2:** L2 beats M7 and the QDA-type baseline.
- **H3 (theory test):** the rank pattern across simulation scenarios matches the predictions of proposal A.
- **W2 (WGCNA)** becomes a reported comparator, not the primary.

### 6.8 Topology metric details

- **Rescaling to [−1, 1] for signed clustering and betweenness:** say *how*. A per-patient maximum throws away scale information, which is itself discriminative. A global, training-fold-based rescaling keeps it. Prefer the latter.
- **Betweenness and clustering on complete signed graphs are unstable.** Given the quadratic structure, strength and pathway-level summaries carry most of the information. Make betweenness exploratory.

### 6.9 Pathway size

- With G = 150 and N ≈ 130 per training fold, shrinkage dominates, and LIONESS-partial ≈ scaled LIONESS-Pearson (Section 3.2, point 7).
- **Recommendation:** primary analysis on pathways with 15–50 genes (G/N ≲ 0.4); 51–150 genes as secondary. Report the λ values chosen.

### 6.10 Smaller points

- **One sample per patient at the first visit:** good. For GSE65391 the controls include technical replicates; average them, as planned.
- **The LIONESS reference** (IFN-low + controls, both classes) is right. Note one implication: the reference mean lies *between* the classes, so class-mean differences appear in each patient's d and hence in the edges (Section 1.5, point 4). That's another reason S1 needs care.
- **XIST and the female-only analysis:** fine. The note about male XIST expression (Masson 2026) is well taken.
- **Precision table:** I re-computed one entry with the Hanley–McNeil formula (150 vs 60, AUC 0.65 → ±0.078). It matches.
- **The "go" minimum of 40 vs 40 gives ±0.12 on a single AUC.** That's too imprecise for a primary cohort; fine for replication. Reflected in D1.

---

## 7. Open decisions D1–D12

| # | Decision | My recommendation | Reasoning |
|---|---|---|---|
| **D1** | Go criterion | **One primary cohort with ≥ 80 female IFN-low (under the *stricter* cutoff, Section 6.1) and ≥ 60 female controls, not batch-confounded; plus ≥ 1 replication cohort of any size ≥ 25/25, reported descriptively.** Also add the expanded checks of Section 5.4 (linear-signal AUC, residual IFN AUC, glucocorticoid and composition AUCs). | 40/40 gives ±0.12 on an AUC, too imprecise for primary inference. Requiring two large cohorts will probably fail on GSE88884's female controls. Under the extended scope, the within-SLE contrasts don't need controls at all, so the go criterion applies only to the HC contrasts. |
| **D2** | Primary cohorts and structure | **GSE319130 as the likely primary; GSE88884 as replication or second primary depending on counts.** Within-cohort analysis; **fixed-effect pooling or "consistent sign" rather than random effects.** | k = 2 can't support random effects (Section 6.4). |
| **D3** | IFN gene set | **A short, widely used ISG panel**, ideally the genes of the anifrolumab-trial 4-gene IFNGS test (IFI27, IFI44, IFI44L, RSAD2; *from memory, (unverified): check the source*), or the plan's 6-gene panel. Others as sensitivity. | It ties the IFN-low definition to the clinical-trial literature ("IFNGS-low"), which helps readers and reviewers. |
| **D4** | Exclude IFN pathways from features? | **Exclude the whole Reactome Interferon Signaling subtree in the primary analysis**; include it as sensitivity. Plus IFN-score matching and an L3-IFN comparison (Section 6.1). | Because of truncation, residual IFN signal is likely (Section 6.1). A conservative primary makes any "IFN-independent" claim credible. |
| **D5** | How to handle confounding | **Design-based primary (agree), plus a composition baseline (M0c), composition-adjusted sensitivity analysis, and the glucocorticoid score as both a baseline and an adjustment in the population-level tests (proposal C).** | Design alone can't handle composition, which is the biggest driver of whole-blood co-expression. |
| **D6** | Pathway set and version | **Immune subtree, 15–50 genes primary; 51–150 secondary; all Reactome exploratory.** Pin the Reactome release *and* the `msigdbr`/MSigDB version, and save the gene lists in the repo. | The G/N issue (Section 6.9); reproducibility. |
| **D7** | Composition proxies in the conditioning set? | **Yes, as a key sensitivity analysis** (not optional). Consider making it co-primary if deconvolution is reliable on the platform. | Partial correlation conditional on composition is exactly "co-expression beyond composition", the most defensible biological interpretation. |
| **D8** | LIONESS reference | **Analysis set (IFN-low + controls) primary; agree.** IFN-high-inclusive reference as sensitivity. | The symmetry argument is right, and verified (Section 2.3). An IFN-high-inclusive reference changes Ω towards IFN-driven structure, which complicates interpretation. |
| **D9** | Topology metric set | **Primary: s⁺, s⁻ per node; mean \|w\|; leading eigenvalue; ‖W − P‖_F (labelled as a dispersion-type feature). Exploratory: signed clustering, betweenness, global efficiency.** Global, fold-based rescaling. | The theory shows strength and pathway summaries carry most of the information; betweenness and clustering are noisy on complete signed graphs. |
| ~~D10~~ | Framing and venue | Decided (BiB, method-centred). **Under the extended scope this decision is stronger**, because the paper becomes a methods paper whichever way the result goes. | — |
| **D11** | Independent check of the derivation | **Yes: Tyler first, then a statistician colleague.** Include the shrinkage extension (Section 2.3) and any unification results from proposal A. | New theory is the paper's main claim under the extended scope; it must be right. |
| **D12** | Simulation scope | **Tier 1 in full** (add QDA, SSN, SWEET, BONOBO, and the population-level tests). **Tier 2 reduced**: 50 replicates, 2 sample sizes, S0/S1/S3. Set the final counts after a timing run. | Tier 1 carries the theory test. Tier 2 mainly checks the stacking and attribution machinery, which my simplification (Section 6.5) makes less central. |

---

## 8. Questions to ask Tyler

**Scope and framing**
1. Would you support reframing the paper around a unifying theory of single-sample networks plus a multi-contrast benchmark, with IFN-low SLE as the hardest test case? Or do you see SLE biology as the main story?
2. When you said "more substantial", did you mean more data and contrasts, more method (theory and other ssN methods), or more clinical relevance? Which matters most to you?
3. Is it OK to use **dnapath** for the population-level differential-network tests? Would you be the right person to check the theoretical extensions (D11)?

**Data**

4. Do you have, or could we get, access to **PRECISESADS** (controlled access via ELIXIR Luxembourg)? Is it worth the application effort and time?
5. Do you know anyone with access to anifrolumab or other trial transcriptome data, or contacts at Lilly about GSE319130's origin (e.g. whether its controls overlap GSE88884's)?
6. Are you happy for the go criterion to require one strong primary cohort plus a smaller replication cohort, rather than two cohorts of ≥ 40/40?

**Methods**

7. Should the primary hypothesis be "L2 beats WGCNA" (as now) or "networks add to expression" (L3 vs M2)? Do you agree that WGCNA eigengenes are a low bar?
8. How much of the stacking machinery do you want to keep? Would group lasso or a simple average of per-pathway scores be acceptable as primary?
9. What's your view on cell-type deconvolution for whole-blood SLE (methods, reference panels)? Should composition proxies be in the partial-correlation conditioning set in the primary analysis?
10. For CV-based inference, do you have a preferred approach (Bates et al. nested-CV standard error, corrected t-test, full bootstrap)?

**Timeline and workload**

11. Should paper 1 (leakage) be finished, or only well underway, before paper 2 starts in earnest? Running both at once is the biggest risk to the timeline.
12. Is a 12–14 month timeline acceptable for the extended scope, or should we trim to keep 10–11 months (e.g. defer the longitudinal/tabalumab analysis to a follow-up paper)?

---

## Appendix R1. Numerical checks

Script: `reviews/2026-10-06_appendixA_checks.py` (Python + numpy). Data: Gaussian, tridiagonal precision matrix (off-diagonal 0.4). Shrinkage: Σ_λ = (1 − λ)S + λ·diag(S), λ fixed.

**Check 1: exact LIONESS-partial vs first-order formulas** (correlation over all patients and edges):

| N | G | λ | Plan's formula | Shrinkage-corrected formula (Section 2.3) |
|---|---|---|---|---|
| 100 | 12 | 0 | 0.9986 | 0.9986 |
| 300 | 12 | 0 | 0.9999 | 0.9999 |
| 100 | 40 | 0 | 0.9918 | 0.9918 |
| 100 | 40 | 0.2 | 0.9948 | 0.9966 |
| 300 | 12 | 0.2 | 0.9983 | 0.9999 |
| 100 | 40 | 0.5 | 0.9944 | 0.9988 |
| 130 | 100 | 0.5 | 0.9954 | 0.9980 |
| 130 | 150 | 0.7 | 0.9955 | 0.9987 |

**Check 2: residual features with an in-sample reference are on a different scale for training vs test patients** (mean Σũ²/G):

| N | G | λ | Training (in-sample) | Test (new) | Ratio |
|---|---|---|---|---|---|
| 130 | 15 | 0.1 | 0.87 | 1.22 | 1.40 |
| 130 | 50 | 0.3 | 0.66 | 1.06 | 1.61 |
| 130 | 100 | 0.5 | 0.53 | 1.00 | 1.90 |
| 130 | 150 | 0.7 | 0.54 | 1.00 | 1.87 |

→ M4, M5 and M7 must use leave-one-out residuals for training patients.

**Check 3: exact LIONESS edges are on the same scale for training (leave-one-out) and test (add-one-in) patients** (SD of edge deviation from the reference):

| N | G | λ | Training | Test | Ratio |
|---|---|---|---|---|---|
| 130 | 15 | 0.1 | 0.917 | 0.936 | 1.02 |
| 130 | 50 | 0.3 | 0.593 | 0.589 | 0.99 |
| 130 | 100 | 0.5 | 0.374 | 0.368 | 0.98 |
| 130 | 150 | 0.7 | 0.211 | 0.217 | 1.03 |

→ The plan's symmetry and exchangeability argument holds for exact LIONESS.

**Check 4: LIONESS-partial vs LIONESS-Pearson** (mean per-edge correlation across patients):

| N | G | λ | Correlation |
|---|---|---|---|
| 130 | 15 | 0.1 | 0.62 |
| 130 | 50 | 0.3 | 0.70 |
| 130 | 100 | 0.6 | 0.84 |
| 130 | 150 | 0.8 | 0.94 |

→ For large pathways, heavy shrinkage makes the partial and Pearson versions nearly the same, so L2 vs L2-P is only informative for small pathways.

**Residual-IFN illustration** (Section 6.1) was a one-off calculation, not in the script: controls N(0, 1); SLE = 25% N(μ_low, 1) + 75% N(4, 1.5); cutoff 2.0; AUC of the IFN score among those below the cutoff.

---

## Appendix R2. Sources and verification status

**Not checked against NCBI** (network blocked). Found by web search only. Verify the PMID, journal and details before citing.

| Source | What it's used for | Link seen |
|---|---|---|
| "Type I interferon gene signature test-low and -high patients with SLE have distinct gene expression signatures" (AstraZeneca group; *Lupus* 2019?) PMID 31660791 | IFN-low SLE has whole-blood signatures vs HC | pubmed.ncbi.nlm.nih.gov/31660791 |
| Gómez-Bañuelos E et al. "Uncoupling interferons and the interferon signature explains clinical and transcriptional subsets in SLE", 2024 (journal to confirm) | IFN-independent endotypes | PMC11148857 |
| Cross H et al. "Type I interferon endotypes drive divergent clinical trajectories in childhood-onset SLE…", *Ann Rheum Dis* 2026, PMID 41539892 | Paediatric IFN-low endotype (35%) | pubmed.ncbi.nlm.nih.gov/41539892 |
| Barturen G et al. "Integrative analysis reveals a molecular stratification of systemic autoimmune diseases" (PRECISESADS), *Arthritis Rheumatol* 2021 | Cross-disease cohort; controlled access, ELIXIR Luxembourg | medRxiv 10.1101/2020.02.21.20021618; datacatalogue.elixir-luxembourg.org |
| Grimes T, Potter SS, Datta S. "Integrating gene regulatory pathways into differential network analysis of gene expression data", *Sci Rep* 2019 (dnapath) | Population-level differential network tests | CRAN dnapath; github.com/tgrimes/dnapath |
| Saha E et al. "Bayesian inference of sample-specific coexpression networks" (BONOBO), *Genome Res* 2024;34(9):1397 | Comparator method | PMC11529861 |
| Chen HH et al. "SWEET: a single-sample network inference method…", *Brief Bioinform* 2023;24(2):bbad032 | Comparator method | — |
| Gregorich M et al. "Individual-specific networks for prediction modelling – a scoping review of methods", *BMC Med Res Methodol* 2022 | Prediction value of ISNs is unproven | PMC8898441 |
| De Marzio M, Glass K, Kuijjer ML. "Single-sample network modeling on omics data", *BMC Biol* 2023 | Background review | PMC10755944 |
| Kuijjer, De Marzio & Glass 2026, "Challenges and opportunities in single-sample network modeling" | Already in the plan (PMID 41867852); web search shows a PMC version (PMC13001488), so check whether it is now published beyond bioRxiv | PMC13001488 |
| LIONESS + PANDA in rheumatoid arthritis synovium ("Cell-specific gene networks and drivers in RA synovial tissues") | ssN applied to autoimmune disease (not SLE) | PMC10793435 / PMC11330812 |
| Whole-blood deconvolution in SLE (MMF study; CIBERSORTx) | Composition confounding; 76% fewer DEGs after adjustment | PMC10311871 |
| Hu Y et al. 2018 (already in the plan) | 64 up + 18 down genes; correlation with neutrophil counts and lymphocyte % | PMC6099349 |
| Bates S, Hastie T, Tibshirani R. "Cross-validation: what does it estimate and how well does it do it?" *JASA* 2023 (arXiv 2104.00673) | CV-aware inference | from memory, *(unverified)* |
| Parodis group: "Transcriptome analysis to decipher the molecular underpinnings of response to treatment in SLE", PMID 40081913 | Possible treatment-response data (availability unknown) | pubmed.ncbi.nlm.nih.gov/40081913 |

**GEO facts seen via web search only** (OmicsDI or papers citing the series). Check on GEO:

| Accession | Claimed content | Use |
|---|---|---|
| GSE88885 / GSE88886 | ILLUMINATE-1/-2 longitudinal (baseline, week 16, week 52), HTA 2.0; tabalumab vs placebo. **Arm labels not confirmed.** | Proposal D |
| GSE65391 | 158 paediatric SLE, 924 samples, up to 4 years; SLEDAI-2K per visit | Proposals B (activity) and D |
| GSE51092 | 190 Sjögren's + 32 controls, whole blood, GPL6884 | Proposal B (cross-study, so confounded) |
| GSE93272 | RA whole blood, GPL570, Tasaki 2018; treatment-response subsets; HC count unclear (35–43) | Possible RA cohort (cross-study) |
| GSE99967 | Whole blood, GPL21970: 29 LN, 16 HC (+ non-LN SLE?) | Proposal B (LN) |
| GSE17755 | PBMC: RA, SLE, polyJIA, sJIA, healthy adults and children; 248 patients | Same-study multi-disease contrast (PBMC, older platform) |
| GSE149050 | Panwar 2021 sorted-cell IFNpos/IFNneg SLE | Background |
| GSE319130 | 720 SLE (679 F), 84 HC (77 F): matches the plan | — |

**Searches that found nothing relevant:** "LIONESS" + "lupus"; "single-sample network" + SLE; "LIONESS" + "partial correlation"; "graphical lasso" + LIONESS. Each search used one general web search engine; repeat in PubMed and Europe PMC when access allows.
