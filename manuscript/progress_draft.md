# Progress draft

**Status:** skeleton only. Sections are added one at a time when instructed.

## Title

[Not yet written]

## Key Points

[Not yet written]

## Abstract

[Not yet written]

## 1. Introduction

### 1.1 Interferon-low lupus

[Not yet written]

### 1.2 Single-sample networks

[Not yet written]

### 1.3 What is missing

[Not yet written]

### 1.4 IFN-low lupus as a stress test

[Not yet written]

### 1.5 Contributions

[Not yet written]

## 2. Methods

### 2.1 Data sources and cohort eligibility

This study used publicly available whole-blood gene-expression cohorts of systemic lupus erythematosus (SLE) that included either healthy controls (HC) or patients with a comparison disease (Table 1). Two cohorts were considered as candidate primary cohorts because of their size. The first, GSE319130, was profiled by RNA sequencing and contains 720 SLE patients and 84 HC, of whom 679 and 77, respectively, were female [V1]. The second, GSE88884, was profiled on the Affymetrix Human Transcriptome Array 2.0 and contains baseline samples from 1,760 SLE patients enrolled in the ILLUMINATE trials, together with 60 HC [V2].

Four further cohorts were selected because each supports a specific comparison or check. GSE110169 contains 82 SLE patients, 84 patients with rheumatoid arthritis (RA) and 77 HC processed together, with recorded glucocorticoid use, and therefore allows IFN-low SLE to be compared with another autoimmune disease [V3]. GSE65391 follows 158 children with SLE across repeated visits with disease-activity scores, alongside 46 HC, and allows changes in interferon status over time to be described [V4]. GSE99967 includes SLE patients with and without lupus nephritis (LN) as well as HC, and supports the comparison of renal and non-renal disease [V5]. GSE224705 records prednisone dose and was used to examine the effect of treatment [V6]. The PRECISESADS cohort, which covers seven systemic autoimmune diseases and controls under controlled access, will be added if access is granted [V7].

Because several public series reuse the same samples, duplicated series were excluded to prevent the same individuals from appearing in both training and test data. GSE72326 duplicates GSE49454 [V8], and GSE45291, GSE121239 and GSE224705 share patients and controls [V9]; at most one of these series was therefore used in any single analysis. Within each cohort, one sample was used per patient, taken from the first visit in longitudinal cohorts, and technical replicates were averaged.

Before the analysis was registered, and before any model was fitted to the outcome, a feasibility (go/no-go) check was carried out. For each cohort, IFN-low patients and controls were counted by inferred sex (Section 2.4), and batch, age, ancestry and medication were tabulated by group. A cohort qualified as a primary cohort if it contained at least 80 female IFN-low patients and 60 female controls, and if batch was not confounded with group, that is, if patients and controls had not been processed in separate batches. With these numbers, the 95% confidence interval for an area under the curve (AUC) of 0.70 has a half-width of about ±0.085 by the Hanley–McNeil method [V10]. Cohorts with at least 25 patients per group, which gives a half-width of about ±0.15, qualified as replication cohorts and were reported descriptively.

---

*Working note (not part of the manuscript; delete when every row is checked).*

**Links to verify before this section is final**

| Tag | What to check | Link |
|---|---|---|
| V1 | GSE319130: platform, 720 SLE / 84 HC, 679 / 77 female, whole blood | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130 |
| V2 | GSE88884: HTA 2.0, 1,760 SLE baseline, 60 HC, ILLUMINATE trials | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE88884 |
| V3 | GSE110169: 82 SLE / 84 RA / 77 HC, glucocorticoid use recorded | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169 |
| V4 | GSE65391: 158 paediatric SLE, repeated visits, 46 HC, SLEDAI recorded | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391 |
| V5 | GSE99967: numbers of LN, non-LN SLE and HC; whole blood or not *(unverified)* | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE99967 |
| V6 | GSE224705: prednisone dose recorded; sample counts | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705 |
| V7 | PRECISESADS: access route (ELIXIR Luxembourg) and data type | https://www.precisesads.eu/ |
| V8 | GSE72326 duplicates GSE49454 (compare sample titles) | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72326 and https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE49454 |
| V9 | GSE45291, GSE121239 and GSE224705 share patients (compare sample titles) | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE45291, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121239 |
| V10 | Hanley–McNeil half-widths: recomputed, ±0.086 (80 vs 60) and ±0.146 (25 vs 25) | Checked; cite Hanley & McNeil (1982) |

### 2.2 Pre-processing and harmonization

[Not yet written]

### 2.3 IFN score and IFN-low definition

[Not yet written]

### 2.4 Confounding control

[Not yet written]

### 2.5 Pathways

[Not yet written]

### 2.6 Theory

[Not yet written]

### 2.7 LIONESS partial-correlation estimation

[Not yet written]

### 2.8 Topology features

[Not yet written]

### 2.9 Baseline and comparator models

All models below are fitted inside the training folds only, use the same cross-validation splits, and are scored in the same way, so that any difference between them comes from the features and not from the set-up.

**Baselines (simple explanations to rule out first)**

- **M0a. IFN score within the IFN-low range.** The IFN score itself, used as the only feature, in patients who fall below the IFN-low cutoff. It asks whether leftover interferon signal below the cutoff is enough to separate IFN-low patients from healthy controls.
- **M0b. Glucocorticoid-response score.** A score built from the Hu 2018 glucocorticoid-response genes. It asks whether the separation is just a sign of steroid treatment.

**Expression-based comparators (no network)**

- **M1. Elastic net or random forest on all genes.** The standard approach of putting every gene into one model.
- **M2. Pathway-by-pathway expression, then stacked.** One model per pathway on gene expression, combined in the same way as the LIONESS models. It asks whether any gain comes from the pathways themselves rather than from the networks.
- **M3. Pathway scores and non-linear models.** One activity score per pathway (singscore, mean z-score or first principal component), the classic pathway-activity approach; and non-linear models (boosting, kernel support vector machine) on pathway expression, which capture general gene interactions without using network structure.
- **M7. Distance from health per pathway.** For each pathway, how far a patient lies from the healthy centre (sum of squared standardized expression, Σũ², or Mahalanobis distance). It asks whether patients simply scatter further from the healthy centre.

**Established network comparators**

- **W1. Published WGCNA and hub-gene pipeline, without leakage.** A typical weighted gene co-expression network analysis (WGCNA) pipeline as used in the lupus literature, with every step fitted inside the training folds.
- **W2. WGCNA module eigengenes fitted inside each training fold.** Module summary scores (eigengenes) built only from training data. This is the main established-network comparator.

**LIONESS models**

- **L1. LIONESS partial-correlation edges.** Edge-level features from the single-sample partial-correlation networks.
- **L2. LIONESS partial-correlation topology.** Network summary features (node strength, clustering and others; Section 2.8). This is the main model.
- **L2-P. Pearson LIONESS topology.** The same as L2 but with Pearson correlation in place of partial correlation. It asks whether partial correlation matters.
- **L3. L2 plus M2.** Network topology together with pathway expression. It asks whether networks add information beyond expression.

### 2.10 Aggregation across pathways and contrasts

[Not yet written]

### 2.11 Validation and statistical inference

[Not yet written]

### 2.12 Population-level tests

[Not yet written]

### 2.13 Simulation study

[Not yet written]

### 2.14 Software, reproducibility, pre-registration and availability

[Not yet written]

## 3. Results

[Not yet written]

## 4. Discussion

[Not yet written]

## 5. Conclusion

[Not yet written]

## References

[Not yet written]

## Supplementary material

[Not yet written]
