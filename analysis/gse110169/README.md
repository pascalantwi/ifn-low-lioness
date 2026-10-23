# GSE110169 analysis code

R scripts for the analysis of GSE110169 (Sections 2.2–2.12 of the manuscript). Run from `analysis/gse110169/R/`.

| Script | What it does |
|---|---|
| `lib.R` | Functions: sub-pathways, cell scores, partial and Pearson correlation, balanced LIONESS, network features, group lasso, comparator models |
| `run_real.R` | Repeated nested cross-validation of all models for C1–C3: `Rscript run_real.R 10 C1,C2,C3`; leakage check: `Rscript run_real.R 1 C2 <n_permutations>` |
| `poptests.R` | Population-level tests T1–T3 with Freedman–Lane permutation and the subgroup check |
| `summarise.R` | AUC, AUPRC, Brier score, paired AUC differences, pathway selection |
| `descriptive.R` | Group-level partial correlations and full-data LIONESS features (for figures only) |
| `figures.R` | Figures 1–4 and Supplementary Figures S1–S4, written to `manuscript/figures/` |
| `network_figure.R` | Figures 5 and 6: differential co-expression networks (partial and Pearson; IFN-low SLE vs HC and vs IFN-low RA) |

Outputs are written to `results/`.
