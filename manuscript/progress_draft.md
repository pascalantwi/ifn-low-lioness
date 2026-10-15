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

[Not yet written]

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
