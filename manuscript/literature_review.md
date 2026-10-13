# Literature review: single-sample co-expression networks and interferon-low lupus

**Date:** 2026-10-13
**Purpose:** to summarise what is already known, and to show where the planned study adds to it.
**Note:** NCBI and PubMed could not be reached when this review was written. References marked "to verify" in the list were found by web search and must be checked before they are cited.

---

## 1. Introduction

This review covers three bodies of work that meet in our study. The first is the biology of systemic lupus erythematosus (SLE) without the type I interferon signature. The second is the family of methods that estimate a separate gene co-expression network for each patient. The third is the statistics needed to use such networks fairly: partial-correlation estimation, testing for differences in network structure, and control of leakage and confounding. For each area we summarise the main findings and then state what remains unknown. The final section brings these gaps together and sets out, plainly, which parts of our planned work are new and which build on existing results.

## 2. The interferon signature and interferon-low lupus

In most people with SLE, blood cells show a strong type I interferon (IFN) signature: dozens of IFN-stimulated genes (ISGs), such as IFI27, IFI44L and RSAD2, are switched on together [1–3]. Modular analyses of adult cohorts found the signature in about 87% of patients [1], and other cohorts report proportions between roughly 65% and 85%, depending on disease activity [2, 3]. The signature is linked to more active and more severe disease, and it was the basis for developing drugs that block type I IFN.

A substantial minority of patients, roughly 13–35%, are *IFN-low*. Their disease is clinically real, but its molecular basis is less clear. In sorted classical monocytes, Panwar et al. found only 5 genes that differed between IFN-negative SLE and healthy controls, compared with 1,288 for IFN-positive SLE [4]. Whole-blood studies give a less extreme picture: patients with a low IFN gene signature showed distinct eosinophil, IFN-γ and lymphocyte signatures [5]. Endotype analyses have repeatedly found a group of patients who resemble healthy controls [6–8]. These include a cross-disease study of seven systemic autoimmune diseases, which identified a "healthy-like" cluster [8], and a study showing that levels of the interferons themselves explain the IFN signature in only a minority of patients, which suggests IFN-independent disease mechanisms [7].

This matters for treatment. In pooled data from two phase III trials, the benefit of the type I IFN receptor antibody anifrolumab was clear in patients with a high IFN gene signature but smaller and statistically uncertain in those with a low signature [9]. Patients without the signature therefore lack the main target of current IFN-directed therapy, and what drives their disease remains an open question.

**What is unknown.** No study we found has asked whether IFN-low patients differ from healthy people in the *relationships* between genes rather than in gene levels. No published classifier reports its performance separately for IFN-low SLE.

## 3. Transcriptomic classifiers in SLE and the problem of leakage

Many studies have built classifiers that separate SLE from healthy controls using blood transcriptomes. Reported performance is often near perfect: one support-vector machine reached a cross-validated AUC of 0.998 [10], and a single ISG, MX2, has been reported to reach AUCs above 0.95 [11]. Because ISGs dominate these models, their success says little about patients who lack the IFN signature.

Such high numbers should also be read with care. Selecting genes on the full dataset before cross-validation can produce near-perfect apparent accuracy even when there is no real signal [12], and data leakage has been documented across many scientific fields [13]. Our companion study (paper 1) measures how much leakage inflates accuracy in SLE transcriptomic classifiers.

**What is unknown.** How well any method separates IFN-low SLE from health, when evaluated without leakage, has not been reported.

## 4. Single-sample network methods

Most network methods estimate one network for a whole group of samples. Single-sample methods instead estimate one network per individual, so that networks can be compared between patients or used as features for prediction.

**LIONESS** (Linear Interpolation to Obtain Network Estimates for Single Samples) estimates a sample's network by comparing a network built from all samples with one built after removing that sample, and scaling the difference [14]. It can be combined with any network estimator, and Pearson correlation is the most common choice. **Sample-specific networks (SSN)** take a related approach: they measure how much the correlation between two genes changes when one sample is added to a reference group, and test the change with a z-score [15]. **P-SSN** applies the same idea to partial correlation, so that indirect associations are removed [16]. **SWEET** weights an SSN-type network by how similar each sample is to the rest of the cohort, to correct for differences in subgroup size [17]. **BONOBO** takes a Bayesian approach, giving each sample a posterior co-expression matrix that combines a prior built from the other samples with that sample's own data [18]. Two recent reviews summarise the field [19, 20].

## 5. What single-sample networks measure

Two strands of work have begun to ask what these networks actually contain.

**Theory.** Liu et al. gave a first-order formula for SSN with Pearson correlation: the change in an edge is approximately a function of the product of the sample's standardized expression values for the two genes [15]. Benchmark and review studies have observed that LIONESS and SSN edges are almost perfectly linearly related when they share a reference network [20, 21]. LIONESS edges are also known to encode differences in mean expression, and to give larger weights to samples from under-represented groups [20, 21]. To our knowledge, no comparable first-order result has been published for partial correlation or for shrinkage estimators, and no common framework explains what the different methods share.

**Prediction.** The evidence that single-sample networks improve prediction is limited. A scoping review of individual-specific networks in medicine found that most studies were proofs of concept rather than validated prediction models [22]. In one recent comparison, Pearson-based LIONESS edges reached a held-out AUC of 0.467, against 0.815 for expression modules [23], and adding SWEET edges to expression gave only small gains in another study [24]. Turning complete, weighted networks into usable features is itself a methodological problem; threshold-integrated graph features have been proposed to avoid choosing a single sparsification threshold [25].

**What is unknown.** It is not established when, or why, single-sample network features should outperform simpler summaries of the same expression data, such as residuals, distances from a healthy reference, or quadratic classifiers.

## 6. Estimating and testing network structure

**Partial correlation with few samples.** Partial correlations come from the inverse of the covariance matrix, which is unstable or impossible to compute when the number of genes approaches the number of samples. Shrinkage estimation, which blends the sample covariance with a simple target, gives stable estimates in this setting [26]. The nonparanormal transform extends Gaussian network estimation to monotone non-linear relationships by working on rank-based normal scores [27].

**Testing for differences between groups.** Whether two groups differ in network structure can be tested directly. Pathway-based differential network analysis compares group-specific networks within known pathways and assesses significance by permutation [28]. Weighted gene co-expression network analysis (WGCNA) remains the most widely used way to summarise co-expression into modules [29], although it was designed for description rather than prediction. Tests for differences in multivariate spread are also available [30].

**What is unknown.** In practice, differences in network structure between groups can arise from genuine changes in co-regulation, from differences in spread, or from hidden subgroups. How to separate these explanations in blood transcriptomic data has received little attention.

## 7. Confounding in whole-blood studies of SLE

Three confounders are especially important when comparing SLE patients with healthy controls.

**Treatment.** Most patients take glucocorticoids, which change blood gene expression. Hu et al. derived a prednisolone-response signature that tracks glucocorticoid exposure; it also correlates with neutrophil and lymphocyte counts [31], so it partly reflects blood cell composition.

**Cell composition.** Variation in the proportions of blood cell types drives much of the co-expression seen in whole blood, so apparent network differences can simply reflect different cell mixtures.

**Sex.** About 90% of SLE patients are female. In a large whole-blood cohort, 54% of male patients showed abnormal XIST expression and silencing of X-linked genes [32], so XIST cannot be used to infer sex in SLE, and sex must be handled carefully in the design.

## 8. Synthesis: gaps and the contribution of this study

Bringing these strands together, the literature leaves four gaps:
1. The biology of IFN-low SLE is poorly understood, and no study has examined gene–gene relationships in these patients or reported classifier performance for them specifically.
2. Single-sample networks are widely used, but there is no theory explaining what partial-correlation or shrinkage-based networks contain.
3. The evidence that such networks improve prediction is weak, and they are rarely compared with baselines that capture the same information.
4. Differences in network structure are rarely separated from differences in mean or spread, or from hidden subgroups.

The planned study addresses these gaps, but not every part of it is new. Its relation to existing work is as follows.

**Already known, and to be cited rather than claimed:**
- Single-sample networks based on partial correlation exist as P-SSN [16].
- The first-order formula for SSN with Pearson correlation was given by Liu et al. [15].
- The near-perfect linear relationship between LIONESS and SSN edges has been observed empirically [20, 21].

**A modest extension:**
- We show that SSN is an *exact* rescaling of LIONESS for any association measure. This explains the observed relationship but does not by itself constitute a major result.
- Our exact shrinkage implementation with a symmetric, class-balanced reference is a design contribution.

**Probably new** (not found in our searches; a full PubMed and arXiv search is still required):
- A first-order formula for LIONESS with partial correlation, and its extension to shrinkage estimators.
- The predictions that follow from it: that a linear model on edges is equivalent to a quadratic classifier, and that unusual samples strengthen partial-correlation edges but weaken Pearson edges.
- A framework of mechanism-matched baselines and layered tests that separates differences in mean, spread and structure, including a check for hidden subgroups.
- The first application of single-sample networks to SLE, and the first classifier results reported specifically for IFN-low SLE.

In short, the study's main contribution is not a new network method but an explanation of what existing methods measure, tested rigorously in a demanding clinical setting.

---

## References

| # | Reference | Status |
|---|---|---|
| 1 | Chiche L, et al. Modular transcriptional repertoire analyses of adults with systemic lupus erythematosus reveal distinct type I and type II interferon signatures. *Arthritis Rheumatol* 2014. PMID 24644022. | Verified |
| 2 | Catalina MD, et al. Gene expression analysis delineates the potential roles of multiple interferons in systemic lupus erythematosus. *Commun Biol* 2019. PMID 31044165. | Verified |
| 3 | Banchereau R, et al. Personalized immunomonitoring uncovers molecular networks that stratify lupus patients. *Cell* 2016. PMID 27040498. | Verified |
| 4 | Panwar B, et al. Multi-cell type gene coexpression network analysis reveals coordinated interferon response and cross-cell type correlations in systemic lupus erythematosus. *Genome Res* 2021. PMID 33674349. | Verified |
| 5 | [Authors to confirm]. Type I interferon gene signature test-low and -high patients with systemic lupus erythematosus have distinct gene expression signatures. *Lupus* 2019. PMID 31660791. | To verify |
| 6 | Hubbard EL, et al. Analysis of transcriptomic features reveals molecular endotypes of SLE with clinical implications. *Genome Med* 2023. PMID 37845772. | Verified |
| 7 | Gómez-Bañuelos E, et al. Uncoupling interferons and the interferon signature explains clinical and transcriptional subsets in SLE. [Journal to confirm] 2024. PMC11148857. | To verify |
| 8 | Barturen G, et al. Integrative analysis reveals a molecular stratification of systemic autoimmune diseases. *Arthritis Rheumatol* 2021. | To verify |
| 9 | Vital EM, et al. Anifrolumab efficacy and safety by type I interferon gene signature and clinical subgroups in patients with SLE: post hoc analysis of pooled data from two phase III trials. *Ann Rheum Dis* 2022;81(7):951–961. PMID 35338035. | To verify |
| 10 | Li W, et al. Cuproptosis-related gene identification and immune infiltration analysis in systemic lupus erythematosus. *Front Immunol* 2023. PMID 37313407. | Verified |
| 11 | Meng XW, et al. MX2: identification and systematic mechanistic analysis of a novel immune-related biomarker for systemic lupus erythematosus. *Front Immunol* 2022. PMID 36059547. | Verified |
| 12 | Ambroise C, McLachlan GJ. Selection bias in gene extraction on the basis of microarray gene-expression data. *PNAS* 2002. PMID 11983868. | Verified |
| 13 | Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. *Patterns* 2023. PMID 37720327. | Verified |
| 14 | Kuijjer ML, et al. Estimating sample-specific regulatory networks. *iScience* 2019. PMID 30981959. | Verified |
| 15 | Liu X, et al. Personalized characterization of diseases using sample-specific networks. *Nucleic Acids Res* 2016. PMID 27596597. | Verified |
| 16 | Huang Y, et al. Disease characterization using a partial correlation-based sample-specific network. *Brief Bioinform* 2021;22(3):bbaa062. PMID 32422654. | Verified |
| 17 | Chen HH, et al. SWEET: a single-sample network inference method for deciphering individual features in disease. *Brief Bioinform* 2023;24(2):bbad032. | To verify |
| 18 | Saha E, et al. Bayesian inference of sample-specific coexpression networks. *Genome Res* 2024;34(9):1397. | To verify |
| 19 | De Marzio M, Glass K, Kuijjer ML. Single-sample network modeling on omics data. *BMC Biol* 2023. | To verify |
| 20 | Kuijjer ML, De Marzio M, Glass K. Challenges and opportunities in single-sample network modeling. *bioRxiv* 2026 (preprint). PMID 41867852. | Verified |
| 21 | Deschildre J, et al. Evaluation of single-sample network inference methods for precision oncology. *NPJ Syst Biol Appl* 2024. PMID 38360881. | Verified |
| 22 | Gregorich M, et al. Individual-specific networks for prediction modelling – a scoping review of methods. *BMC Med Res Methodol* 2022. | To verify |
| 23 | Leyva A, Niazi MKK. [Title to confirm]. *PLoS One* 2026. PMID 42743314. | Verified (title to confirm) |
| 24 | Yin L, et al. Sample-specific network analysis identifies gene co-expression patterns of immunotherapy response. *iScience* 2025. PMID 40740488. | Verified |
| 25 | Gregorich M, et al. Flexible parametrization of graph-theoretical features from individual-specific networks for prediction. *Stat Med* 2024. PMID 38664934. | Verified |
| 26 | Schäfer J, Strimmer K. A shrinkage approach to large-scale covariance matrix estimation and implications for functional genomics. *Stat Appl Genet Mol Biol* 2005. PMID 16646851. | Verified |
| 27 | Liu H, Lafferty J, Wasserman L. The nonparanormal: semiparametric estimation of high dimensional undirected graphs. *J Mach Learn Res* 2009;10:2295–2328. | To verify |
| 28 | Grimes T, Potter SS, Datta S. Integrating gene regulatory pathways into differential network analysis of gene expression data. *Sci Rep* 2019. | To verify |
| 29 | Zhang B, Horvath S. A general framework for weighted gene co-expression network analysis. *Stat Appl Genet Mol Biol* 2005. PMID 16646834. | Verified |
| 30 | Anderson MJ. Distance-based tests for homogeneity of multivariate dispersions. *Biometrics* 2006;62(1):245–253. | To verify |
| 31 | Hu Y, et al. Development of a molecular signature to monitor pharmacodynamic responses mediated by in vivo administration of glucocorticoids. *Arthritis Rheumatol* 2018. PMID 29534336. | Verified |
| 32 | Masson HO, et al. XIST expression and hypermethylation of the X chromosome in males with systemic lupus erythematosus. *Front Immunol* 2026. PMID 42039161. | Verified |

"Verified" means the PMID was checked against NCBI on 2026-10-01 (listed as verified in the study plan or the paper 1 plan).
