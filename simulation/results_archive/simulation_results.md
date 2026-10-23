# Simulation results (archived)

This file holds the simulation results, the simulation details and the simulation code that were removed from `manuscript/progress_draft.md` on request. They are kept here unchanged, to be added back to the manuscript later. Section, table, figure and equation numbers are those of the manuscript at the time of removal.

<a id="sec-3"></a>

## 3. Results

<a id="sec-3-1"></a>

### 3.1 Simulated data

Because the real GSE319130 controls could not be obtained in the computing environment used for this analysis, all results in this section come from the generative design of [Section 2.13](#sec-2-13) applied to a synthetic stand-in: a pathway of $`G`$ genes whose gene-specific variation followed a sparse partial-correlation network, with normal margins, and whose expression also followed a shared IFN activity factor (equation 31). The resampling design, which requires the real controls, was not run. Pathways of 10, 20, 30, 50 and 60 genes were simulated; the 60-gene setting exceeds the 50-gene limit of [Section 2.5](#sec-2-5) and is reported as a stress test. Each setting was repeated 50 times. The following simplifications of the planned protocol were made to keep the computation feasible and are listed in full in [Supplementary Section S1](#supp-s1): LIONESS used 5 rather than 20 balanced reference subsets; the population-level tests used 199 rather than 10,000 permutations; the standard error of AUC differences was estimated with the corrected variance of Nadeau and Bengio rather than the method of Bates et al.; cross-validation used one repeat of 5 folds; the IFN cutoff was computed once per dataset; each dataset contained a single pathway, so no aggregation across pathways was needed; and models W1, M0b and M0c, which require real annotations, were not run. M1 used the elastic net only, M3 was run as three models (M3-score, M3-boost and M3-SVM), and W2 used a WGCNA-like module construction. Exploratory network features were computed for partial-correlation networks only. Scenarios S5–S7 used fixed effect sizes because their best possible classifier was not computed.

Model performance is reported both as the AUC and as the relative AUC,

```math
r = \frac{\mathrm{AUC} - 0.5}{\mathrm{AUC}^{*} - 0.5} \qquad\qquad (32)
```

where $`\mathrm{AUC}^{*}`$ is the AUC of the best possible classifier for that scenario; $`r = 1`$ means that a model captured all of the available signal and $`r = 0`$ that it captured none. The calibrated effect sizes reached $`\mathrm{AUC}^{*}`$ values between 0.697 and 0.701 for a target of 0.70.

In the synthetic data, the correlations between genes in 5,000 simulated control samples agreed with the target correlations of the model (correlation 0.996; largest absolute difference 0.048; [Figure 1](#figure-1)a). Under the IFN activity model, 98% of simulated controls and 37% of simulated SLE patients had IFN scores at or below the cutoff $`\theta`$ ([Figure 1](#figure-1)b).

<a id="figure-1"></a>

![Figure 1](figures/fig1_synthetic_check.png)

**Figure 1.** Check of the synthetic stand-in data. (a) Correlations between the 20 genes of a simulated pathway in 5,000 simulated controls against the target correlations of the model; the dashed line is the line of equality. (b) Distribution of the IFN score (equation 2) in simulated controls and SLE patients, with the cutoff $`\theta`$ (equation 3).

<a id="sec-3-2"></a>

### 3.2 Classification performance

[Table 1](#table-1) gives the AUC of every model in each scenario for pathways of 20 genes, and [Figure 2](#figure-2) gives the relative AUC for all pathway sizes. In the null scenario S0, the mean AUC of every model lay between 0.48 and 0.51 at all pathway sizes. In the level scenario S1 at 20 genes, the highest AUCs were obtained by M5 (0.62), M1 (0.62) and M2 (0.62); the network-only models L1, L2 and L2-P had AUCs of 0.50, 0.50 and 0.49. In the spread scenario S2, M4 had the highest AUC (0.68; $`r`$ = 0.89), followed by M3-SVM (0.60) and L2-P (0.58). In the subgroup scenario S3, no model exceeded an AUC of 0.55 at 20 genes; at 10 genes, the highest AUCs were L2-S (0.59), L2-S-P (0.59), M6 (0.58). In the rewiring scenario S4 at 20 genes, the highest AUCs were obtained by L2-P (0.57), L3-P (0.56), M6 (0.56); L2 reached 0.54 and M5 0.51. At 10 genes in S4, L2-P reached 0.62 ($`r`$ = 0.60), the highest AUC of all models in that setting. The relative AUC of the best model in each scenario did not exceed 0.93 in any setting ([Figure 2](#figure-2)). The variation of the AUC between simulated datasets is shown in [Figure 3](#figure-3); at 20 genes in S4, the AUC of individual datasets ranged from 0.41 to 0.69 for L2-P and from 0.34 to 0.64 for M5.

<a id="table-1"></a>

**Table 1. AUC of each model by scenario, pathways of 20 genes.**

| Model | S0 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| M0a | 0.48 (0.01) | 0.49 (0.01) [-0.03] | 0.48 (0.01) [-0.10] | 0.48 (0.01) [-0.11] | 0.49 (0.01) [-0.05] |
| M1 | 0.50 (0.01) | 0.62 (0.01) [0.62] | 0.50 (0.01) [0.01] | 0.50 (0.01) [-0.01] | 0.51 (0.01) [0.05] |
| M2 | 0.50 (0.01) | 0.62 (0.01) [0.61] | 0.51 (0.01) [0.03] | 0.50 (0.01) [-0.01] | 0.51 (0.01) [0.05] |
| M3-score | 0.48 (0.01) | 0.53 (0.01) [0.15] | 0.48 (0.01) [-0.12] | 0.49 (0.01) [-0.05] | 0.49 (0.01) [-0.05] |
| M3-boost | 0.50 (0.01) | 0.56 (0.01) [0.30] | 0.55 (0.01) [0.25] | 0.49 (0.01) [-0.05] | 0.52 (0.01) [0.12] |
| M3-SVM | 0.49 (0.01) | 0.58 (0.01) [0.40] | 0.60 (0.01) [0.52] | 0.50 (0.01) [-0.01] | 0.54 (0.01) [0.21] |
| M4 | 0.50 (0.01) | 0.52 (0.01) [0.08] | 0.68 (0.01) [0.89] | 0.55 (0.01) [0.23] | 0.49 (0.01) [-0.05] |
| M5 | 0.50 (0.01) | 0.62 (0.01) [0.62] | 0.51 (0.01) [0.03] | 0.50 (0.01) [-0.01] | 0.51 (0.01) [0.05] |
| M6 | 0.50 (0.01) | 0.56 (0.01) [0.30] | 0.54 (0.01) [0.21] | 0.53 (0.01) [0.13] | 0.56 (0.01) [0.31] |
| W2 | 0.49 (0.01) | 0.51 (0.01) [0.06] | 0.49 (0.01) [-0.03] | 0.51 (0.01) [0.05] | 0.50 (0.01) [-0.00] |
| L1 | 0.51 (0.01) | 0.50 (0.01) [-0.02] | 0.49 (0.01) [-0.03] | 0.52 (0.01) [0.10] | 0.53 (0.01) [0.17] |
| L2 | 0.51 (0.01) | 0.50 (0.01) [0.01] | 0.56 (0.01) [0.29] | 0.52 (0.01) [0.11] | 0.54 (0.01) [0.18] |
| L2-P | 0.51 (0.01) | 0.49 (0.01) [-0.03] | 0.58 (0.01) [0.38] | 0.51 (0.01) [0.05] | 0.57 (0.01) [0.35] |
| L2-S | 0.51 (0.01) | 0.51 (0.01) [0.03] | 0.55 (0.01) [0.27] | 0.53 (0.01) [0.16] | 0.53 (0.01) [0.16] |
| L2-S-P | 0.50 (0.01) | 0.50 (0.01) [-0.01] | 0.55 (0.01) [0.27] | 0.51 (0.01) [0.06] | 0.55 (0.01) [0.26] |
| L3 | 0.51 (0.01) | 0.55 (0.01) [0.26] | 0.56 (0.01) [0.28] | 0.52 (0.01) [0.09] | 0.54 (0.01) [0.18] |
| L3-P | 0.50 (0.01) | 0.57 (0.01) [0.34] | 0.57 (0.01) [0.34] | 0.50 (0.01) [0.01] | 0.56 (0.01) [0.32] |
| L-explo | 0.51 (0.01) | 0.50 (0.01) [0.02] | 0.56 (0.01) [0.31] | 0.50 (0.01) [-0.00] | 0.51 (0.01) [0.03] |
| L-sec+explo | 0.51 (0.01) | 0.51 (0.01) [0.04] | 0.56 (0.01) [0.28] | 0.52 (0.01) [0.10] | 0.53 (0.01) [0.17] |

Values are mean AUC (Monte Carlo standard error) [relative AUC, $`r`$, equation 32] over 50 simulated datasets; 90 patients and 77 controls; best possible AUC 0.70 in S1–S4.

The corresponding tables for pathways of 10, 30, 50 and 60 genes are given in [Supplementary Table S4](#table-s4) to [Supplementary Table S7](#table-s7).

<a id="figure-2"></a>

![Figure 2](figures/fig2_performance_map.png)

**Figure 2.** Performance map. Each cell gives the relative AUC $`r`$ (equation 32) of one model (rows, grouped by family) in one scenario and pathway size (columns); the first block gives the AUC in the null scenario S0. Darker cells indicate a larger share of the available signal captured. The 60-gene columns are a stress test beyond the 50-gene limit of [Section 2.5](#sec-2-5).

<a id="figure-3"></a>

![Figure 3](figures/fig3_auc_distribution.png)

**Figure 3.** AUC of six models in each of the 50 simulated datasets, pathways of 20 genes, in the null scenario S0 and the rewiring scenario S4. Each point is one dataset, the shaded area shows the distribution and the horizontal bar the median; the dashed line marks the AUC of the best possible classifier.

<a id="sec-3-3"></a>

### 3.3 Effect of pathway size

[Figure 4](#figure-4) shows the AUC of six models as the pathway size increased from 10 to 60 genes, with the planted effect calibrated to the same best possible AUC (0.70) at every size. In S1, the AUC of M2 decreased from 0.66 at 10 genes to 0.58 at 50 genes and 0.56 at 60 genes. In S2, the AUC of M4 decreased from 0.69 to 0.66 at 50 genes and 0.65 at 60 genes, and that of L2-P from 0.61 to 0.56. In S4, the AUC of L2-P decreased from 0.62 at 10 genes to 0.57, 0.55, 0.53 and 0.52 at 20, 30, 50 and 60 genes, and that of M6 from 0.59 to 0.53. In S3, all six models had AUCs between 0.49 and 0.55 at 20 genes or more.

<a id="figure-4"></a>

![Figure 4](figures/fig4_pathway_size.png)

**Figure 4.** AUC of six models against the number of genes in the pathway, for scenarios S1–S4. Shaded bands are 95% Monte Carlo intervals over 50 simulated datasets; the dashed line is the AUC of the best possible classifier (0.70) and the dotted line an AUC of 0.5. The grey area marks the 60-gene stress test.

<a id="sec-3-4"></a>

### 3.4 Network feature sets and association measures

[Table 2](#table-2) compares the network feature sets of [Section 2.8](#sec-2-8). At 20 genes, the primary features (L2) and the secondary features (L2-S) had similar AUCs in every scenario (S2: 0.56 and 0.55; S3: 0.52 and 0.53; S4: 0.54 and 0.53). The exploratory features alone had AUCs of 0.56 in S2 and 0.51 in S4, and adding them to the secondary features changed the AUC by at most 0.01. At 60 genes, all four feature sets had AUCs between 0.50 and 0.51 in S3 and S4.

[Table 3](#table-3) compares partial-correlation and Pearson LIONESS. In S4, Pearson LIONESS had higher AUCs than partial-correlation LIONESS for all three model pairs at 10 genes (L2-P 0.62 versus L2 0.56; L3-P 0.60 versus L3 0.56) and at 20 genes (L2-P 0.57 versus L2 0.54). In S3 at 10 genes, the partial-correlation models had AUCs of 0.57 (L2) and 0.59 (L2-S), and the Pearson models 0.56 (L2-P) and 0.59 (L2-S-P). In S1, L3 and L3-P had AUCs of 0.55 and 0.57 at 20 genes, compared with 0.62 for M5.

<a id="table-2"></a>

**Table 2. AUC of the network feature sets (partial-correlation networks), pathways of 20 and 60 genes.**

| Feature set (model) | Genes | S0 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|---|
| Primary (L2) | 20 | 0.51 (0.01) | 0.50 (0.01) | 0.56 (0.01) | 0.52 (0.01) | 0.54 (0.01) |
| Primary (L2) | 60 | 0.50 (0.01) | 0.50 (0.01) | 0.55 (0.01) | 0.50 (0.01) | 0.51 (0.01) |
| Secondary (L2-S) | 20 | 0.51 (0.01) | 0.51 (0.01) | 0.55 (0.01) | 0.53 (0.01) | 0.53 (0.01) |
| Secondary (L2-S) | 60 | 0.50 (0.01) | 0.50 (0.01) | 0.54 (0.01) | 0.50 (0.01) | 0.50 (0.01) |
| Exploratory only | 20 | 0.51 (0.01) | 0.50 (0.01) | 0.56 (0.01) | 0.50 (0.01) | 0.51 (0.01) |
| Exploratory only | 60 | 0.50 (0.01) | 0.51 (0.01) | 0.54 (0.01) | 0.50 (0.01) | 0.50 (0.01) |
| Secondary + exploratory | 20 | 0.51 (0.01) | 0.51 (0.01) | 0.56 (0.01) | 0.52 (0.01) | 0.53 (0.01) |
| Secondary + exploratory | 60 | 0.50 (0.01) | 0.51 (0.01) | 0.54 (0.01) | 0.50 (0.01) | 0.50 (0.01) |

Values are mean AUC (Monte Carlo standard error) over 50 datasets.

<a id="table-3"></a>

**Table 3. AUC with partial-correlation and Pearson LIONESS, pathways of 10 and 20 genes.**

| Model pair | Genes | S0 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|---|
| L2 / L2-P | 10 | 0.51 / 0.51 | 0.49 / 0.49 | 0.60 / 0.61 | 0.57 / 0.56 | 0.56 / 0.62 |
| L2 / L2-P | 20 | 0.51 / 0.51 | 0.50 / 0.49 | 0.56 / 0.58 | 0.52 / 0.51 | 0.54 / 0.57 |
| L2-S / L2-S-P | 10 | 0.51 / 0.50 | 0.49 / 0.49 | 0.59 / 0.59 | 0.59 / 0.59 | 0.56 / 0.59 |
| L2-S / L2-S-P | 20 | 0.51 / 0.50 | 0.51 / 0.50 | 0.55 / 0.55 | 0.53 / 0.51 | 0.53 / 0.55 |
| L3 / L3-P | 10 | 0.51 / 0.51 | 0.61 / 0.63 | 0.59 / 0.59 | 0.56 / 0.55 | 0.56 / 0.60 |
| L3 / L3-P | 20 | 0.51 / 0.50 | 0.55 / 0.57 | 0.56 / 0.57 | 0.52 / 0.50 | 0.54 / 0.56 |

Values are mean AUC over 50 datasets (partial-correlation / Pearson); Monte Carlo standard errors were at most 0.01.

<a id="sec-3-5"></a>

### 3.5 Similarity between models

[Figure 5](#figure-5) places each model on a map according to its AUC across scenarios S1–S4 and the five pathway sizes. The first two components accounted for 54% and 30% of the variation in AUC between models. The network-only models L2, L2-P, L2-S, L2-S-P, L-explo and L-sec+explo formed one group; M1, M2 and M5 formed a second group; M0a, L1, W2 and M3-score lay together in the upper part of the map; M4 and M3-SVM lay in the lower part; and L3, L3-P, M6 and M3-boost lay near the centre.

<a id="figure-5"></a>

![Figure 5](figures/fig5_model_map.png)

**Figure 5.** Model similarity map. Principal component analysis of the mean AUC of each model in scenarios S1–S4 at the five pathway sizes; models close together had similar performance profiles. Colours indicate model families.

<a id="sec-3-6"></a>

### 3.6 False positives and confidence-interval coverage

[Table 4](#table-4) reports, for the null scenario S0, how often each model comparison of [Section 2.11](#sec-2-11) produced a confidence interval entirely above zero and how often the interval contained zero. Across the six comparisons and five pathway sizes, the false-positive rate ranged from 0% to 14% and the coverage from 80% to 100%. The highest false-positive rate, 14%, and the lowest coverage, 80%, occurred for L3 versus M5 at 10 genes.

<a id="table-4"></a>

**Table 4. False-positive rate and confidence-interval coverage of the model comparisons in the null scenario S0.**

| Comparison | 10 genes | 20 genes | 30 genes | 50 genes | 60 genes |
|---|---|---|---|---|---|
| L3 vs M5 | 14% / 80% | 8% / 86% | 2% / 98% | 0% / 100% | 2% / 94% |
| L3-P vs M5 | 8% / 88% | 6% / 92% | 2% / 96% | 2% / 90% | 10% / 86% |
| L2 vs M6 | 4% / 90% | 4% / 88% | 6% / 92% | 6% / 88% | 4% / 92% |
| L2-P vs M6 | 6% / 90% | 2% / 96% | 4% / 94% | 2% / 88% | 8% / 88% |
| L2 vs M4 | 6% / 92% | 2% / 96% | 6% / 90% | 0% / 98% | 0% / 98% |
| L2-P vs M4 | 4% / 92% | 8% / 86% | 4% / 92% | 4% / 96% | 4% / 94% |

Each cell gives the false-positive rate (percentage of 50 datasets in which the 95% confidence interval of equation 25 lay entirely above 0) / the coverage (percentage in which the interval contained 0, the true difference in S0). Monte Carlo standard errors were at most 6 percentage points.

<a id="sec-3-7"></a>

### 3.7 Population-level tests and subgroup check

[Table 5](#table-5) and [Figure 6](#figure-6) give the rejection rates of the three layers of [Section 2.12](#sec-2-12). In S0, the rejection rates at 20 genes were 4% (level), 4% (spread) and 6% and 6% (structure, partial and Pearson), and across all sizes they ranged from 0% to 8%. The level test rejected in 100%, 76%, 66%, 48% and 42% of datasets in S1 at 10, 20, 30, 50 and 60 genes. The spread test rejected in at least 98% of datasets in S2 at every size. In S4, the Pearson structure test rejected in 76%, 40%, 40%, 20% and 16% of datasets at the five sizes, and the partial-correlation structure test in 14%, 12%, 8%, 4% and 2%. In S3, the partial-correlation structure test rejected in 38% of datasets at 10 genes and in 6% to 8% at 20 genes or more. The subgroup check flagged 0% of S3 datasets at every size and 4% or fewer of datasets in any scenario. In the positive-control scenario S7, with expression adjusted for the IFN score, the rejection rates of all four tests were at most 12%.

<a id="table-5"></a>

**Table 5. Rejection rates of the population-level tests and flag rate of the subgroup check, pathways of 20 genes.**

| Scenario | Level | Spread | Structure (partial) | Structure (Pearson) | Subgroup flag |
|---|---|---|---|---|---|
| S0 null | 4% | 4% | 6% | 6% | 0% |
| S1 level | 76% | 4% | 6% | 10% | 0% |
| S2 spread | 2% | 100% | 0% | 2% | 0% |
| S3 subgroups | 8% | 14% | 6% | 8% | 0% |
| S4 rewiring | 2% | 8% | 12% | 40% | 0% |
| S7 positive control | 0% | 6% | 0% | 0% | 0% |

Percentage of 50 datasets with p < 0.05 (199 permutations); expression adjusted for the IFN score. Results for 50 genes are shown in Figure 6 and for all sizes in Supplementary Table S8.

<a id="figure-6"></a>

![Figure 6](figures/fig6_detection_fingerprint.png)

**Figure 6.** Detection fingerprint of the population-level tests. Each circle gives the percentage of 50 simulated datasets in which a test (columns) rejected at p < 0.05 in a scenario (rows), for pathways of 20 and 50 genes; circle area is proportional to the percentage.

<a id="sec-3-8"></a>

### 3.8 Treatment, selection and positive-control scenarios

[Table 6](#table-6) and [Figure 7](#figure-7) show the scenarios in which patients and controls differed only through treatment (S5) or through IFN activity before selection (S6), analysed with and without the safeguards of [Section 2.3](#sec-2-3). In S5 without safeguards, L3 had a mean AUC of 0.71 at 20 genes and between 0.70 and 0.75 across sizes, and the confidence interval for L3 versus M5 lay above zero in 60% of datasets at 20 genes and 90% at 60 genes. Conditioning on the IFN score alone gave similar values (L3 AUC 0.72; L3 above M5 in 52%). Excluding treated patients reduced the L3 AUC to 0.50 and the proportion of datasets with L3 above M5 to 4%; with both safeguards these values were 0.51 and 2%. The level test rejected in 62% of S5 datasets without safeguards and in 18% with conditioning.

In S6 without safeguards, M0a had a mean AUC of 0.64 and L3 of 0.54 at 20 genes, and the confidence interval for L3 versus M5 lay above zero in 0% to 6% of datasets across sizes. The Pearson structure test rejected in 6%, 24% and 28% of datasets at 20, 50 and 60 genes without safeguards, and in 6%, 4% and 6% with conditioning on the IFN score. The level test rejected in 50% of datasets at 20 genes without safeguards and 2% with conditioning; matching alone gave 46%.

In the positive-control scenario S7, M0a, M2, M5, M6, L3 and L3-P had mean AUCs between 0.98 and 1.00 at every pathway size, M4 between 0.76 and 0.82, and the network-only models L2 and L2-P between 0.50 and 0.51.

<a id="table-6"></a>

**Table 6. Treatment (S5) and selection (S6) scenarios with and without safeguards, pathways of 20 genes.**

| Scenario | Safeguard | Patients / controls | AUC M0a | AUC M5 | AUC L3 | AUC L3-P | Level test | Structure (Pearson) | L3 > M5 |
|---|---|---|---|---|---|---|---|---|---|
| S5 | None | 90 / 77 | 0.65 | 0.59 | 0.71 | 0.72 | 62% | 12% | 60% |
| S5 | IFN-score conditioning | 90 / 77 | 0.65 | 0.59 | 0.72 | 0.72 | 18% | 4% | 52% |
| S5 | Exclusion (S5) / matching (S6) | 45 / 77 | 0.50 | 0.50 | 0.50 | 0.51 | 4% | 2% | 4% |
| S5 | Both | 45 / 77 | 0.48 | 0.51 | 0.51 | 0.51 | 6% | 2% | 2% |
| S6 | None | 90 / 77 | 0.64 | 0.58 | 0.54 | 0.55 | 50% | 6% | 2% |
| S6 | IFN-score conditioning | 90 / 77 | 0.64 | 0.58 | 0.54 | 0.55 | 2% | 6% | 2% |
| S6 | Exclusion (S5) / matching (S6) | 77 / 77 | 0.64 | 0.58 | 0.54 | 0.56 | 46% | 4% | 4% |
| S6 | Both | 77 / 77 | 0.63 | 0.58 | 0.54 | 0.55 | 4% | 4% | 6% |

AUCs are means over 50 datasets; test columns give the percentage of datasets with p < 0.05; the last column gives the percentage in which the 95% confidence interval for the AUC difference between L3 and M5 lay entirely above 0. Neither scenario contains a difference other than treatment (S5) or IFN activity (S6). Results for all pathway sizes are shown in Figure 7.

<a id="figure-7"></a>

![Figure 7](figures/fig7_safeguards.png)

**Figure 7.** Effect of the safeguards in the treatment (S5, top) and selection (S6, bottom) scenarios across pathway sizes. Columns show the AUC of L3, the proportion of datasets in which L3 was significantly better than M5, and the rejection rates of the Pearson structure test and the level test. Dotted lines mark an AUC of 0.5 or a rate of 5%; the grey area marks the 60-gene stress test.

<a id="sec-3-9"></a>

### 3.9 Power and smallest detectable difference

[Table 7](#table-7) and [Figure 8](#figure-8) report the primary comparison of [Section 2.11](#sec-2-11) at 20 genes. The smallest detectable difference in AUC, defined as

```math
\mathrm{MDD} = (z_{0.975} + z_{0.80})\; \mathrm{median}\big(\widehat{\mathrm{SE}}(\Delta)\big) = 2.80\; \mathrm{median}\big(\widehat{\mathrm{SE}}(\Delta)\big) \qquad\qquad (33)
```

where $`z_{0.975}`$ and $`z_{0.80}`$ are standard normal quantiles and the median is taken over simulated datasets, ranged from 0.14 to 0.20 with 90 patients and 77 controls and from 0.20 to 0.27 with 40 per group. In S4, the power of L3 versus M5 was 0%, 12% and 24% for best possible AUCs of 0.60, 0.70 and 0.80, and that of L3-P versus M5 was 4%, 18% and 46%. In S2 at a best possible AUC of 0.80, the power was 56% for L3 and 58% for L3-P. In S1, the mean difference between L3 and M5 was negative at every best possible AUC (-0.037, -0.075 and -0.110).

<a id="table-7"></a>

**Table 7. Primary comparison (L3 and L3-P versus M5): observed AUC difference, power and smallest detectable difference, pathways of 20 genes.**

| Scenario | Best possible AUC | Patients / controls | Δ, L3 vs M5 | Power | MDD | Δ, L3-P vs M5 | Power | MDD |
|---|---|---|---|---|---|---|---|---|
| S0 | – | 90 / 77 | -0.008 | 10% | 0.18 | -0.005 | 2% | 0.17 |
| S0 | – | 90 / 77 | +0.010 | 8% | 0.16 | +0.005 | 6% | 0.18 |
| S0 | – | 40 / 40 | +0.012 | 6% | 0.25 | +0.003 | 6% | 0.22 |
| S1 | 0.6 | 90 / 77 | -0.037 | 0% | 0.19 | -0.030 | 0% | 0.17 |
| S1 | 0.7 | 90 / 77 | -0.075 | 0% | 0.16 | -0.061 | 0% | 0.16 |
| S1 | 0.8 | 90 / 77 | -0.110 | 0% | 0.14 | -0.086 | 0% | 0.14 |
| S1 | 0.7 | 40 / 40 | -0.013 | 2% | 0.20 | -0.029 | 0% | 0.22 |
| S2 | 0.6 | 90 / 77 | +0.047 | 18% | 0.18 | +0.035 | 14% | 0.16 |
| S2 | 0.7 | 90 / 77 | +0.047 | 12% | 0.20 | +0.059 | 24% | 0.16 |
| S2 | 0.8 | 90 / 77 | +0.142 | 56% | 0.18 | +0.162 | 58% | 0.18 |
| S2 | 0.7 | 40 / 40 | +0.054 | 14% | 0.26 | +0.051 | 14% | 0.23 |
| S3 | 0.6 | 90 / 77 | +0.014 | 6% | 0.19 | +0.016 | 12% | 0.17 |
| S3 | 0.7 | 90 / 77 | +0.018 | 8% | 0.20 | +0.000 | 6% | 0.17 |
| S3 | 0.8 | 90 / 77 | +0.064 | 20% | 0.19 | +0.069 | 24% | 0.19 |
| S3 | 0.7 | 40 / 40 | +0.012 | 12% | 0.25 | +0.027 | 8% | 0.21 |
| S4 | 0.6 | 90 / 77 | -0.008 | 0% | 0.19 | -0.001 | 4% | 0.18 |
| S4 | 0.7 | 90 / 77 | +0.024 | 12% | 0.16 | +0.053 | 18% | 0.14 |
| S4 | 0.8 | 90 / 77 | +0.087 | 24% | 0.19 | +0.128 | 46% | 0.19 |
| S4 | 0.7 | 40 / 40 | +0.029 | 8% | 0.27 | +0.039 | 6% | 0.22 |

Δ is the mean paired AUC difference (equation 24) over 50 datasets; power is the percentage of datasets in which the 95% confidence interval lay entirely above 0; MDD is the smallest detectable difference, 2.80 times the median standard error of Δ.

<a id="figure-8"></a>

![Figure 8](figures/fig8_power.png)

**Figure 8.** Power of the primary comparison against the AUC of the best possible classifier, for the subgroup (S3) and rewiring (S4) scenarios, pathways of 20 genes. Lines show 90 patients versus 77 controls and diamonds 40 per group; the dashed line marks 80% power.

<a id="sec-3-10"></a>

### 3.10 Agreement with the first-order formula

[Figure 9](#figure-9) compares the exact LIONESS edges (equation 6) with the first-order approximation of equation (9) for 30 samples of a simulated control set of 167 samples. With shrinkage ($`\lambda`$ = 0.2), the correlation between exact and approximate edges was 0.9998, 0.9997, 0.9993, 0.9993 and 0.9989 for 10, 20, 30, 50 and 60 genes, and the median absolute difference was 0.010, 0.021, 0.034, 0.060 and 0.065, against a standard deviation of the exact edges of 0.67 to 0.78. Without shrinkage (equation 8), the correlations were 0.9998 to 0.9958 and the median absolute differences 0.014 to 0.199. At 60 genes, the approximate edges were smaller in absolute value than the exact edges for the largest edges ([Figure 9](#figure-9)b); the 95th percentile of the absolute difference was 0.42 with shrinkage and 1.26 without.

<a id="figure-9"></a>

![Figure 9](figures/fig9_first_order.png)

**Figure 9.** Exact LIONESS edges (equation 6) against the first-order approximation (equation 9) with shrinkage intensity $`\lambda`$ = 0.2, for pathways of (a) 20 and (b) 60 genes. Each point is one edge of one sample; the dashed line is the line of equality.



# Supplementary material (simulation)

<a id="supp-s1"></a>

### Supplementary Section S1. Simulation details

**Resampling design.** The female healthy controls of [GSE319130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130) were randomly divided into two groups of about 38 samples, labelled pseudo-patients and pseudo-controls, and the known signal of each scenario was added to the pseudo-patients only. This design keeps the exact noise, skewness and correlation of real blood data.

**How the scenarios were generated.** In S1, a constant was added to the mean of 20% of the genes of a sub-pathway. In S2, the deviations of all genes from the patient mean were multiplied by a common factor greater than 1, which increases spread without changing correlations. In S3, half of the pseudo-patients were shifted upwards and half downwards on 20% of the genes, so that the average was unchanged. In S4, 10% of the gene pairs had their partial correlations reversed in sign, removed or created, giving a new correlation matrix $`\mathbf{R}_{\mathrm{R}}`$, adjusted where necessary to remain a valid correlation matrix. In the generative design, pseudo-patients were drawn from equation (30) with $`\mathbf{R}_{\mathrm{R}}`$ in place of $`\hat{\mathbf{R}}`$. In the resampling design, they were transformed to the new structure by

```math
\mathbf{x}^{\mathrm{R}} = \boldsymbol{\mu} + \mathbf{D}_{\sigma}\, \mathbf{R}_{\mathrm{R}}^{1/2}\, \hat{\mathbf{R}}^{-1/2}\, \mathbf{D}_{\sigma}^{-1} \big(\mathbf{x} - \boldsymbol{\mu}\big) \qquad\qquad (\mathrm{S}1)
```

where $`\mathbf{x}`$ is a pseudo-patient's expression vector, $`\boldsymbol{\mu}`$ the vector of gene means, $`\mathbf{D}_{\sigma}`$ the diagonal matrix of gene standard deviations, and the powers $`1/2`$ and $`-1/2`$ the symmetric matrix square root and its inverse; this changes the correlations exactly while keeping the means and variances. In S5, simulated patients with high IFN activity had the expression of the interferon genes reduced by a common factor, which lowered their IFN score below the cutoff while leaving the correlations of the IFN-high state in place. In S6, patients and controls differed only in the distribution of $`f`$ in equation (31).

**Interferon activity model.** In equation (31), the loadings $`l_g`$ were estimated from the first principal component of the interferon genes in all SLE patients of the primary cohort, where IFN activity varies widely, and the distribution of $`f`$ was chosen so that the simulated IFN scores of patients and controls matched those observed. The four IFN-score genes were generated from the same model, the IFN score was computed by equation (2), and the cutoff $`\theta`$ of equation (3) was estimated and applied inside each training fold, so that the simulated IFN-low group was selected in the same way as the real one.

**Outcomes.** For every scenario, the recorded outcomes were the AUC of each model, also expressed relative to the AUC of the best possible classifier; the rejection rates of the hypothesis tests and of the three population-level layers; how often the subgroup check flagged each scenario; the false-positive rates in scenarios S0 and S6, which should not exceed 5%; the coverage of the 95% confidence intervals of equation (25); and the smallest AUC difference detectable with 80% power at each sample size. Scenarios S5 and S6 were analysed with and without the safeguards of [Section 2.3](#sec-2-3). The results were used to write a reading guide linking each pattern of results to the kind of difference that causes it, which was fixed before any model was fitted to the real outcome data.

**Implementation used for the results in Section 3.** Because the real controls of GSE319130 could not be obtained in the computing environment used, the simulation results in [Section 3](#sec-3) were produced with a synthetic stand-in for the generative design: for each pathway size $`G`$, the gene-specific variation followed a sparse partial-correlation network (a chain of partial correlations of 0.3 plus $`G/2`$ random partial correlations of ±0.25), with normal margins; the loadings $`l_g`$ in equation (31) were drawn from a uniform distribution between 0.2 and 0.5; IFN activity $`f`$ had mean 0 and standard deviation 1 in controls and mean 3 in IFN-high patients; and each IFN-score gene was generated as $`0.9 f`$ plus independent noise with standard deviation 0.3. S5 contained equal numbers of untreated patients and treated IFN-high patients whose deviations were multiplied by 0.3; S6 drew patients from a population in which 75% were IFN-high; and in S7 controls were not filtered by the cutoff. Each setting was repeated 50 times. To keep the computation feasible, LIONESS used 5 balanced reference subsets, the population-level tests used 199 permutations of the group labels on expression adjusted for the IFN score, the standard error of AUC differences used the corrected variance of Nadeau and Bengio, cross-validation used one repeat of 5 folds, and the IFN cutoff and the matching on IFN score were computed once per dataset rather than within each fold. Models W1, M0b and M0c were not run because they require real annotations; M1 used the elastic net; M3 was run as a pathway-score model, gradient boosting and a kernel support vector machine; W2 used modules formed by hierarchical clustering of the adjacency $`|\mathrm{cor}|^6`$ with first principal components as eigengenes; and when a group in a training fold had fewer samples than genes, M6 used class covariance matrices shrunk towards the identity. The code is given in [Supplementary Section S2](#supp-s2).

**Repeats and computation.** Each setting was repeated 200 times when a single sub-pathway was analysed and 100 times when the full pipeline over all sub-pathways was run, giving Monte Carlo standard errors of at most 0.035 and 0.05 for estimated proportions; these are reported with every estimate. The generative design was run at both sample sizes, and the resampling design at the largest size the controls allow. The full-pipeline runs used one repeat of 5 outer folds instead of ten, with all other steps unchanged. LIONESS used $`B = 20`$ balanced reference subsets and both association measures, as in the real analysis.

**Checking the simulated data.** For each sub-pathway, simulated data without added signal were compared with the real controls in four respects: the mean and variance of each gene, the distribution of all pairwise correlations, the distribution of the LIONESS edges, and, for equation (31), the distribution of the IFN score and the proportion of patients below the cutoff. The simulated and real distributions are shown overlaid.

**Agreement with the theory.** The exact LIONESS edges were compared with the first-order formulas of [Section 2.6](#sec-2-6) in every scenario.

**Pilot simulation.** A smaller pilot, run while the study was being designed, used multivariate normal data for single pathways of 10, 20 and 30 genes with 20 to 30 repeats per setting. Its results guided the choice of network features ([Section 2.8](#sec-2-8)) and population-level tests ([Section 2.12](#sec-2-12)); its code and results are archived with the analysis code. The full simulation replaces it for all inferences.


<a id="table-s3"></a>

**Supplementary Table S3.** Simulation scenarios.

| Scenario | How the pseudo-patients differ | What it checks |
|---|---|---|
| S0 Null | No difference | False-positive rate of all tests; AUC close to 0.5 |
| S1 Level | Mean shifted in 20% of genes | Level test; whether network features ignore level differences ([Section 2.6](#sec-2-6)) |
| S2 Spread | Deviations multiplied by a factor above 1 | Spread test; distance-from-health baseline (M4) |
| S3 Subgroups | Half shifted up, half down, on 20% of genes | Structure test; subgroup check; secondary features (L2-S) |
| S4 Rewiring | Partial correlations changed in 10% of gene pairs | Structure test; primary network models (L2, L2-P, L3, L3-P) |
| S5 Treatment | IFN-high patients with IFN genes reduced by treatment | Whether treated patients create false network differences; treatment exclusion |
| S6 Selection | Only the distribution of IFN activity differs | Size of the selection effect; IFN-score conditioning and matching |
| S7 Positive control | IFN-high patients versus controls | Whether contrast C1 detects a known difference |

<a id="table-s4"></a>

**Supplementary Table S4. AUC of each model by scenario, pathways of 10 genes.**

| Model | S0 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| M0a | 0.49 (0.01) | 0.49 (0.01) [-0.05] | 0.50 (0.01) [-0.02] | 0.49 (0.01) [-0.06] | 0.49 (0.01) [-0.03] |
| M1 | 0.50 (0.01) | 0.68 (0.01) [0.89] | 0.50 (0.01) [-0.00] | 0.49 (0.01) [-0.07] | 0.50 (0.01) [-0.01] |
| M2 | 0.49 (0.01) | 0.66 (0.01) [0.81] | 0.50 (0.01) [-0.01] | 0.49 (0.01) [-0.07] | 0.50 (0.01) [-0.00] |
| M3-score | 0.50 (0.01) | 0.53 (0.01) [0.16] | 0.50 (0.01) [-0.01] | 0.49 (0.01) [-0.06] | 0.51 (0.01) [0.03] |
| M3-boost | 0.50 (0.01) | 0.60 (0.01) [0.51] | 0.58 (0.01) [0.39] | 0.54 (0.01) [0.20] | 0.52 (0.01) [0.11] |
| M3-SVM | 0.51 (0.01) | 0.63 (0.01) [0.65] | 0.62 (0.01) [0.58] | 0.55 (0.01) [0.24] | 0.57 (0.01) [0.37] |
| M4 | 0.49 (0.01) | 0.52 (0.01) [0.09] | 0.69 (0.00) [0.93] | 0.58 (0.01) [0.41] | 0.47 (0.01) [-0.17] |
| M5 | 0.50 (0.01) | 0.68 (0.01) [0.88] | 0.50 (0.01) [-0.01] | 0.49 (0.01) [-0.07] | 0.50 (0.01) [-0.02] |
| M6 | 0.51 (0.01) | 0.62 (0.01) [0.58] | 0.58 (0.01) [0.41] | 0.58 (0.01) [0.42] | 0.59 (0.01) [0.44] |
| W2 | 0.50 (0.01) | 0.54 (0.01) [0.20] | 0.49 (0.01) [-0.04] | 0.50 (0.01) [-0.01] | 0.50 (0.01) [0.02] |
| L1 | 0.50 (0.01) | 0.50 (0.01) [-0.00] | 0.49 (0.01) [-0.07] | 0.56 (0.01) [0.29] | 0.56 (0.01) [0.31] |
| L2 | 0.51 (0.01) | 0.49 (0.01) [-0.03] | 0.60 (0.01) [0.49] | 0.57 (0.01) [0.37] | 0.56 (0.01) [0.32] |
| L2-P | 0.51 (0.01) | 0.49 (0.01) [-0.05] | 0.61 (0.01) [0.56] | 0.56 (0.01) [0.31] | 0.62 (0.01) [0.60] |
| L2-S | 0.51 (0.01) | 0.49 (0.01) [-0.03] | 0.59 (0.01) [0.44] | 0.59 (0.01) [0.48] | 0.56 (0.01) [0.30] |
| L2-S-P | 0.50 (0.01) | 0.49 (0.01) [-0.07] | 0.59 (0.01) [0.46] | 0.59 (0.01) [0.43] | 0.59 (0.01) [0.46] |
| L3 | 0.51 (0.01) | 0.61 (0.01) [0.55] | 0.59 (0.01) [0.44] | 0.56 (0.01) [0.30] | 0.56 (0.01) [0.31] |
| L3-P | 0.51 (0.01) | 0.63 (0.01) [0.63] | 0.59 (0.01) [0.47] | 0.55 (0.01) [0.24] | 0.60 (0.01) [0.52] |
| L-explo | 0.50 (0.01) | 0.51 (0.01) [0.03] | 0.61 (0.01) [0.53] | 0.54 (0.01) [0.21] | 0.52 (0.01) [0.11] |
| L-sec+explo | 0.51 (0.01) | 0.51 (0.01) [0.04] | 0.58 (0.01) [0.41] | 0.58 (0.01) [0.39] | 0.54 (0.01) [0.21] |

Values are mean AUC (Monte Carlo standard error) [relative AUC, $`r`$, equation 32] over 50 simulated datasets; 90 patients and 77 controls; best possible AUC 0.70 in S1–S4.

<a id="table-s5"></a>

**Supplementary Table S5. AUC of each model by scenario, pathways of 30 genes.**

| Model | S0 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| M0a | 0.50 (0.01) | 0.50 (0.01) [-0.01] | 0.48 (0.01) [-0.08] | 0.50 (0.01) [0.02] | 0.48 (0.01) [-0.10] |
| M1 | 0.51 (0.01) | 0.61 (0.01) [0.56] | 0.50 (0.01) [0.00] | 0.50 (0.01) [-0.01] | 0.47 (0.01) [-0.15] |
| M2 | 0.50 (0.01) | 0.60 (0.01) [0.50] | 0.50 (0.01) [0.01] | 0.50 (0.01) [0.01] | 0.47 (0.01) [-0.15] |
| M3-score | 0.49 (0.01) | 0.51 (0.01) [0.03] | 0.49 (0.01) [-0.04] | 0.51 (0.01) [0.04] | 0.48 (0.01) [-0.08] |
| M3-boost | 0.49 (0.01) | 0.55 (0.01) [0.23] | 0.53 (0.01) [0.16] | 0.51 (0.01) [0.03] | 0.49 (0.01) [-0.03] |
| M3-SVM | 0.50 (0.01) | 0.56 (0.01) [0.32] | 0.60 (0.01) [0.49] | 0.51 (0.01) [0.04] | 0.50 (0.01) [-0.01] |
| M4 | 0.50 (0.01) | 0.52 (0.01) [0.08] | 0.67 (0.01) [0.85] | 0.53 (0.01) [0.16] | 0.47 (0.01) [-0.13] |
| M5 | 0.51 (0.01) | 0.61 (0.01) [0.56] | 0.50 (0.01) [0.01] | 0.50 (0.01) [0.01] | 0.47 (0.01) [-0.15] |
| M6 | 0.50 (0.01) | 0.54 (0.01) [0.20] | 0.53 (0.01) [0.15] | 0.51 (0.01) [0.07] | 0.52 (0.01) [0.12] |
| W2 | 0.50 (0.01) | 0.52 (0.01) [0.09] | 0.50 (0.01) [0.02] | 0.50 (0.01) [0.01] | 0.49 (0.01) [-0.07] |
| L1 | 0.49 (0.01) | 0.50 (0.01) [-0.02] | 0.50 (0.01) [-0.01] | 0.51 (0.01) [0.06] | 0.51 (0.01) [0.07] |
| L2 | 0.49 (0.01) | 0.49 (0.01) [-0.06] | 0.54 (0.01) [0.22] | 0.52 (0.01) [0.12] | 0.51 (0.01) [0.07] |
| L2-P | 0.49 (0.01) | 0.50 (0.01) [0.01] | 0.56 (0.01) [0.30] | 0.51 (0.01) [0.03] | 0.55 (0.01) [0.27] |
| L2-S | 0.50 (0.01) | 0.48 (0.01) [-0.08] | 0.54 (0.01) [0.21] | 0.52 (0.01) [0.11] | 0.52 (0.01) [0.08] |
| L2-S-P | 0.49 (0.01) | 0.50 (0.01) [-0.00] | 0.55 (0.01) [0.26] | 0.50 (0.01) [-0.00] | 0.54 (0.01) [0.23] |
| L3 | 0.50 (0.01) | 0.54 (0.01) [0.18] | 0.54 (0.01) [0.22] | 0.53 (0.01) [0.13] | 0.50 (0.01) [0.02] |
| L3-P | 0.50 (0.01) | 0.56 (0.01) [0.31] | 0.56 (0.01) [0.28] | 0.51 (0.01) [0.05] | 0.53 (0.01) [0.14] |
| L-explo | 0.50 (0.01) | 0.49 (0.01) [-0.05] | 0.56 (0.01) [0.28] | 0.50 (0.01) [0.02] | 0.52 (0.01) [0.08] |
| L-sec+explo | 0.50 (0.01) | 0.48 (0.01) [-0.08] | 0.56 (0.01) [0.28] | 0.51 (0.01) [0.07] | 0.52 (0.01) [0.08] |

Values are mean AUC (Monte Carlo standard error) [relative AUC, $`r`$, equation 32] over 50 simulated datasets; 90 patients and 77 controls; best possible AUC 0.70 in S1–S4.

<a id="table-s6"></a>

**Supplementary Table S6. AUC of each model by scenario, pathways of 50 genes.**

| Model | S0 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| M0a | 0.49 (0.01) | 0.49 (0.01) [-0.07] | 0.48 (0.01) [-0.11] | 0.49 (0.01) [-0.05] | 0.48 (0.01) [-0.09] |
| M1 | 0.51 (0.01) | 0.59 (0.01) [0.44] | 0.49 (0.01) [-0.07] | 0.49 (0.01) [-0.04] | 0.50 (0.01) [-0.00] |
| M2 | 0.51 (0.01) | 0.58 (0.01) [0.42] | 0.49 (0.01) [-0.07] | 0.49 (0.01) [-0.03] | 0.50 (0.01) [0.00] |
| M3-score | 0.49 (0.01) | 0.51 (0.01) [0.03] | 0.48 (0.01) [-0.08] | 0.50 (0.01) [-0.00] | 0.49 (0.01) [-0.06] |
| M3-boost | 0.50 (0.01) | 0.53 (0.01) [0.13] | 0.51 (0.01) [0.04] | 0.50 (0.01) [-0.01] | 0.50 (0.01) [-0.01] |
| M3-SVM | 0.51 (0.01) | 0.55 (0.01) [0.23] | 0.56 (0.01) [0.28] | 0.50 (0.01) [-0.02] | 0.51 (0.01) [0.05] |
| M4 | 0.49 (0.01) | 0.51 (0.01) [0.05] | 0.66 (0.01) [0.78] | 0.53 (0.01) [0.16] | 0.50 (0.01) [-0.00] |
| M5 | 0.51 (0.01) | 0.59 (0.01) [0.45] | 0.49 (0.01) [-0.07] | 0.49 (0.01) [-0.04] | 0.50 (0.01) [0.01] |
| M6 | 0.51 (0.01) | 0.52 (0.01) [0.11] | 0.51 (0.01) [0.06] | 0.52 (0.01) [0.10] | 0.52 (0.01) [0.09] |
| W2 | 0.50 (0.01) | 0.51 (0.01) [0.06] | 0.48 (0.01) [-0.12] | 0.50 (0.01) [-0.01] | 0.49 (0.01) [-0.03] |
| L1 | 0.51 (0.01) | 0.49 (0.01) [-0.06] | 0.50 (0.01) [0.02] | 0.52 (0.01) [0.10] | 0.50 (0.01) [-0.02] |
| L2 | 0.51 (0.01) | 0.50 (0.01) [-0.01] | 0.54 (0.01) [0.21] | 0.52 (0.01) [0.10] | 0.49 (0.01) [-0.03] |
| L2-P | 0.50 (0.01) | 0.49 (0.01) [-0.03] | 0.55 (0.01) [0.27] | 0.51 (0.01) [0.04] | 0.53 (0.01) [0.16] |
| L2-S | 0.51 (0.01) | 0.51 (0.01) [0.04] | 0.54 (0.01) [0.18] | 0.51 (0.01) [0.04] | 0.49 (0.01) [-0.03] |
| L2-S-P | 0.49 (0.01) | 0.50 (0.01) [-0.01] | 0.55 (0.01) [0.23] | 0.50 (0.01) [0.00] | 0.52 (0.01) [0.08] |
| L3 | 0.51 (0.01) | 0.55 (0.01) [0.23] | 0.53 (0.01) [0.16] | 0.51 (0.01) [0.04] | 0.50 (0.01) [-0.02] |
| L3-P | 0.51 (0.01) | 0.54 (0.01) [0.22] | 0.54 (0.01) [0.21] | 0.50 (0.01) [0.01] | 0.52 (0.01) [0.11] |
| L-explo | 0.50 (0.01) | 0.50 (0.01) [0.01] | 0.55 (0.01) [0.23] | 0.49 (0.01) [-0.03] | 0.49 (0.01) [-0.07] |
| L-sec+explo | 0.51 (0.01) | 0.50 (0.01) [0.02] | 0.54 (0.01) [0.22] | 0.50 (0.01) [-0.01] | 0.49 (0.01) [-0.07] |

Values are mean AUC (Monte Carlo standard error) [relative AUC, $`r`$, equation 32] over 50 simulated datasets; 90 patients and 77 controls; best possible AUC 0.70 in S1–S4.

<a id="table-s7"></a>

**Supplementary Table S7. AUC of each model by scenario, pathways of 60 genes (stress test).**

| Model | S0 | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| M0a | 0.49 (0.01) | 0.49 (0.01) [-0.06] | 0.49 (0.01) [-0.05] | 0.49 (0.01) [-0.07] | 0.49 (0.01) [-0.04] |
| M1 | 0.50 (0.01) | 0.56 (0.01) [0.32] | 0.49 (0.01) [-0.07] | 0.50 (0.01) [0.00] | 0.52 (0.01) [0.11] |
| M2 | 0.50 (0.01) | 0.56 (0.01) [0.31] | 0.49 (0.01) [-0.06] | 0.50 (0.01) [0.00] | 0.52 (0.01) [0.11] |
| M3-score | 0.50 (0.01) | 0.49 (0.01) [-0.05] | 0.49 (0.01) [-0.03] | 0.49 (0.01) [-0.03] | 0.49 (0.01) [-0.04] |
| M3-boost | 0.50 (0.01) | 0.52 (0.01) [0.11] | 0.51 (0.01) [0.06] | 0.51 (0.01) [0.04] | 0.52 (0.01) [0.08] |
| M3-SVM | 0.50 (0.01) | 0.53 (0.01) [0.16] | 0.56 (0.01) [0.29] | 0.51 (0.01) [0.05] | 0.53 (0.01) [0.15] |
| M4 | 0.50 (0.01) | 0.51 (0.01) [0.05] | 0.65 (0.01) [0.75] | 0.52 (0.01) [0.10] | 0.51 (0.01) [0.05] |
| M5 | 0.50 (0.01) | 0.57 (0.01) [0.34] | 0.49 (0.01) [-0.06] | 0.50 (0.01) [0.01] | 0.52 (0.01) [0.10] |
| M6 | 0.50 (0.01) | 0.52 (0.01) [0.12] | 0.51 (0.01) [0.07] | 0.51 (0.01) [0.03] | 0.53 (0.01) [0.16] |
| W2 | 0.50 (0.01) | 0.50 (0.01) [0.01] | 0.50 (0.01) [0.01] | 0.49 (0.01) [-0.05] | 0.51 (0.01) [0.03] |
| L1 | 0.51 (0.01) | 0.50 (0.01) [-0.00] | 0.50 (0.01) [-0.01] | 0.49 (0.01) [-0.04] | 0.51 (0.01) [0.04] |
| L2 | 0.50 (0.01) | 0.50 (0.01) [0.00] | 0.55 (0.01) [0.23] | 0.50 (0.01) [-0.02] | 0.51 (0.01) [0.05] |
| L2-P | 0.51 (0.01) | 0.51 (0.01) [0.04] | 0.56 (0.01) [0.28] | 0.51 (0.01) [0.07] | 0.52 (0.01) [0.10] |
| L2-S | 0.50 (0.01) | 0.50 (0.01) [0.02] | 0.54 (0.01) [0.20] | 0.50 (0.01) [0.02] | 0.50 (0.01) [-0.01] |
| L2-S-P | 0.51 (0.01) | 0.51 (0.01) [0.06] | 0.55 (0.01) [0.23] | 0.51 (0.01) [0.03] | 0.51 (0.01) [0.07] |
| L3 | 0.50 (0.01) | 0.54 (0.01) [0.21] | 0.53 (0.01) [0.14] | 0.50 (0.01) [-0.00] | 0.52 (0.01) [0.12] |
| L3-P | 0.51 (0.01) | 0.55 (0.01) [0.25] | 0.54 (0.01) [0.20] | 0.51 (0.01) [0.06] | 0.53 (0.01) [0.15] |
| L-explo | 0.50 (0.01) | 0.51 (0.01) [0.04] | 0.54 (0.01) [0.19] | 0.50 (0.01) [0.01] | 0.50 (0.01) [0.02] |
| L-sec+explo | 0.50 (0.01) | 0.51 (0.01) [0.04] | 0.54 (0.01) [0.22] | 0.50 (0.01) [0.00] | 0.50 (0.01) [0.01] |

Values are mean AUC (Monte Carlo standard error) [relative AUC, $`r`$, equation 32] over 50 simulated datasets; 90 patients and 77 controls; best possible AUC 0.70 in S1–S4.

<a id="table-s8"></a>

**Supplementary Table S8. Rejection rates of the population-level tests and flag rate of the subgroup check, all pathway sizes.**

| Scenario | Genes | Level | Spread | Structure (partial) | Structure (Pearson) | Subgroup flag |
|---|---|---|---|---|---|---|
| S0 null | 10 | 4% | 4% | 6% | 6% | 0% |
| S0 null | 20 | 4% | 4% | 6% | 6% | 0% |
| S0 null | 30 | 8% | 4% | 6% | 2% | 0% |
| S0 null | 50 | 8% | 4% | 4% | 4% | 4% |
| S0 null | 60 | 0% | 4% | 2% | 2% | 0% |
| S1 level | 10 | 100% | 2% | 2% | 4% | 0% |
| S1 level | 20 | 76% | 4% | 6% | 10% | 0% |
| S1 level | 30 | 66% | 2% | 2% | 4% | 0% |
| S1 level | 50 | 48% | 2% | 2% | 6% | 0% |
| S1 level | 60 | 42% | 4% | 2% | 8% | 0% |
| S2 spread | 10 | 4% | 100% | 6% | 2% | 0% |
| S2 spread | 20 | 2% | 100% | 0% | 2% | 0% |
| S2 spread | 30 | 6% | 100% | 4% | 4% | 0% |
| S2 spread | 50 | 4% | 98% | 6% | 2% | 0% |
| S2 spread | 60 | 8% | 100% | 2% | 0% | 0% |
| S3 subgroups | 10 | 4% | 30% | 38% | 22% | 0% |
| S3 subgroups | 20 | 8% | 14% | 6% | 8% | 0% |
| S3 subgroups | 30 | 0% | 10% | 6% | 6% | 0% |
| S3 subgroups | 50 | 2% | 10% | 6% | 8% | 0% |
| S3 subgroups | 60 | 8% | 6% | 8% | 2% | 0% |
| S4 rewiring | 10 | 4% | 28% | 14% | 76% | 0% |
| S4 rewiring | 20 | 2% | 8% | 12% | 40% | 0% |
| S4 rewiring | 30 | 0% | 12% | 8% | 40% | 0% |
| S4 rewiring | 50 | 4% | 2% | 4% | 20% | 0% |
| S4 rewiring | 60 | 4% | 6% | 2% | 16% | 0% |
| S7 positive control | 10 | 0% | 0% | 4% | 4% | 0% |
| S7 positive control | 20 | 0% | 6% | 0% | 0% | 0% |
| S7 positive control | 30 | 0% | 8% | 6% | 4% | 0% |
| S7 positive control | 50 | 0% | 0% | 2% | 12% | 0% |
| S7 positive control | 60 | 0% | 6% | 6% | 8% | 0% |

Percentage of 50 datasets with p < 0.05.


<a id="supp-s2"></a>

### Supplementary Section S2. Simulation code

The simulation code is kept as separate script files in [`simulation/code/`](../code/): `simlib.py` (data generation, LIONESS, features, models and tests), `run.py` (runs all settings), `aggregate.py` (summaries), `fig_results.py` and `figs_static.py` (figures).
