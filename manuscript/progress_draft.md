# Progress draft

**Status:** skeleton only. Sections are added one at a time.

## Title

[Not yet written]

## Key Points

[Not yet written]

## Abstract

[Not yet written]

<a id="sec-1"></a>

## 1. Introduction

<a id="sec-1-1"></a>

### 1.1 Interferon-low lupus

[Not yet written]

<a id="sec-1-2"></a>

### 1.2 Single-sample networks

[Not yet written]

<a id="sec-1-3"></a>

### 1.3 What is missing

[Not yet written]

<a id="sec-1-4"></a>

### 1.4 IFN-low lupus as a stress test

[Not yet written]

<a id="sec-1-5"></a>

### 1.5 Contributions

[Not yet written]

<a id="sec-2"></a>

## 2. Methods

<a id="sec-2-1"></a>

### 2.1 Data sources and cohort eligibility

All data were obtained from public whole-blood transcriptomic studies of systemic lupus erythematosus (SLE) deposited in the Gene Expression Omnibus (GEO) [[1]](https://pubmed.ncbi.nlm.nih.gov/23193258/). A study was eligible if it profiled peripheral whole blood, included either healthy controls (HC) or patients with another autoimmune disease, and provided enough sample annotation to infer sex and to separate patients from controls. The cohorts that met these criteria, and the role of each in the analysis, are summarized in [Table 1](#table-1).

[GSE319130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130) served as the primary cohort. It is an RNA-sequencing study of 720 SLE patients and 84 HC, of whom 679 patients and 77 controls are female [[2]](https://pubmed.ncbi.nlm.nih.gov/42039161/), and it is the only cohort expected to have enough female controls to meet the primary-cohort criteria described below. [GSE88884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE88884) was generated on the Affymetrix Human Transcriptome Array 2.0 and contains baseline blood samples from 1,760 SLE patients enrolled in the ILLUMINATE-1 and ILLUMINATE-2 phase III trials of tabalumab [[3]](https://pubmed.ncbi.nlm.nih.gov/27723281/). It contains 60 HC in total, so it could meet the requirement of 60 female controls for a primary cohort only if every control were female and none were removed by the IFN filter ([Section 2.3](#sec-2-3)); GSE88884 was therefore treated as a replication cohort.

Four smaller cohorts were included because each answers a question the primary cohort cannot. [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169) profiled 82 SLE patients, 84 patients with rheumatoid arthritis (RA) and 77 HC in a single study with recorded glucocorticoid use [[4]](https://pubmed.ncbi.nlm.nih.gov/29534336/), which allows IFN-low SLE to be compared with another autoimmune disease rather than only with health. [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) followed 158 children with SLE over repeated visits with disease-activity scores, alongside 46 HC [[5]](https://pubmed.ncbi.nlm.nih.gov/27040498/), and makes it possible to observe whether patients move between IFN-low and IFN-high states over time. [GSE99967](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE99967) includes adult SLE patients with and without active lupus nephritis (LN) as well as HC [[6]](https://pubmed.ncbi.nlm.nih.gov/29742110/), and [GSE224705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705) records the prednisone dose of each patient [[7]](https://pubmed.ncbi.nlm.nih.gov/38260685/). Because these last two cohorts contain fewer than 25 HC, neither was used for comparisons with controls: GSE99967 contributed only a descriptive comparison of patients with and without LN, and GSE224705 contributed only analyses of treatment within patients. The PRECISESADS cohort, which covers seven systemic autoimmune diseases and controls under controlled access [[8]](https://pubmed.ncbi.nlm.nih.gov/?term=Barturen+Integrative+analysis+molecular+stratification+systemic+autoimmune+diseases), was to be included only if access was granted before the analysis was registered.

Public SLE series frequently reuse the same patients, and the same individual appearing in both training and test data would inflate performance. Overlap between series was checked by comparing GEO sample identifiers, sample titles and recorded patient characteristics such as age, sex and visit date. [GSE72326](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72326) duplicates [GSE49454](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE49454) and was not used. [GSE45291](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE45291), [GSE121239](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121239) and GSE224705 share patients and controls; of these three, only GSE224705 was used, because it records prednisone dose. Within each cohort, a single sample was kept per patient, taken from the first visit in longitudinal studies, and technical replicates were averaged.

Whether a cohort could support the primary analysis was decided by a feasibility (go/no-go) check carried out before registration and before any model was fitted to the outcome. For each cohort, IFN-low patients and controls were counted by inferred sex ([Section 2.4](#sec-2-4)), and batch, age, ancestry and medication were tabulated by group. A cohort qualified as a primary cohort if it contained at least 80 female IFN-low patients and 60 female controls, and if batch was not confounded with group, meaning that patients and controls had not been processed in separate batches. Cohorts with at least 25 patients per group qualified as replication cohorts and were reported descriptively. As a rough guide to precision, the 95% confidence interval for an area under the receiver operating characteristic curve (AUC) of 0.70 has a half-width of about ±0.085 at the primary-cohort minimum and about ±0.15 at the replication minimum, based on the standard error of Hanley and McNeil [[9]](https://pubmed.ncbi.nlm.nih.gov/7063747/). These figures assume a single independent test set; the inference used for the actual model comparisons accounts for cross-validation and is described in [Section 2.11](#sec-2-11). Fixing these rules in advance ensured that the choice of cohorts could not be influenced by the results.

<a id="table-1"></a>

**Table 1.** Cohorts and their roles in the analysis. Counts are as reported in GEO and the original publications, before the go/no-go check.

| GEO series | Platform | Population | SLE | Comparator | HC | Role |
|---|---|---|---|---|---|---|
| [GSE319130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130) | RNA-seq | Adults | 720 (679 F) | None | 84 (77 F) | Primary cohort |
| [GSE88884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE88884) | Affymetrix HTA 2.0 | Adults, trial baseline | 1,760 | None | 60 (sex to confirm) | Replication cohort |
| [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169) | Affymetrix | Adults | 82 | 84 RA | 77 | Comparison with RA; treatment checks |
| [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) | Illumina HT-12 | Children, longitudinal | 158 | None | 46 | Changes in IFN state over time; treatment checks |
| [GSE99967](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE99967) | Affymetrix HuGene 2.0 | Adults | LN and non-LN (to confirm) | None | Fewer than 25 (to confirm) | Descriptive LN comparison only |
| [GSE224705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705) | Affymetrix | Adults with LN | 163 | None | About 20, shared (to confirm) | Treatment analyses within patients only |
| PRECISESADS | RNA-seq | Adults, seven diseases | If access granted | If access granted | If access granted | Extension, if access granted |

F, female; HC, healthy controls; HTA, Human Transcriptome Array; LN, lupus nephritis; RA, rheumatoid arthritis.

<a id="sec-2-2"></a>

### 2.2 Pre-processing and harmonization

Each cohort was processed separately, and no batch correction was applied across cohorts. Affymetrix arrays were re-processed from the raw files with robust multi-array averaging (RMA) [[10]](https://pubmed.ncbi.nlm.nih.gov/12925520/) where raw files were available; otherwise, the normalized data supplied by the submitters were used. Illumina BeadChip data (GSE65391) were taken as the submitters' normalized values and log2-transformed where this had not already been done. For RNA-sequencing data, lowly expressed genes were removed with the `filterByExpr` function of edgeR [[11]](https://pubmed.ncbi.nlm.nih.gov/19910308/), [[12]](https://f1000research.com/articles/5-1438). Because this filter can use the group labels, it was applied within each training fold, and the resulting gene list was applied unchanged to the corresponding test fold, so that test samples could not influence which genes were kept. Counts were then normalized by the trimmed mean of M-values (TMM) method [[13]](https://pubmed.ncbi.nlm.nih.gov/20196867/) and converted to log counts per million (log-CPM).

Probes were mapped to gene symbols within each platform. Where several probes mapped to the same gene, the probe with the highest variance in the training fold was kept. Known technical batches within a cohort, such as the two ILLUMINATE trials in GSE88884, were not removed by correction; instead, cross-validation folds were stratified by batch, and batch was included as an adjustment covariate in the population-level tests ([Section 2.12](#sec-2-12)). For analyses that compared cohorts, pathways were restricted to the genes measured in all cohorts involved, and the gene coverage of each pathway is reported. Before network estimation, each gene was winsorized at ±4 standard deviations (SD), using means and SDs estimated in the training fold, to limit the influence of outlying values on the correlation estimates.

<a id="sec-2-3"></a>

### 2.3 IFN score and IFN-low definition

<a id="sec-2-3-1"></a>

#### 2.3.1 IFN score

Interferon (IFN) activity was measured with a score built from four interferon-stimulated genes: IFI27, IFI44, IFI44L and RSAD2. This panel is used in clinical trials of type I IFN blockade to divide patients into IFN-high and IFN-low groups [[14]](https://pubmed.ncbi.nlm.nih.gov/31660791/). To place every sample on the scale of healthy blood, the expression of each gene was first standardized against the healthy controls (HC) of the training fold:

```math
z_{gi} = \frac{x_{gi} - \hat{\mu}_g^{\mathrm{HC}}}{\hat{\sigma}_g^{\mathrm{HC}}} \qquad\qquad (1)
```

Here, $`x_{gi}`$ is the expression of gene $`g`$ in sample $`i`$, and $`\hat{\mu}_g^{\mathrm{HC}}`$ and $`\hat{\sigma}_g^{\mathrm{HC}}`$ are the mean and standard deviation (SD) of that gene among the training-fold controls. The IFN score of sample $`i`$, written $`I_i`$, is the mean of its four standardized values over the set $`\mathcal{G}_{\mathrm{IFN}}`$ of IFN-score genes:

```math
I_i = \frac{1}{4} \sum_{g \in \mathcal{G}_{\mathrm{IFN}}} z_{gi}, \qquad \mathcal{G}_{\mathrm{IFN}} = \lbrace \mathrm{IFI27},\;\mathrm{IFI44},\;\mathrm{IFI44L},\;\mathrm{RSAD2} \rbrace \qquad\qquad (2)
```

<a id="sec-2-3-2"></a>

#### 2.3.2 IFN-low cutoff

A sample was classified as IFN-low when its score lay no more than two SD above the control mean, that is, at or below the cutoff $`\theta`$:

```math
I_i \le \theta, \qquad \theta = \hat{\mu}_I^{\mathrm{HC}} + 2\,\hat{\sigma}_I^{\mathrm{HC}} \qquad\qquad (3)
```

Here, $`\hat{\mu}_I^{\mathrm{HC}}`$ and $`\hat{\sigma}_I^{\mathrm{HC}}`$ are the mean and SD of the score among the training-fold controls. The clinical-trial assay is a qualitative polymerase chain reaction (PCR) test with its own fixed threshold [[14]](https://pubmed.ncbi.nlm.nih.gov/31660791/), which cannot be transferred to microarray or sequencing data. The cutoff was therefore defined relative to the healthy controls of each cohort, a rule that can be applied in the same way on every platform.

Because the cutoff $`\theta`$ depends on the data, it was estimated within each training fold and then applied, without change, to the test samples of that fold. Controls were filtered by the same rule, so that patients and controls entered the analysis on an equal footing; if the score were normally distributed among controls, this would remove about 2.3% of them. The cutoff is estimated from a modest number of controls (about 60 per training fold in the primary cohort), so its value varies between folds; this variation, and the number of patients classified as IFN-low in each fold, are reported. A stricter cutoff, $`\theta = \hat{\mu}_I^{\mathrm{HC}} + \hat{\sigma}_I^{\mathrm{HC}}`$, was examined in a sensitivity analysis.

<a id="sec-2-3-3"></a>

#### 2.3.3 Residual IFN signal

No cutoff can make IFN-low patients identical to controls in IFN activity, since patients who fall just below it may still carry a mildly raised signature. The residual IFN score was therefore kept as a baseline model that every other model had to outperform ([Section 2.9](#sec-2-9)). The network analysis was carried out on the interferon pathway itself ([Section 2.5](#sec-2-5)), and the four genes that make up the IFN score were removed from the network features. Because the other interferon genes move closely with these four, removing them does not by itself prevent the networks from re-measuring IFN activity, so three further safeguards were used. First, the IFN score was added to the set of variables on which each partial correlation was conditioned ([Section 2.7](#sec-2-7)), so that partial-correlation edges describe co-expression beyond the shared IFN signal; for Pearson networks, a sensitivity analysis recomputed the edges after regressing each gene on the IFN score within the training fold. Second, the primary comparison used a reference model that already contains the residual IFN score (M5, [Section 2.9](#sec-2-9)), so a network gain had to go beyond residual IFN activity. Third, a sensitivity analysis removed all genes of the *Interferon alpha/beta signaling* pathway (R-HSA-909733) [[15]](https://doi.org/10.1093/nar/gkab1028), leaving only the remaining interferon genes.

Selecting patients by their IFN score can itself change gene correlations. Restricting the range of a shared driver weakens the correlations among the genes it drives, so IFN-low patients could show weaker links between interferon genes than controls because of the selection rather than the disease. Applying the same cutoff to controls reduces this effect, and conditioning on the IFN score removes most of the shared driver from partial-correlation edges. In addition, a sensitivity analysis compared IFN-low patients with controls matched on IFN score, each patient being paired within the training fold with the control whose score was closest, so that both groups covered the same part of the IFN range. The expected size of this selection effect was also estimated by simulation ([Section 2.13](#sec-2-13)). Because LIONESS edges built from a balanced reference do not respond to differences in average expression ([Section 2.6](#sec-2-6)), a network difference that survives these safeguards indicates a change in how the interferon pathway genes are coordinated rather than in their overall level.

<a id="sec-2-3-4"></a>

#### 2.3.4 Treatment and IFN status

Hydroxychloroquine and immunosuppressants can lower the IFN signature, so some patients classified as IFN-low may be IFN-high patients whose signature has been suppressed by treatment. In the cohorts with medication records ([GSE224705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705), [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) and [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169)), the proportion of IFN-low patients was compared between patients with and without each recorded treatment. In GSE65391, which follows patients over time, the movement of individual patients between IFN states across visits was also described. Because treated IFN-high patients could appear IFN-low while keeping the gene links of the IFN-high state, a sensitivity analysis repeated the primary comparison after excluding patients with recorded hydroxychloroquine or immunosuppressant use, in the cohorts that recorded it.

<a id="sec-2-4"></a>

### 2.4 Confounding control

Differences between IFN-low patients and controls could arise from factors other than disease. Five such factors were addressed: sex, batch, treatment, cell composition, and age and ancestry. Each was handled either by the study design or by an explicit baseline model and adjustment covariate.

The first factor, sex, was inferred from the expression of Y-chromosome genes (RPS4Y1, DDX3Y, KDM5D, UTY and EIF1AY) rather than from XIST, because XIST expression is unreliable for this purpose in SLE: in GSE319130, 54% of male patients (22 of 41) showed elevated XIST expression [[2]](https://pubmed.ncbi.nlm.nih.gov/42039161/). Inferred sex was compared with reported sex where it was available. The primary analysis was restricted to females. X-chromosome genes were retained, because removing them would delete immune genes located on the X chromosome, such as TLR7, CXCR3, CD40LG and FOXP3. A sensitivity analysis included both sexes after removing the Y-chromosome genes and XIST/TSIX.

Batch effects were controlled mainly by design. Cohorts in which patients and controls had been processed in separate batches were not eligible as primary cohorts ([Section 2.1](#sec-2-1)). Within eligible cohorts, cross-validation folds were stratified by batch, batch was included as an adjustment covariate in the population-level tests ([Section 2.2](#sec-2-2)), and the distribution of batches by group is reported.

Treatment was the third factor. Glucocorticoids change blood gene expression and could therefore create differences between patients and controls that are unrelated to disease. A glucocorticoid-response score was computed for each sample with singscore [[16]](https://doi.org/10.1186/s12859-018-2435-4) from the 64 genes that Hu et al. found to be up-regulated by glucocorticoids [[4]](https://pubmed.ncbi.nlm.nih.gov/29534336/). The score served three purposes: as a baseline model (M0b, [Section 2.9](#sec-2-9)), to define a sensitivity analysis in which its genes were removed from the network features, and as an adjustment covariate in the population-level tests. In cohorts that recorded steroid use or dose, we checked that the score was associated with the recorded treatment. Where medication was not recorded for each patient, treatment exposure could be estimated only through this score.

Cell composition required particular care, because gene co-expression in whole blood is strongly influenced by differences in the proportions of blood cell types between samples. For each sample, singscore [[16]](https://doi.org/10.1186/s12859-018-2435-4) was used to score marker gene sets for neutrophils, monocytes, B cells, plasmablasts, T cells, natural killer cells and eosinophils, with the marker sets fixed before analysis. Because each score uses only the sample being scored, it cannot carry information between training and test data. The cell-type scores served as a baseline model, as additional conditioning variables in the partial correlations ([Section 2.7](#sec-2-7)) and as adjustment covariates in the population-level tests.

Finally, age and recorded race or ancestry were tabulated by group and used both as a baseline model and as adjustment covariates. A sensitivity analysis restricted the data to the age range shared by patients and controls. The paediatric cohort ([GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391)) was analysed separately from the adult cohorts.

<a id="sec-2-5"></a>

### 2.5 Pathways

The primary network analysis used one pathway, REACTOME INTERFERON SIGNALING, taken from the Molecular Signatures Database (MSigDB) [[17]](https://pubmed.ncbi.nlm.nih.gov/21546393/) and accessed in R through the msigdbr package [[18]](https://cran.r-project.org/web/packages/msigdbr/index.html), with the database version recorded. It corresponds to the Reactome *Interferon Signaling* pathway (R-HSA-913531) [[15]](https://doi.org/10.1093/nar/gkab1028), which covers both type I (alpha/beta) and type II (gamma) IFN signalling. The same pathway was used in every contrast ([Section 2.10](#sec-2-10)). In the comparison of IFN-low patients with controls, the question is whether the coordination of the interferon pathway differs even when its overall activity is low. In the comparison of IFN-high patients with healthy controls, the interferon genes are both more highly expressed and more strongly co-expressed, so this contrast served as a positive control for the pipeline; because network edges respond mainly to co-expression rather than to expression level ([Section 2.6](#sec-2-6)), it was reported together with the expression-based models and the level test of [Section 2.12](#sec-2-12).

Partial correlations become unstable as the number of genes approaches the number of samples, so each network was limited to between 15 and 50 genes after filtering. This keeps the number of genes well below the smallest training set expected in a primary cohort, about 110 samples per fold (80% of 80 IFN-low patients and 60 controls). The four IFN-score genes were removed first ([Section 2.3](#sec-2-3)). Because the interferon pathway contains more than 50 genes, it was then divided into its Reactome sub-pathways, which include *Interferon alpha/beta signaling* (R-HSA-909733) and *Interferon gamma signaling* (R-HSA-877300). Sub-pathways that still exceeded 50 genes were restricted to the 50 genes with the highest variance in the training fold, sub-pathways with fewer than 15 genes were removed, and near-duplicate sub-pathways, defined as pairs with a Jaccard index of gene overlap above 0.8, were reduced to a single representative. In what follows, "pathway" refers to each of the resulting sub-pathways. The genes retained in each sub-pathway are listed, and genes shared between sub-pathways, such as signalling genes common to type I and type II IFN, are reported; a sensitivity analysis removed the shared genes so that each gene contributed to one sub-pathway only.

Restricting the analysis to the interferon pathway cannot detect disease processes outside it, such as the B-cell, neutrophil or eosinophil signatures reported in other studies. A secondary analysis therefore applied the same pipeline to pathways from the Reactome *Immune System* subtree (R-HSA-168256), excluding the *Interferon Signaling* subtree, with the same size and overlap rules. All gene lists were archived with the analysis code.

<a id="sec-2-6"></a>

### 2.6 Theory: what single-sample networks contain

This section derives a simple formula for what a LIONESS edge measures. The formula explains how the network features should be interpreted and which baseline models they must be compared with.

**Set-up.** Consider a pathway with $`G`$ genes and a reference set of $`N`$ samples. Let $`\mathbf{x}_q`$ be the expression vector of sample $`q`$, $`\boldsymbol{\mu}`$ the reference mean and $`\mathbf{d} = \mathbf{x}_q - \boldsymbol{\mu}`$ the deviation of sample $`q`$ from that mean. Let $`\mathbf{S}`$ be the reference covariance matrix (with divisor $`N`$). Because $`G`$ can be large relative to $`N`$, the covariance matrix was stabilized by shrinkage with a fixed intensity $`\lambda \in [0, 1]`$ [[19]](https://pubmed.ncbi.nlm.nih.gov/16646851/):

```math
\boldsymbol{\Sigma}_\lambda = (1-\lambda)\,\mathbf{S} + \lambda\,\mathrm{diag}(\mathbf{S}) \qquad\qquad (4)
```

where $`\mathrm{diag}(\mathbf{S})`$ keeps the variances of the genes and sets their covariances to zero. Let $`\boldsymbol{\Omega} = \boldsymbol{\Sigma}_\lambda^{-1}`$ be the precision matrix. The partial correlation between genes $`i`$ and $`j`$, that is, their association after removing the effect of the other genes in the pathway, is

```math
\rho_{ij} = -\frac{\Omega_{ij}}{\sqrt{\Omega_{ii}\,\Omega_{jj}}} \qquad\qquad (5)
```

The LIONESS edge for sample $`q`$ is [[20]](https://pubmed.ncbi.nlm.nih.gov/30981959/)

```math
e_{ij}^{(q)} = N\,\rho_{ij} - (N-1)\,\rho_{ij}^{(-q)} \qquad\qquad (6)
```

where $`\rho_{ij}^{(-q)}`$ is computed without sample $`q`$. The edge therefore measures how much sample $`q`$ changes the association between the two genes. Equation (6) has the same form as the jackknife pseudo-value of classical statistics [[21]](https://scholar.google.com/scholar?q=Tukey+1958+Bias+and+confidence+in+not-quite+large+samples), which has already been used for differential network analysis [[22]](https://pubmed.ncbi.nlm.nih.gov/36624383/).

**Conditional residuals.** Let $`\mathbf{u} = \boldsymbol{\Omega}\mathbf{d}`$, with entries $`u_i`$, and

```math
\tilde{u}_i = \frac{u_i}{\sqrt{\Omega_{ii}}} \qquad\qquad (7)
```

Up to scaling, $`\tilde{u}_i`$ is the residual of gene $`i`$ in sample $`q`$ after regression on the other genes of the pathway, divided by its standard deviation; it measures how unexpected the value of gene $`i`$ is, given the other genes. Across the reference population, each $`\tilde{u}_i`$ has variance 1, and two residuals have covariance $`-\rho_{ij}`$: when two genes are positively partially correlated, their residuals are negatively correlated.

**Result 1 (no shrinkage, $`\lambda = 0`$).** To first order in $`1/(N-1)`$,

```math
e_{ij}^{(q)} \approx \tilde{u}_i\,\tilde{u}_j + \rho_{ij}\left(1 + \frac{\tilde{u}_i^2 + \tilde{u}_j^2}{2}\right) \qquad\qquad (8)
```

An edge is therefore built from two ingredients: the product of the two genes' residuals, which is positive when both genes deviate in the same direction, and the squares of the residuals, which grow when the sample is unusual for either gene. Averaged over the reference population, the edge equals $`\rho_{ij}`$, as LIONESS requires.

**Result 2 (with shrinkage).** When $`\lambda`$ is fixed, $`\boldsymbol{\Sigma}_\lambda`$ is a linear function of $`\mathbf{S}`$, and the same expansion gives

```math
e_{ij}^{(q)} \approx \rho_{ij} + \tilde{M}_{ij} + \rho_{ij}\,\frac{\tilde{M}_{ii} + \tilde{M}_{jj}}{2}, \qquad \mathbf{M} = (1-\lambda)\,\mathbf{u}\mathbf{u}^{\top} + \lambda\,\boldsymbol{\Omega}\mathbf{D}_d\boldsymbol{\Omega} \qquad\qquad (9)
```

where $`d_g`$ is the deviation of gene $`g`$ (the $`g`$-th entry of $`\mathbf{d}`$), $`\mathbf{D}_d = \mathrm{diag}(d_1^2, \ldots, d_G^2)`$ is the diagonal matrix of squared deviations, $`M_{ij}`$ is the entry in row $`i`$ and column $`j`$ of $`\mathbf{M}`$, and $`\tilde{M}_{ij} = M_{ij} / \sqrt{\Omega_{ii}\,\Omega_{jj}}`$. The matrix $`\mathbf{M}`$ mixes the products of residuals, $`\mathbf{u}\mathbf{u}^{\top}`$, with a term built from the squared deviations of the individual genes, in proportions set by $`\lambda`$. Equation (9) reduces to equation (8) when $`\lambda = 0`$, and with shrinkage the edge is still made only of products and squares of the sample's deviations.

**Pearson analogue.** For the Pearson correlation $`r_{ij}`$ between genes $`i`$ and $`j`$ in the reference set ([Section 2.7](#sec-2-7)), and with $`z_i = d_i/\sigma_i`$ the deviation of gene $`i`$ in sample $`q`$ divided by its reference standard deviation $`\sigma_i`$, the same expansion gives

```math
e_{ij}^{(q)} \approx z_i\,z_j + r_{ij}\left(1 - \frac{z_i^2 + z_j^2}{2}\right) \qquad\qquad (10)
```

**Result 3 (SSN is an exact rescaling of LIONESS).** The sample-specific network (SSN) method defines an edge as the change in an association measure $`c`$ when sample $`q`$ is added to a reference set $`R`$ of $`n`$ samples, $`\Delta_{ij}^{(q)} = c_{ij}(R \cup \{q\}) - c_{ij}(R)`$ [[23]](https://pubmed.ncbi.nlm.nih.gov/27596597/). LIONESS with the same reference gives $`e_{ij}^{(q)} = (n+1)\,c_{ij}(R \cup \{q\}) - n\,c_{ij}(R)`$, so

```math
\Delta_{ij}^{(q)} = \frac{e_{ij}^{(q)} - c_{ij}(R)}{n+1} \qquad\qquad (11)
```

exactly, for any association measure. Equations (8)–(10) therefore also describe SSN and its partial-correlation version, P-SSN [[24]](https://pubmed.ncbi.nlm.nih.gov/32422654/). Numerical checks on simulated data confirmed that equations (8)–(10) agree closely with exact LIONESS and that equation (11) holds exactly; the check code is provided with the analysis code.

**Predictions.** Equations (8)–(11) lead to six predictions.

*P1 (no new information).* Each edge is a fixed function of $`\mathbf{d}`$, so a network contains no information beyond the sample's own expression values within the pathway; it can only represent that information differently. Network models must therefore be compared with models built directly on pathway expression ([Section 2.9](#sec-2-9)). *P2 (quadratic classifier).* A linear model on a pathway's edges is a quadratic function of $`\mathbf{d}`$, so its natural competitor is a quadratic classifier on the pathway's expression values, such as regularized quadratic discriminant analysis. *P3 (mean and spread).* Because each edge is built from products and squares, changing the sign of a deviation does not change the edge. As a result, a group that differs from the other only in how widely its values are spread produces the same average edges, and, when the reference contains equal numbers of the two groups, so does a group that differs only in its mean expression. Edges are therefore expected to separate groups mainly when the genes co-vary differently. The pilot simulation confirmed this prediction. *P4 (opposite signs).* The squared terms carry a positive sign for partial correlation (equation 8) and a negative sign for Pearson correlation (equation 10), so unusual samples strengthen partial-correlation edges but weaken Pearson edges. Partial-correlation and Pearson LIONESS (models L2 and L2-P) can therefore behave differently on the same data. *P5 (node strength).* Node strength, the sum of a gene's edges, is approximately $`\tilde{u}_i \sum_{j \ne i} \tilde{u}_j`$ plus squared terms, and is therefore closely related to how far a sample lies from the healthy centre, the distance-from-health baseline (M4). *P6 (equivalence).* By equation (11), SSN, P-SSN and LIONESS differ edge by edge only by a fixed rescaling, so any difference in their performance must come from the network summaries or the choice of reference.

 All network features were computed with exact LIONESS ([Section 2.7](#sec-2-7)), and the agreement between exact and first-order edges on the real data, including in the tails of the distribution.

<a id="sec-2-7"></a>

### 2.7 LIONESS estimation with Pearson and partial correlation

Single-sample networks were estimated with two association measures: Pearson correlation and partial correlation. Pearson correlation measures the overall association between two genes, including associations that arise because both genes are linked to other genes in the pathway. For genes $`i`$ and $`j`$ it is computed from the reference covariance matrix $`\mathbf{S}`$, whose entry in row $`i`$ and column $`j`$ is $`S_{ij}`$, as

```math
r_{ij} = \frac{S_{ij}}{\sqrt{S_{ii}\,S_{jj}}} \qquad\qquad (12)
```

Partial correlation, $`\rho_{ij}`$ in equation (5), measures the association between the two genes after removing the effect of all other genes in the pathway, so it is closer to a direct link. Using both measures with the same pipeline shows whether the choice of measure matters (models L2 and L2-P, [Section 2.9](#sec-2-9)); equations (8) and (10) predict that the two can behave differently, because unusual samples strengthen partial-correlation edges but weaken Pearson edges.

Every sample, whether patient or control and whether in a training or a test fold, was given a network by exactly the same rule, and the same rule was used for both measures. [Section 2.6](#sec-2-6) showed that the composition of the reference determines what the edges respond to: when the reference contains more samples of one group, differences in mean expression also enter the edges, whereas with equal numbers of the two groups the edges mainly reflect how the genes co-vary. Class-balanced references were therefore used. Within each training fold, $`B = 20`$ reference subsets $`R_1, \ldots, R_B`$ were formed, each containing all training samples of the smaller class and an equal-sized random sample of the larger class.

For a sample $`q`$ and a reference subset $`R_b`$, let $`R = R_b \setminus \{q\}`$ be that subset with sample $`q`$ removed if it was a member. Writing $`c_{ij}`$ for either association measure, $`r_{ij}`$ or $`\rho_{ij}`$, the edge between genes $`i`$ and $`j`$ was

```math
e_{ij}^{(q,b)} = \big(|R| + 1\big)\,c_{ij}\big(R \cup \{q\}\big) - |R|\,c_{ij}(R) \qquad\qquad (13)
```

where $`|R|`$ is the number of samples in $`R`$ and $`c_{ij}(\cdot)`$ is the association estimated from the samples shown. When sample $`q`$ belongs to $`R_b`$, equation (13) is the leave-one-out form of LIONESS in equation (6); when it does not, as for every test sample, it is the add-one-in form. The final edge was the average over the $`B`$ subsets,

```math
e_{ij}^{(q)} = \frac{1}{B} \sum_{b=1}^{B} e_{ij}^{(q,b)} \qquad\qquad (14)
```

which reduces the variation that comes from the random choice of each reference subset.

The two measures differed only in how the association was estimated. Pearson correlations were computed directly from the covariance matrix by equation (12). Shrinkage was not applied to them, because shrinking the covariances towards zero while keeping the variances fixed, as in equation (4), would multiply every Pearson correlation by the same factor $`1-\lambda`$ and would not change the network structure. Partial correlations were computed by equation (5) from the shrinkage covariance of equation (4), because inverting the covariance matrix is unstable without it. The shrinkage intensity $`\lambda`$ was chosen in the inner cross-validation from 0.5, 1 and 2 times the analytic estimate of Schäfer and Strimmer [[19]](https://pubmed.ncbi.nlm.nih.gov/16646851/), and was then held fixed within the fold. Because each pathway contains at most 50 genes, the covariance matrix could be inverted directly. In the primary analysis, the cell-composition scores of [Section 2.4](#sec-2-4) and the IFN score of [Section 2.3](#sec-2-3) were added to the set of variables on which each partial correlation was conditioned, so that partial-correlation edges describe co-expression beyond what is explained by differences in blood cell proportions and by the shared IFN signal; a sensitivity analysis conditioned on the pathway genes only. Pearson edges, being unconditional, were not adjusted in this way, and this difference is part of what the comparison between the two measures examines.

The implementation was checked against direct recomputation of equation (13) for both measures, against the `pcor.shrink` function of the R package corpcor at a fixed $`\lambda`$ for partial correlation [[19]](https://pubmed.ncbi.nlm.nih.gov/16646851/), and against the lionessR package [[25]](https://pubmed.ncbi.nlm.nih.gov/31653243/), which implements the original LIONESS method [[20]](https://pubmed.ncbi.nlm.nih.gov/30981959/), for Pearson correlation.

<a id="sec-2-8"></a>

### 2.8 Topology features

The same network features were computed from the Pearson and the partial-correlation LIONESS networks. LIONESS edges are signed, can lie outside the range $`[-1, 1]`$, and are present between every pair of genes, so each sample has a complete, weighted network for each pathway. For sample $`q`$ and a given pathway, let $`\mathbf{W}^{(q)}`$ be the $`G \times G`$ matrix of rescaled edges, with zeros on the diagonal and off-diagonal entries

```math
w_{ij}^{(q)} = \frac{e_{ij}^{(q)}}{\kappa} \qquad\qquad (15)
```

where $`\kappa`$ is the 99th percentile of $`|e_{ij}|`$ over all training samples and gene pairs of that pathway and association measure. Because the same factor $`\kappa`$ is used for every sample, the rescaling puts the edges on a common scale without removing genuine differences in edge size between samples. In what follows, the superscript $`(q)`$ is dropped, $`m = G(G-1)/2`$ is the number of gene pairs, and $`\mathbf{P}`$, with entries $`p_{ij}`$, is the reference network, the matrix of reference associations ($`r_{ij}`$ or $`\rho_{ij}`$) rescaled by the same $`\kappa`$ and with zeros on the diagonal. The features were organized in three tiers, fixed before the analysis: primary features, used in the main models; secondary features, used to examine hidden subgroups; and exploratory features, reported descriptively only.

The four primary features each answer a different question about the sample's network. The first, the differential-network score, measures how closely the sample's network follows the pattern that separates patients from controls:

```math
\mathrm{DN} = \sum_{i < j} \big(c_{ij}^{\mathrm{pat}} - c_{ij}^{\mathrm{con}}\big)\, e_{ij} \qquad\qquad (16)
```

where $`c_{ij}^{\mathrm{pat}}`$ and $`c_{ij}^{\mathrm{con}}`$ are the associations between genes $`i`$ and $`j`$ estimated separately in the training patients and the training controls. Because it uses the group labels, the score was computed inside the training folds only, and the resulting weights were applied unchanged to the test samples. The second is the mean absolute edge weight, which summarizes how strongly the genes of the pathway are connected overall:

```math
\bar{w} = \frac{1}{m} \sum_{i < j} |w_{ij}| \qquad\qquad (17)
```

The third is the largest eigenvalue of the network,

```math
\eta_{1} = \max_{\|\mathbf{v}\| = 1} \mathbf{v}^{\top} \mathbf{W} \mathbf{v} \qquad\qquad (18)
```

where $`\mathbf{v}`$ is a vector of length $`G`$ with unit length, $`\|\mathbf{v}\| = 1`$, so that $`\eta_1`$ is the largest eigenvalue of $`\mathbf{W}`$; it is large when many genes are connected in a single coordinated block. The fourth is the distance between the sample's network and the reference network,

```math
D = \big\|\mathbf{W} - \mathbf{P}\big\|_F = \sqrt{\sum_{i \ne j} \big(w_{ij} - p_{ij}\big)^2} \qquad\qquad (19)
```

where $`\|\cdot\|_F`$ is the Frobenius norm, the square root of the sum of squared entries. By equation (8), an edge departs from its reference value through the products and squares of the sample's residuals, so $`D`$ reflects how far the sample lies from the reference centre and was interpreted as a measure of distance rather than of rewiring.

The secondary features add the positive and negative strength of each gene, which sum its positive and negative edges separately so that they do not cancel:

```math
s_i^{+} = \sum_{j \ne i} \max\big(w_{ij}, 0\big), \qquad s_i^{-} = \sum_{j \ne i} \max\big(-w_{ij}, 0\big) \qquad\qquad (20)
```

Together with the four primary features, they form a secondary feature set used to examine whether IFN-low patients contain hidden subgroups, because groups of genes that shift together in a subset of patients change the strength of those genes.

The exploratory features are the classical graph measures used in earlier single-sample network studies. Most of them are defined only for networks in which weak edges have been removed, so a threshold was applied:

```math
a_{ij} = \mathbb{1}\big(|w_{ij}| > \tau\big) \qquad\qquad (21)
```

where $`\mathbb{1}(\cdot)`$ equals 1 when the condition holds and 0 otherwise, and $`\tau`$ is the 90th percentile of $`|w_{ij}|`$ over the training samples, the same for every sample. From the thresholded network, we computed the number of edges, $`\sum_{i<j} a_{ij}`$; the degree of each gene, $`k_i = \sum_{j \ne i} a_{ij}`$; the diameter, the longest shortest path between two genes; the transitivity, the proportion of connected triples of genes that form triangles; and the betweenness centrality of each gene, the proportion of shortest paths between other genes that pass through it. For path-based measures, the length of an edge was set to $`1/|w_{ij}|`$, so that strong edges count as short. Because these measures depend on the threshold, they were also computed at the 80th and 95th percentiles as a sensitivity analysis. The signed clustering coefficient [[26]](https://doi.org/10.2202/1544-6115.1128), [[27]](https://doi.org/10.1371/journal.pone.0088669), the proportion of positive edges, the entropy of the edge weights and the correlation between the sample's edges and the reference edges were also reported as exploratory features.


<a id="sec-2-9"></a>

### 2.9 Baseline and comparator models

Eighteen models were compared; they are listed in [Table 2](#table-2). Each model was chosen to answer one question about where any separation between IFN-low patients and controls comes from, and the models are labelled by group: M0 for baselines, M for expression-based comparators, W for established network methods and L for LIONESS models. All models were fitted within the training folds only, used the same cross-validation splits and were scored in the same way, so that differences in performance reflect the features rather than the set-up.

<a id="sec-2-9-1"></a>

#### 2.9.1 Baselines

Four baselines tested the simplest explanations for a difference between the groups. M0a used the residual IFN score of [Section 2.3](#sec-2-3) as its only feature, to test whether IFN activity below the cutoff is enough to separate the groups. M0b used the glucocorticoid-response score built from the genes of Hu et al. [[4]](https://pubmed.ncbi.nlm.nih.gov/29534336/) ([Section 2.4](#sec-2-4)), to test whether the separation merely reflects steroid treatment. M0c used the cell-composition scores of [Section 2.4](#sec-2-4), to test whether it reflects differences in the proportions of blood cell types. M0d used age and recorded ancestry, to test whether the groups differ only in these characteristics.

<a id="sec-2-9-2"></a>

#### 2.9.2 Expression-based comparators

Six comparators used gene expression without any network. M1 applied an elastic net [[28]](https://doi.org/10.1111/j.1467-9868.2005.00503.x) or a random forest [[29]](https://doi.org/10.1023/A:1010933404324) to all genes, the standard approach of entering every gene into one model. M2 fitted one model per pathway on gene expression and combined the pathway models in the same way as the network models ([Section 2.10](#sec-2-10)), to test whether any gain comes from the pathways themselves rather than from the networks. M3 summarized each pathway by a single activity score (singscore [[16]](https://doi.org/10.1186/s12859-018-2435-4), mean z-score or first principal component) and also applied gradient boosting [[30]](https://doi.org/10.1145/2939672.2939785) and a kernel support vector machine [[31]](https://doi.org/10.1007/BF00994018) to pathway expression; these methods capture general interactions between genes without using network structure. M4 measured, for each pathway, the Mahalanobis distance of a sample from the mean of the training controls, to test whether patients simply lie further from the healthy centre. M5 combined pathway expression with the residual IFN score (M2 plus M0a) and served as the reference model for the primary comparison. M6 applied regularized quadratic discriminant analysis [[32]](https://doi.org/10.2307/2289860) to the expression of each pathway. Because a linear model on network edges is a quadratic function of the sample's deviations ([Section 2.6](#sec-2-6)), M6 is the most direct competitor to the network models.

<a id="sec-2-9-3"></a>

#### 2.9.3 Established network comparators

Two comparators represented network methods already used in lupus research. W1 reproduced a typical published weighted gene co-expression network analysis (WGCNA) [[33]](https://pubmed.ncbi.nlm.nih.gov/19114008/) with hub-gene selection, with every step fitted within the training folds to avoid data leakage. W2 used WGCNA module eigengenes, the summary scores of gene modules, estimated from training data only, and was the main established-network comparator.

<a id="sec-2-9-4"></a>

#### 2.9.4 LIONESS models

Six LIONESS models used the network features of [Section 2.8](#sec-2-8), computed from the partial-correlation and the Pearson networks ([Section 2.7](#sec-2-7)). L1 used the network edges themselves. L2 used the four primary network features of each pathway from the partial-correlation networks, and L2-P used the same features from the Pearson networks; comparing the two shows whether the choice of association measure matters. L2-S used the secondary feature set, which adds the positive and negative strength of each gene, to examine hidden subgroups. L3 added the primary partial-correlation features to the reference model M5, and L3-P did the same with the Pearson features.

<a id="sec-2-9-5"></a>

#### 2.9.5 Primary comparison

The primary hypothesis was tested by comparing L3 with M5, and L3-P with M5. Because each pair of models differs only in the network features, a gain over M5 is evidence that networks carry information beyond both pathway expression and residual IFN activity. Two secondary comparisons placed the network models against their strongest competitors: L2 and L2-P were compared with M6, the quadratic classifier, and with M4, the distance from health. All other comparisons were descriptive.

<a id="table-2"></a>

**Table 2.** Models compared in the study.

| Group | Model | Features | Question answered |
|---|---|---|---|
| Baselines | M0a | Residual IFN score | Is residual IFN activity enough to separate the groups? |
| | M0b | Glucocorticoid-response score | Is the separation due to steroid treatment? |
| | M0c | Cell-composition scores | Is it due to blood cell proportions? |
| | M0d | Age and ancestry | Is it due to age or ancestry? |
| Expression | M1 | All genes (elastic net or random forest) | How well does the standard all-genes approach perform? |
| | M2 | Pathway expression, combined across pathways | Do the pathways themselves carry the signal? |
| | M3 | Pathway scores; boosting and kernel SVM on pathway expression | Do general gene interactions help, without networks? |
| | M4 | Distance from the healthy centre per pathway | Do patients simply lie further from health? |
| | M5 | M2 + M0a | Reference model for the primary comparison |
| | M6 | Regularized quadratic discriminant analysis per pathway | Strongest direct competitor to network features |
| Network methods | W1 | Published WGCNA and hub-gene pipeline, without leakage | What does the usual lupus network analysis achieve? |
| | W2 | WGCNA module eigengenes from training data | Main established-network comparator |
| LIONESS | L1 | Network edges | Do the raw edges carry the signal? |
| | L2 | Four primary features, partial correlation | Main network model |
| | L2-P | Four primary features, Pearson correlation | Does the association measure matter? |
| | L2-S | Secondary features (primary + gene strengths) | Are there hidden subgroups? |
| | L3 | L2 + M5 | Do partial-correlation networks add to expression and IFN? (primary) |
| | L3-P | L2-P + M5 | Do Pearson networks add to expression and IFN? (primary) |

<a id="sec-2-10"></a>

### 2.10 Aggregation across pathways and contrasts

Each sample has features from many pathways, and these had to be combined into a single prediction. The primary method was group lasso logistic regression [[34]](https://doi.org/10.1111/j.1467-9868.2005.00532.x), which treats the features of each pathway as a group and keeps or drops a pathway as a whole. For a model with intercept $`\beta_0`$, coefficient vector $`\boldsymbol{\beta}_k`$ for the $`p_k`$ features of pathway $`k`$, $`\boldsymbol{\beta}`$ the collection of all $`\boldsymbol{\beta}_k`$, and $`\ell`$ the log-likelihood of the logistic model on the training data, the coefficients were estimated by

```math
\hat{\boldsymbol{\beta}} = \arg\min_{\beta_0,\,\boldsymbol{\beta}} \Big\{ -\ell(\beta_0, \boldsymbol{\beta}) + \gamma \sum_{k} \sqrt{p_k}\, \big\|\boldsymbol{\beta}_k\big\|_2 \Big\} \qquad\qquad (22)
```

where $`\|\cdot\|_2`$ is the Euclidean length of a vector and $`\gamma`$ controls how many pathways are kept; $`\gamma`$ was chosen in the inner cross-validation. The factor $`\sqrt{p_k}`$ prevents larger pathways from being favoured simply because they contribute more features. The same aggregation was used for every pathway-based model (M2, M5, M6, L2, L2-P, L2-S, L3 and L3-P), so that differences between models reflect the features rather than the way they were combined. A two-level stacking approach, in which an elastic net was fitted to each pathway and the pathway predictions were combined by a non-negative elastic net, was used as a sensitivity analysis.

To identify which pathways drive a result, the group lasso was refitted on $`B_s = 100`$ random half-samples of the training data, and, with $`\hat{\boldsymbol{\beta}}_k^{(b)}`$ the estimated coefficients of pathway $`k`$ in refit $`b`$, the selection proportion of pathway $`k`$ was recorded as

```math
\hat{\Pi}_k = \frac{1}{B_s} \sum_{b=1}^{B_s} \mathbb{1}\big(\hat{\boldsymbol{\beta}}_k^{(b)} \ne \mathbf{0}\big) \qquad\qquad (23)
```

the proportion of refits in which the pathway was kept. This procedure, known as stability selection [[35]](https://doi.org/10.1111/j.1467-9868.2010.00740.x), favours pathways that are selected consistently rather than by chance. A pathway was described as implicated only if three conditions held: its selection proportion exceeded 0.6, within the range suggested by Meinshausen and Bühlmann [[35]](https://doi.org/10.1111/j.1467-9868.2010.00740.x); it differed between the groups in the population-level tests ([Section 2.12](#sec-2-12)); and both results remained after adjustment for cell composition and treatment.

The pipeline was applied to five comparisons between groups, called contrasts. C1 compared IFN-high patients with healthy controls and served as a positive control, because the interferon pathway is strongly activated in these patients and a clear network difference is expected ([Section 2.5](#sec-2-5)). C2 compared IFN-low patients with healthy controls and was the primary contrast. C3 compared IFN-low patients with patients with rheumatoid arthritis in [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169). C4 compared IFN-low patients with high and low disease activity (SLEDAI-2K of at least 6 and at most 4, respectively) in cohorts that recorded disease activity. C5 compared IFN-low patients with and without lupus nephritis, using the renal involvement recorded in each cohort. For each contrast, the LIONESS reference subsets and the differential-network score were built from the two groups being compared only. Because the primary analysis contains only a few interferon sub-pathways, results were also reported for each sub-pathway separately; stability selection is most informative in the secondary analysis of Immune System pathways, which contains many more. Contrasts C3 to C5 were analysed in a cohort only if each group contained at least 25 patients after the go/no-go check ([Section 2.1](#sec-2-1)); contrasts that did not meet this rule are reported with their group sizes, without model fitting.

<a id="sec-2-11"></a>

### 2.11 Validation and statistical inference

Model performance was estimated within each eligible cohort by repeated, stratified, nested cross-validation, with one sample per patient: 10 repeats of 5 outer folds, each containing 5 inner folds. The outer folds estimated performance and the inner folds chose the tuning parameters, and repeating the whole procedure with different random splits reduced the dependence of the results on any single split. Folds were stratified by group and by batch ([Section 2.4](#sec-2-4)). Every step that learns from the data was carried out within the training folds only and then applied unchanged to the test fold: winsorizing and standardization, probe selection and gene filtering ([Section 2.2](#sec-2-2)), the IFN cutoff ([Section 2.3](#sec-2-3)), the shrinkage intensity $`\lambda`$ and the LIONESS reference subsets ([Section 2.7](#sec-2-7)), the rescaling factor $`\kappa`$, the differential-network weights and the threshold $`\tau`$ ([Section 2.8](#sec-2-8)), the WGCNA modules ([Section 2.9](#sec-2-9)), the group-lasso penalty $`\gamma`$ ([Section 2.10](#sec-2-10)) and the recalibration of predicted probabilities. Where two cohorts shared a platform and a contrast, models trained on one cohort were also applied unchanged to the other as an external validation.

The primary performance measure was the area under the receiver operating characteristic curve (AUC). Secondary measures were the Brier score, which measures the accuracy of predicted probabilities, and the calibration slope and intercept after Platt recalibration within the training folds [[36]](https://scholar.google.com/scholar?q=Platt+1999+Probabilistic+outputs+for+support+vector+machines). The area under the precision–recall curve was reported for each cohort together with the proportion of cases, because its value depends on the balance between the groups.

Three hypotheses were specified in advance for contrast C2 (IFN-low patients versus healthy controls) in the primary cohort, restricted to females ([Section 2.4](#sec-2-4)). The primary hypothesis, H1, was that the network models add information beyond pathway expression and the residual IFN score: L3 has a higher AUC than M5 (H1a), and L3-P has a higher AUC than M5 (H1b) ([Table 2](#table-2)). The secondary hypothesis, H2, was that the network models outperform their strongest competitors: L2 and L2-P each have a higher AUC than M6, the quadratic classifier, and than M4, the distance from health. The third hypothesis, H3, was that the ranking of the models across the simulation scenarios agrees with the predictions of [Section 2.6](#sec-2-6) ([Section 2.13](#sec-2-13)). The Holm correction for multiple testing was applied across the two comparisons of H1 and, separately, across the four comparisons of H2. All other comparisons and contrasts were treated as exploratory and reported as estimates with confidence intervals.

Each comparison between two models, A and B, was summarized by the paired difference in AUC,

```math
\Delta_{AB} = \mathrm{AUC}_A - \mathrm{AUC}_B \qquad\qquad (24)
```

computed from the out-of-fold predictions of both models on the same samples and averaged over the repeats. Predictions from different folds of the same cross-validation are not independent, so standard tests such as DeLong's test understate the uncertainty. The standard error of $`\Delta_{AB}`$ was therefore estimated with the nested cross-validation method of Bates et al. [[37]](https://doi.org/10.1080/01621459.2023.2197686), and the 95% confidence interval, with $`\widehat{\mathrm{SE}}`$ denoting this estimated standard error, was

```math
\Delta_{AB} \pm 1.96\, \widehat{\mathrm{SE}}\big(\Delta_{AB}\big) \qquad\qquad (25)
```

The corrected variance estimator of Nadeau and Bengio [[38]](https://doi.org/10.1023/A:1024068626366) was used as a sensitivity analysis. The false-positive rate of these tests was checked in the simulation scenario with no true difference ([Section 2.13](#sec-2-13)). Because differences between related models are expected to be small, results are reported mainly as estimates with confidence intervals, together with the smallest difference that each cohort could detect, which was computed by simulation before the analysis.

When more than one cohort was eligible for a contrast, the differences $`\Delta_c`$ estimated in each cohort $`c`$ were combined by fixed-effect inverse-variance pooling, in which each cohort is weighted by $`\pi_c`$, the inverse of its squared standard error, and $`\bar{\Delta}`$ is the pooled difference:

```math
\bar{\Delta} = \frac{\sum_c \pi_c\, \Delta_c}{\sum_c \pi_c}, \qquad \pi_c = \frac{1}{\widehat{\mathrm{SE}}(\Delta_c)^2}, \qquad \widehat{\mathrm{SE}}(\bar{\Delta}) = \Big(\sum_c \pi_c\Big)^{-1/2} \qquad\qquad (26)
```

A fixed-effect model was used because the variation between cohorts cannot be estimated reliably from two or three cohorts, and whether the cohorts agreed in the direction of the effect is reported. Finally, as a check for data leakage, the group labels were randomly permuted and the full pipeline was re-run 200 times; without leakage, the AUC from permuted labels should be close to 0.5.

<a id="sec-2-12"></a>

### 2.12 Population-level tests

Prediction shows whether IFN-low patients can be told apart from controls, but not how the two groups differ. To answer that question directly, each pathway ([Section 2.5](#sec-2-5)) was tested at the population level in three layers, each targeting one kind of difference: average expression, spread and correlation structure. Before testing, the expression of each gene was adjusted for age, ancestry, batch, the cell-composition scores, the glucocorticoid-response score and the IFN score ([Section 2.3](#sec-2-3), [Section 2.4](#sec-2-4)). Let $`\bar{\mathbf{x}}_{\mathrm{pat}}`$ and $`\bar{\mathbf{x}}_{\mathrm{con}}`$ denote the mean vectors of the adjusted expression of a pathway in patients and controls, and let $`\mathbf{V}`$ be the pooled within-group covariance matrix of the same genes, stabilized by the shrinkage of equation (4); the superscript $`\top`$ denotes the transpose and $`\mathbf{V}^{-1}`$ the inverse.

The first layer tested for a difference in average expression with a shrinkage-based Hotelling-type statistic,

```math
T_1 = \big(\bar{\mathbf{x}}_{\mathrm{pat}} - \bar{\mathbf{x}}_{\mathrm{con}}\big)^{\top} \mathbf{V}^{-1} \big(\bar{\mathbf{x}}_{\mathrm{pat}} - \bar{\mathbf{x}}_{\mathrm{con}}\big) \qquad\qquad (27)
```

which is large when the two group centres are far apart. The second layer tested for a difference in spread, that is, whether one group is more scattered around its own centre than the other. With $`d_i^2`$ the squared Mahalanobis distance of sample $`i`$ from the centre of its own group, computed with $`\mathbf{V}`$, the statistic was the absolute difference between the group averages $`\overline{d^2}_{\mathrm{pat}}`$ and $`\overline{d^2}_{\mathrm{con}}`$,

```math
T_2 = \Big| \overline{d^2}_{\mathrm{pat}} - \overline{d^2}_{\mathrm{con}} \Big| \qquad\qquad (28)
```

The third layer tested for a difference in correlation structure, the kind of difference that single-sample networks are designed to capture. It compared the association matrices of the two groups, estimated separately with the same method as the networks,

```math
T_3 = \big\| \mathbf{C}_{\mathrm{pat}} - \mathbf{C}_{\mathrm{con}} \big\|_F \qquad\qquad (29)
```

where $`\mathbf{C}_{\mathrm{pat}}`$ and $`\mathbf{C}_{\mathrm{con}}`$ are the association matrices of patients and controls: the partial-correlation matrix, computed with a common shrinkage intensity, or, in a parallel analysis, the Pearson correlation matrix. This follows the differential-network framework of Grimes et al. [[39]](https://pubmed.ncbi.nlm.nih.gov/30940863/), which allows any association measure and assesses significance by permutation. Both correlation measures are unchanged when a gene is rescaled, so a difference in spread alone does not affect $`T_3`$.

P-values for all three layers were obtained with 10,000 Freedman–Lane permutations [[40]](https://doi.org/10.1080/07350015.1983.10509354). In this scheme, expression is first regressed on the adjustment covariates, and the residuals rather than the raw data are permuted between groups, so that the covariates are not shuffled together with the group labels. Permutation restricted within batches was used as a sensitivity analysis. The false discovery rate was controlled within each layer by the Benjamini–Hochberg procedure [[41]](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x). In the pilot simulation, each layer detected its own kind of difference and rarely responded to the others: the mean test detected level differences in all simulated datasets, the spread test detected spread differences in all datasets, and the structure test detected rewired genes in 97% of datasets, while each test responded to a difference of another kind in at most 10% of datasets, except for the hidden-subgroup scenario described below ([Section 2.13](#sec-2-13)).

A difference in structure can arise in two ways: through a genuine change in how genes are co-regulated, or through hidden subgroups of patients whose expression is shifted in different directions, which creates correlation among the shifted genes. In the pilot simulation, the structure test detected hidden subgroups in all datasets. Every pathway with a significant structure difference was therefore checked for subgroups. Gaussian mixture models with one and two components were fitted to the first three principal components of the pathway's adjusted expression, separately in patients and controls, and compared by the Bayesian information criterion (BIC) [[42]](https://doi.org/10.1214/aos/1176344136),

```math
\Delta\mathrm{BIC} = \mathrm{BIC}_{1} - \mathrm{BIC}_{2} \qquad\qquad (30)
```

where $`\mathrm{BIC}_1`$ and $`\mathrm{BIC}_2`$ are the BIC values of the one- and two-component models, and a value of $`\Delta\mathrm{BIC}`$ above 2 favours two groups. In the pilot simulation, this check flagged 80% of datasets with hidden subgroups and none of the datasets with rewired genes or with no difference. Pathways flagged in patients but not in controls were reported as showing a structure difference that may be due to subgroups. Because the check can miss weak subgroups, structure differences that were not flagged were described as differences in correlation structure, not as proof of rewiring. The same layered tests were also used to interpret the classification results ([Section 2.11](#sec-2-11)), because a network model that performs well should be accompanied by a structure difference in the same pathways.

<a id="sec-2-13"></a>

### 2.13 Simulation study

The simulated data were built to mimic the real data, so that the behaviour of the pipeline in the simulation would carry over to the real analysis. Six features of the real data were reproduced: the genes analysed (the interferon sub-pathways without the four IFN-score genes, [Section 2.5](#sec-2-5)); the distribution of each gene; the correlations between genes; the shared IFN activity that makes the interferon genes rise and fall together; the selection of IFN-low patients by the in-fold cutoff ([Section 2.3](#sec-2-3)); and the group sizes of the primary cohort. All simulations started from the real expression data of the female healthy controls of [GSE319130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130), processed and adjusted as in the real analysis ([Section 2.2](#sec-2-2), [Section 2.4](#sec-2-4)). Controls contain no disease signal, so any difference between simulated groups was added deliberately and is known.

Two designs were used. In the resampling design, real control samples were randomly divided into pseudo-patients and pseudo-controls, and a known signal was added to the pseudo-patients; this keeps the exact noise of real blood data but allows only about 38 samples per group. In the generative design, new samples of any size were drawn from a model fitted to the same controls. For each sub-pathway, with $`\hat{F}_g`$ the distribution of gene $`g`$ in the controls and $`\hat{\mathbf{R}}`$ their shrinkage correlation matrix (equation 4), each sample was generated as

```math
x_g = \hat{F}_g^{-1}\big(\Phi(z_g)\big), \qquad \mathbf{z} = (z_1, \ldots, z_G)^{\top} \sim \mathcal{N}\big(\mathbf{0}, \hat{\mathbf{R}}\big) \qquad\qquad (31)
```

where $`\Phi`$ is the standard normal cumulative distribution function and $`\hat{F}_g^{-1}`$ the quantile function of gene $`g`$. This Gaussian copula gives every simulated gene the distribution of the real gene and the genes the real correlations. To reproduce the shared IFN activity and the selection of IFN-low patients, each interferon gene, including the four score genes, was modelled as

```math
x_g = \mu_g + l_g\, f + \varepsilon_g \qquad\qquad (32)
```

where $`\mu_g`$ is the mean of gene $`g`$, $`f`$ the IFN activity of the sample, $`l_g`$ the loading of gene $`g`$ (how strongly it follows IFN activity), estimated from the first principal component of the interferon genes in all SLE patients of the primary cohort, and $`\varepsilon_g`$ the remaining variation, generated by equation (31). The distribution of $`f`$ was chosen so that the simulated IFN scores matched the observed ones, and the IFN score and cutoff (equations 2 and 3) were then computed inside each training fold exactly as in the real analysis. How closely the simulated data resemble the real data was checked before use ([Supplementary Section S1](#supp-s1)).

Known differences were added in eight scenarios ([Table 3](#table-3)): a shift in average expression (S1), an increase in spread (S2), hidden subgroups shifted in opposite directions (S3), changed partial correlations in 10% of gene pairs (S4), IFN-high patients whose interferon genes were lowered by treatment (S5), a difference only in the distribution of IFN activity, which isolates the selection effect (S6), IFN-high patients versus controls as a positive control (S7), and no difference (S0). The size of each difference was set so that the best possible classifier, which knows the true model, would reach an AUC of 0.60, 0.70 or 0.80, and every model's AUC was reported relative to this ceiling. Simulated group sizes were the numbers of female IFN-low patients and controls observed in the primary cohort after the go/no-go check ([Section 2.1](#sec-2-1)) and 40 per group. Each setting was repeated 200 times for single sub-pathways and 100 times for the full pipeline (details in [Supplementary Section S1](#supp-s1)).

Each simulated dataset was analysed with exactly the real pipeline ([Section 2.7](#sec-2-7)–[Section 2.12](#sec-2-12)), including all models of [Table 2](#table-2). The recorded outcomes were the AUC of each model relative to the ceiling; the rejection rates of the hypothesis tests and of the three population-level layers; how often the subgroup check flagged each scenario; the false-positive rates in scenarios S0 and S6, which should not exceed 5%; the coverage of the confidence intervals of equation (25), which should be close to 95%; and the smallest AUC difference detectable with 80% power at the real sample size ([Section 2.11](#sec-2-11)). Scenarios S5 and S6 were analysed with and without the safeguards of [Section 2.3](#sec-2-3) to show how much each one reduces a false signal. The results were also used to write a reading guide that links each pattern of results to the kind of difference that causes it; all simulations were completed and the guide was fixed before any model was fitted to the real outcome data.

<a id="table-3"></a>

**Table 3.** Simulation scenarios.

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


<a id="sec-2-14"></a>

### 2.14 Application to the SLE cohorts

After the simulation study was complete and the reading guide fixed ([Section 2.13](#sec-2-13)), the pipeline was applied to the real cohorts in a fixed order, so that later steps could not influence earlier decisions. First, the go/no-go check was carried out on the IFN status, sex and group sizes of each cohort, without fitting any outcome model, and each cohort was assigned its role as primary, replication or descriptive ([Section 2.1](#sec-2-1), [Table 1](#table-1)). Second, the positive-control contrast C1, IFN-high patients versus healthy controls, was analysed to confirm that the pipeline detects a known difference in the real data ([Section 2.10](#sec-2-10)). Third, the primary analysis was run: contrast C2, IFN-low patients versus healthy controls, in the females of the primary cohort, [GSE319130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130), testing hypotheses H1 and H2 ([Section 2.11](#sec-2-11)) and applying the population-level tests and subgroup check ([Section 2.12](#sec-2-12)). Fourth, the same analysis was repeated in the replication cohort, [GSE88884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE88884), and the results were combined where possible (equation 26). Fifth, the secondary contrasts C3 to C5 were analysed in the cohorts that met the size rule, together with the secondary analysis of Immune System pathways ([Section 2.5](#sec-2-5)) and the treatment analyses ([Section 2.3](#sec-2-3)). The paediatric cohort, [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391), was analysed separately.



## 3. Results

[Not yet written]

<a id="sec-4"></a>

## 4. Discussion

[Not yet written]

<a id="sec-5"></a>

## 5. Conclusion

[Not yet written]

<a id="references"></a>

## References

1. Barrett T, Wilhite SE, Ledoux P, et al. NCBI GEO: archive for functional genomics data sets—update. *Nucleic Acids Res* 2013;41(Database issue):D991–D995. PMID [23193258](https://pubmed.ncbi.nlm.nih.gov/23193258/).
2. Masson HO, et al. XIST expression and hypermethylation of the X chromosome in males with systemic lupus erythematosus. *Front Immunol* 2026. PMID [42039161](https://pubmed.ncbi.nlm.nih.gov/42039161/).
3. Hoffman RW, et al. Gene expression and pharmacodynamic changes in 1,760 systemic lupus erythematosus patients from two phase III trials of BAFF blockade with tabalumab. *Arthritis Rheumatol* 2017;69(3):643–654. PMID [27723281](https://pubmed.ncbi.nlm.nih.gov/27723281/).
4. Hu Y, et al. Development of a molecular signature to monitor pharmacodynamic responses mediated by in vivo administration of glucocorticoids. *Arthritis Rheumatol* 2018;70(8):1331–1342. PMID [29534336](https://pubmed.ncbi.nlm.nih.gov/29534336/).
5. Banchereau R, et al. Personalized immunomonitoring uncovers molecular networks that stratify lupus patients. *Cell* 2016. PMID [27040498](https://pubmed.ncbi.nlm.nih.gov/27040498/).
6. Wither JE, et al. Identification of a neutrophil-related gene expression signature that is enriched in adult systemic lupus erythematosus patients with active nephritis: clinical/pathologic associations and etiologic mechanisms. *PLoS One* 2018;13(5):e0196117. PMID [29742110](https://pubmed.ncbi.nlm.nih.gov/29742110/).
7. López-Domínguez R, et al. Immune and molecular landscape behind non-response to mycophenolate mofetil and azathioprine in lupus nephritis therapy. *Res Sq* 2024 (preprint). PMID [38260685](https://pubmed.ncbi.nlm.nih.gov/38260685/).
8. Barturen G, et al. Integrative analysis reveals a molecular stratification of systemic autoimmune diseases. *Arthritis Rheumatol* 2021. [PubMed search](https://pubmed.ncbi.nlm.nih.gov/?term=Barturen+Integrative+analysis+molecular+stratification+systemic+autoimmune+diseases).
9. Hanley JA, McNeil BJ. The meaning and use of the area under a receiver operating characteristic (ROC) curve. *Radiology* 1982;143(1):29–36. PMID [7063747](https://pubmed.ncbi.nlm.nih.gov/7063747/).
10. Irizarry RA, Hobbs B, Collin F, et al. Exploration, normalization, and summaries of high density oligonucleotide array probe level data. *Biostatistics* 2003;4(2):249–264. PMID [12925520](https://pubmed.ncbi.nlm.nih.gov/12925520/).
11. Robinson MD, McCarthy DJ, Smyth GK. edgeR: a Bioconductor package for differential expression analysis of digital gene expression data. *Bioinformatics* 2010;26(1):139–140. PMID [19910308](https://pubmed.ncbi.nlm.nih.gov/19910308/).
12. Chen Y, Lun ATL, Smyth GK. From reads to genes to pathways: differential expression analysis of RNA-Seq experiments using Rsubread and the edgeR quasi-likelihood pipeline. *F1000Res* 2016;5:1438. [Article](https://f1000research.com/articles/5-1438).
13. Robinson MD, Oshlack A. A scaling normalization method for differential expression analysis of RNA-seq data. *Genome Biol* 2010;11(3):R25. PMID [20196867](https://pubmed.ncbi.nlm.nih.gov/20196867/).
14. Brohawn PZ, Streicher K, Higgs BW, et al. Type I interferon gene signature test-low and -high patients with systemic lupus erythematosus have distinct gene expression signatures. *Lupus* 2019;28(13):1524–1533. PMID [31660791](https://pubmed.ncbi.nlm.nih.gov/31660791/).
15. Gillespie M, Jassal B, Stephan R, et al. The reactome pathway knowledgebase 2022. *Nucleic Acids Res* 2022;50(D1):D687–D692. doi:[10.1093/nar/gkab1028](https://doi.org/10.1093/nar/gkab1028).
16. Foroutan M, Bhuva DD, Lyu R, et al. Single sample scoring of molecular phenotypes. *BMC Bioinformatics* 2018;19(1):404. doi:[10.1186/s12859-018-2435-4](https://doi.org/10.1186/s12859-018-2435-4).
17. Liberzon A, Subramanian A, Pinchback R, et al. Molecular signatures database (MSigDB) 3.0. *Bioinformatics* 2011;27(12):1739–1740. PMID [21546393](https://pubmed.ncbi.nlm.nih.gov/21546393/).
18. Dolgalev I. msigdbr: MSigDB gene sets for multiple organisms in a tidy data format. R package. [CRAN](https://cran.r-project.org/web/packages/msigdbr/index.html).
19. Schäfer J, Strimmer K. A shrinkage approach to large-scale covariance matrix estimation and implications for functional genomics. *Stat Appl Genet Mol Biol* 2005;4:Article32. PMID [16646851](https://pubmed.ncbi.nlm.nih.gov/16646851/).
20. Kuijjer ML, Tung MG, Yuan G, Quackenbush J, Glass K. Estimating sample-specific regulatory networks. *iScience* 2019;14:226–240. PMID [30981959](https://pubmed.ncbi.nlm.nih.gov/30981959/).
21. Tukey JW. Bias and confidence in not-quite large samples (abstract). *Ann Math Stat* 1958;29(2):614.
22. Ahn S, Grimes T, Datta S. A pseudo-value regression approach for differential network analysis of co-expression data. *BMC Bioinformatics* 2023;24(1):8. PMID [36624383](https://pubmed.ncbi.nlm.nih.gov/36624383/).
23. Liu X, et al. Personalized characterization of diseases using sample-specific networks. *Nucleic Acids Res* 2016. PMID [27596597](https://pubmed.ncbi.nlm.nih.gov/27596597/).
24. Huang Y, et al. Disease characterization using a partial correlation-based sample-specific network. *Brief Bioinform* 2021. PMID [32422654](https://pubmed.ncbi.nlm.nih.gov/32422654/).
25. Kuijjer ML, et al. lionessR: single sample network inference in R. *BMC Cancer* 2019. PMID [31653243](https://pubmed.ncbi.nlm.nih.gov/31653243/).
26. Zhang B, Horvath S. A general framework for weighted gene co-expression network analysis. *Stat Appl Genet Mol Biol* 2005;4:Article17. doi:[10.2202/1544-6115.1128](https://doi.org/10.2202/1544-6115.1128).
27. Costantini G, Perugini M. Generalization of clustering coefficients to signed correlation networks. *PLoS One* 2014;9(2):e88669. doi:[10.1371/journal.pone.0088669](https://doi.org/10.1371/journal.pone.0088669).
28. Zou H, Hastie T. Regularization and variable selection via the elastic net. *J R Stat Soc Series B Stat Methodol* 2005;67(2):301–320. doi:[10.1111/j.1467-9868.2005.00503.x](https://doi.org/10.1111/j.1467-9868.2005.00503.x).
29. Breiman L. Random forests. *Mach Learn* 2001;45:5–32. doi:[10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324).
30. Chen T, Guestrin C. XGBoost: a scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* 2016:785–794. doi:[10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785).
31. Cortes C, Vapnik V. Support-vector networks. *Mach Learn* 1995;20:273–297. doi:[10.1007/BF00994018](https://doi.org/10.1007/BF00994018).
32. Friedman JH. Regularized discriminant analysis. *J Am Stat Assoc* 1989;84(405):165–175. doi:[10.2307/2289860](https://doi.org/10.2307/2289860).
33. Langfelder P, Horvath S. WGCNA: an R package for weighted correlation network analysis. *BMC Bioinformatics* 2008;9:559. PMID [19114008](https://pubmed.ncbi.nlm.nih.gov/19114008/).
34. Yuan M, Lin Y. Model selection and estimation in regression with grouped variables. *J R Stat Soc Series B Stat Methodol* 2006;68(1):49–67. doi:[10.1111/j.1467-9868.2005.00532.x](https://doi.org/10.1111/j.1467-9868.2005.00532.x).
35. Meinshausen N, Bühlmann P. Stability selection. *J R Stat Soc Series B Stat Methodol* 2010;72(4):417–473. doi:[10.1111/j.1467-9868.2010.00740.x](https://doi.org/10.1111/j.1467-9868.2010.00740.x).
36. Platt J. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In: Smola AJ, et al., editors. *Advances in Large Margin Classifiers*. MIT Press; 1999.
37. Bates S, Hastie T, Tibshirani R. Cross-validation: what does it estimate and how well does it do it? *J Am Stat Assoc* 2024;119(546):1434–1445. doi:[10.1080/01621459.2023.2197686](https://doi.org/10.1080/01621459.2023.2197686).
38. Nadeau C, Bengio Y. Inference for the generalization error. *Mach Learn* 2003;52:239–281. doi:[10.1023/A:1024068626366](https://doi.org/10.1023/A:1024068626366).
39. Grimes T, Potter SS, Datta S. Integrating gene regulatory pathways into differential network analysis of gene expression data. *Sci Rep* 2019;9:5479. PMID [30940863](https://pubmed.ncbi.nlm.nih.gov/30940863/).
40. Freedman D, Lane D. A nonstochastic interpretation of reported significance levels. *J Bus Econ Stat* 1983;1(4):292–298. doi:[10.1080/07350015.1983.10509354](https://doi.org/10.1080/07350015.1983.10509354).
41. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *J R Stat Soc Series B Stat Methodol* 1995;57(1):289–300. doi:[10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
42. Schwarz G. Estimating the dimension of a model. *Ann Stat* 1978;6(2):461–464. doi:[10.1214/aos/1176344136](https://doi.org/10.1214/aos/1176344136).

## Supplementary material

<a id="supp-s1"></a>

### Supplementary Section S1. Simulation details

**Resampling design.** The female healthy controls of [GSE319130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130) were randomly divided into two groups of about 38 samples, labelled pseudo-patients and pseudo-controls, and the known signal of each scenario was added to the pseudo-patients only. This design keeps the exact noise, skewness and correlation of real blood data.

**How the scenarios were generated.** In S1, a constant was added to the mean of 20% of the genes of a sub-pathway. In S2, the deviations of all genes from the patient mean were multiplied by a common factor greater than 1, which increases spread without changing correlations. In S3, half of the pseudo-patients were shifted upwards and half downwards on 20% of the genes, so that the average was unchanged. In S4, 10% of the gene pairs had their partial correlations reversed in sign, removed or created, giving a new correlation matrix $`\mathbf{R}_{\mathrm{R}}`$, adjusted where necessary to remain a valid correlation matrix. In the generative design, pseudo-patients were drawn from equation (31) with $`\mathbf{R}_{\mathrm{R}}`$ in place of $`\hat{\mathbf{R}}`$. In the resampling design, they were transformed to the new structure by

```math
\mathbf{x}^{\mathrm{R}} = \boldsymbol{\mu} + \mathbf{D}_{\sigma}\, \mathbf{R}_{\mathrm{R}}^{1/2}\, \hat{\mathbf{R}}^{-1/2}\, \mathbf{D}_{\sigma}^{-1} \big(\mathbf{x} - \boldsymbol{\mu}\big) \qquad\qquad (\mathrm{S}1)
```

where $`\mathbf{x}`$ is a pseudo-patient's expression vector, $`\boldsymbol{\mu}`$ the vector of gene means, $`\mathbf{D}_{\sigma}`$ the diagonal matrix of gene standard deviations, and the powers $`1/2`$ and $`-1/2`$ the symmetric matrix square root and its inverse; this changes the correlations exactly while keeping the means and variances. In S5, simulated patients with high IFN activity had the expression of the interferon genes reduced by a common factor, which lowered their IFN score below the cutoff while leaving the correlations of the IFN-high state in place. In S6, patients and controls differed only in the distribution of $`f`$ in equation (32).

**Repeats and computation.** Each setting was repeated 200 times when a single sub-pathway was analysed and 100 times when the full pipeline over all sub-pathways was run, giving Monte Carlo standard errors of at most 0.035 and 0.05 for estimated proportions; these are reported with every estimate. The generative design was run at both sample sizes, and the resampling design at the largest size the controls allow. The full-pipeline runs used one repeat of 5 outer folds instead of ten, with all other steps unchanged. LIONESS used $`B = 20`$ balanced reference subsets and both association measures, as in the real analysis.

**Checking the simulated data.** For each sub-pathway, simulated data without added signal were compared with the real controls in four respects: the mean and variance of each gene, the distribution of all pairwise correlations, the distribution of the LIONESS edges, and, for equation (32), the distribution of the IFN score and the proportion of patients below the cutoff. The simulated and real distributions are shown overlaid.

**Agreement with the theory.** The exact LIONESS edges were compared with the first-order formulas of [Section 2.6](#sec-2-6) in every scenario.

**Pilot simulation.** A smaller pilot, run while the study was being designed, used multivariate normal data for single pathways of 10, 20 and 30 genes with 20 to 30 repeats per setting. Its results guided the choice of network features ([Section 2.8](#sec-2-8)) and population-level tests ([Section 2.12](#sec-2-12)); its code and results are archived with the analysis code. The full simulation replaces it for all inferences.
