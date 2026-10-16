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

All models were fitted within the training folds only, used the same cross-validation splits and were scored in the same way, so that any difference in performance reflects the features rather than the set-up. The models fall into four groups.

#### 2.9.1 Baselines

Two baselines tested the simplest explanations for any separation between IFN-low patients and controls. The first (M0a) used the IFN score of Section 2.3 as its only feature, and asked whether residual IFN activity below the cutoff is enough to separate the groups. The second (M0b) used a glucocorticoid-response score built from the prednisolone-responsive genes of Hu et al. [[4]](https://pubmed.ncbi.nlm.nih.gov/29534336/), and asked whether the separation merely reflects steroid treatment.

#### 2.9.2 Expression-based comparators

Four comparators used gene expression without any network structure. M1 applied an elastic net [[16]](https://doi.org/10.1111/j.1467-9868.2005.00503.x) or a random forest [[17]](https://doi.org/10.1023/A:1010933404324) to all genes, the standard approach of entering every gene into a single model. M2 fitted one model per pathway on gene expression and combined the pathway models in the same way as the LIONESS models (Section 2.10); it asked whether any gain comes from the pathways themselves rather than from the networks. M3 summarized each pathway by a single activity score (singscore [[18]](https://doi.org/10.1186/s12859-018-2435-4), mean z-score or first principal component), the classic pathway-activity approach, and also applied non-linear models, gradient boosting [[19]](https://doi.org/10.1145/2939672.2939785) and a kernel support vector machine [[20]](https://doi.org/10.1007/BF00994018), to pathway expression, which capture general interactions between genes without using network structure. M4 measured, for each pathway, how far a patient lies from the healthy centre, as the sum of squared standardized expression values or as the Mahalanobis distance, and asked whether patients simply scatter further from the healthy centre than controls do.

#### 2.9.3 Established network comparators

Two comparators represented network methods already used in lupus research. W1 reproduced a typical published weighted gene co-expression network analysis (WGCNA) [[21]](https://pubmed.ncbi.nlm.nih.gov/19114008/) and hub-gene pipeline, with every step fitted within the training folds to avoid data leakage. W2 used WGCNA module eigengenes, the summary scores of gene modules, estimated only from training data; W2 was the main established-network comparator.

#### 2.9.4 LIONESS models

Four models used single-sample networks estimated by LIONESS [[22]](https://pubmed.ncbi.nlm.nih.gov/30981959/). L1 used the edges of the partial-correlation networks as features. L2, the main model, used network summary features such as node strength and clustering (Section 2.8). L2-P was identical to L2 except that Pearson correlation replaced partial correlation, and asked whether partial correlation matters. L3 combined L2 with M2 and M0a, so that the network features were added to both pathway expression and the residual IFN score.

#### 2.9.5 Primary comparison

The primary hypothesis was tested by comparing L3 with a reference model, M5, that contains pathway expression and the residual IFN score (M2 plus M0a) but no network features. A gain of L3 over M5 is therefore evidence that networks carry information beyond both expression and residual IFN activity. All other comparisons were secondary.

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
3. Hoffman RW, et al. Gene expression and pharmacodynamic changes in 1,760 systemic lupus erythematosus patients from two phase III trials of BAFF blockade with tabalumab. *Arthritis Rheumatol* 2017;69(3):643–654. PMID [27723281](https://pubmed.ncbi.nlm.nih.gov/27723281/).
4. Hu Y, et al. Development of a molecular signature to monitor pharmacodynamic responses mediated by in vivo administration of glucocorticoids. *Arthritis Rheumatol* 2018. PMID [29534336](https://pubmed.ncbi.nlm.nih.gov/29534336/).
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
16. Zou H, Hastie T. Regularization and variable selection via the elastic net. *J R Stat Soc Series B Stat Methodol* 2005;67(2):301–320. doi:[10.1111/j.1467-9868.2005.00503.x](https://doi.org/10.1111/j.1467-9868.2005.00503.x).
17. Breiman L. Random forests. *Mach Learn* 2001;45:5–32. doi:[10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324).
18. Foroutan M, Bhuva DD, Lyu R, et al. Single sample scoring of molecular phenotypes. *BMC Bioinformatics* 2018;19(1):404. doi:[10.1186/s12859-018-2435-4](https://doi.org/10.1186/s12859-018-2435-4).
19. Chen T, Guestrin C. XGBoost: a scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* 2016:785–794. doi:[10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785).
20. Cortes C, Vapnik V. Support-vector networks. *Mach Learn* 1995;20:273–297. doi:[10.1007/BF00994018](https://doi.org/10.1007/BF00994018).
21. Langfelder P, Horvath S. WGCNA: an R package for weighted correlation network analysis. *BMC Bioinformatics* 2008;9:559. PMID [19114008](https://pubmed.ncbi.nlm.nih.gov/19114008/).
22. Kuijjer ML, Tung MG, Yuan G, Quackenbush J, Glass K. Estimating sample-specific regulatory networks. *iScience* 2019;14:226–240. PMID [30981959](https://pubmed.ncbi.nlm.nih.gov/30981959/).

## Supplementary material

