# Paper 2 Plan: Single-sample partial-correlation networks in interferon-low SLE. A pathway-based LIONESS vs WGCNA comparison

**How to read the markers:**
- **⚠ D#** marks a decision that needs your input. All of them are collected in [Section 8](#8-open-decisions).
- *(unverified)* marks a claim not confirmed from a primary source.
- *(estimate)* marks a projection to be replaced by the feasibility counts in Section 0.
- GEO accessions and PMIDs were checked against NCBI on 2026-10-01.

---

## Summary

About 13–35% of SLE patients don't carry the type I interferon (IFN) signature. In these **IFN-low** patients, blood expression levels look almost like those of healthy people: Panwar 2021 found only 5 differentially expressed genes in classical monocytes, against 1,288 for IFN-positive SLE. No published classifier reports its performance separately for this group.

**Question:** do **per-patient (LIONESS) partial-correlation networks**, built within Reactome pathways and combined across pathways, separate IFN-low SLE from healthy controls better than (a) WGCNA module features, (b) linear expression, and (c) simple measures of how far a patient deviates from health?

**Why networks might help here.** To first order, a LIONESS partial-correlation edge is a quadratic function of the patient's expression (Appendix A):

> e_ij ≈ ũ_i ũ_j + ρ_ij (1 + (ũ_i² + ũ_j²)/2)

Here ũ_i is gene i's standardized residual after regressing it on the rest of its pathway. The squared terms pick up **heterogeneity**: patients who deviate from health in *different directions* show no mean difference but do show larger squared deviations. So the hypothesis is testable, and it implies a simple competing baseline: each patient's per-pathway **distance from health**. LIONESS has to beat that baseline as well as WGCNA.

**Main threats, addressed in the design:**
- Confounding by **treatment**, **sex** and **batch**: IFN-low patients are usually treated; controls are often unmatched on sex and processed in separate batches.
- **Leakage** in the IFN-low definition itself: the cutoff comes from the controls, who are also the comparison group.
- **Small samples:** the number of controls per cohort is the limit.

The project starts with a **2-week go/no-go feasibility check** (Section 0).

**Framing.** The lasting contribution is methodological:
- LIONESS with shrinkage partial correlation (new as far as we found)
- its quadratic approximation
- leakage-free scoring of new patients
- mechanism-aware baselines
- a simulation study showing which model wins under which mechanism

IFN-low SLE is a demanding application. Distinguishing SLE from health isn't a clinical diagnostic need, so the paper is framed as *biology plus method*, not as a diagnostic test.

---

## 0. Go/no-go feasibility check (weeks 1–2)

**Per candidate cohort** (Section 3), using scripted GEO downloads:
1. Compute an IFN score. Count **IFN-low SLE patients** (IFN score ≤ control mean + 2 SD; one sample per patient) and **controls**.
2. **Infer sex from expression** using Y-chromosome genes only (RPS4Y1, DDX3Y, KDM5D, UTY, EIF1AY), not XIST: in the GSE319130 cohort, 54% of male SLE patients have abnormal XIST expression (Masson 2026). Check the calls against reported sex where GEO has it, and tabulate sex by group.
3. Cross-tabulate **batch or processing date** by group, where available.
4. Tabulate **medications** (glucocorticoids, HCQ, MMF) for IFN-low patients, where available (GSE224705, GSE65391, GSE110169).

**Go criterion:** at least **2 cohorts**, each with **≥ 40 female IFN-low SLE and ≥ 40 female controls**, and with **batch not confounded with group**. That means controls and SLE patients aren't in disjoint batches. ⚠ **D1**

**If no-go:** fall back to (i) a single-cohort study in GSE88884 or GSE319130, framed as exploratory, or (ii) the IFN-low SLE vs RA contrast (Section 4.10).

**Precision at plausible sizes** (Hanley–McNeil 95% CI half-width for one AUC; paired model comparisons are tighter):

| Scenario | AUC 0.65 | AUC 0.75 |
|---|---|---|
| About 150 IFN-low vs 60 HC (GSE88884-like) | ±0.078 | ±0.067 |
| About 90 IFN-low vs 77 HC (GSE319130, female-only) | ±0.083 | ±0.073 |
| 40 vs 40 (the go minimum) | ±0.120 | ±0.107 |
| About 45 vs 23 (GSE138458-like) | ±0.133 | ±0.116 |

---

## 1. Background and rationale

### 1.1 IFN-low SLE

- **Prevalence of the IFN signature:**
  - 87% of patients IFN-positive (Chiche 2014, GSE49454)
  - 66–73% depending on activity status (Catalina 2019)
  - 84.8% of samples in pediatric GSE65391 (Banchereau 2016)
- **Almost no expression signal vs controls:** Panwar 2021 (*Genome Res*) found 5 DEGs between IFN-negative SLE and controls in classical monocytes, against 1,288 for IFN-positive SLE.
- **Endotypes:** Hubbard 2023 (*Genome Med*) found a "least-perturbed" SLE endotype that resembles controls.
- **Gap:** no paper reports classifier performance separately for IFN-low patients. Published SLE-vs-control AUCs (0.85–1.0) are driven almost entirely by IFN-stimulated genes.

### 1.2 Single-sample networks and prediction

- **No application to SLE** of LIONESS, SSN, SWEET, CSN, iENA or BONOBO turned up in our PubMed and web searches.
- **No paper combining LIONESS with partial correlation** turned up in PubMed (2026-10-01). The closest precedent is P-SSN, a partial-correlation version of SSN (Huang 2021 *Brief Bioinform*, PMID 32422654; abstract only).
- **Evidence that these networks help prediction is thin:**
  - Leyva & Niazi 2026 (*PLoS One*): Pearson-LIONESS edges reached held-out AUC 0.467, against 0.815 for expression modules.
  - Yin 2025 (*iScience*): small gains when SWEET edges were added to expression.
- **Known biases:** LIONESS gives higher weights to under-represented groups and encodes differential expression in its edges (Deschildre 2024 *NPJ Syst Biol Appl*; Kuijjer, De Marzio & Glass 2026, bioRxiv preprint).

### 1.3 Why the IFN-low comparison suits second-order features

- Where linear (mean) differences are small, any separation has to come from **structure**: deviations in different directions, changes in variance, or changes in co-regulation.
- The quadratic form of LIONESS (Appendix A) captures this through its squared-residual and product terms.
- So the design must distinguish three explanations:
  - (a) a simple dispersion effect, captured by distance from health (baseline M7)
  - (b) generic second-order effects (baselines M5, M6)
  - (c) a genuine network effect (L2 beats both)
- A simulation study with known mechanisms (Section 4.11) checks that the design can actually tell these apart at our sample sizes.

### 1.4 Lessons carried over

From the osteosarcoma pilot (`PROJECT_SUMMARY.md`) and paper 1 (`LEAKAGE_PAPER_PLAN.md`):
- No label-based selection outside the training fold. That includes the **IFN-low cutoff**.
- No unweighted metrics on complete graphs; betweenness uses explicit distances.
- Overlapping datasets are excluded, using paper 1's overlap catalog.
- One sample per patient.

---

## 2. Questions, aims, hypotheses

**Primary question:** in IFN-low SLE vs healthy controls, does pathway-wise LIONESS partial-correlation topology beat WGCNA, linear expression, and distance-from-health baselines?

**Aims:**
1. **Define and characterize the IFN-low group** without leakage, and quantify confounding (sex, batch, treatment).
2. **Build the predictors:** LIONESS-partial topology per Reactome pathway, combined by stacking; then compare with WGCNA and the mechanism-aware baselines inside a leakage-free design.
3. **Explain any signal:** which pathways contribute, and is the signal dispersion, generic second-order structure, or network-specific? A simulation study with known mechanisms (Section 4.11) shows how reliably the design can tell these apart.

**Pre-specified hypotheses** (female-only; within-cohort nested CV, pooled across eligible cohorts; Holm correction across H1–H3):
- **H1 (primary):** LIONESS-partial topology (L2) has a higher AUROC than fold-internal WGCNA eigengenes (W2).
- **H2:** L2 beats pathway-wise linear expression (M2).
- **H3:** L2 beats distance from health (M7) and residual-product networks (M5).
- **H4 (descriptive):** IFN-low SLE shows larger per-pathway dispersion than controls (distance-from-health scores) in identifiable pathways.
- **Robustness:** conclusions for H1–H3 hold after excluding glucocorticoid-response genes, and in an all-sex analysis (Section 4.2).
- **Positive control:** in IFN-high SLE vs controls, every model reaches a high AUC. We'll also plot the advantage of each model class against how large the linear signal is (IFN-high → IFN-low).

> **Expected outcome, stated honestly.** A plausible result is a modest AUC (about 0.6–0.7) that the distance-from-health baseline matches, or a separation largely explained by treatment. Both are informative: they'd show that IFN-low SLE differs from health mainly in dispersion or treatment rather than in co-regulation. The design makes these outcomes interpretable, and the target journal (*Briefings in Bioinformatics*, Section 7) suits either outcome.

---

## 3. Data

### 3.1 Candidate cohorts (SLE and healthy controls)

All verified against GEO 2026-10-01. Group counts come from series-matrix sample annotations; IFN-low counts are *(estimate)*, using a 13–35% IFN-low rate, and will be replaced in Section 0.

| GSE | Platform | Tissue / age | SLE patients (arrays) | HC | IFN-low SLE *(estimate)* | Covariates in GEO | Notes |
|---|---|---|---|---|---|---|---|
| **GSE88884** | Affymetrix HTA 2.0 (GPL17586) | WB, adults | 1,760 | 60 | ≈230–620 | age, sex, race, region, `batch` (trial); no medications | Hoffman 2017, PMID 27723281. Expression is in the supplementary files. Controls are split across trial batches. **Likely primary cohort.** |
| **GSE319130** | RNA-seq (GPL24676) | WB | 720 (679 F) | 84 (77 F) | ≈90–240 (female) | SLE/HC only in the GEO matrix | Masson 2026 *Front Immunol*, PMID 42039161 (Eli Lilly). Sex counts are from the paper; per-sample sex must be inferred (Y-chromosome genes, Section 0). Trial origin not stated in the abstract *(unverified)*. Expression in supplementary files. **Likely primary cohort.** |
| GSE138458 | Illumina HT-12 v4 (GPL10558) | WB, adults | 198 (312) | 23 (24 arrays) | ≈25–70 | none | Guthridge 2020, PMID 32154507. Controls limit power. |
| GSE65391 | GPL10558 | WB, **pediatric** | 158 (924) | 46 (72 arrays; 36 female) | ≈24 | race, gender, age, `batch`, oral and IV steroids (0/1), MMF, HCQ | Banchereau 2016, PMID 27040498. Controls include technical replicates. 58 girls off steroids at first visit. **Used for the steroid checks** (Section 4.2). |
| GSE110169 | Affymetrix (GPL13667) | WB | 82 | 77 (+84 RA) | ≈11–29 | `batch`, `glucocorticoids` (TRUE/FALSE) | Hu 2018 (Bristol-Myers Squibb), PMID 29534336: the glucocorticoid-signature paper. Enough controls but few IFN-low patients; only 25 women off steroids. **RA available.** |
| GSE61635 | Affymetrix U133 Plus 2 (GPL570) | Blood | 80 (99 arrays) | 30 | ≈10–28 | — | RNP-autoantibody-positive patients only; no PMID |
| GSE72509 | RNA-seq (GPL16791) | WB | 99 | 18 | ≈13–35 | `anti-ro`, `ism` | Hung 2015 *Science*, PMID 26382853 |
| GSE112087 | RNA-seq (GPL16791) | WB | 31 | 29 (2 lanes each) | ≈4–11 | — | Figgett 2019, PMID 31921420 |
| GSE49454 | GPL10558 | WB, adults | 62 (157) | 20 | ≈8 | medications | Too few IFN-low patients alone; only 10 women off steroids, so not used for the steroid checks. **Contained in GSE72326.** |
| GSE45291 / GSE121239 / GSE224705 (Hopkins) | Affymetrix (GPL13158) | WB, adults | 292 / 65 / 163 (428) | 20 (shared; sex not recorded) | ≈21–57 (GSE224705) | GSE224705 only: prednisone mg/day, MMF/AZA dose, HCQ, sex (SLE only) | One Hopkins cohort: the series share patients, and the 20 controls are probably the same in all three. Use one series per analysis and never pool them. **GSE224705 is used for the steroid checks** (Section 4.2): 94 women off prednisone at first visit, 53 on. It's a lupus nephritis cohort on MMF or azathioprine (López-Domínguez 2024, preprint), so its IFN-low patients aren't typical SLE. GSE45291 also has 493 RA. |

**Excluded:** GSE50772 (PBMC; matrix not log2; small); GSE72326 (duplicates GSE49454); single-cell series.

**Likely shape of the study.** The number of controls is the binding limit. GSE88884 and GSE319130 are the only cohorts likely to pass the go criterion. They're on different platforms (array vs RNA-seq), so the primary analysis is **within-cohort, then pooled** (Section 4.8), and cross-cohort transfer is exploratory. The female-only primary analysis lowers the control counts further: GSE319130 has 77 female controls; the female count for GSE88884 comes from the go check. ⚠ **D2**

### 3.2 Harmonization

- **Inputs:** normalized log2 data; RNA-seq as log-CPM with TMM normalization. One sample per patient; technical replicates averaged.
- **No cross-cohort batch correction.** Each cohort is analysed separately.
- **Sex-chromosome genes** stay in the features in the primary (female-only) analysis. In the all-sex sensitivity analysis, Y-chromosome genes and XIST/TSIX are removed (Section 4.2). Genes are mapped to symbols within each platform.

---

## 4. Methods

### 4.1 IFN score and IFN-low definition (leakage-safe)

- **IFN gene set:** pre-specified ⚠ **D3**. Options:
  - a standard IFN-stimulated-gene panel, e.g. IFI27, IFI44L, IFIT1, ISG15, RSAD2, SIGLEC1
  - the Catalina 2019 WGCNA IFN-module genes
  - Reactome "Interferon alpha/beta signaling"
- **Score:** mean z-score of the panel genes, standardized with **training-fold control** means and SDs.
- **Cutoff:** IFN-low = score ≤ training-fold control mean + 2 SD. **Computed inside each training fold** and applied unchanged to that fold's test samples.
- **The same filter applies to controls**, dropping roughly 2.5% of them. Both groups then meet the same IFN criterion, and the IFN score carries little information by construction.
- **Features exclude the IFN-score genes** (primary analysis). **D4** decides whether to also drop Reactome *Interferon Signaling* (R-HSA-913531) pathways, since residual IFN signal inside the truncated range could still discriminate. Report both.

### 4.2 Confounding controls (design-based, minimal)

We are **not** fitting covariate-adjusted models. Instead, the design removes or exposes the main confounders. This departs from the earlier "don't adjust unless WGCNA did" rule, because with a weak true signal, confounders can produce all of the apparent separation ⚠ **D5**.

| Confounder | Control |
|---|---|
| **Sex** (SLE about 90% female) | **Primary analysis is female-only**, with sex inferred from Y-chromosome genes in every cohort (Section 0). X-chromosome genes stay in the features: removing them would delete TLR7, TLR8, CXCR3, CD40LG, FOXP3, BTK and IKBKG from the immune pathways. Sensitivity analysis: **all sexes**, with Y-chromosome genes and XIST/TSIX removed. Male SLE patients can show X-chromosome silencing (Masson 2026), so X-linked genes in the all-sex analysis are interpreted with care. |
| **Batch / processing** | Cohorts where controls and SLE patients are in disjoint batches are **ineligible** (Section 0). Report the batch × group table. |
| **Treatment** (glucocorticoids, HCQ, MMF) | (a) A **glucocorticoid-response score** built from the 64 prednisolone-induced genes of Hu 2018 is reported as a baseline model (M0b). Hu 2018 showed that the score rises with prednisolone dose in healthy volunteers and largely agrees with reported steroid use in SLE and RA. If it alone separates the groups well, the result is flagged. (b) Primary models are re-run **excluding the 64 signature genes**. (c) **Steroid checks** in the two cohorts that record steroid use per patient: GSE224705 (prednisone dose) and GSE65391 (oral and IV steroids; pediatric). One sample per patient, from the first visit, never chosen by steroid status. They have too few IFN-low women off steroids (about 10–35 per cohort) to re-run the classifiers, so two checks are run instead. **(c1)** Among IFN-low patients, compare those on and off steroids on the top-weighted pathways from the primary cohorts, with the per-pathway features computed within each steroid cohort. A difference means those pathways track treatment. This check needs no controls. **(c2)** Check that the glucocorticoid score tracks recorded steroid use and dose, using all SLE patients and then IFN-low patients only. If it does, the score stands in for the missing medication data in GSE88884 and GSE319130. |
| **Age** | Reported where available; pediatric cohort (GSE65391) analysed separately. |

### 4.3 Pathways

- **Primary:** Reactome pathways in the *Immune System* subtree (R-HSA-168256), with 15–150 genes present after filtering, minus the IFN pathways if D4 says so. Reduce redundancy with a Jaccard > 0.8 filter. This pre-specified, moderate-sized set limits overfitting at the stacking step. The count will be reported after filtering.
- **Secondary:** all Reactome pathways with 15–150 genes, for discovery outside the immune system (e.g. metabolism or cell-cycle programs).
- MSigDB version pinned ⚠ **D6**.

### 4.4 LIONESS partial-correlation networks

- **Edges:** shrinkage partial correlation among the pathway's genes, ρ_ij = −Ω_ij / √(Ω_ii Ω_jj).
  - Ω is the inverse of a Schäfer–Strimmer shrinkage covariance (`corpcor`, diagonal target; PMID 16646851).
  - **λ and the target are estimated once per training fold and held fixed.**
  - Conditioning set: the pathway's genes. Optionally add cell-composition proxies ⚠ **D7**.
- **Reference population:** the training fold of the **analysis set** (IFN-low SLE + controls), one sample per patient.
- **All samples are computed the same way, whatever their class:**
  - Training samples: exact **leave-one-out** (one matrix inversion plus a Sherman–Morrison update per sample).
  - Test samples: exact **add-one-in** against the training reference.
  - Do **not** use a control-only reference. Control networks would then be computed leaving one out and SLE networks not, and that asymmetry can create separation on its own.
  - Sensitivity analysis: a reference that also includes IFN-high SLE (larger N, more stable estimates) ⚠ **D8**.
- **Robust transform** before LIONESS: winsorize at ±4 SD, or rank-based inverse-normal transform.
- **Pearson-LIONESS arm (L2-P):** same pipeline, Pearson edges.
- **Implementation:** our own closed-form code, unit-tested against naive recomputation, `corpcor::pcor.shrink` with λ fixed, and lionessR (Pearson arm).

### 4.5 Topology features (per patient per pathway)

LIONESS weights are signed, complete, and unbounded, so each metric is defined explicitly. The same metrics are also computed on residual-product networks (M5).

| Metric | Definition |
|---|---|
| Node strength | Positive strength s⁺ and negative strength s⁻ kept separate; also \|s\|. Unweighted degree is constant on a complete graph. |
| Clustering / transitivity | Signed weighted clustering (Costantini & Perugini 2014) on weights rescaled to [−1, 1]; global = mean over nodes |
| Betweenness | Weighted betweenness with distance 1/\|w̃\| on rescaled weights; plus a threshold-integrated version (top 5–30% of \|w\|; Gregorich 2024) |
| Pathway-level | Mean \|w\|; leading eigenvalue; global efficiency; ‖W − P‖_F (distance from the reference partial-correlation matrix) |

⚠ **D9**: the final metric set. Recommendation: pre-specify s⁺, s⁻, signed clustering, threshold-integrated betweenness and the four pathway-level summaries; everything else is exploratory.

### 4.6 Aggregating across pathways

1. **Level 1:** a per-pathway elastic-net logistic model, with out-of-fold predictions from inner CV.
2. **Level 2:** a non-negative elastic-net stacker. Its weights give **pathway attribution**.
3. **The same scheme applies to every pathway-based baseline**, so only the feature type differs between models.
4. **Sensitivity analysis:** one global elastic net on all features concatenated.

### 4.7 Models compared

| ID | Features | Purpose |
|---|---|---|
| M0a | Residual IFN score (inside the truncated range) | Checks for leftover IFN signal |
| M0b | Glucocorticoid-response score (Hu 2018 signature) | **Treatment confounding check** |
| M1 | All-gene expression (elastic net; random forest) | Standard expression baseline |
| M2 | Pathway expression, stacked | Linear baseline with matched aggregation |
| M3 | Pathway scores (singscore, mean z, PC1), stacked | Module-style scores |
| M4 | Conditional residuals ũ, stacked | Linear building block of LIONESS-partial |
| **M7** | **Distance from health per pathway**: (a) Σũ² against the pooled reference; (b) Mahalanobis distance from the training-fold control distribution (shrinkage covariance); stacked | **Heterogeneity baseline** (Section 1.3) |
| M5 | Residual-product networks ũ_i ũ_j, same topology as L2, stacked | LIONESS null model |
| M6 | Pathway expression with interactions (gradient boosting / kernel SVM), stacked | Generic second-order baseline |
| W1 | Typical published SLE-vs-HC WGCNA + hub-gene + ML pipeline, implemented **leak-free** (shared with paper 1) | Literature-style comparator |
| **W2** | Fold-internal signed WGCNA eigengenes, projected onto test samples | **Primary comparator** |
| L1 | LIONESS-partial edges, stacked | Edge level |
| **L2** | LIONESS-partial topology, stacked | **Primary model** |
| L2-P | LIONESS-Pearson topology, stacked | Partial vs marginal correlation |
| L3 | L2 + M2 | Added value over expression |

### 4.8 Validation and statistics

- **Within each eligible cohort:** repeated nested CV (10 × 5 outer folds, stratified, one sample per patient). Everything is fitted inside the folds: IFN cutoff, standardization, shrinkage λ, LIONESS reference, WGCNA, feature selection, stacking.
- **Pooling:** random-effects meta-analysis of the **paired AUROC differences** (L2 − W2, L2 − M2, L2 − M7, L2 − M5) across cohorts.
- **Cross-cohort transfer** (exploratory): between same-platform cohorts if counts allow (e.g. GSE138458 ↔ GSE65391), with per-cohort label-free standardization.
- **Leakage check:** label permutation through the whole pipeline should give AUC ≈ 0.5.
- **Metrics:** AUROC (primary), AUPRC, Brier score, calibration; bootstrap CIs; paired DeLong or bootstrap tests; Holm across H1–H3.

### 4.9 Interpretation (Aim 3)

- **Pathway attribution:** stacking weights for each model.
- **Dispersion analysis (H4):** for each pathway, compare the distance-from-health distribution between IFN-low SLE and controls; check for unequal variance.
- **Network-specific signal:** pathways where L2 beats M7 and M5 are candidates for genuine co-regulation changes. Report which genes' strength and centrality differ.
- **Treatment check:** do the top pathways overlap glucocorticoid-response genes?

### 4.10 Secondary contrasts

- **Positive control:** IFN-high SLE vs controls, same pipeline.
- **A more clinically relevant contrast:** IFN-low SLE vs **rheumatoid arthritis**: GSE110169 (84 RA) and GSE45291 (493 RA). Exploratory, and also the fallback if the go check fails.

### 4.11 Simulation study

**Purpose.** Real data can't show which mechanism produced a separation. The simulation generates data where the mechanism is known and runs the same pipeline on it. It answers three questions before the real-data models are run:
1. **Which model wins under which mechanism?** This turns the reading of the real-data results (Section 1.3, Aim 3) into an empirical lookup instead of an assumption. M7 measures distance with a covariance matrix, so it also responds to co-regulation changes. The simulation measures how well M7, M5 and L2 can actually be told apart.
2. **Power at our sample sizes:** how often the H1–H3 tests detect a real advantage, and how often they give a false positive when there is none.
3. **Do the design safeguards work?** The symmetric LIONESS reference (Section 4.4) should give no separation under the null, and a control-only reference should create spurious separation, as predicted.

**Generating model** (per pathway; "cases" stand for IFN-low SLE):
- Controls are multivariate normal with mean 0. Their partial-correlation structure comes from one of two sources:
  - networks generated with SeqNet (Grimes & Datta 2021): hub-and-module structures of realistic sparsity
  - shrinkage partial-correlation matrices estimated from the real **female control** samples for three Reactome pathways (about 15, 50 and 150 genes). This gives realistic structure without touching any SLE data.
- As a check on the Gaussian results, one setting is repeated with RNA-seq-like counts from SeqNet, analysed as log-CPM.

**Scenarios:**

| ID | How cases differ from controls | What it stands for | Expected winner |
|---|---|---|---|
| S0 | No difference. Also run with a control-only LIONESS reference. | Null; the asymmetry artefact (Section 4.4) | None (AUC ≈ 0.5); spurious separation with the control-only reference |
| S1 | Mean shift in a subset of genes | Ordinary differential expression | M2, M4 |
| S2a | Covariance scaled up (Σ_case = cΣ), so partial correlations are unchanged | Patients deviate more, in no particular direction | M7 |
| S2b | Cases are a mix of 2–3 subtypes shifted in different directions, with no net mean shift | Deviations in different directions (Section 1.3) | M7, M5 |
| S3 | Partial correlations changed within a gene module (edges added, removed or sign-flipped); means and marginal variances held equal | Genuine co-regulation change | M5, L2 |
| S4 | A "treated" 60% of cases has a shifted, co-expressed module; no disease effect | Treatment confounding (Section 4.2) | The module score (M0b analogue); the signal disappears once the module genes are excluded |

The expected winners are hypotheses. Measuring them is the point of the simulation.

**Effect sizes.** In each scenario, the effect size is tuned so that the best possible classifier reaches an AUC of 0.60, 0.70 or 0.80. That classifier is the true likelihood ratio, which can be computed because the generating model is known. This puts all scenarios on one scale, and each model is reported as its AUC against that ceiling.

**Two tiers:**
- **Tier 1, single pathway.**
  - Pathway size G: 15, 50 and 150.
  - Sample sizes (cases vs controls): 40 vs 40 (the go minimum), 90 vs 77 (GSE319130, female-only) and 150 vs 60 (GSE88884-like).
  - 200 replicates per setting, 5-fold CV.
  - Models: the oracle (true likelihood ratio), M2, M4, M5, M6, M7, W2, L1, L2 and L2-P.
- **Tier 2, full pipeline.**
  - 30 pathways with sizes drawn from the real pathway set; 1–3 of them carry the signal.
  - Scenarios S0, S1, S2b and S3, at an oracle AUC of 0.70 and the three sample sizes.
  - 100 replicates, with the full nested CV and stacking (outer CV reduced to 1 × 5 to save compute) and the H1–H3 tests as in Section 4.8.
  - Also checks pathway attribution: do the stacking weights rank the true signal pathways first?
- **Precision:** 200 replicates estimate a power near 0.5 to within about ±0.07 (95% CI); 100 replicates to within about ±0.10.

**Outputs:**
- AUC against the oracle for every model, scenario, sample size and pathway size.
- Power and false-positive rate for the H1–H3 comparisons.
- Accuracy of the first-order approximation at each G/N under shrinkage, extending the table in Appendix A.
- A **reading guide**: which pattern of model ranks (M2/M4, M7, M5, L2) points to which mechanism, and how reliably at our sample sizes. It's written down before the real-data models are run. If the simulation shows the mechanisms can't be told apart at our sizes, Aim 3 is reported as descriptive only.

**Implementation.** The code lives in `sim/` and calls the same pipeline functions as the real analysis, so the simulation also serves as an end-to-end test. Seeds are recorded. A timing run will confirm the replicate counts. ⚠ **D12**

---

## 5. Expected outputs

| Item | Content |
|---|---|
| Fig. 1 | Design: leakage-safe IFN-low definition, nested CV, symmetric LIONESS reference |
| Fig. 2 | Confounding audit: sex, batch and treatment by group in each cohort; how well the glucocorticoid score alone separates the groups |
| Fig. 3 | **Simulation:** each model's AUC against the oracle by scenario, and power at the cohort sizes (Section 4.11) |
| Fig. 4 | **Main result:** paired AUROC differences vs W2, M2, M7 and M5, per cohort and pooled |
| Fig. 5 | Model advantage vs signal strength (IFN-high → IFN-low) |
| Fig. 6 | Pathway attribution, and dispersion vs network-specific signal, read against the simulation's reading guide |
| Fig. 7 | LIONESS-partial ≈ quadratic form, checked on real data (Appendix A) |
| Table 1 | Cohorts, counts after the go check, covariates |
| Supplement | Full simulation results (all settings, RNA-seq-like check); closed-form derivation and unit tests; sensitivity analyses (all sexes, glucocorticoid genes excluded, IFN pathways included, references, λ); RA contrast |

---

## 6. Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Too few IFN-low patients or controls | Moderate | Go/no-go check (Section 0); fall back to a single cohort or the RA contrast |
| Treatment confounding explains the separation | **High** | Glucocorticoid-score baseline (Hu 2018 signature, checked against recorded steroid use), glucocorticoid-gene exclusion, on- vs off-steroid comparisons in GSE224705 and GSE65391. Report honestly; this is a finding in itself. |
| Sex or batch confounding | Moderate | Female-only primary analysis (sex inferred from Y-chromosome genes), all-sex sensitivity; batch-confounded cohorts ineligible |
| Leakage through the IFN-low definition | Certain if ignored | Cutoff fitted inside folds; same filter for both groups |
| Asymmetric reference creates artificial separation | Certain if ignored | Mixed-class training reference; identical computation for all samples |
| The distance-from-health baseline matches LIONESS | Moderate–high | Built in as M7. "Dispersion, not co-regulation" is a valid conclusion. |
| The design can't tell the mechanisms apart at our sample sizes | Moderate | The simulation study (Section 4.11) measures this before the real-data models are run. If so, Aim 3 is reported as descriptive only. |
| Noisy partial-correlation edges | Moderate | Shrinkage; pathway size cap of 150; Pearson arm |
| Cross-platform cohorts can't be pooled at the model level | Certain | Within-cohort analysis plus meta-analysis of paired differences |
| LIONESS-partial correctness questioned (no precedent) | Moderate | Appendix A derivation; numerical checks; unit tests; independent review of the derivation ⚠ D11 |
| Limited clinical relevance of SLE vs HC | Certain | Frame as biology plus method; RA contrast as secondary |

---

## 7. Timeline (proposed, about 10–11 months after the go decision)

Paper 1 should be underway first; paper 2 reuses its pipeline and overlap catalog.

| Month | Work |
|---|---|
| 0 (2 weeks) | **Go/no-go check** (Section 0); register the analysis plan on OSF |
| 1–2 | Data harmonization; sex inference; confounding audit; closed-form LIONESS-partial with unit tests |
| 2–3 | Feature and topology functions; baselines M0–M7; leak-free WGCNA comparators (W1, W2) |
| 3–4 | Simulation study (Section 4.11) on the finished pipeline; write the reading guide |
| 4–7 | Nested CV in eligible cohorts; pooling; permutation checks |
| 7–8 | Interpretation (dispersion vs network); sensitivity analyses; positive control; RA contrast |
| 8–10 | Writing; code release |
| 10–11 | Submission |

**Target journal (D10, decided): *Briefings in Bioinformatics*,** with a method-centred framing.
- It suits either outcome: a LIONESS advantage, or a mechanistic explanation of why there isn't one. P-SSN (Huang 2021), the closest precedent, was published there.
- Paper 1 targets the same journal, so paper 2's stated contribution is the method and the quadratic result, not the leakage-free design.
- To do: confirm article type and length limits in the author guidelines.

**Fallback: *Statistics in Medicine*,** if the SLE result is null and the theory carries the paper (precedent: Gregorich 2024). That version would need these additions:
- **An extended simulation study:** Section 4.11 expanded with more network structures and non-Gaussian data, checked against the predictions of Appendix A, and promoted to the main evidence.
- **Appendix A extended to the shrinkage estimator**, with a bound on the first-order error. The shrinkage case is currently supported only numerically.
- **A formal statement that training and test features are exchangeable:** leave-one-out (training) and add-one-in (test) are the same operation against a reference of N−1 vs N samples.
- **The SLE analysis cut down to an illustration.**

Other fallbacks: *NAR Genomics and Bioinformatics*, *BMC Bioinformatics*. A rheumatology journal only if there's a clear, unconfounded positive result.

---

## 8. Open decisions

| # | Decision | Options | Recommendation |
|---|---|---|---|
| **D1** | Go criterion | Thresholds for IFN-low and control counts; number of cohorts | ≥ 2 cohorts with ≥ 40 IFN-low and ≥ 40 controls each, and no batch confounding |
| **D2** | Primary cohorts and analysis structure | GSE88884 + GSE319130 (cross-platform) / add Illumina cohorts | Decide after the go check; within-cohort CV plus meta-analysis either way |
| **D3** | IFN gene set | Standard IFN panel / Catalina IFN module / Reactome IFN-α/β | A standard panel (simple, widely used); others as sensitivity |
| **D4** | Exclude IFN pathways from features? | IFN-score genes only / also IFN Reactome subtree | Exclude IFN-score genes (primary); report with the IFN subtree removed as well |
| **D5** | How to handle confounding | Design-based controls (this plan) / covariate-adjusted models / none | Design-based. This overrides the earlier "no covariates" default, for the reasons in Section 4.2. Your call. **Sex: decided, female-only primary with an all-sex sensitivity analysis. Glucocorticoid panel: decided, the Hu 2018 signature (64 genes; take the list from the paper's supplement).** |
| **D6** | Pathway set and MSigDB version | Immune subtree / all Reactome; version | Immune subtree primary, all Reactome secondary; latest MSigDB release, pinned |
| **D7** | Add cell-composition proxies to the partial-correlation conditioning set? | No / yes (sensitivity) | Sensitivity only |
| **D8** | LIONESS reference | Analysis set (IFN-low + controls) / also IFN-high SLE | Analysis set primary |
| **D9** | Topology metric set | See Section 4.5 | Pre-specified subset |
| ~~D10~~ | Framing and venue | — | **Decided: method-centred, *Briefings in Bioinformatics*.** Fallback: *Statistics in Medicine*, with the additions listed in Section 7. |
| **D11** | Independent check of the partial-correlation derivation | Internal / statistician colleague | Ask a colleague before submission |
| **D12** | Simulation scope (Section 4.11) | Tier 1 only / Tiers 1 and 2; replicate counts | Both tiers, with Tier 2 at 1 × 5 outer CV; set the replicate counts after a timing run |

---

## 9. References (PMIDs verified 2026-10-01 unless noted)

- Banchereau R et al. Personalized immunomonitoring uncovers molecular networks that stratify lupus patients. *Cell* 2016. PMID 27040498.
- Catalina MD et al. Gene expression analysis delineates the potential roles of multiple interferons in SLE. *Commun Biol* 2019. PMID 31044165.
- Chiche L et al. Modular transcriptional repertoire analyses of adults with SLE. *Arthritis Rheumatol* 2014. PMID 24644022.
- Costantini G, Perugini M. Generalization of clustering coefficients to signed correlation networks. *PLoS One* 2014. PMID 24586367.
- Deschildre J et al. Evaluation of single-sample network inference methods for precision oncology. *NPJ Syst Biol Appl* 2024. PMID 38360881.
- Figgett WA et al. Machine learning applied to whole-blood RNA-sequencing data uncovers distinct subsets of patients with SLE. *Clin Transl Immunology* 2019. PMID 31921420.
- Gregorich M et al. Flexible parametrization of graph-theoretical features from individual-specific networks. *Stat Med* 2024. PMID 38664934.
- Grimes T, Datta S. SeqNet: an R package for generating gene-gene networks and simulating RNA-seq data. *J Stat Softw* 2021. PMID 34321962.
- Guthridge JM et al. Adults with systemic lupus exhibit distinct molecular phenotypes. *EClinicalMedicine* 2020. PMID 32154507.
- Hoffman RW et al. Gene expression and pharmacodynamic changes in 1,760 SLE patients (ILLUMINATE). *Arthritis Rheumatol* 2017. PMID 27723281.
- Huang Y et al. Disease characterization using a partial correlation-based sample-specific network. *Brief Bioinform* 2021. PMID 32422654.
- Hu Y et al. Development of a molecular signature to monitor pharmacodynamic responses mediated by in vivo administration of glucocorticoids. *Arthritis Rheumatol* 2018. PMID 29534336.
- Hubbard EL et al. Analysis of transcriptomic features reveals molecular endotypes of SLE. *Genome Med* 2023. PMID 37845772.
- Hung T et al. The Ro60 autoantigen binds endogenous retroelements and regulates inflammatory gene expression. *Science* 2015. PMID 26382853.
- Kuijjer ML et al. Estimating sample-specific regulatory networks. *iScience* 2019. PMID 30981959.
- Kuijjer ML, De Marzio M, Glass K. Challenges and opportunities in single-sample network modeling. *bioRxiv* 2026, preprint. PMID 41867852.
- Leyva A, Niazi MKK. *PLoS One* 2026. PMID 42743314.
- Liu X et al. Personalized characterization of diseases using sample-specific networks. *NAR* 2016. PMID 27596597.
- López-Domínguez R et al. Immune and molecular landscape behind non-response to mycophenolate mofetil and azathioprine in lupus nephritis therapy. *Res Sq* 2024, preprint. PMID 38260685. GEO-linked publication for GSE224705.
- Masson HO et al. XIST expression and hypermethylation of the X chromosome in males with systemic lupus erythematosus. *Front Immunol* 2026. PMID 42039161. GEO-linked publication for GSE319130.
- Panwar B et al. Multi-cell type gene coexpression network analysis reveals coordinated interferon response. *Genome Res* 2021. PMID 33674349.
- Schäfer J, Strimmer K. A shrinkage approach to large-scale covariance matrix estimation. *Stat Appl Genet Mol Biol* 2005. PMID 16646851.
- Yin L et al. Sample-specific network analysis identifies gene co-expression patterns of immunotherapy response. *iScience* 2025. PMID 40740488.
- Zhang B, Horvath S. A general framework for weighted gene co-expression network analysis. *Stat Appl Genet Mol Biol* 2005. PMID 16646834.

---

## Appendix A. LIONESS partial correlation is approximately quadratic in expression

**Notation.**
- Σ is the reference covariance (divisor N) of the pathway genes, Ω = Σ⁻¹ the precision matrix, and ρ_ij = −Ω_ij / √(Ω_ii Ω_jj) the partial correlation.
- d is patient q's deviation from the reference mean, and a = 1/(N−1).

**Derivation.**
- Removing patient q gives Σ₋q ≈ Σ − a(d dᵀ − Σ), so Ω₋q ≈ Ω + a(u uᵀ − Ω), where u = Ω d.
- Let ũ_i = u_i / √Ω_ii. Then Var(ũ_i) = 1 and Cov(ũ_i, ũ_j) = −ρ_ij. Here ũ_i is gene i's residual after regressing it on the other pathway genes, divided by its SD.
- Perturbing ρ gives ρ − ρ₋q ≈ a[ũ_i ũ_j + ρ_ij(ũ_i² + ũ_j²)/2].
- LIONESS is e_q = ρ + (N−1)(ρ − ρ₋q), which gives:

> **e_q ≈ ũ_i ũ_j + ρ_ij (1 + (ũ_i² + ũ_j²)/2)**

Check: the expected value of e_q is −ρ + 2ρ = ρ, as LIONESS requires.

**Numerical check** (exact leave-one-out LIONESS on partial correlation vs the first-order form):

| Setting | cor(exact, first-order) | cor(exact, ũ_i ũ_j), strong edges |
|---|---|---|
| N = 100, G = 12, unshrunk | 0.9984 | 0.84 |
| N = 300, G = 12, unshrunk | 0.9998 | 0.94 |
| N = 100, G = 40, unshrunk | 0.9930 (max \|diff\| 7.0) | 0.86 |
| N = 100, G = 40, shrinkage λ = 0.2 | 0.9953 | 0.96 |
| N = 300, G = 12, shrinkage λ = 0.2 | 0.9989 | 0.98 |

The shrinkage rows plug the shrunk covariance into the formula. That's supported empirically, not derived.

**The Pearson analogue** (consistent with Liu 2016, Eq. 4): e_q ≈ z_i z_j + r_ij (1 − (z_i² + z_j²)/2). Correlation with exact LIONESS: 0.9987 at N = 50 and 1.0000 at N = 200.

**Implications for this study:**
- Each LIONESS-partial feature is a fixed quadratic form in the patient's conditional residuals ũ.
- The squared terms respond to **dispersion** (distance from the reference), which motivates baseline M7.
- The product terms respond to **joint deviations** of gene pairs, which motivates baseline M5.
- A genuine network effect is what remains when L2 beats both.

