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

All data were obtained from public whole-blood transcriptomic studies of systemic lupus erythematosus (SLE) deposited in the Gene Expression Omnibus (GEO) [[1]](https://pubmed.ncbi.nlm.nih.gov/23193258/). A study was eligible if it profiled peripheral whole blood, included either healthy controls (HC) or patients with another autoimmune disease, and provided enough sample annotation to infer sex and to separate patients from controls. The cohorts that met these criteria, and the role each plays in the analysis, are summarized in Table 1.

Two large cohorts were candidates for the primary analysis. [GSE319130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319130) is an RNA-sequencing study of 720 SLE patients and 84 HC, of whom 679 patients and 77 controls are female [[2]](https://pubmed.ncbi.nlm.nih.gov/42039161/). [GSE88884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE88884) was generated on the Affymetrix Human Transcriptome Array 2.0 and contains baseline blood samples from 1,760 SLE patients enrolled in the ILLUMINATE-1 and ILLUMINATE-2 phase III trials of tabalumab, together with 60 HC [[3]](https://pubmed.ncbi.nlm.nih.gov/27723281/). Their size makes them the only cohorts likely to contain enough IFN-low patients for a well-powered comparison with controls.

Four smaller cohorts were included because each answers a question the primary cohorts cannot. [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169) profiled 82 SLE patients, 84 patients with rheumatoid arthritis (RA) and 77 HC in a single study with recorded glucocorticoid use [[4]](https://pubmed.ncbi.nlm.nih.gov/29534336/), which allows IFN-low SLE to be compared with another autoimmune disease rather than only with health. [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) followed 158 children with SLE over repeated visits with disease-activity scores, alongside 46 HC [[5]](https://pubmed.ncbi.nlm.nih.gov/27040498/), and makes it possible to observe whether patients move between IFN-low and IFN-high states over time. [GSE99967](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE99967) includes SLE patients with and without biopsy-confirmed active lupus nephritis (LN) as well as HC [[6]](https://pmc.ncbi.nlm.nih.gov/articles/PMC5942792/), and supports a comparison of renal and non-renal disease. [GSE224705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705) records prednisone dose for each patient [[7]](https://pubmed.ncbi.nlm.nih.gov/38260685/) and was used to examine how treatment relates to the transcriptomic signal. The PRECISESADS cohort, which covers seven systemic autoimmune diseases and matched controls under controlled access [[8]](https://pubmed.ncbi.nlm.nih.gov/?term=Barturen+Integrative+analysis+molecular+stratification+systemic+autoimmune+diseases), will be added if access is granted.

Public SLE series frequently reuse the same patients, and the same individual appearing in both training and test data would inflate performance. [GSE72326](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE72326) duplicates [GSE49454](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE49454) and was not used, and because [GSE45291](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE45291), [GSE121239](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121239) and [GSE224705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705) share patients and controls, no analysis used more than one of these three series. Within each cohort, a single sample was kept per patient, taken from the first visit in longitudinal studies, and technical replicates were averaged.

Whether a cohort could support the primary analysis was decided by a feasibility (go/no-go) check carried out before registration and before any model was fitted to the outcome. For each cohort, we counted IFN-low patients and controls by inferred sex (Section 2.4) and tabulated batch, age, ancestry and medication by group. A cohort qualified as a primary cohort if it contained at least 80 female IFN-low patients and 60 female controls, and if batch was not confounded with group, meaning that patients and controls had not been processed in separate batches. At these sample sizes, the 95% confidence interval for an area under the receiver operating characteristic curve (AUC) of 0.70 has a half-width of about ±0.085 based on the standard error of Hanley and McNeil [[9]](https://pubmed.ncbi.nlm.nih.gov/7063747/). Cohorts with at least 25 patients per group, for which the half-width is about ±0.15, qualified as replication cohorts and were reported descriptively. Fixing these rules in advance ensured that the choice of cohorts could not be influenced by the results.

### 2.2 Pre-processing and harmonization

Each cohort was processed separately, and no batch correction was applied across cohorts. Affymetrix arrays were re-processed from the raw files with robust multi-array averaging (RMA) [[10]](https://pubmed.ncbi.nlm.nih.gov/12925520/) where raw files were available; otherwise, the normalized data supplied by the submitters were used. For RNA-sequencing data, lowly expressed genes were removed with the `filterByExpr` function of edgeR [[11]](https://pubmed.ncbi.nlm.nih.gov/19910308/), [[13]](https://pubmed.ncbi.nlm.nih.gov/27508061/), and counts were normalized by the trimmed mean of M-values (TMM) method [[12]](https://pubmed.ncbi.nlm.nih.gov/20196867/) and converted to log counts per million (log-CPM). Probes were mapped to gene symbols within each platform. Where several probes mapped to the same gene, the probe with the highest variance in the training fold was kept. For analyses that compared cohorts, pathways were restricted to the genes measured in all cohorts involved, and the gene coverage of each pathway is reported. Before network estimation, each gene was winsorized at ±4 standard deviations (SD), using means and SDs estimated in the training fold, to limit the influence of outlying values on the correlation estimates.

### 2.3 IFN score and IFN-low definition

Interferon (IFN) activity was measured with a score built from four interferon-stimulated genes, IFI27, IFI44, IFI44L and RSAD2. This panel is used in clinical trials of type I IFN blockade to divide patients into IFN-high and IFN-low groups [[14]](https://pubmed.ncbi.nlm.nih.gov/31660791/). To place every sample on the scale of healthy blood, the expression of each gene was standardized against the healthy controls of the training fold,

$$z_{gs} = \frac{x_{gs} - \bar{x}_g^{\mathrm{HC}}}{s_g^{\mathrm{HC}}}, \tag{1}$$

where $x_{gs}$ is the expression of gene $g$ in sample $s$, and $\bar{x}_g^{\mathrm{HC}}$ and $s_g^{\mathrm{HC}}$ are the mean and SD of that gene among the training-fold controls. The IFN score of a sample was then the mean of its four standardized values,

$$S_s = \frac{1}{4} \sum_{g \in \mathcal{G}_{\mathrm{IFN}}} z_{gs}, \qquad \mathcal{G}_{\mathrm{IFN}} = \{\mathrm{IFI27}, \mathrm{IFI44}, \mathrm{IFI44L}, \mathrm{RSAD2}\}. \tag{2}$$

Samples were classified as IFN-low when their score lay within two SD above the control mean,

$$S_s \le c, \qquad c = \bar{S}^{\mathrm{HC}} + 2\, s_S^{\mathrm{HC}}, \tag{3}$$

where $\bar{S}^{\mathrm{HC}}$ and $s_S^{\mathrm{HC}}$ are the mean and SD of the score among the training-fold controls. Because the cutoff $c$ depends on the data, it was estimated within each training fold and then applied, without change, to the test samples of that fold. Controls were filtered by the same rule, which removed about 2.5% of them, so that patients and controls entered the analysis on an equal footing. A stricter cutoff, $c = \bar{S}^{\mathrm{HC}} + s_S^{\mathrm{HC}}$, was examined in a sensitivity analysis.

No cutoff can make IFN-low patients identical to controls in IFN activity, since patients who fall just below it may still carry a mildly raised signature. For this reason, the residual IFN score was kept as a baseline model that every other model had to outperform (Section 2.9). To stop the network features from simply re-measuring IFN activity, the four score genes and all genes in the Reactome *Interferon Signaling* subtree (R-HSA-913531) [[15]](https://doi.org/10.1093/nar/gkab1028) were removed from them; a sensitivity analysis restored the subtree.

Treatment may also shape IFN status. Hydroxychloroquine and immunosuppressants can lower the IFN signature, so some patients classified as IFN-low may be IFN-high patients whose signature has been suppressed. In the cohorts with medication records ([GSE224705](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224705), [GSE65391](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65391) and [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169)), we therefore compared the proportion of IFN-low patients between treated and untreated patients, and in GSE65391 we described how individual patients moved between IFN states across visits.

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


1. Barrett T, Wilhite SE, Ledoux P, et al. NCBI GEO: archive for functional genomics data sets—update. *Nucleic Acids Res* 2013;41(Database issue):D991–D995. PMID [23193258](https://pubmed.ncbi.nlm.nih.gov/23193258/). 
2. Masson HO, et al. XIST expression and hypermethylation of the X chromosome in males with systemic lupus erythematosus. *Front Immunol* 2026. PMID [42039161](https://pubmed.ncbi.nlm.nih.gov/42039161/).
3. Hoffman RW, et al. Gene expression and pharmacodynamic changes in 1,760 systemic lupus erythematosus patients from two phase III trials of BAFF blockade with tabalumab. *Arthritis Rheumatol* 2017. PMID [27723281](https://pubmed.ncbi.nlm.nih.gov/27723281/).
4. Hu Y, et al. Development of a molecular signature to monitor pharmacodynamic responses mediated by in vivo administration of glucocorticoids. *Arthritis Rheumatol* 2018. PMID [29534336](https://pubmed.ncbi.nlm.nih.gov/29534336/).
5. Banchereau R, et al. Personalized immunomonitoring uncovers molecular networks that stratify lupus patients. *Cell* 2016. PMID [27040498](https://pubmed.ncbi.nlm.nih.gov/27040498/).
6. Wither JE, et al. Identification of a neutrophil-related gene expression signature that is enriched in adult systemic lupus erythematosus patients with active nephritis: clinical/pathologic associations and etiologic mechanisms. *PLoS One* 2018. [PMC5942792](https://pmc.ncbi.nlm.nih.gov/articles/PMC5942792/). 
7. López-Domínguez R, et al. Immune and molecular landscape behind non-response to mycophenolate mofetil and azathioprine in lupus nephritis therapy. *Res Sq* 2024 (preprint). PMID [38260685](https://pubmed.ncbi.nlm.nih.gov/38260685/).
8. Barturen G, et al. Integrative analysis reveals a molecular stratification of systemic autoimmune diseases. *Arthritis Rheumatol* 2021. [PubMed search](https://pubmed.ncbi.nlm.nih.gov/?term=Barturen+Integrative+analysis+molecular+stratification+systemic+autoimmune+diseases). 
9. Hanley JA, McNeil BJ. The meaning and use of the area under a receiver operating characteristic (ROC) curve. *Radiology* 1982;143(1):29–36. PMID [7063747](https://pubmed.ncbi.nlm.nih.gov/7063747/). 
10. Irizarry RA, Hobbs B, Collin F, et al. Exploration, normalization, and summaries of high density oligonucleotide array probe level data. *Biostatistics* 2003;4(2):249–264. PMID [12925520](https://pubmed.ncbi.nlm.nih.gov/12925520/).
11. Robinson MD, McCarthy DJ, Smyth GK. edgeR: a Bioconductor package for differential expression analysis of digital gene expression data. *Bioinformatics* 2010;26(1):139–140. PMID [19910308](https://pubmed.ncbi.nlm.nih.gov/19910308/).
12. Robinson MD, Oshlack A. A scaling normalization method for differential expression analysis of RNA-seq data. *Genome Biol* 2010;11(3):R25. PMID [20196867](https://pubmed.ncbi.nlm.nih.gov/20196867/).
13. Chen Y, Lun ATL, Smyth GK. From reads to genes to pathways: differential expression analysis of RNA-Seq experiments using Rsubread and the edgeR quasi-likelihood pipeline. *F1000Res* 2016;5:1438. PMID [27508061](https://pubmed.ncbi.nlm.nih.gov/27508061/).
14. Brohawn PZ, et al. Type I interferon gene signature test-low and -high patients with systemic lupus erythematosus have distinct gene expression signatures. *Lupus* 2019. PMID [31660791](https://pubmed.ncbi.nlm.nih.gov/31660791/).
15. Gillespie M, Jassal B, Stephan R, et al. The reactome pathway knowledgebase 2022. *Nucleic Acids Res* 2022;50(D1):D687–D692. doi:[10.1093/nar/gkab1028](https://doi.org/10.1093/nar/gkab1028).

## Supplementary material

