# Literature review: single-sample co-expression networks and interferon-low lupus

**Date:** 2026-10-13 (version 3)
**Purpose:** to summarise and appraise what is known, and to show where the planned study adds to it.
**Reference status:** of 45 references, 21 were checked against NCBI on 2026-10-01, 18 have identifiers (PMID, DOI or journal details) confirmed by web search, and 6 still need checking. All 24 not checked against NCBI must be confirmed on PubMed before citation (see the reference list).

---

## 1. Introduction

Our planned study sits where three bodies of work meet:
- the biology of systemic lupus erythematosus (SLE) in patients who lack the type I interferon signature
- methods that estimate a separate gene co-expression network for each patient
- the statistics needed to use such networks fairly: estimating partial correlations, testing for differences in network structure, and controlling leakage and confounding

For each area, this review summarises the main findings, appraises the strength of the evidence and states what remains unknown. The final section brings the gaps together and sets out which parts of the planned work are new and which build on existing results.

## 2. How this review was done

This is a structured narrative review, not a systematic review.
- **Sources.** A PubMed search was run on 2026-10-01 while the study plan was being prepared. The searches for this review were general web searches, run between 2026-10-06 and 2026-10-13; they index PubMed Central, publisher sites, bioRxiv and medRxiv. Direct access to PubMed, Europe PMC and GEO was not available for these later searches.
- **Search terms.** Combinations of: *LIONESS*, *single-sample network*, *sample-specific network*, *individual-specific network*, *cell-specific network*, *partial correlation*, *shrinkage*, *differential co-expression*, *differential network*, *covariance test*; *systemic lupus erythematosus*, *interferon signature*, *interferon-low*, *interferon-negative*, *endotype*, *single-cell*, *longitudinal*; *anifrolumab*; *deconvolution*, *whole blood*; *glucocorticoid signature*.
- **Inclusion.** Methods papers that define or benchmark single-sample or differential network methods; studies of interferon status, its stability or endotypes in SLE blood; trials reporting outcomes by interferon status; and methodological papers on leakage, shrinkage estimation, covariance testing and confounding that bear directly on the planned design.
- **Limitations.** There was a single reviewer, with no formal screening or risk-of-bias tool. Full texts were not available for several papers, so some appraisals rely on abstracts; this is stated where it applies. Not finding a study in these searches means only that it was not found, not that it does not exist.

## 3. The interferon signature and interferon-low lupus

### 3.1 How common the signature is

In most people with SLE, blood cells show a strong type I interferon (IFN) signature: dozens of IFN-stimulated genes (ISGs), such as IFI27, IFI44L and RSAD2, are switched on together. The proportion of patients who carry it depends on the cohort and the definition:
- 87% in a modular analysis of adult patients [1]
- 66–73% in an analysis by disease-activity state [2]
- 84.8% of samples in a longitudinal paediatric cohort of 158 patients [3]

The remaining 13–35% of patients are what we call *IFN-low*.

**Appraisal.** These figures come from different platforms, gene sets and cut-offs, so they are not directly comparable. A study that defines IFN status must therefore state its gene set and threshold explicitly.

### 3.2 What is known about IFN-low patients

Gene expression in IFN-low patients differs much less from that of healthy people, but it is not normal:
- **Sorted cells.** In sorted immune cell types, Panwar et al. found only 5 genes that differed between IFN-negative SLE and healthy controls in classical monocytes, against 1,288 for IFN-positive SLE [4].
- **Whole blood.** Patients with a low IFN gene signature showed distinct eosinophil, IFN-γ and T-cell or B-cell signatures [5].
- **Endotypes.** Endotype studies have repeatedly found a group of patients who resemble healthy controls. These include a "least-perturbed" endotype [6], and a "healthy-like" cluster in an integrated transcriptome and methylome study of 955 patients with seven systemic autoimmune diseases and 267 controls [8].
- **Interferon proteins.** Levels of the interferons themselves did not explain the IFN signature in 64% of patients, suggesting IFN-independent disease mechanisms [7].
- **Single cells.** Single-cell RNA sequencing of about 276,000 blood mononuclear cells from 33 children with SLE and 11 controls showed that the ISG signature comes from a small number of subpopulations within major cell types, especially plasma cells, and that these subpopulations expand with disease activity [9].

**Appraisal.** The evidence consistently shows that IFN-low patients form a distinct group with weaker, but not absent, molecular differences. The studies differ in tissue and design:
- Panwar et al. used purified cells, so the result says little about changes in blood cell composition, which whole-blood studies capture [4].
- The endotype studies are cross-sectional and use different clustering methods [6, 8]. The largest cross-disease study holds its data under controlled access, which limits re-analysis [8].
- The single-cell study is small and paediatric [9].

None of these studies examined relationships between genes within IFN-low patients.

### 3.3 Is IFN status stable over time?

Two longitudinal studies suggest that IFN status is mostly stable within patients:
- In 243 patients, the IFN signature was the most stable of the gene signatures studied, measured by intra-class correlation. Changes in the signature did not track changes in disease activity [10].
- In 142 patients with repeated samples, 87.3% kept the same IFN status over time, and most of those whose status changed were receiving high-dose glucocorticoids [11].

**Appraisal.** These cohorts were mostly of long-standing disease and used different thresholds [10, 11]. Status appears stable for most patients, but treatment can change it. A single measurement can therefore classify most patients correctly, but treatment must be considered when interpreting IFN-low status.

### 3.4 Why it matters for treatment

The type I IFN receptor antibody anifrolumab was tested in two phase III trials in moderate-to-severe SLE:
- TULIP-1 missed its primary endpoint (SRI-4 response 36% with anifrolumab versus 40% with placebo) [12].
- TULIP-2 met its primary endpoint (BICLA response 48% versus 32%) [13].

In pooled post hoc data, the benefit was clear in patients with a high IFN gene signature. In the IFN-low group (about 17% of patients), the difference in BICLA response was 9.3 percentage points, with a 95% confidence interval from −8.0 to 26.5 [14].

**Appraisal.** The IFN-low result is post hoc and based on small groups (62 and 64 patients), so it is inconclusive rather than evidence of no benefit. It nevertheless supports the view that IFN-low patients lack the main target of current IFN-directed therapy.

**What is unknown.** No study we found has examined whether IFN-low patients differ from healthy people in the *relationships* between genes rather than in gene levels, and no published classifier reports its performance separately for IFN-low SLE.

**Table 1. Key studies of interferon status in SLE**

| Study | Tissue | Design and size | Main finding relevant here |
|---|---|---|---|
| Chiche 2014 [1] | Whole blood | Cross-sectional, adults | IFN modules positive in 87% |
| Catalina 2019 [2] | Whole blood | Several cohorts, by activity | 66–73% IFN-positive; several IFN types involved |
| Banchereau 2016 [3] | Whole blood | Longitudinal, paediatric, 158 patients | 84.8% of samples IFN-positive |
| Panwar 2021 [4] | Sorted immune cells | IFN-negative vs IFN-positive vs controls | 5 DEGs (IFN-negative vs controls) in classical monocytes |
| IFNGS test-low vs high, 2019 [5] | Whole blood | Signature-low vs signature-high patients | Low-signature patients have eosinophil, IFN-γ and lymphocyte signatures |
| Hubbard 2023 [6] | Whole blood | Endotyping | A least-perturbed endotype resembling controls |
| Gómez-Bañuelos 2024 [7] | Blood and serum | IFN protein levels vs signature | Signature not explained by IFN levels in 64% |
| Barturen 2021 [8] | Whole blood | 955 patients, 7 diseases, 267 controls | Healthy-like cluster across diseases |
| Nehar-Belaid 2020 [9] | Single cells (PBMC) | 33 children with SLE, 11 controls | ISG signature from specific subpopulations, especially plasma cells |
| Petri 2019 [10] | Whole blood | Longitudinal, 243 patients | IFN signature the most stable signature over time |
| Northcott 2022 [11] | Whole blood | Longitudinal, 142 with repeat samples | 87.3% kept the same IFN status |
| Vital 2022 [14] | Trial data | Pooled post hoc, TULIP-1 and TULIP-2 | Anifrolumab benefit uncertain in IFN-low patients |

## 4. Transcriptomic classifiers in SLE and the problem of leakage

Many studies separate SLE from healthy controls using blood transcriptomes, and reported performance is often near perfect. One support-vector machine reached a cross-validated AUC of 0.998 [15], and a single ISG, MX2, was reported to reach AUCs of 0.958–0.976 [16].

**Appraisal.** These estimates should be read with caution, for two reasons:
1. ISGs dominate such models, so their success says little about patients without the signature.
2. Both studies show practices known to inflate accuracy, as documented in our companion leakage study (paper 1). The first merged datasets and selected genes on the full training set before cross-validation [15]. The second treated two GEO series that share patients and arrays as independent datasets [16].

Selecting genes before cross-validation can produce near-perfect apparent accuracy even when there is no real signal [17], and data leakage has been documented across many scientific fields [18].

**What is unknown.** How well any method separates IFN-low SLE from health, when evaluated without leakage, has not been reported.

## 5. Single-sample network methods

Most network methods estimate one network for a group of samples. Single-sample methods estimate one network per individual, so that networks can be compared between patients or used as features for prediction. Table 2 summarises the main methods:
- **LIONESS** (Linear Interpolation to Obtain Network Estimates for Single Samples) compares a network built from all samples with one built after removing the sample of interest, and scales the difference [19]. It works with any network estimator; Pearson correlation is the most common choice.
- **SSN** (sample-specific networks) measures how much the correlation between two genes changes when one sample is added to a reference group, and tests the change with a z-score [20].
- **P-SSN** applies the SSN idea to partial correlation, so that indirect associations are removed [21].
- **SWEET** weights an SSN-type network by how similar each sample is to the rest of the cohort, to correct for differences in subgroup size. In 16 cancers, its networks fitted known interactomes better than those of competing methods [22].
- **BONOBO** gives each sample a posterior co-expression matrix, combining a prior built from the other samples with that sample's data, and needs no external reference data [23].
- **CSN** (cell-specific networks) tests, for each cell, whether two genes are co-expressed in the cell's local neighbourhood more often than independence would predict. It was designed for single-cell data and can detect non-linear association [24].
- **iENA** (individual-specific edge-network analysis) builds single-sample edge features for detecting early disease states; in influenza cohorts it reported AUCs above 0.9 for early warning [25].

Two recent reviews describe the field and its open problems [26, 27].

**Table 2. Single-sample network methods**

| Method | Association measure | How a sample's network is formed | Known theory | Known issues |
|---|---|---|---|---|
| LIONESS [19] | Any (usually Pearson) | Scaled difference between all-sample and leave-one-out networks | Linear-interpolation assumption [19] | Encodes mean differences; favours under-represented groups [27, 28] |
| SSN [20] | Pearson | Change in correlation when the sample is added to a reference | First-order formula for Pearson [20] | Depends on the reference; near-identical to LIONESS [27, 28] |
| P-SSN [21] | Partial correlation | As SSN, with partial correlation | None found | Needs a reference set |
| SWEET [22] | Pearson | SSN-type network weighted by sample similarity | None found | Designed to correct subgroup-size bias |
| BONOBO [23] | Covariance (Bayesian) | Posterior from a prior of the other samples plus the sample | Closed-form posterior [23] | Prior strength must be chosen |
| CSN [24] | Local co-occurrence | Neighbourhood-based independence test per cell | Statistical test [24] | Built for single-cell data |
| iENA [25] | Edge features | Single-sample edge network against a reference | None found | Mainly used for early-warning signals |

## 6. What single-sample networks measure

### 6.1 Theory

Theory on what these networks contain is limited:
- For SSN with Pearson correlation, Liu et al. gave a first-order formula: the change in an edge depends approximately on the product of the sample's standardized expression values for the two genes [20].
- A benchmark in cancer data found an almost perfect linear relationship between LIONESS and SSN edges when the two methods share a reference network [28], and a 2026 review stated that they are always perfectly correlated, differing only in magnitude [27].
- LIONESS edges are known to encode differences in mean expression, and to give larger weights to samples from under-represented groups [27, 28].

**Appraisal.** These are mostly empirical observations, or results for Pearson correlation only. We found no first-order result for partial correlation or for shrinkage estimators, and no framework explaining what the different methods share.

### 6.2 Evidence for prediction

The evidence that single-sample networks improve prediction is limited:
- A scoping review of individual-specific networks in medicine (2000–2020) found that most studies were proofs of concept rather than validated models for predicting outcomes in new individuals. It called for more work on network sparsification, outcome-guided feature extraction and use of networks in prediction models [29].
- In one recent comparison, Pearson-based LIONESS edges reached a held-out AUC of 0.467, against 0.815 for expression modules [30].
- In renal cancer, adding SWEET edges to expression features gave only small gains in predicting immunotherapy response [31].
- Turning complete, weighted networks into features is itself a problem. Threshold-integrated graph features were proposed to avoid choosing a single sparsification threshold [32].

**Appraisal.** Few studies compare network features with baselines that capture the same information, such as expression residuals or distances from a reference group; where they do, networks rarely win clearly. We could not access the full text of [30], so its design could not be appraised in detail.

**What is unknown.** When, and why, single-sample network features should outperform simpler summaries of the same expression data has not been established.

## 7. Estimating and testing network structure

### 7.1 Partial correlation with few samples

Partial correlations come from the inverse of the covariance matrix. That inverse is unstable, or impossible to compute, when the number of genes approaches the number of samples.
- **Shrinkage estimation** blends the sample covariance with a simple target and gives stable estimates in this setting [33].
- **The nonparanormal transform** extends Gaussian network estimation to monotone non-linear relationships by working on rank-based normal scores [34].
- **Weighted gene co-expression network analysis (WGCNA)** remains the most widely used way to summarise co-expression into modules [35], although it was designed for description rather than prediction.

### 7.2 Testing for differences between groups

Several families of tests ask whether co-expression differs between two groups:
- **Pairwise tests.** DiffCorr compares the correlation of each gene pair between conditions using Fisher's z-transform [36]. DGCA extends this with permutation-based p-values and gene-to-gene-set comparisons [37].
- **Pathway-level tests.** Differential network analysis can be run within known pathways, with any association measure (including partial correlation) and significance assessed by permutation [38].
- **Whole-matrix tests from statistics.** Two-sample tests for high-dimensional covariance matrices compare entire matrices, using either a Frobenius-norm statistic [39] or a maximum-type statistic that is powerful against sparse differences [40].
- **Tests of spread.** Tests of homogeneity of multivariate dispersion compare how widely samples scatter around their group centres [41].

**Appraisal.** The number of gene pairs grows with the square of the number of genes, so pairwise tests carry a heavy multiple-testing burden. Pathway-level and whole-matrix tests reduce this burden but give less detail about which edges differ. More importantly, a difference in network structure can arise from genuine changes in co-regulation, from differences in spread, or from hidden subgroups shifted in different directions, and none of these tests distinguishes between these explanations on its own. We found no study that addresses this problem in blood transcriptomic data.

## 8. Confounding in whole-blood studies of SLE

Three confounders are especially important when comparing SLE patients with healthy controls.

**Treatment.** Most patients take glucocorticoids, which change blood gene expression. Hu et al. derived a prednisolone-response signature (64 up-regulated and 18 down-regulated genes) that tracks glucocorticoid exposure. It also correlates positively with neutrophil counts and negatively with lymphocyte percentages [42], so it partly reflects blood cell composition. Glucocorticoids can also change IFN status itself [11].

**Cell composition.** Variation in the proportions of blood cell types drives much of the expression variation seen in whole blood.
- Deconvolution of SLE blood microarrays showed that expansion and activation of monocytes, NK cells and T helper cells partly underlie the IFN signature [43].
- In whole-blood RNA-seq from 109 patients with active SLE, mycophenolate mofetil had a significant and persisting effect on the transcriptomic signature and on predicted cell composition [44].

Apparent network differences can therefore simply reflect different cell mixtures or treatments.

**Sex.** About 90% of SLE patients are female. In a whole-blood cohort of 720 patients, 54% of the 41 male patients showed abnormal XIST expression and silencing of X-linked genes [45]. XIST therefore cannot be used to infer sex in SLE.

**Appraisal.** Each confounder is well documented. In the single-sample network studies reviewed here [28, 30, 31], however, we found no adjustment for treatment or cell composition, and no SLE network study has handled all three confounders together.

## 9. Synthesis: gaps and the contribution of the planned study

The literature leaves five gaps:
1. **Biology.** IFN-low SLE is a distinct, clinically important and mostly stable group, but no study has examined gene–gene relationships in these patients or reported classifier performance for them specifically (Section 3).
2. **Leakage.** Published SLE classifiers report near-perfect accuracy that is partly inflated by leakage, and none addresses IFN-low patients (Section 4).
3. **Theory.** Single-sample networks are widely used, but there is no theory for partial-correlation or shrinkage-based networks, and the known links between methods are empirical (Sections 5–6).
4. **Fair comparison.** Network features are rarely compared with baselines that capture the same information, and the evidence that they improve prediction is weak (Section 6).
5. **Mechanism and confounding.** Existing tests cannot separate changes in co-regulation from differences in mean or spread, or from hidden subgroups, and treatment and cell composition are rarely accounted for (Sections 7–8).

The planned study addresses these gaps, but not every part of it is new.

**Already known, to be cited rather than claimed:**
- Single-sample networks based on partial correlation exist as P-SSN [21].
- The first-order formula for SSN with Pearson correlation was given by Liu et al. [20].
- The near-perfect linear relationship between LIONESS and SSN edges has been observed empirically [27, 28].
- Tests for differences in co-expression and covariance between groups exist [36–41].

**A modest extension:**
- SSN is an *exact* rescaling of LIONESS for any association measure. This explains the observed relationship, but it is not a major result on its own.
- An exact shrinkage implementation with a symmetric, class-balanced reference is a design contribution.

**Probably new** (not found in our searches; a full PubMed and arXiv search is still required):
- A first-order formula for LIONESS with partial correlation, and its extension to shrinkage estimators.
- The predictions that follow from it: a linear model on edges is equivalent to a quadratic classifier, and unusual samples strengthen partial-correlation edges but weaken Pearson edges.
- A framework of mechanism-matched baselines and layered tests that separates differences in mean, spread and structure, with a check for hidden subgroups and adjustment for treatment and cell composition.
- The first application of single-sample networks to SLE, and the first leakage-free classifier results reported specifically for IFN-low SLE.

In short, the main contribution is not a new network method but an explanation of what existing methods measure, tested rigorously in a demanding clinical setting.

---

## References

**Status key.** *Verified*: PMID checked against NCBI on 2026-10-01 (listed as verified in the study plan or the paper 1 plan). *Confirmed online*: identifier or journal details confirmed by web search; recheck on PubMed. *To verify*: details not yet confirmed.

| # | Reference | Status |
|---|---|---|
| 1 | Chiche L, et al. Modular transcriptional repertoire analyses of adults with systemic lupus erythematosus reveal distinct type I and type II interferon signatures. *Arthritis Rheumatol* 2014. PMID 24644022. | Verified |
| 2 | Catalina MD, et al. Gene expression analysis delineates the potential roles of multiple interferons in systemic lupus erythematosus. *Commun Biol* 2019. PMID 31044165. | Verified |
| 3 | Banchereau R, et al. Personalized immunomonitoring uncovers molecular networks that stratify lupus patients. *Cell* 2016. PMID 27040498. | Verified |
| 4 | Panwar B, et al. Multi-cell type gene coexpression network analysis reveals coordinated interferon response and cross-cell type correlations in systemic lupus erythematosus. *Genome Res* 2021. PMID 33674349. | Verified |
| 5 | [Authors to confirm]. Type I interferon gene signature test-low and -high patients with systemic lupus erythematosus have distinct gene expression signatures. *Lupus* 2019. PMID 31660791. | Confirmed online (authors to confirm) |
| 6 | Hubbard EL, et al. Analysis of transcriptomic features reveals molecular endotypes of SLE with clinical implications. *Genome Med* 2023. PMID 37845772. | Verified |
| 7 | Gómez-Bañuelos E, Goldman DW, Andrade V, Darrah E, Petri M, Andrade F. Uncoupling interferons and the interferon signature explains clinical and transcriptional subsets in SLE. *Cell Rep Med* 2024;5(5):101569. PMID 38744279. | Confirmed online |
| 8 | Barturen G, et al. Integrative analysis reveals a molecular stratification of systemic autoimmune diseases. *Arthritis Rheumatol* 2021. | To verify |
| 9 | Nehar-Belaid D, et al. Mapping systemic lupus erythematosus heterogeneity at the single-cell level. *Nat Immunol* 2020;21(9):1094–1106. PMID 32747814. | Confirmed online |
| 10 | Petri M, et al. Association between changes in gene signatures expression and disease activity among patients with systemic lupus erythematosus. *BMC Med Genomics* 2019. PMC6327466. | Confirmed online |
| 11 | Northcott M, et al. Type 1 interferon status in systemic lupus erythematosus: a longitudinal analysis. *Lupus Sci Med* 2022. PMC8867321. | To verify (authors and title) |
| 12 | Furie RA, et al. Type I interferon inhibitor anifrolumab in active systemic lupus erythematosus (TULIP-1): a randomised, controlled, phase 3 trial. *Lancet Rheumatol* 2019;1:e208–e219. doi:10.1016/S2665-9913(19)30076-1. | Confirmed online |
| 13 | Morand EF, et al. Trial of anifrolumab in active systemic lupus erythematosus. *N Engl J Med* 2020;382:211–221. doi:10.1056/NEJMoa1912196. | Confirmed online |
| 14 | Vital EM, et al. Anifrolumab efficacy and safety by type I interferon gene signature and clinical subgroups in patients with SLE: post hoc analysis of pooled data from two phase III trials. *Ann Rheum Dis* 2022;81(7):951–961. PMID 35338035. | Confirmed online |
| 15 | Li W, et al. Cuproptosis-related gene identification and immune infiltration analysis in systemic lupus erythematosus. *Front Immunol* 2023. PMID 37313407. | Verified |
| 16 | Meng XW, et al. MX2: identification and systematic mechanistic analysis of a novel immune-related biomarker for systemic lupus erythematosus. *Front Immunol* 2022. PMID 36059547. | Verified |
| 17 | Ambroise C, McLachlan GJ. Selection bias in gene extraction on the basis of microarray gene-expression data. *PNAS* 2002. PMID 11983868. | Verified |
| 18 | Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. *Patterns* 2023. PMID 37720327. | Verified |
| 19 | Kuijjer ML, et al. Estimating sample-specific regulatory networks. *iScience* 2019. PMID 30981959. | Verified |
| 20 | Liu X, et al. Personalized characterization of diseases using sample-specific networks. *Nucleic Acids Res* 2016. PMID 27596597. | Verified |
| 21 | Huang Y, et al. Disease characterization using a partial correlation-based sample-specific network. *Brief Bioinform* 2021;22(3):bbaa062. PMID 32422654. | Verified |
| 22 | Chen HH, et al. SWEET: a single-sample network inference method for deciphering individual features in disease. *Brief Bioinform* 2023;24(2):bbad032. | Confirmed online |
| 23 | Saha E, et al. Bayesian inference of sample-specific coexpression networks. *Genome Res* 2024;34(9):1397. | Confirmed online |
| 24 | Dai H, Li L, Zeng T, Chen L. Cell-specific network constructed by single-cell RNA sequencing data. *Nucleic Acids Res* 2019;47(11):e62. | Confirmed online |
| 25 | Yu X, Zhang J, Sun S, Zhou X, Zeng T, Chen L. Individual-specific edge-network analysis for disease prediction. *Nucleic Acids Res* 2017. | Confirmed online |
| 26 | De Marzio M, Glass K, Kuijjer ML. Single-sample network modeling on omics data. *BMC Biol* 2023. PMC10755944. | Confirmed online |
| 27 | Kuijjer ML, De Marzio M, Glass K. Challenges and opportunities in single-sample network modeling. *bioRxiv* 2026 (preprint). PMID 41867852. | Verified |
| 28 | Deschildre J, et al. Evaluation of single-sample network inference methods for precision oncology. *NPJ Syst Biol Appl* 2024. PMID 38360881. | Verified |
| 29 | Gregorich M, et al. Individual-specific networks for prediction modelling – a scoping review of methods. *BMC Med Res Methodol* 2022. PMC8898441. | Confirmed online |
| 30 | Leyva A, Niazi MKK. [Title to confirm]. *PLoS One* 2026. PMID 42743314. | Verified (title to confirm) |
| 31 | Yin L, et al. Sample-specific network analysis identifies gene co-expression patterns of immunotherapy response. *iScience* 2025. PMID 40740488. | Verified |
| 32 | Gregorich M, et al. Flexible parametrization of graph-theoretical features from individual-specific networks for prediction. *Stat Med* 2024. PMID 38664934. | Verified |
| 33 | Schäfer J, Strimmer K. A shrinkage approach to large-scale covariance matrix estimation and implications for functional genomics. *Stat Appl Genet Mol Biol* 2005. PMID 16646851. | Verified |
| 34 | Liu H, Lafferty J, Wasserman L. The nonparanormal: semiparametric estimation of high dimensional undirected graphs. *J Mach Learn Res* 2009;10:2295–2328. | To verify |
| 35 | Zhang B, Horvath S. A general framework for weighted gene co-expression network analysis. *Stat Appl Genet Mol Biol* 2005. PMID 16646834. | Verified |
| 36 | Fukushima A. DiffCorr: an R package to analyze and visualize differential correlations in biological networks. *Gene* 2013. | To verify |
| 37 | McKenzie AT, et al. DGCA: a comprehensive R package for Differential Gene Correlation Analysis. *BMC Syst Biol* 2016. doi:10.1186/s12918-016-0349-1. | Confirmed online |
| 38 | Grimes T, Potter SS, Datta S. Integrating gene regulatory pathways into differential network analysis of gene expression data. *Sci Rep* 2019;9(1):1–12. | Confirmed online |
| 39 | Li J, Chen SX. Two sample tests for high-dimensional covariance matrices. *Ann Stat* 2012;40(2):908–940. | Confirmed online |
| 40 | Cai T, Liu W, Xia Y. Two-sample covariance matrix testing and support recovery in high-dimensional and sparse settings. *J Am Stat Assoc* 2013;108:265–277. doi:10.1080/01621459.2012.758041. | Confirmed online |
| 41 | Anderson MJ. Distance-based tests for homogeneity of multivariate dispersions. *Biometrics* 2006;62(1):245–253. | To verify |
| 42 | Hu Y, et al. Development of a molecular signature to monitor pharmacodynamic responses mediated by in vivo administration of glucocorticoids. *Arthritis Rheumatol* 2018. PMID 29534336. | Verified |
| 43 | Abbas AR, et al. Deconvolution of blood microarray data identifies cellular activation patterns in systemic lupus erythematosus. *PLoS One* 2009. PMC2699551. | To verify (authors) |
| 44 | Akthar M, et al. Deconvolution of whole blood transcriptomics identifies changes in immune cell composition in patients with systemic lupus erythematosus (SLE) treated with mycophenolate mofetil. *Arthritis Res Ther* 2023;25:111. PMID 37391799. | Confirmed online |
| 45 | Masson HO, et al. XIST expression and hypermethylation of the X chromosome in males with systemic lupus erythematosus. *Front Immunol* 2026. PMID 42039161. | Verified |
