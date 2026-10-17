# Progress draft

**Status:** skeleton only. Sections are added one at a time.

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

All data were obtained from public whole-blood transcriptomic studies of systemic lupus erythematosus (SLE) deposited in the Gene Expression Omnibus (GEO) [[1]](https://pubmed.ncbi.nlm.nih.gov/23193258/). A study was eligible if it profiled peripheral whole blood, included either healthy controls (HC) or patients with another autoimmune disease, and provided enough sample annotation to infer sex and to separate patients from controls. The cohorts that met these criteria, and the role of each in the analysis, are summarized in Table 1.

[GSE319130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130) served as the primary cohort. It is an RNA-sequencing study of 720 SLE patients and 84 HC, of whom 679 patients and 77 controls are female [[2]](https://pubmed.ncbi.nlm.nih.gov/42039161/), and it is the only cohort expected to have enough female controls to meet the primary-cohort criteria described below. [GSE88884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE88884) was generated on the Affymetrix Human Transcriptome Array 2.0 and contains baseline blood samples from 1,760 SLE patients enrolled in the ILLUMINATE-1 and ILLUMINATE-2 phase III trials of tabalumab [[3]](https://pubmed.ncbi.nlm.nih.gov/27723281/). It contains 60 HC in total, so it could meet the requirement of 60 female controls for a primary cohort only if every control were female and none were removed by the IFN filter (Section 2.3); GSE88884 was therefore treated as a replication cohort.

Four smaller cohorts were included because each answers a question the primary cohort cannot. [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169) profiled 82 SLE patients, 84 patients with rheumatoid arthritis (RA) and 77 HC in a single study with recorded glucocorticoid use [[4]](https://pubmed.ncbi.nlm.nih.gov/29534336/), which allows IFN-low SLE to be compared with another autoimmune disease rather than only with health. [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) followed 158 children with SLE over repeated visits with disease-activity scores, alongside 46 HC [[5]](https://pubmed.ncbi.nlm.nih.gov/27040498/), and makes it possible to observe whether patients move between IFN-low and IFN-high states over time. [GSE99967](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE99967) includes adult SLE patients with and without active lupus nephritis (LN) as well as HC [[6]](https://pubmed.ncbi.nlm.nih.gov/29742110/), and [GSE224705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705) records the prednisone dose of each patient [[7]](https://pubmed.ncbi.nlm.nih.gov/38260685/). Because these last two cohorts contain fewer than 25 HC, neither was used for comparisons with controls: GSE99967 contributed only a descriptive comparison of patients with and without LN, and GSE224705 contributed only analyses of treatment within patients. The PRECISESADS cohort, which covers seven systemic autoimmune diseases and controls under controlled access [[8]](https://pubmed.ncbi.nlm.nih.gov/?term=Barturen+Integrative+analysis+molecular+stratification+systemic+autoimmune+diseases), was to be included only if access was granted before the analysis was registered.

Public SLE series frequently reuse the same patients, and the same individual appearing in both training and test data would inflate performance. Overlap between series was checked by comparing GEO sample identifiers, sample titles and recorded patient characteristics such as age, sex and visit date. [GSE72326](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72326) duplicates [GSE49454](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE49454) and was not used. [GSE45291](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE45291), [GSE121239](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121239) and GSE224705 share patients and controls; of these three, only GSE224705 was used, because it records prednisone dose. Within each cohort, a single sample was kept per patient, taken from the first visit in longitudinal studies, and technical replicates were averaged.

Whether a cohort could support the primary analysis was decided by a feasibility (go/no-go) check carried out before registration and before any model was fitted to the outcome. For each cohort, IFN-low patients and controls were counted by inferred sex (Section 2.4), and batch, age, ancestry and medication were tabulated by group. A cohort qualified as a primary cohort if it contained at least 80 female IFN-low patients and 60 female controls, and if batch was not confounded with group, meaning that patients and controls had not been processed in separate batches. Cohorts with at least 25 patients per group qualified as replication cohorts and were reported descriptively. As a rough guide to precision, the 95% confidence interval for an area under the receiver operating characteristic curve (AUC) of 0.70 has a half-width of about ±0.085 at the primary-cohort minimum and about ±0.15 at the replication minimum, based on the standard error of Hanley and McNeil [[9]](https://pubmed.ncbi.nlm.nih.gov/7063747/). These figures assume a single independent test set; the inference used for the actual model comparisons accounts for cross-validation and is described in Section 2.11. Fixing these rules in advance ensured that the choice of cohorts could not be influenced by the results.

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

### 2.2 Pre-processing and harmonization

Each cohort was processed separately, and no batch correction was applied across cohorts. Affymetrix arrays were re-processed from the raw files with robust multi-array averaging (RMA) [[10]](https://pubmed.ncbi.nlm.nih.gov/12925520/) where raw files were available; otherwise, the normalized data supplied by the submitters were used. Illumina BeadChip data (GSE65391) were taken as the submitters' normalized values and log2-transformed where this had not already been done. For RNA-sequencing data, lowly expressed genes were removed with the `filterByExpr` function of edgeR [[11]](https://pubmed.ncbi.nlm.nih.gov/19910308/), [[12]](https://f1000research.com/articles/5-1438). Because this filter can use the group labels, it was applied within each training fold, and the resulting gene list was applied unchanged to the corresponding test fold, so that test samples could not influence which genes were kept. Counts were then normalized by the trimmed mean of M-values (TMM) method [[13]](https://pubmed.ncbi.nlm.nih.gov/20196867/) and converted to log counts per million (log-CPM).

Probes were mapped to gene symbols within each platform. Where several probes mapped to the same gene, the probe with the highest variance in the training fold was kept. Known technical batches within a cohort, such as the two ILLUMINATE trials in GSE88884, were not removed by correction; instead, cross-validation folds were stratified by batch, and batch was included as an adjustment covariate in the population-level tests (Section 2.12). For analyses that compared cohorts, pathways were restricted to the genes measured in all cohorts involved, and the gene coverage of each pathway is reported. Before network estimation, each gene was winsorized at ±4 standard deviations (SD), using means and SDs estimated in the training fold, to limit the influence of outlying values on the correlation estimates.

### 2.3 IFN score and IFN-low definition

#### 2.3.1 IFN score

Interferon (IFN) activity was measured with a score built from four interferon-stimulated genes: IFI27, IFI44, IFI44L and RSAD2. This panel is used in clinical trials of type I IFN blockade to divide patients into IFN-high and IFN-low groups [[14]](https://pubmed.ncbi.nlm.nih.gov/31660791/). To place every sample on the scale of healthy blood, the expression of each gene was first standardized against the healthy controls (HC) of the training fold:

```math
z_{gi} = \frac{x_{gi} - \hat{\mu}_g^{\mathrm{HC}}}{\hat{\sigma}_g^{\mathrm{HC}}} \qquad\qquad (1)
```

Here, $`x_{gi}`$ is the expression of gene $`g`$ in sample $`i`$, and $`\hat{\mu}_g^{\mathrm{HC}}`$ and $`\hat{\sigma}_g^{\mathrm{HC}}`$ are the mean and standard deviation (SD) of that gene among the training-fold controls. The IFN score of a sample is the mean of its four standardized values:

```math
S_i = \frac{1}{4} \sum_{g \in \mathcal{G}_{\mathrm{IFN}}} z_{gi}, \qquad \mathcal{G}_{\mathrm{IFN}} = \lbrace \mathrm{IFI27},\;\mathrm{IFI44},\;\mathrm{IFI44L},\;\mathrm{RSAD2} \rbrace \qquad\qquad (2)
```

#### 2.3.2 IFN-low cutoff

A sample was classified as IFN-low when its score lay no more than two SD above the control mean:

```math
S_i \le c, \qquad c = \hat{\mu}_S^{\mathrm{HC}} + 2\,\hat{\sigma}_S^{\mathrm{HC}} \qquad\qquad (3)
```

Here, $`\hat{\mu}_S^{\mathrm{HC}}`$ and $`\hat{\sigma}_S^{\mathrm{HC}}`$ are the mean and SD of the score among the training-fold controls. The clinical-trial assay is a qualitative polymerase chain reaction (PCR) test with its own fixed threshold [[14]](https://pubmed.ncbi.nlm.nih.gov/31660791/), which cannot be transferred to microarray or sequencing data. The cutoff was therefore defined relative to the healthy controls of each cohort, a rule that can be applied in the same way on every platform.

Because the cutoff $`c`$ depends on the data, it was estimated within each training fold and then applied, without change, to the test samples of that fold. Controls were filtered by the same rule, so that patients and controls entered the analysis on an equal footing; if the score were normally distributed among controls, this would remove about 2.3% of them. The cutoff is estimated from a modest number of controls (about 60 per training fold in the primary cohort), so its value varies between folds; this variation, and the number of patients classified as IFN-low in each fold, are reported. A stricter cutoff, $`c = \hat{\mu}_S^{\mathrm{HC}} + \hat{\sigma}_S^{\mathrm{HC}}`$, was examined in a sensitivity analysis.

#### 2.3.3 Residual IFN signal

No cutoff can make IFN-low patients identical to controls in IFN activity, since patients who fall just below it may still carry a mildly raised signature. The residual IFN score was therefore kept as a baseline model that every other model had to outperform (Section 2.9). To stop the network features from simply re-measuring type I IFN activity, the four score genes and all genes in the Reactome *Interferon alpha/beta signaling* pathway (R-HSA-909733) [[15]](https://doi.org/10.1093/nar/gkab1028) were removed from them. Genes in the *Interferon gamma signaling* pathway (R-HSA-877300) were retained, because type II IFN acts through a pathway distinct from the type I signal that defines the IFN-low group, and removing it would discard biology that the network analysis is intended to examine. A sensitivity analysis removed the whole *Interferon Signaling* subtree (R-HSA-913531).

#### 2.3.4 Treatment and IFN status

Hydroxychloroquine and immunosuppressants can lower the IFN signature, so some patients classified as IFN-low may be IFN-high patients whose signature has been suppressed by treatment. In the cohorts with medication records ([GSE224705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705), [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) and [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169)), the proportion of IFN-low patients was compared between patients with and without each recorded treatment. In GSE65391, which follows patients over time, the movement of individual patients between IFN states across visits was also described.

### 2.4 Confounding control

Differences between IFN-low patients and controls could arise from factors other than disease. Five such factors were addressed: sex, batch, treatment, cell composition, and age and ancestry. Each was handled either by the study design or by an explicit baseline model and adjustment covariate.

The first factor, sex, was inferred from the expression of Y-chromosome genes (RPS4Y1, DDX3Y, KDM5D, UTY and EIF1AY) rather than from XIST, because XIST expression is unreliable for this purpose in SLE: in GSE319130, 54% of male patients (22 of 41) showed elevated XIST expression [[2]](https://pubmed.ncbi.nlm.nih.gov/42039161/). Inferred sex was compared with reported sex where it was available. The primary analysis was restricted to females. X-chromosome genes were retained, because removing them would delete immune genes located on the X chromosome, such as TLR7, CXCR3, CD40LG and FOXP3. A sensitivity analysis included both sexes after removing the Y-chromosome genes and XIST/TSIX.

Batch effects were controlled mainly by design. Cohorts in which patients and controls had been processed in separate batches were not eligible as primary cohorts (Section 2.1). Within eligible cohorts, cross-validation folds were stratified by batch, batch was included as an adjustment covariate in the population-level tests (Section 2.2), and the distribution of batches by group is reported.

Treatment was the third factor. Glucocorticoids change blood gene expression and could therefore create differences between patients and controls that are unrelated to disease. A glucocorticoid-response score was computed for each sample with singscore [[16]](https://doi.org/10.1186/s12859-018-2435-4) from the 64 genes that Hu et al. found to be up-regulated by glucocorticoids [[4]](https://pubmed.ncbi.nlm.nih.gov/29534336/). The score served three purposes: as a baseline model (M0b, Section 2.9), to define a sensitivity analysis in which its genes were removed from the network features, and as an adjustment covariate in the population-level tests. In cohorts that recorded steroid use or dose, we checked that the score was associated with the recorded treatment. Where medication was not recorded for each patient, treatment exposure could be estimated only through this score.

Cell composition required particular care, because gene co-expression in whole blood is strongly influenced by differences in the proportions of blood cell types between samples. For each sample, singscore [[16]](https://doi.org/10.1186/s12859-018-2435-4) was used to score marker gene sets for neutrophils, monocytes, B cells, plasmablasts, T cells, natural killer cells and eosinophils, with the marker sets fixed before analysis. Because each score uses only the sample being scored, it cannot carry information between training and test data. The cell-type scores served as a baseline model, as additional conditioning variables in the partial correlations (Section 2.7) and as adjustment covariates in the population-level tests.

Finally, age and recorded race or ancestry were tabulated by group and used both as a baseline model and as adjustment covariates. A sensitivity analysis restricted the data to the age range shared by patients and controls. The paediatric cohort ([GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391)) was analysed separately from the adult cohorts.

### 2.5 Pathways

Gene sets were taken from the Molecular Signatures Database (MSigDB) [[17]](https://pubmed.ncbi.nlm.nih.gov/21546393/), accessed in R through the msigdbr package [[18]](https://cran.r-project.org/web/packages/msigdbr/index.html), and the database version was recorded. The interferon pathway used in this study, REACTOME INTERFERON SIGNALING, corresponds to the Reactome *Interferon Signaling* pathway (R-HSA-913531) [[15]](https://doi.org/10.1093/nar/gkab1028), which covers both type I (alpha/beta) and type II (gamma) IFN signalling. Because its genes largely define IFN status, this pathway was used only in the positive-control comparison of IFN-high patients with healthy controls (Section 2.10), where a network difference is expected, and not in the comparison of IFN-low patients with controls. A clear signal in the positive control shows that the pipeline can detect a network difference when one is known to exist; without it, a null result in IFN-low patients could not be interpreted.

For the comparisons involving IFN-low patients, pathways were drawn from the Reactome *Immune System* subtree (R-HSA-168256), excluding the *Interferon alpha/beta signaling* pathway in line with Section 2.3. Partial correlations become unstable as the number of genes approaches the number of samples, so each network was limited to between 15 and 50 genes after filtering. This keeps the number of genes well below the smallest training set expected in a primary cohort, about 110 samples per fold (80% of 80 IFN-low patients and 60 controls). Pathways with more than 50 genes, including REACTOME INTERFERON SIGNALING, were replaced by their Reactome sub-pathways; sub-pathways that still exceeded 50 genes were restricted to the 50 genes with the highest variance in the training fold, and pathways with fewer than 15 genes were removed. Near-duplicate pathways, defined as pairs with a Jaccard index of gene overlap above 0.8, were reduced to a single representative. A secondary analysis used all Reactome pathways that met the same size criteria. All gene lists were archived with the analysis code.

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

**Conditional residuals.** Let $`\mathbf{u} = \boldsymbol{\Omega}\mathbf{d}`$ and

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

where $`\mathbf{D}_d = \mathrm{diag}(d_1^2, \ldots, d_G^2)`$ and $`\tilde{M}_{ij} = M_{ij} / \sqrt{\Omega_{ii}\,\Omega_{jj}}`$. The matrix $`\mathbf{M}`$ mixes the products of residuals, $`\mathbf{u}\mathbf{u}^{\top}`$, with a term built from the squared deviations of the individual genes, in proportions set by $`\lambda`$. Equation (9) reduces to equation (8) when $`\lambda = 0`$, and with shrinkage the edge is still made only of products and squares of the sample's deviations.

**Pearson analogue.** For Pearson correlation $`r_{ij}`$ and standardized expression values $`z_i`$, the same expansion gives

```math
e_{ij}^{(q)} \approx z_i\,z_j + r_{ij}\left(1 - \frac{z_i^2 + z_j^2}{2}\right) \qquad\qquad (10)
```

**Result 3 (SSN is an exact rescaling of LIONESS).** The sample-specific network (SSN) method defines an edge as the change in an association measure $`c`$ when sample $`q`$ is added to a reference set $`R`$ of $`n`$ samples, $`\Delta_{ij}^{(q)} = c_{ij}(R \cup \{q\}) - c_{ij}(R)`$ [[23]](https://pubmed.ncbi.nlm.nih.gov/27596597/). LIONESS with the same reference gives $`e_{ij}^{(q)} = (n+1)\,c_{ij}(R \cup \{q\}) - n\,c_{ij}(R)`$, so

```math
\Delta_{ij}^{(q)} = \frac{e_{ij}^{(q)} - c_{ij}(R)}{n+1} \qquad\qquad (11)
```

exactly, for any association measure. Equations (8)–(10) therefore also describe SSN and its partial-correlation version, P-SSN [[24]](https://pubmed.ncbi.nlm.nih.gov/32422654/). Numerical checks on simulated data confirmed that equations (8)–(10) agree closely with exact LIONESS and that equation (11) holds exactly; the check code is provided with the analysis code.

**Predictions.** Equations (8)–(11) lead to six predictions.

*P1 (no new information).* Each edge is a fixed function of $`\mathbf{d}`$, so a network contains no information beyond the sample's own expression values within the pathway; it can only represent that information differently. Network models must therefore be compared with models built directly on pathway expression (Section 2.9). *P2 (quadratic classifier).* A linear model on a pathway's edges is a quadratic function of $`\mathbf{d}`$, so its natural competitor is a quadratic classifier on the pathway's expression values, such as regularized quadratic discriminant analysis. *P3 (mean and spread).* Because each edge is built from products and squares, changing the sign of a deviation does not change the edge. As a result, a group that differs from the other only in how widely its values are spread produces the same average edges, and, when the reference contains equal numbers of the two groups, so does a group that differs only in its mean expression. Edges are therefore expected to separate groups mainly when the genes co-vary differently. The pilot simulation confirmed this prediction. *P4 (opposite signs).* The squared terms carry a positive sign for partial correlation (equation 8) and a negative sign for Pearson correlation (equation 10), so unusual samples strengthen partial-correlation edges but weaken Pearson edges. Partial-correlation and Pearson LIONESS (models L2 and L2-P) can therefore behave differently on the same data. *P5 (node strength).* Node strength, the sum of a gene's edges, is approximately $`\tilde{u}_i \sum_{j \ne i} \tilde{u}_j`$ plus squared terms, and is therefore closely related to how far a sample lies from the healthy centre, the distance-from-health baseline (M4). *P6 (equivalence).* By equation (11), SSN, P-SSN and LIONESS differ edge by edge only by a fixed rescaling, so any difference in their performance must come from the network summaries or the choice of reference.

 All network features were computed with exact LIONESS (Section 2.7), and the agreement between exact and first-order edges on the real data, including in the tails of the distribution.

### 2.7 LIONESS estimation with Pearson and partial correlation

Single-sample networks were estimated with two association measures: Pearson correlation and partial correlation. Pearson correlation measures the overall association between two genes, including associations that arise because both genes are linked to other genes in the pathway. For genes $`i`$ and $`j`$ it is computed from the reference covariance matrix $`\mathbf{S}`$ as

```math
r_{ij} = \frac{S_{ij}}{\sqrt{S_{ii}\,S_{jj}}} \qquad\qquad (12)
```

Partial correlation, $`\rho_{ij}`$ in equation (5), measures the association between the two genes after removing the effect of all other genes in the pathway, so it is closer to a direct link. Using both measures with the same pipeline shows whether the choice of measure matters (models L2 and L2-P, Section 2.9); equations (8) and (10) predict that the two can behave differently, because unusual samples strengthen partial-correlation edges but weaken Pearson edges.

Every sample, whether patient or control and whether in a training or a test fold, was given a network by exactly the same rule, and the same rule was used for both measures. Section 2.6 showed that the composition of the reference determines what the edges respond to: when the reference contains more samples of one group, differences in mean expression also enter the edges, whereas with equal numbers of the two groups the edges mainly reflect how the genes co-vary. Class-balanced references were therefore used. Within each training fold, $`B = 20`$ reference subsets $`R_1, \ldots, R_B`$ were formed, each containing all training samples of the smaller class and an equal-sized random sample of the larger class.

For a sample $`q`$ and a reference subset $`R_b`$, let $`R = R_b \setminus \{q\}`$ be that subset with sample $`q`$ removed if it was a member. Writing $`c_{ij}`$ for either association measure, $`r_{ij}`$ or $`\rho_{ij}`$, the edge between genes $`i`$ and $`j`$ was

```math
e_{ij}^{(q,b)} = \big(|R| + 1\big)\,c_{ij}\big(R \cup \{q\}\big) - |R|\,c_{ij}(R) \qquad\qquad (13)
```

where $`|R|`$ is the number of samples in $`R`$ and $`c_{ij}(\cdot)`$ is the association estimated from the samples shown. When sample $`q`$ belongs to $`R_b`$, equation (13) is the leave-one-out form of LIONESS in equation (6); when it does not, as for every test sample, it is the add-one-in form. The final edge was the average over the $`B`$ subsets,

```math
e_{ij}^{(q)} = \frac{1}{B} \sum_{b=1}^{B} e_{ij}^{(q,b)} \qquad\qquad (14)
```

which reduces the variation that comes from the random choice of each reference subset.

The two measures differed only in how the association was estimated. Pearson correlations were computed directly from the covariance matrix by equation (12). Shrinkage was not applied to them, because shrinking the covariances towards zero while keeping the variances fixed, as in equation (4), would multiply every Pearson correlation by the same factor $`1-\lambda`$ and would not change the network structure. Partial correlations were computed by equation (5) from the shrinkage covariance of equation (4), because inverting the covariance matrix is unstable without it. The shrinkage intensity $`\lambda`$ was chosen in the inner cross-validation from 0.5, 1 and 2 times the analytic estimate of Schäfer and Strimmer [[19]](https://pubmed.ncbi.nlm.nih.gov/16646851/), and was then held fixed within the fold. Because each pathway contains at most 50 genes, the covariance matrix could be inverted directly. In the primary analysis, the cell-composition scores of Section 2.4 were added to the set of variables on which each partial correlation was conditioned, so that partial-correlation edges describe co-expression beyond what is explained by differences in blood cell proportions; a sensitivity analysis conditioned on the pathway genes only. Pearson edges, being unconditional, were not adjusted in this way, and this difference is part of what the comparison between the two measures examines.

The implementation was checked against direct recomputation of equation (13) for both measures, against the `pcor.shrink` function of the R package corpcor at a fixed $`\lambda`$ for partial correlation [[19]](https://pubmed.ncbi.nlm.nih.gov/16646851/), and against the lionessR package [[25]](https://pubmed.ncbi.nlm.nih.gov/31653243/), which implements the original LIONESS method [[20]](https://pubmed.ncbi.nlm.nih.gov/30981959/), for Pearson correlation.

### 2.8 Topology features

The same network features were computed from the Pearson and the partial-correlation LIONESS networks. LIONESS edges are signed, can lie outside the range $`[-1, 1]`$, and are present between every pair of genes, so each sample has a complete, weighted network for each pathway. For sample $`q`$ and a given pathway, let $`\mathbf{W}^{(q)}`$ be the $`G \times G`$ matrix of rescaled edges, with zeros on the diagonal and off-diagonal entries

```math
w_{ij}^{(q)} = \frac{e_{ij}^{(q)}}{\kappa} \qquad\qquad (15)
```

where $`\kappa`$ is the 99th percentile of $`|e_{ij}|`$ over all training samples and gene pairs of that pathway and association measure. Because the same factor $`\kappa`$ is used for every sample, the rescaling puts the edges on a common scale without removing genuine differences in edge size between samples. In what follows, the superscript $`(q)`$ is dropped, $`m = G(G-1)/2`$ is the number of gene pairs, and $`\mathbf{P}`$ is the reference network, the matrix of reference associations ($`r_{ij}`$ or $`\rho_{ij}`$) rescaled by the same $`\kappa`$ and with zeros on the diagonal. The features were organized in three tiers, fixed before the analysis: primary features, used in the main models; secondary features, used to examine hidden subgroups; and exploratory features, reported descriptively only.

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
\lambda_{1} = \max_{\|\mathbf{v}\| = 1} \mathbf{v}^{\top} \mathbf{W} \mathbf{v} \qquad\qquad (18)
```

which is large when many genes are connected in a single coordinated block. The fourth is the distance between the sample's network and the reference network,

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

The choice of tiers was guided by the pilot simulation (Section 2.13). The four primary features detected rewired gene pairs (AUC 0.69–0.79 across pathways of 10–30 genes), whereas a larger set of nine summary features did not (AUC about 0.50). Adding the gene strengths improved the detection of hidden subgroups (AUC up to 0.94 for Pearson networks) but slightly reduced the detection of rewiring, and adding the exploratory graph measures reduced performance for both. Per pathway and association measure, the primary set contains 4 features and the secondary set $`2G + 4`$ features.

### 2.9 Baseline and comparator models


#### 2.9.1 Baselines


#### 2.9.2 Expression-based comparators


#### 2.9.3 Established network comparators


#### 2.9.4 LIONESS models


#### 2.9.5 Primary comparison


### 2.10 Aggregation across pathways and contrasts

[Not yet written]

### 2.11 Validation and statistical inference

[Not yet written]

### 2.12 Population-level tests

[Not yet written]

### 2.13 Simulation study

[Not yet written]


## 3. Results

[Not yet written]

## 4. Discussion

[Not yet written]

## 5. Conclusion

[Not yet written]

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
32. Langfelder P, Horvath S. WGCNA: an R package for weighted correlation network analysis. *BMC Bioinformatics* 2008;9:559. PMID [19114008](https://pubmed.ncbi.nlm.nih.gov/19114008/).

## Supplementary material

