# Manuscript draft v3: Introduction to Methods

**Status:** working draft, 2026-10-13. No analysis has been run; results are placeholders ([RESULT: …]).
**Authors:** Pascal Antwi, Tyler Grimes [author list and affiliations to confirm].
**Target journal:** *Briefings in Bioinformatics* (author guidelines to be checked: article type, word limits, Key Points, reference style).

**How to read the markers:**
- **†** a proposed default setting, to be confirmed with Tyler before the stage 1 registration (rationale in Supplementary Table S3).
- **[TBD: …]** a decision or source still needed. **[RESULT: …]** filled in after the analysis.
- *(unverified)* a reference not yet checked against NCBI or the publisher (NCBI was unreachable when this draft was written). See `references.md`.

Main-text word count: about 5,360 (Key Points 149, Abstract 242, Introduction 989, Methods 3,979).

---

## Title options

1. **What do single-sample co-expression networks measure? A quadratic theory and a leakage-free benchmark, with interferon-low lupus as a stress test**
2. **Partial-correlation LIONESS: first-order theory, mechanism-matched baselines and a graded benchmark across autoimmune contrasts**
3. **When do patient-specific networks add information beyond expression? Theory and evidence from interferon-low systemic lupus erythematosus**

**Running title:** Single-sample networks in interferon-low lupus

## Key Points

- Single-sample co-expression networks are widely used as patient-level features, but it is unclear what information they contain beyond the patient's own gene expression.
- We show that sample-specific network (SSN) edges are an exact rescaling of LIONESS edges, and that LIONESS edges built on shrinkage partial correlation are, to first order, fixed quadratic functions of a patient's conditional expression residuals.
- This theory predicts which group differences the networks detect (shifts in mean, in spread or in co-regulation) and which simple baselines they must beat; we test these predictions in simulation and real data.
- In a leakage-free, graded benchmark of autoimmune contrasts, from interferon-high lupus to the near-null interferon-low lupus versus healthy contrast, [RESULT: whether and when network features added information beyond expression and residual interferon signal].
- We release an R implementation of exact LIONESS with shrinkage partial correlation and all analysis code.

## Abstract

Single-sample network methods, such as LIONESS, estimate a separate gene co-expression network for each patient, and these networks are increasingly used as features for prediction. It is not known, however, what information they contain beyond the patient's own expression profile, and evidence that they improve prediction is limited. We address both gaps. First, we show that sample-specific networks (SSN) are an exact rescaling of LIONESS, and we derive a first-order representation of LIONESS applied to shrinkage partial correlation: each edge is approximately a fixed quadratic function of the patient's standardized conditional residuals. This result predicts which group differences the networks respond to (differences in mean, in spread and in co-regulation) and defines mechanism-matched baseline models. Second, we test these predictions in simulation (Gaussian, network-based and plasmode designs) and in a leakage-free benchmark of whole-blood transcriptomic contrasts of decreasing signal strength: interferon (IFN)-high systemic lupus erythematosus (SLE) versus healthy controls, IFN-low SLE versus controls, IFN-low SLE versus rheumatoid arthritis, and disease activity and nephritis within IFN-low SLE. Every model is compared against pathway expression and the residual IFN score, with explicit controls for sex, treatment, cell composition, age and ancestry. Third, we use layered permutation tests to ask whether IFN-low SLE differs from health in pathway means, spread or partial-correlation structure. [RESULT: main finding on added value of network features across contrasts]. [RESULT: main finding on IFN-low SLE biology]. [RESULT: one-sentence take-home message]. Code and an R implementation are freely available.

## 1. Introduction

### 1.1 Interferon-low lupus: a disease without its main molecular signal

Systemic lupus erythematosus (SLE) is a chronic autoimmune disease that can affect almost any organ. In most patients, blood cells show a strong type I interferon (IFN) signature: the coordinated up-regulation of IFN-stimulated genes (ISGs) such as IFI27, IFI44L and RSAD2 [1–3]. The signature is so dominant that published classifiers separating SLE from healthy controls report AUCs (areas under the receiver operating characteristic curve) close to 1, and single ISGs such as MX2 have been reported to reach AUCs above 0.95 [4, 5], although such estimates can be inflated by data leakage [6, 7].

A substantial minority of patients, roughly 13–35% depending on the cohort and on disease activity, do not show this signature [1–3]. We call these patients *IFN-low*. Their blood expression levels differ much less from those of healthy people. In sorted classical monocytes, Panwar et al. found only 5 differentially expressed genes between IFN-negative SLE and controls, against 1,288 for IFN-positive SLE [8]. Whole-blood studies have reported other signatures in IFN-low patients, involving eosinophil, IFN-γ and lymphocyte genes [9], and endotype analyses have described a "least-perturbed" group that resembles controls [10–12]. What drives disease in these patients therefore remains unclear. The question matters clinically: IFN-low patients lack the main target of IFN-directed therapies, and in pooled phase III data the benefit of the type I IFN receptor antibody anifrolumab was smaller and statistically uncertain in patients with a low IFN gene signature [13]. To our knowledge, no published classifier reports its performance separately for IFN-low SLE.

### 1.2 Single-sample networks

When average expression differs little between groups, a natural idea is to ask whether the *relationships* between genes differ. Most network methods estimate one network for a whole group; single-sample methods estimate one network per individual. LIONESS (Linear Interpolation to Obtain Network Estimates for Single Samples) does this by comparing a network estimated from all samples with one estimated after removing the sample of interest [14]. Related methods include sample-specific networks (SSN) [15], their partial-correlation version P-SSN [16], SWEET [17] and the Bayesian method BONOBO [18]; reviews are given in [19, 20].

Two problems limit the use of these networks for prediction. First, the evidence that they improve prediction is thin. A scoping review found that most studies were proofs of concept rather than validated prediction models [21]; in one recent comparison, Pearson-based LIONESS edges reached a held-out AUC of 0.467, against 0.815 for expression modules [22]; and adding SWEET edges to expression gave only small gains [23]. Second, it is not well understood what the networks measure. LIONESS edges are known to encode differential expression and to give higher weights to under-represented groups [20, 24]. For Pearson correlation, a first-order formula links an edge to products of a sample's standardized expression values [15], and SSN and LIONESS edges have been observed to be almost perfectly linearly related [24], but the reason has not been made explicit. No first-order result exists for partial correlation or for shrinkage estimators, and no common framework explains what the different methods share.

### 1.3 What is missing

These gaps lead to three needs.

**(i) Theory.** Without knowing what a single-sample network contains, one cannot tell whether a successful network classifier detected changed gene–gene relationships or something simpler, such as a mean shift or a wider spread of expression values.

**(ii) Mechanism-matched baselines.** Network features are usually compared with no baseline, or with weighted gene co-expression network analysis (WGCNA) module summaries [25], which were designed for description rather than prediction. A fair test compares network features with the simplest models that capture the same information.

**(iii) Separating mechanism from prediction.** Whether two groups differ in gene–gene structure is a population-level question, best answered by direct two-sample tests [26] rather than by comparing classifier accuracies. Prediction accuracy answers a different question: which representation of the data a classifier can exploit at a given sample size.

All of this must be done without data leakage, that is, without information from test samples reaching model fitting. Leakage inflates reported accuracy in transcriptomic prediction [6, 7] and can enter single-sample network pipelines in subtle ways, for example when the outcome is used to define subgroups or when training and test networks are computed differently.

### 1.4 IFN-low lupus as a stress test

IFN-low SLE is a demanding test case. The linear signal is weak, so any separation is likely to come from second-order structure, and the setting contains the main confounders of blood transcriptomics: treatment, especially glucocorticoids [27]; shifts in blood cell composition; sex, since about 90% of patients are female [28]; and differences in processing batch, age and ancestry between patients and healthy donors. A design that gives interpretable answers here should transfer to easier settings.

### 1.5 Contributions

1. **An exact link between methods, and LIONESS with shrinkage partial correlation.** We show that SSN edges are an exact, sample-independent rescaling of LIONESS edges for any association measure, and we provide an exact implementation of LIONESS for shrinkage partial correlation [TBD: confirm novelty after a full reading of P-SSN [16]].
2. **A first-order theory.** Each LIONESS partial-correlation edge is approximately a fixed quadratic function of the patient's conditional residuals, including under shrinkage. The theory yields six testable predictions about what single-sample networks can detect.
3. **Mechanism-matched baselines and a leakage-free framework,** including a symmetric, class-balanced reference design, a regularized quadratic discriminant baseline and inference that accounts for cross-validation.
4. **A graded benchmark** of whole-blood contrasts, from IFN-high SLE versus controls to activity and nephritis within IFN-low SLE, interpreted with a pre-registered simulation-based reading guide.
5. **Layered population-level tests** of mean, spread and partial-correlation structure, applied to characterize how IFN-low SLE differs from health after adjustment for treatment, cell composition, age and ancestry.

Section 2 describes the data and design (2.1–2.5), the theory (2.6), network estimation and features (2.7–2.8), models and validation (2.9–2.11), population-level tests (2.12) and the simulation study (2.13).

## 2. Methods

Settings marked † are pre-specified defaults that were fixed in the stage 1 registration (Section 2.14); the rationale for each is given in the text or in Supplementary Table S3.

### 2.1 Data sources and cohort eligibility

**Cohorts.** We used public whole-blood transcriptomic cohorts of SLE with healthy controls (HC) or a comparator disease (Table 1). The candidate primary cohorts were GSE319130 (RNA sequencing; 720 SLE patients and 84 HC, of whom 679 and 77 were female) [28] and GSE88884 (Affymetrix Human Transcriptome Array 2.0; baseline samples of 1,760 SLE patients from the ILLUMINATE trials and 60 HC) [29]. Contrast-specific cohorts were GSE110169 (82 SLE, 84 rheumatoid arthritis (RA) and 77 HC processed together, with recorded glucocorticoid use) [27], GSE65391 (158 paediatric SLE patients with repeated visits and disease-activity scores; 46 HC) [3], GSE99967 (lupus nephritis (LN), non-LN SLE and HC) *(unverified)* and GSE224705 (SLE with recorded prednisone dose) [30]. PRECISESADS (seven systemic autoimmune diseases and controls; controlled access) [12] was to be added if access was granted.

Series that duplicate others were excluded (GSE72326 duplicates GSE49454; GSE45291, GSE121239 and GSE224705 share patients and controls, so at most one was used per analysis), using the overlap catalogue of our companion study [REF: paper 1, in preparation]. One sample was used per patient (the first visit in longitudinal cohorts), and technical replicates were averaged.

**Feasibility (go/no-go) check.** Before registration, and without fitting any outcome model, we counted IFN-low patients and controls by inferred sex (Section 2.4) and tabulated batch, age, ancestry and medication by group. A cohort qualified as a **primary cohort** for contrasts with controls if it had at least 80 female IFN-low patients and 60 female controls and if batch was not confounded with group (patients and controls not processed in disjoint batches). These counts give a 95% confidence interval half-width of about ±0.085 for an AUC of 0.70 (Hanley–McNeil). Cohorts with at least 25 patients per group (half-width about ±0.15) qualified as **replication cohorts** and were reported descriptively. [RESULT: cohorts passing the check; N_IFNlow_female and N_HC_female per cohort.]

### 2.2 Pre-processing and harmonization

Each cohort was processed separately, without cross-cohort batch correction. Affymetrix arrays were re-processed from raw files with robust multi-array averaging where raw files were available†, and otherwise the submitters' normalized data were used. RNA-seq counts were filtered with edgeR's `filterByExpr`† and converted to log counts per million (log-CPM) after trimmed mean of M-values (TMM) normalization. Probes were mapped to gene symbols within each platform, keeping the probe with the highest training-fold variance for genes with several probes. For analyses that compared cohorts, pathways were restricted to genes measured in all cohorts involved, and per-pathway gene coverage is reported. Before network estimation, each gene was winsorized at ±4 standard deviations (SD) using training-fold means and SDs, to limit the influence of outliers on second-order statistics.

### 2.3 IFN score and IFN-low definition

**IFN score.** The IFN score was the mean of standardized expression values of four ISGs, IFI27, IFI44, IFI44L and RSAD2†, a panel used to stratify patients in clinical trials [TBD: confirm panel and source]. Each gene was standardized with the mean and SD of the **controls in the training fold**.

**IFN-low definition.** A sample was IFN-low if its score was at most the training-fold control mean plus 2 SD. The cutoff was computed inside each training fold and applied unchanged to that fold's test samples, and the same filter was applied to controls (removing about 2.5% of them), so both groups met the same criterion. A stricter cutoff (mean plus 1 SD) was a sensitivity analysis.

**Residual IFN signal.** A cutoff cannot make the groups identical in IFN activity: patients just below it may still have mildly raised IFN activity. The residual IFN score was therefore treated as a **baseline that every model had to beat** (Section 2.9). In addition, the IFN-score genes and all genes in the Reactome *Interferon Signaling* subtree (R-HSA-913531) were excluded from network features; a sensitivity analysis included the subtree.

**Treatment and IFN status.** Hydroxychloroquine and immunosuppressants may lower the IFN signature, so some IFN-low patients could be treated IFN-high patients. In cohorts with medication data (GSE224705, GSE65391, GSE110169) we compared the proportion of IFN-low patients by treatment, and in GSE65391 we described within-patient transitions between IFN states across visits.

### 2.4 Confounding control

We combined design-based controls with explicit confounder baselines.

**Sex.** Sex was inferred from Y-chromosome genes (RPS4Y1, DDX3Y, KDM5D, UTY, EIF1AY), not from XIST, because 54% of male SLE patients in GSE319130 express XIST abnormally [28]; inferred sex was checked against reported sex where available. The primary analysis was restricted to females. X-chromosome genes were retained, because removing them would delete immune genes such as TLR7, CXCR3, CD40LG and FOXP3. A sensitivity analysis included all sexes after removing Y-chromosome genes and XIST/TSIX.

**Batch.** Cohorts with patients and controls in disjoint batches were ineligible (Section 2.1); batch-by-group tables are reported.

**Treatment.** A glucocorticoid-response score was computed from the prednisolone-responsive genes of Hu et al. [27] (up-regulated genes†). It served (a) as a baseline model, (b) to define a sensitivity analysis excluding its genes and (c) as an adjustment covariate in the population-level tests. In cohorts that recorded steroid use, we checked that the score tracked recorded use and dose. Medication was not recorded per patient in GSE88884 or GSE319130, so treatment exposure in these cohorts could only be estimated through this score.

**Cell composition.** Whole-blood co-expression is strongly affected by variation in cell-type proportions. For each sample, we computed single-sample scores (singscore) for marker gene sets of neutrophils, monocytes, B cells, plasmablasts, T cells, natural killer cells and eosinophils† [TBD: marker-set source]; because each score uses only that sample, it introduces no leakage. The scores served (a) as a baseline model, (b) as additional conditioning variables in the partial correlations (Section 2.7) and (c) as adjustment covariates in the population-level tests.

**Age and ancestry.** Age and recorded race or ancestry were tabulated by group and used as a baseline model and as adjustment covariates; a sensitivity analysis restricted the data to the age range shared by patients and controls. The paediatric cohort (GSE65391) was analysed separately.

### 2.5 Pathways

Gene sets came from Reactome (release current at registration, accessed through `msigdbr`; version recorded). The primary set comprised the *Immune System* subtree (R-HSA-168256) without the Interferon Signaling subtree. Pathways with more than 50 genes were replaced by their Reactome sub-pathways, so that every network had **15–50 genes** after filtering; this keeps the number of genes well below the roughly 100–150 training samples per fold, which stable partial-correlation estimation requires. Near-duplicate pathways (Jaccard index > 0.8) were reduced to one representative. A secondary analysis used all Reactome pathways meeting the same size criteria. Gene lists were archived with the code. [RESULT: number of pathways after filtering.]

### 2.6 Theory: what single-sample networks contain

**Set-up.** Consider a pathway with G genes and a reference set of N samples. Let x_q be the expression vector of sample q, μ the reference mean, d = x_q − μ the deviation of sample q, S the reference covariance (divisor N), Σ_λ = (1 − λ)S + λ·diag(S) the shrinkage covariance with fixed intensity λ ∈ [0, 1] [31], Ω = Σ_λ⁻¹ the precision matrix, and ρ_ij = −Ω_ij / √(Ω_ii Ω_jj) the partial correlation between genes i and j given the other pathway genes. The LIONESS edge for sample q is e_ij^(q) = N·ρ_ij − (N − 1)·ρ_ij^(−q), where ρ^(−q) is computed without sample q [14].

**Conditional residuals.** Let u = Ωd and ũ_i = u_i / √Ω_ii. Up to scaling, ũ_i is the residual of gene i for sample q after regression on the other pathway genes, divided by its SD; across the reference population, Var(ũ_i) = 1 and Cov(ũ_i, ũ_j) = −ρ_ij (residuals of two genes are negatively correlated when their partial correlation is positive).

**Result 1 (no shrinkage, λ = 0).** To first order in 1/(N − 1),

  e_ij^(q) ≈ ũ_i ũ_j + ρ_ij (1 + (ũ_i² + ũ_j²)/2).   (1)

**Result 2 (shrinkage).** With λ fixed, Σ_λ is linear in S, and

  e_ij^(q) ≈ ρ_ij + M̃_ij + ρ_ij (M̃_ii + M̃_jj)/2,   (2)

where M = (1 − λ)uuᵀ + λ Ω D_d Ω, D_d = diag(d_1², …, d_G²) and M̃_ij = M_ij / √(Ω_ii Ω_jj). Equation (2) reduces to (1) when λ = 0, and in both cases E[e_ij^(q)] = ρ_ij over the reference population, as LIONESS requires.

**Pearson analogue.** For Pearson correlation r_ij and standardized expression z_i,

  e_ij^(q) ≈ z_i z_j + r_ij (1 − (z_i² + z_j²)/2),   (3)

consistent with [15].

**Result 3 (SSN is an exact rescaling of LIONESS).** SSN defines the edge as the change in an association measure c when sample q is added to a reference R of n samples, Δ_ij^(q) = c_ij(R ∪ {q}) − c_ij(R) [15]. LIONESS with the same reference gives e_ij^(q) = (n + 1)c_ij(R ∪ {q}) − n·c_ij(R), so

  Δ_ij^(q) = (e_ij^(q) − c_ij(R)) / (n + 1)   (4)

exactly, for any association measure. Hence equations (1)–(3) also describe SSN and, if defined analogously, P-SSN [16] [TBD: confirm definition]. SWEET weights an SSN-type network by a sample-specific factor [17], so its edges are a sample-specific multiple of the same quadratic form [TBD: confirm formula]. Derivations, numerical checks and the status of BONOBO [18] are given in Supplementary Appendix A.

**Predictions.** Equations (1)–(4) give six predictions, which we tested:
- **P1 (no new information).** Each edge is a fixed quadratic function of d, so a network contains no information beyond the sample's expression within the pathway; it can only represent that information differently.
- **P2 (quadratic classifier).** A linear model on a pathway's edges is a quadratic discriminant in d; its natural competitor is regularized quadratic discriminant analysis (QDA).
- **P3 (means and spread).** Group differences in mean shift ũ and differences in spread scale it; both change the product and squared terms, so edges respond to differential expression and dispersion, not only to co-regulation.
- **P4 (opposite signs).** The squared terms have a positive sign for partial correlation (1) and a negative sign for Pearson correlation (3), so unusual samples strengthen partial-correlation edges but weaken Pearson edges.
- **P5 (node strength).** Node strength s_i = Σ_j e_ij ≈ ũ_i·Σ_{j≠i} ũ_j plus squared terms, closely related to the residual (M4) and distance-from-health (M7) baselines.
- **P6 (equivalence).** For per-edge features, SSN, P-SSN and LIONESS differ only by a fixed per-edge rescaling, so any performance difference between them must come from topology summaries or the reference design.

The approximations were used only for interpretation and baseline design; all features were computed with exact LIONESS, and agreement between exact and first-order edges on real data, including in the tails, is reported.

### 2.7 LIONESS partial-correlation estimation

**Reference design.** All samples were treated identically, because computing control and patient networks differently can create spurious separation. Within each training fold, B = 20† class-balanced reference subsets were formed, each containing all samples of the smaller class and an equal-sized random sample of the larger class. For any sample q (training or test) and subset R_b, with R = R_b \ {q}, the edge was

  e^(q,b) = (|R| + 1)·ρ(R ∪ {q}) − |R|·ρ(R),

which equals leave-one-out LIONESS when q ∈ R_b and add-one-in LIONESS otherwise; edges were averaged over the 20 subsets. Balancing removes the dependence of edge weights on class proportions [24], and averaging reduces variance from the choice of reference.

**Shrinkage and conditioning.** Partial correlations used the shrinkage covariance of Section 2.6 (variances not shrunk). λ was chosen in the inner cross-validation from {0.5, 1, 2} times the Schäfer–Strimmer analytic estimate† [31] and then held fixed within the fold. Matrices were inverted directly, which is fast for G ≤ 50. In the primary analysis, the conditioning set of each partial correlation included the cell-composition scores (Section 2.4), so edges represent co-expression beyond composition; a sensitivity analysis conditioned on pathway genes only.

**Comparator arms and testing.** Pearson LIONESS (L-P) used the same reference design. A rank-based arm, other single-sample methods and their implementations are described in Supplementary Section S4. Our R implementation was unit-tested against naive recomputation, `corpcor::pcor.shrink` at fixed λ [31] and `lionessR` for the Pearson arm.

### 2.8 Topology features

LIONESS weights are signed and unbounded, and the networks are complete. Weights were rescaled by one global factor, the training-fold 99th percentile of |e|†, which preserves between-sample differences in scale. The pre-specified features per sample and pathway were positive and negative node strength (s_i⁺, s_i⁻), mean absolute edge weight, the leading eigenvalue of the weight matrix, and the Frobenius distance ‖W − P‖_F between the sample's network W and the reference partial-correlation matrix P. By P3, ‖W − P‖_F behaves mainly as a dispersion measure and was interpreted as such. Exploratory metrics designed for sparse graphs (signed clustering [32] and threshold-integrated betweenness [33]) are reported in the supplement.

### 2.9 Baseline and comparator models

All models used the same pathways, folds and aggregation (Section 2.10). Every feature type was fitted with two learners, elastic-net logistic regression and gradient-boosted trees (`xgboost`†), each with an equal, pre-specified budget of 20 tuning evaluations† (Supplementary Table S3), so that no model gained from extra tuning. Residual-based features (M4, M7) were computed for each training sample from a leave-one-out mean and precision matrix, matching the LIONESS reference design; otherwise training residuals would be systematically smaller than test residuals.

**Table 2. Models compared in the main text.**

| ID | Features | Question addressed |
|---|---|---|
| M0a–d | Residual IFN score; glucocorticoid score; cell-type scores; age and ancestry | Do leftover IFN, treatment, composition or demographics explain the separation? |
| M2 | Pathway expression | Linear baseline with the same aggregation |
| M4 | Conditional residuals ũ | Linear building block of LIONESS partial correlation |
| M7 | Distance from health: Σũ², and Mahalanobis distance from training-fold controls | Dispersion baseline |
| Q | Regularized QDA per pathway [34]; ridge logistic regression on ũ and ũ_iũ_j | Quadratic baseline implied by P2 |
| W2 | WGCNA module eigengenes fitted within folds and projected onto test samples [25] | Established network comparator |
| L2 | LIONESS partial-correlation topology | Main network model |
| L-P | Pearson LIONESS topology | Effect of correlation type |
| L3 | L2 + M2 | Added value over expression |

A superscript "+" denotes a model that also includes M0a; for example, L3⁺ = L2 + M2 + M0a. Further comparators (pathway scores, residual-product networks, boosting on expression, edge-level LIONESS, rank-based LIONESS, SSN, SWEET and BONOBO) were analysed identically and are listed in Supplementary Table S2.

### 2.10 Aggregation across pathways and contrasts

**Aggregation.** The primary aggregation was a **group lasso** logistic regression [35], which selects or drops each pathway's features together. Pathway attribution used **stability selection** [36]: the model was refitted on 100† random half-samples of the training data, and the proportion of fits selecting each pathway was recorded. A pathway was described as implicated only if (i) its selection proportion exceeded 0.6† (the value recommended in [36]), (ii) it was significant in the population-level tests (Section 2.12) and (iii) both held after adjustment for composition and treatment. Two-level stacking (per-pathway elastic net combined by a non-negative elastic net) was a sensitivity analysis.

**Contrasts.** The pipeline was applied to five contrasts: (C1) IFN-high SLE versus HC, a positive control; (C2) IFN-low SLE versus HC, the primary contrast; (C3) IFN-low SLE versus RA (GSE110169); (C4) high (SLEDAI-2K ≥ 6) versus low (SLEDAI-2K ≤ 4) disease activity within IFN-low SLE†; and (C5) LN versus non-LN within IFN-low SLE, using each cohort's recorded renal involvement†. For each contrast, the LIONESS reference contained only the two classes compared. Contrasts C3–C5 were analysed in a cohort only if each class had at least 25 patients after the go/no-go check; contrasts not meeting this rule are listed with their counts in Supplementary Table S1.

### 2.11 Validation and statistical inference

**Nested cross-validation.** Within each eligible cohort we used repeated, stratified, nested cross-validation (CV) with one sample per patient: 10 repeats of 5 outer folds, each with 5 inner folds. Repetition reduces the variance due to any single split. Every data-dependent step was fitted within training folds: standardization and winsorizing, the IFN cutoff, λ, the LIONESS reference, WGCNA modules, feature scaling, tuning, aggregation and recalibration. Where two cohorts shared a platform and a contrast, models trained on one were applied unchanged to the other as external validation.

**Metrics.** The primary metric was the AUC. Secondary metrics were the Brier score and calibration slope and intercept after Platt recalibration within training folds [37]. The area under the precision–recall curve was reported per cohort only, with the case fraction, because it depends on class balance.

**Hypotheses.** For contrast C2 in the female primary analysis, we pre-specified:
- **H1 (primary):** L3⁺ has a higher AUC than M2⁺, i.e. LIONESS partial-correlation features add information beyond pathway expression and residual IFN signal.
- **H2:** L2 has a higher AUC than M7 and than Q, i.e. beyond dispersion and generic quadratic structure.
- **H3:** the ranking of models across simulation scenarios agrees with predictions P1–P6 (Section 2.13).

Holm correction was applied across H1 and the two comparisons in H2. All other comparisons and contrasts were exploratory and are reported as estimates with confidence intervals.

**Inference.** Out-of-fold predictions are not independent, so tests such as DeLong's understate uncertainty. Standard errors of paired AUC differences were estimated with the nested-CV method of Bates et al. [38]†, with a corrected resampled t-test as a sensitivity analysis, and the false-positive rate of the resulting tests was verified in the null simulation (scenario S0). Because differences between related models are expected to be small, results are reported primarily as estimates with 95% confidence intervals, alongside the minimum detectable difference for each cohort computed by simulation before analysis [RESULT]. Results from eligible cohorts were combined by fixed-effect inverse-variance pooling of paired AUC differences, because between-cohort variance cannot be estimated reliably from two or three cohorts, and agreement in the direction of effect is reported. As a leakage check, outcome labels were permuted and the full pipeline re-run 200 times†; the expected AUC is 0.5.

### 2.12 Population-level tests

To ask *how* IFN-low SLE differs from health, independently of prediction, each pathway was tested in three layers on expression adjusted for age, ancestry, cell composition and the glucocorticoid score (formulas in Supplementary Section S2):
- **Layer 1, mean:** a shrinkage-based Hotelling-type statistic for the difference in mean vectors.
- **Layer 2, spread:** the difference between groups in mean squared Mahalanobis distance from each group's centre.
- **Layer 3, structure:** the Frobenius norm of the difference between group-wise partial-correlation matrices estimated with a common λ, following the differential-network framework of [26]. Partial correlations are unchanged when a gene is rescaled, so differences in spread alone do not affect this statistic.

P-values were obtained with 10,000† Freedman–Lane permutations [39], which permute covariate-model residuals so that covariates are not permuted with the labels; permutation restricted within age bands or batches was a sensitivity analysis. The false discovery rate (FDR) was controlled within each layer by the Benjamini–Hochberg procedure [40].

**Heterogeneity check.** A structure difference can reflect genuine changes in co-regulation or hidden subgroups shifted in different directions, which induce correlation among the shifted genes. In a pilot simulation (10 genes, 80 samples per group), layer 3 held its nominal false-positive rate with no difference (0.05) and with spread-only differences (0.00) but rejected in 99% of datasets with hidden subgroups. Every pathway significant in layer 3 was therefore checked by comparing one- and two-component Gaussian mixture models, fitted to the first three principal components of the pathway's adjusted expression, with the Bayesian information criterion (BIC). In pilot simulations, a threshold of ΔBIC > 2 flagged 1% of null datasets and none with genuine rewiring, but 61% and 100% of datasets with moderate and clear subgroups. Pathways flagged in the patient group but not in controls were reported as "structure difference, possibly due to subgroups". Because the check can miss weak subgroups, unflagged layer-3 results were described as differences in conditional dependence, not as proof of rewiring.

### 2.13 Simulation study

**Aims.** The simulation (i) tested predictions P1–P6, (ii) estimated the power and false-positive rate of H1–H2 and of the population tests at our sample sizes, (iii) checked the design safeguards and (iv) produced a **reading guide** that maps patterns of model performance to mechanisms. The guide was registered before any real-data model was fitted (Section 2.14).

**Designs.** (a) *Gaussian:* controls were multivariate normal with partial-correlation structure from SeqNet networks [41] or from shrinkage estimates in the real female controls for pathways of 15, 30 and 50 genes. (b) *RNA-seq-like counts* were simulated with SeqNet and analysed as log-CPM. (c) *Plasmode:* real female control samples were randomly split into pseudo-cases and pseudo-controls, and known signals were injected into the pseudo-cases, preserving the noise and correlation of real blood data.

**Scenarios.**

| ID | How cases differ | Expected pattern |
|---|---|---|
| S0 | No difference; also with a control-only reference | AUC ≈ 0.5; spurious separation with the control-only reference |
| S1 | Mean shift in some genes | M2 and M4 best; L2 partly (P3) |
| S2a | Covariance scaled; partial correlations unchanged | M7 best; population layer 2 only |
| S2b | Subgroups shifted in opposite directions | M7, Q; layer 3 rejects; heterogeneity check flags |
| S3 | Partial correlations changed in a module | Q and L2; layer 3 rejects; check does not flag |
| S4 | 60% of cases "treated" (shifted module) | Treatment-score baseline |
| S5 | Monotone non-linear dependencies | Rank-based LIONESS |
| S6 | S1 + S4 + a composition factor | Mixed |

**Settings.** For designs (a) and (b), effect sizes were tuned so that the optimal classifier (the true likelihood ratio) reached an AUC of 0.60, 0.70 or 0.80, and model AUCs were reported relative to this ceiling. Plasmode effect sizes were calibrated in a pilot to give the same three ceiling levels for the oracle model of the injected signal†. Sample sizes were 40 versus 40 and the observed sizes of the primary cohorts [N_IFNlow_female versus N_HC_female]. Tier 1 (single pathway) used 200 replicates per setting; Tier 2 (full pipeline, 30 pathways, 1–3 carrying signal) used 100 replicates† with outer CV reduced to 1 × 5. These counts give Monte Carlo standard errors of at most 0.035 and 0.05 for proportions, which are reported for all estimates.

**Outputs.** We report AUC relative to the oracle for every model, scenario and setting; power and false-positive rates; the accuracy of equations (1)–(3); recovery of the true signal pathways by stability selection; and the reading guide. If mechanisms could not be distinguished at our sample sizes, mechanistic interpretation of the real data was to be limited to the population-level tests.

### 2.14 Software, reproducibility, pre-registration and availability

Analyses used R with `corpcor`, `WGCNA`, `glmnet`, `grpreg`, `xgboost`, `pROC`, `singscore`, `SeqNet`, `dnapath` and `lionessR`; versions were fixed with `renv`, workflows were managed with `targets`, seeds were recorded, and a Docker image accompanies the release. The analysis was registered on the Open Science Framework in two stages: stage 1, before any outcome model was fitted (data rules, IFN-low definition, models, hypotheses, inference and all † settings); and stage 2, after the simulation and before any real-data model was fitted (reading guide and simulation-based settings). Deviations are reported [OSF links]. All primary data are public in GEO (Table 1); PRECISESADS data, if used, are available under controlled access from ELIXIR Luxembourg. Code, gene lists and the R implementation of exact LIONESS partial correlation are available at [GitHub URL] and archived at [Zenodo DOI]. AI assistants were used for [planning critique, drafting text and code review]; all analyses, code and text were checked by the authors, who take full responsibility for the content.

## Table 1. Candidate cohorts (draft; counts after the go/no-go check to be added)

| GEO series | Platform | Population | SLE | Comparator | HC | Key annotations | Role |
|---|---|---|---|---|---|---|---|
| GSE319130 | RNA-seq (GPL24676) | Adults, whole blood | 720 (679 F) | — | 84 (77 F) | SLE/HC only; sex inferred | Primary (C1, C2) |
| GSE88884 | Affymetrix HTA 2.0 (GPL17586) | Adults, trial baseline | 1,760 | — | 60 | Age, sex, race, trial batch | Primary or replication (C1, C2, C4†) |
| GSE110169 | Affymetrix (GPL13667) | Adults, whole blood | 82 | 84 RA | 77 | Batch, glucocorticoid use | C3; treatment checks |
| GSE65391 | Illumina HT-12 (GPL10558) | Paediatric, longitudinal | 158 (924 arrays) | — | 46 | SLEDAI, steroids, MMF, HCQ | C4; IFN transitions; treatment checks |
| GSE224705 | Affymetrix (GPL13158) | Adults, LN cohort | 163 | — | 20 (shared) | Prednisone dose, MMF/AZA | Treatment checks |
| GSE99967 | Affymetrix HuGene 2.0 (GPL21970) | Adults | [verify] LN + non-LN | — | [verify] | LN status | C5 *(unverified)* |
| PRECISESADS | RNA-seq | Adults, 7 diseases | [if access] | [if access] | [if access] | Multi-disease | Extension, if access granted |

F, female; HC, healthy controls; LN, lupus nephritis; RA, rheumatoid arthritis; MMF, mycophenolate mofetil; HCQ, hydroxychloroquine; AZA, azathioprine.

## Supplementary Appendix A. Derivations

**A.1 Removing one sample.** Let μ and S be the reference mean and covariance (divisor N). Removing sample q shifts the mean by −d/(N − 1) and gives, exactly, S^(−q) = S − a[(N/(N − 1)) ddᵀ − S] with a = 1/(N − 1). To first order in a, S^(−q) ≈ S − a(ddᵀ − S).

**A.2 Shrinkage covariance.** With λ fixed, Σ_λ = L(S), where L(A) = (1 − λ)A + λ·diag(A) is linear. Hence Σ_λ^(−q) ≈ Σ_λ − a[L(ddᵀ) − Σ_λ], with L(ddᵀ) = (1 − λ)ddᵀ + λD_d.

**A.3 Precision matrix.** For a small perturbation δΣ, δΩ ≈ −Ω δΣ Ω. Therefore Ω^(−q) ≈ Ω + a(M − Ω), where M = Ω L(ddᵀ) Ω = (1 − λ)uuᵀ + λΩD_dΩ and u = Ωd. Note E[M] = Ω Σ_λ Ω = Ω over the reference population.

**A.4 Partial correlation.** Write ρ_ij = −Ω_ij (Ω_iiΩ_jj)^(−1/2). For δΩ = a(M − Ω),
δρ_ij ≈ −δΩ_ij/√(Ω_iiΩ_jj) + (ρ_ij/2)(δΩ_ii/Ω_ii + δΩ_jj/Ω_jj).
Substituting and simplifying (the terms aρ_ij and −aρ_ij cancel) gives
ρ_ij − ρ_ij^(−q) ≈ a[M̃_ij + ρ_ij(M̃_ii + M̃_jj)/2], with M̃_ij = M_ij/√(Ω_iiΩ_jj).

**A.5 LIONESS.** e_ij^(q) = ρ_ij + (N − 1)(ρ_ij − ρ_ij^(−q)), and (N − 1)a = 1, which gives equation (2). With λ = 0, M̃_ij = ũ_iũ_j and M̃_ii = ũ_i², which gives equation (1). Taking expectations, E[M̃_ij] = −ρ_ij and E[M̃_ii] = 1, so E[e_ij^(q)] = ρ_ij − ρ_ij + ρ_ij = ρ_ij.

**A.6 Pearson analogue.** Repeating A.1 and A.4 for r_ij = S_ij(S_iiS_jj)^(−1/2) gives r_ij − r_ij^(−q) ≈ a[z_iz_j − r_ij(z_i² + z_j²)/2], hence equation (3).

**A.7 Result 3.** With reference R of size n, LIONESS gives e = (n + 1)c(R ∪ {q}) − n·c(R), so c(R ∪ {q}) − c(R) = (e − c(R))/(n + 1). No approximation is involved.

**A.8 Numerical checks.** Exact leave-one-out LIONESS on shrinkage partial correlation agreed with equation (2) with correlation 0.997–0.9999 (N = 100–300, G = 12–150, λ = 0–0.7), and better than equation (1) when λ > 0 (for example 0.9987 versus 0.9955 at N = 130, G = 150, λ = 0.7). Equation (4) held to machine precision (maximum absolute difference about 10⁻¹⁶) for Pearson and shrinkage partial correlation. Exact training (leave-one-out) and test (add-one-in) edges had equal spread (ratio 0.98–1.03). Code is provided with the article.

**A.9 SWEET and BONOBO.** [TBD: derive from the published definitions; if BONOBO's posterior mean is linear in ddᵀ, the same first-order argument applies.]

## Supplementary Section S2. Population-level test statistics

**S2.1 Freedman–Lane adjustment.** For pathway expression Y (n × G) and covariates Z, fit Y = Zβ + E without the group label, giving fitted values Ŷ and residuals R̂. For each permutation π, form Y* = Ŷ + R̂_π, regress Y* on Z, and compute the statistic on the residuals split by the observed labels; the observed statistic uses the identity permutation.

**S2.2 Layer 1.** T₁ = (ȳ₁ − ȳ₂)ᵀ Σ̂_λ⁻¹ (ȳ₁ − ȳ₂), with Σ̂_λ the pooled within-group shrinkage covariance.

**S2.3 Layer 2.** D_k = (y_k − ȳ_g(k))ᵀ Σ̂_λ⁻¹ (y_k − ȳ_g(k)); T₂ = |mean_{k∈1} D_k − mean_{k∈2} D_k|, a Mahalanobis analogue of tests of multivariate dispersion [42].

**S2.4 Layer 3.** T₃ = ‖P₁ − P₂‖_F over off-diagonal entries, where P_g is the shrinkage partial-correlation matrix of group g with a common λ chosen on the pooled data.

**S2.5 Heterogeneity check.** Fit one- and two-component Gaussian mixtures to the first three principal components of each group's adjusted data; flag if ΔBIC = BIC₁ − BIC₂ > 2 in patients only. Pilot operating characteristics (200 datasets each, 10 genes, 80 samples): null 1%, rewiring 0%, moderate subgroups 61%, clear subgroups 100%.

## Supplementary Table S3. Pre-specified settings (†) and rationale

| Setting | Value | Rationale |
|---|---|---|
| IFN panel | IFI27, IFI44, IFI44L, RSAD2 | Short panel used for trial stratification; ties results to clinical literature [confirm source] |
| Array processing | RMA from raw files where available | One documented pipeline across samples |
| RNA-seq filter | edgeR `filterByExpr` | Standard, data-adaptive |
| Glucocorticoid score | Up-regulated genes of [27] | Consistent direction; simplest score |
| Cell-type scores | singscore on 7 marker sets | Single-sample, so leakage-free |
| Reference subsets | B = 20, balanced | Variance of averaged edges stabilizes by about 20 draws [confirm in pilot] |
| λ grid | {0.5, 1, 2} × analytic estimate | Brackets the analytic value at modest cost |
| Weight rescaling | Training-fold 99th percentile of \|e\| | Robust to extreme edges; keeps scale differences |
| Tuning budget | 20 evaluations per model | Equal effort for every model |
| Stability selection | 100 half-samples; threshold 0.6 | Values recommended in [36] |
| Activity groups | SLEDAI-2K ≥ 6 vs ≤ 4 | Common threshold for active disease; gap reduces misclassification [clinician to confirm] |
| LN definition | Recorded renal involvement per cohort | Uses available annotation |
| CV inference | Bates et al. [38]; corrected t-test as sensitivity | Accounts for dependence between folds |
| Label permutations | 200 | Enough to estimate the null mean AUC to ±0.01 |
| Population-test permutations | 10,000 | P-values resolved to 10⁻⁴ for FDR control |
| Tier 2 replicates | 100 | Monte Carlo SE ≤ 0.05 for power |

## Supplementary Section S4. Additional comparator arms

**Rank-based LIONESS (L-R).** Each gene was transformed to normal scores using its ranks within the training fold (the nonparanormal transform [43]); test samples were mapped onto the training ranks by interpolation. Partial correlations and LIONESS edges were then computed as in Section 2.7. This arm captures monotone non-linear dependence and is robust to outliers (scenario S5).

**Other single-sample methods.** SSN [15], SWEET [17] and BONOBO [18] were computed with the same reference subsets as LIONESS, using the authors' published implementations where available [TBD: implementations and versions], and summarized with the same topology features (Section 2.8).

**Exploratory topology metrics.** Signed weighted clustering [32] and threshold-integrated betweenness [33] were computed on graphs thresholded at the top 5–30% of |e|.

## Supplementary Table S2. Additional comparators (analysed identically; reported in the supplement)

| ID | Features | Question addressed |
|---|---|---|
| M3 | Pathway scores (singscore, mean z-score, first principal component) | Module-style summaries |
| M5 | Residual products ũ_iũ_j with the same topology features as L2 | LIONESS without the reference network |
| M6 | Pathway expression, gradient boosting | Generic non-linear baseline |
| L1 | LIONESS partial-correlation edges | Edge-level features |
| L-R | Rank-based LIONESS topology | Monotone non-linear dependence |
| S-SSN, S-SWEET, S-BONOBO | Topology of other single-sample networks | Test of P6 and of the unifying theory |

## References

1. Chiche L, et al. Modular transcriptional repertoire analyses of adults with systemic lupus erythematosus reveal distinct type I and type II interferon signatures. *Arthritis Rheumatol* 2014. PMID 24644022.
2. Catalina MD, et al. Gene expression analysis delineates the potential roles of multiple interferons in systemic lupus erythematosus. *Commun Biol* 2019. PMID 31044165.
3. Banchereau R, et al. Personalized immunomonitoring uncovers molecular networks that stratify lupus patients. *Cell* 2016. PMID 27040498.
4. Li W, et al. Cuproptosis-related gene identification and immune infiltration analysis in systemic lupus erythematosus. *Front Immunol* 2023. PMID 37313407.
5. Meng XW, et al. MX2: identification and systematic mechanistic analysis of a novel immune-related biomarker for systemic lupus erythematosus. *Front Immunol* 2022. PMID 36059547.
6. Ambroise C, McLachlan GJ. Selection bias in gene extraction on the basis of microarray gene-expression data. *PNAS* 2002. PMID 11983868.
7. Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. *Patterns* 2023. PMID 37720327.
8. Panwar B, et al. Multi-cell type gene coexpression network analysis reveals coordinated interferon response and cross-cell type correlations in systemic lupus erythematosus. *Genome Res* 2021. PMID 33674349.
9. [Authors to confirm]. Type I interferon gene signature test-low and -high patients with systemic lupus erythematosus have distinct gene expression signatures. *Lupus* 2019. PMID 31660791. *(unverified)*
10. Hubbard EL, et al. Analysis of transcriptomic features reveals molecular endotypes of SLE with clinical implications. *Genome Med* 2023. PMID 37845772.
11. Gómez-Bañuelos E, et al. Uncoupling interferons and the interferon signature explains clinical and transcriptional subsets in SLE. [Journal to confirm] 2024. PMC11148857. *(unverified)*
12. Barturen G, et al. Integrative analysis reveals a molecular stratification of systemic autoimmune diseases. *Arthritis Rheumatol* 2021. *(unverified)*
13. Vital EM, et al. Anifrolumab efficacy and safety by type I interferon gene signature and clinical subgroups in patients with SLE: post hoc analysis of pooled data from two phase III trials. *Ann Rheum Dis* 2022;81(7):951–961. PMID 35338035. *(unverified)*
14. Kuijjer ML, et al. Estimating sample-specific regulatory networks. *iScience* 2019. PMID 30981959.
15. Liu X, et al. Personalized characterization of diseases using sample-specific networks. *Nucleic Acids Res* 2016. PMID 27596597.
16. Huang Y, et al. Disease characterization using a partial correlation-based sample-specific network. *Brief Bioinform* 2021. PMID 32422654.
17. Chen HH, et al. SWEET: a single-sample network inference method for deciphering individual features in disease. *Brief Bioinform* 2023;24(2):bbad032. *(unverified)*
18. Saha E, et al. Bayesian inference of sample-specific coexpression networks. *Genome Res* 2024;34(9):1397. *(unverified)*
19. De Marzio M, Glass K, Kuijjer ML. Single-sample network modeling on omics data. *BMC Biol* 2023. *(unverified)*
20. Kuijjer ML, De Marzio M, Glass K. Challenges and opportunities in single-sample network modeling. *bioRxiv* 2026 (preprint). PMID 41867852.
21. Gregorich M, et al. Individual-specific networks for prediction modelling – a scoping review of methods. *BMC Med Res Methodol* 2022. *(unverified)*
22. Leyva A, Niazi MKK. [Title to confirm]. *PLoS One* 2026. PMID 42743314.
23. Yin L, et al. Sample-specific network analysis identifies gene co-expression patterns of immunotherapy response. *iScience* 2025. PMID 40740488.
24. Deschildre J, et al. Evaluation of single-sample network inference methods for precision oncology. *NPJ Syst Biol Appl* 2024. PMID 38360881.
25. Zhang B, Horvath S. A general framework for weighted gene co-expression network analysis. *Stat Appl Genet Mol Biol* 2005. PMID 16646834.
26. Grimes T, Potter SS, Datta S. Integrating gene regulatory pathways into differential network analysis of gene expression data. *Sci Rep* 2019. *(unverified)*
27. Hu Y, et al. Development of a molecular signature to monitor pharmacodynamic responses mediated by in vivo administration of glucocorticoids. *Arthritis Rheumatol* 2018. PMID 29534336.
28. Masson HO, et al. XIST expression and hypermethylation of the X chromosome in males with systemic lupus erythematosus. *Front Immunol* 2026. PMID 42039161.
29. Hoffman RW, et al. Gene expression and pharmacodynamic changes in 1,760 systemic lupus erythematosus patients from two phase III trials of BAFF blockade with tabalumab. *Arthritis Rheumatol* 2017. PMID 27723281.
30. López-Domínguez R, et al. Immune and molecular landscape behind non-response to mycophenolate mofetil and azathioprine in lupus nephritis therapy. *Res Sq* 2024 (preprint). PMID 38260685.
31. Schäfer J, Strimmer K. A shrinkage approach to large-scale covariance matrix estimation and implications for functional genomics. *Stat Appl Genet Mol Biol* 2005. PMID 16646851.
32. Costantini G, Perugini M. Generalization of clustering coefficients to signed correlation networks. *PLoS One* 2014. PMID 24586367.
33. Gregorich M, et al. Flexible parametrization of graph-theoretical features from individual-specific networks for prediction. *Stat Med* 2024. PMID 38664934.
34. Friedman JH. Regularized discriminant analysis. *J Am Stat Assoc* 1989. *(unverified)*
35. Yuan M, Lin Y. Model selection and estimation in regression with grouped variables. *J R Stat Soc B* 2006. *(unverified)*
36. Meinshausen N, Bühlmann P. Stability selection. *J R Stat Soc B* 2010. *(unverified)*
37. Platt J. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In: *Advances in Large Margin Classifiers*, 1999. *(unverified)*
38. Bates S, Hastie T, Tibshirani R. Cross-validation: what does it estimate and how well does it do it? *J Am Stat Assoc* 2023. *(unverified)*
39. Freedman D, Lane D. A nonstochastic interpretation of reported significance levels. *J Bus Econ Stat* 1983. *(unverified)*
40. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *J R Stat Soc B* 1995. *(unverified)*
41. Grimes T, Datta S. SeqNet: an R package for generating gene-gene networks and simulating RNA-seq data. *J Stat Softw* 2021. PMID 34321962.
42. Anderson MJ. Distance-based tests for homogeneity of multivariate dispersions. *Biometrics* 2006;62(1):245–253. *(unverified)*
43. Liu H, Lafferty J, Wasserman L. The nonparanormal: semiparametric estimation of high dimensional undirected graphs. *J Mach Learn Res* 2009;10:2295–2328. *(unverified)*
