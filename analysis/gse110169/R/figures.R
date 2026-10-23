## Figures for the GSE110169 results (Section 3).
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
suppressPackageStartupMessages({library(ggplot2); library(patchwork); library(igraph); library(ggrepel)})
ROOT <- normalizePath(file.path(here, "../../..")); OUT <- file.path(ROOT, "analysis/gse110169/results")
FIG <- file.path(ROOT, "manuscript/figures"); dir.create(FIG, FALSE)
s <- read.delim(file.path(ROOT, "data/GSE110169/processed/samples.tsv"))
theme_set(theme_minimal(base_size = 10) + theme(panel.grid.minor = element_blank(), strip.text = element_text(face = "bold"),
  plot.title = element_text(face = "bold", size = 11), legend.position = "bottom"))
OI <- c("#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#999999")
CLAB <- c(C1 = "C1: IFN-high SLE vs HC", C2 = "C2: IFN-low SLE vs HC", C3 = "C3: IFN-low SLE vs IFN-low RA")
fam <- function(m) ifelse(grepl("^M0", m), "Baseline", ifelse(grepl("^M", m), "Expression", ifelse(grepl("^W", m), "Established network", "LIONESS")))
FAMCOL <- c(Baseline = "#999999", Expression = "#0072B2", `Established network` = "#009E73", LIONESS = "#D55E00")
ORDER <- c("M0a", "M0c", "M1", "M2", "M3-score", "M3-boost", "M3-SVM", "M4", "M5", "M6", "W1", "W2", "L1", "L2", "L2-P", "L2-S", "L3", "L3-P")

## ---- Figure 1: IFN score by group with the cutoff
ic <- readRDS(file.path(OUT, "ifn_cells_all.rds"))
d1 <- data.frame(group = factor(s$group, c("HC", "RA", "SLE")), I = ic$I, status = ifelse(ic$status == "high", "IFN-high", "IFN-low"))
cnt <- aggregate(I ~ group + status, d1, length)
cnt$lab <- paste0(cnt$status, ": ", cnt$I); lab1 <- aggregate(lab ~ group, cnt, paste, collapse = "\n")
p1 <- ggplot(d1, aes(group, I)) + geom_violin(fill = "grey93", colour = NA, width = 0.9) +
  geom_jitter(aes(colour = status), width = 0.15, size = 1.6, alpha = 0.85) +
  geom_hline(yintercept = ic$theta, linetype = "dashed") +
  annotate("text", x = 0.55, y = ic$theta, label = "cutoff (HC mean + 2 SD)", vjust = -0.5, hjust = 0, size = 3) +
  geom_text(data = lab1, aes(group, max(d1$I) + 1.1, label = lab), size = 3, vjust = 1) + expand_limits(y = max(d1$I) + 1.2) +
  scale_colour_manual(values = c(`IFN-high` = "#D55E00", `IFN-low` = "#0072B2"), name = NULL) +
  labs(x = NULL, y = "IFN score (equation 2)")
ggsave(file.path(FIG, "fig1_ifn_score.png"), p1, width = 5.5, height = 4.2, dpi = 300, bg = "white")

## ---- Figure 2: AUC of all models in the three contrasts
perf <- read.csv(file.path(OUT, "performance.csv")); perf$model <- factor(perf$model, rev(ORDER)); perf$family <- fam(as.character(perf$model))
p2 <- ggplot(perf, aes(AUC, model, colour = family)) + geom_vline(xintercept = 0.5, colour = "grey60", linetype = "dotted") +
  geom_errorbarh(aes(xmin = AUC_min, xmax = AUC_max), height = 0, linewidth = 0.6) + geom_point(size = 2.2) +
  facet_wrap(~ contrast, labeller = as_labeller(CLAB)) + scale_colour_manual(values = FAMCOL, name = NULL) +
  coord_cartesian(xlim = c(0.3, 1)) + labs(x = "AUC (mean; bar = range over 10 repeats)", y = NULL)
ggsave(file.path(FIG, "fig2_auc_all_models.png"), p2, width = 10, height = 5, dpi = 300, bg = "white")

## ---- Figure 3: ROC curves (out-of-fold predictions pooled over repeats)
roc_df <- do.call(rbind, lapply(c("C1", "C2", "C3"), function(cn) { R <- readRDS(file.path(OUT, paste0("oof_", cn, ".rds")))
  do.call(rbind, lapply(c("M0a", "M5", "M6", "W2", "L3", "L3-P"), function(m) {
    y <- unlist(lapply(R, `[[`, "y")); p <- unlist(lapply(R, function(x) x$pred[[m]])); o <- order(-p)
    data.frame(contrast = cn, model = m, fpr = c(0, cumsum(1 - y[o]) / sum(1 - y)), tpr = c(0, cumsum(y[o]) / sum(y))) })) }))
roc_df$model <- factor(roc_df$model, c("M0a", "M5", "M6", "W2", "L3", "L3-P"))
p3 <- ggplot(roc_df, aes(fpr, tpr, colour = model)) + geom_abline(colour = "grey70", linetype = "dotted") + geom_path(linewidth = 0.7) +
  facet_wrap(~ contrast, labeller = as_labeller(CLAB)) + coord_equal() +
  scale_colour_manual(values = c(M0a = "#999999", M5 = "#0072B2", M6 = "#56B4E9", W2 = "#009E73", L3 = "#D55E00", `L3-P` = "#E69F00"),
    labels = c(M0a = "M0a IFN score", M5 = "M5 expression + IFN", M6 = "M6 regularized QDA", W2 = "W2 WGCNA modules", L3 = "L3 partial LIONESS + M5", `L3-P` = "L3-P Pearson LIONESS + M5"), name = NULL) +
  labs(x = "False-positive rate", y = "True-positive rate") + guides(colour = guide_legend(nrow = 2))
ggsave(file.path(FIG, "figS1_roc.png"), p3, width = 10, height = 4.4, dpi = 300, bg = "white")

## ---- Figure 4: paired AUC differences (forest plot)
pd <- read.csv(file.path(OUT, "paired_differences.csv"))
pd$comparison <- factor(pd$comparison, rev(unique(pd$comparison)))
pd$type <- ifelse(startsWith(pd$hypothesis, "H1"), "Primary (H1)", ifelse(startsWith(pd$hypothesis, "H2"), "Secondary (H2)", "Exploratory"))
p4 <- ggplot(pd, aes(delta_AUC, comparison, colour = type)) + geom_vline(xintercept = 0, colour = "grey50") +
  geom_errorbarh(aes(xmin = lo, xmax = hi), height = 0.2) + geom_point(size = 2) +
  facet_wrap(~ contrast, labeller = as_labeller(CLAB)) + scale_colour_manual(values = c(`Primary (H1)` = "#D55E00", `Secondary (H2)` = "#0072B2", Exploratory = "#999999"), name = NULL) +
  labs(x = "Difference in AUC (95% CI, Nadeau-Bengio corrected)", y = NULL)
ggsave(file.path(FIG, "fig3_delta_auc.png"), p4, width = 10, height = 4.2, dpi = 300, bg = "white")

## ---- Figure 5: population-level tests
pt <- read.csv(file.path(OUT, "population_tests.csv"))
pt <- pt[(pt$contrast == "C1" & pt$adjustment == "no_IFN") | (pt$contrast != "C1" & pt$adjustment == "full"), ]
pl <- do.call(rbind, lapply(c("T1", "T2", "T3", "T3P"), function(t) data.frame(contrast = pt$contrast, pathway = pt$pathway, test = t, q = pt[[paste0("q_", t)]], flag = pt$subgroup_flag)))
pl$test <- factor(pl$test, c("T1", "T2", "T3", "T3P"), c("Level\n(T1)", "Spread\n(T2)", "Structure,\npartial (T3)", "Structure,\nPearson"))
pl$pathway <- gsub("_", " ", tolower(pl$pathway)); pl$sig <- ifelse(pl$q < 0.05, "*", "")
p5 <- ggplot(pl, aes(test, pathway, fill = -log10(q))) + geom_tile(colour = "white") + geom_text(aes(label = sig), size = 5, vjust = 0.75) +
  facet_wrap(~ contrast, labeller = as_labeller(CLAB)) + scale_fill_gradient(low = "#F7FBFF", high = "#08306B", name = expression(-log[10]~q)) +
  labs(x = NULL, y = NULL) +
  theme(legend.position = "right")
ggsave(file.path(FIG, "fig4_population_tests.png"), p5, width = 11, height = 3.8, dpi = 300, bg = "white")

## ---- Figures 6-8: descriptive networks
D <- readRDS(file.path(OUT, "descriptive.rds"))
pwn <- grep("ALPHA_BETA", names(D), value = TRUE)
pc <- D[[pwn]]$pcor; g <- D[[pwn]]$genes; hc <- hclust(as.dist(1 - abs(pc$HC + pc$`SLE IFN-low`) / 2))
oo <- g[hc$order]; M <- matrix(NA, length(g), length(g), dimnames = list(oo, oo))
M[lower.tri(M)] <- pc$HC[oo, oo][lower.tri(M)]; M[upper.tri(M)] <- pc$`SLE IFN-low`[oo, oo][upper.tri(M)]
hm <- data.frame(expand.grid(r = oo, c = oo), v = as.vector(M)); hm$r <- factor(hm$r, oo); hm$c <- factor(hm$c, oo)
p6 <- ggplot(hm, aes(c, r, fill = v)) + geom_tile() + scale_fill_gradient2(low = "#2166AC", mid = "white", high = "#B2182B", na.value = "grey90", name = "Partial\ncorrelation", limits = c(-1, 1) * max(abs(hm$v), na.rm = TRUE)) +
  coord_equal(clip = "off") + labs(x = NULL, y = NULL) +
  annotate("label", x = length(oo) - 0.5, y = 1.5, label = "IFN-low SLE", hjust = 1, vjust = 0, size = 3.2, fontface = "bold", label.size = 0) +
  annotate("label", x = 1.5, y = length(oo) - 0.5, label = "HC", hjust = 0, vjust = 1, size = 3.2, fontface = "bold", label.size = 0) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5, size = 5), axis.text.y = element_text(size = 5), legend.position = "right")
ggsave(file.path(FIG, "figS2_pcor_heatmap.png"), p6, width = 7.5, height = 7, dpi = 300, bg = "white")

## Figure 7 (differential networks) is drawn by network_figure.R

## LIONESS primary features by group (full-data, descriptive)
fe <- do.call(rbind, lapply(names(D)[-1], function(n) cbind(pathway = n, D[[n]]$features)))
fe <- fe[fe$pathway == pwn & !is.na(fe$group), ]; fl <- reshape(fe, varying = c("DN", "meanw", "eta1", "D"), v.names = "value", timevar = "feature", times = c("DN score", "Mean |w|", "Largest eigenvalue", "Distance D"), direction = "long")
fl$group <- factor(fl$group, c("HC", "SLE IFN-low", "RA IFN-low", "RA IFN-high", "SLE IFN-high")); fl$measure <- factor(fl$measure, c("partial", "pearson"), c("Partial correlation", "Pearson correlation"))
fl$feature <- factor(fl$feature, c("DN score", "Mean |w|", "Largest eigenvalue", "Distance D"))
fl$panel <- factor(paste0(fl$feature, ", ", tolower(fl$measure)), unique(paste0(fl$feature, ", ", tolower(fl$measure))[order(fl$feature, fl$measure)]))
p8 <- ggplot(fl, aes(group, value, fill = group)) + geom_boxplot(outlier.size = 0.5, width = 0.7) + facet_wrap(~ panel, scales = "free_y", ncol = 2) +
  scale_fill_manual(values = c(HC = "#999999", `SLE IFN-low` = "#0072B2", `RA IFN-low` = "#009E73", `RA IFN-high` = "#56B4E9", `SLE IFN-high` = "#D55E00"), guide = "none") +
  labs(x = NULL, y = NULL) +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))
ggsave(file.path(FIG, "figS3_lioness_features.png"), p8, width = 6.5, height = 8, dpi = 300, bg = "white")

## ---- Figure 9: selection frequency of pathways in the group-lasso models
sl <- read.csv(file.path(OUT, "pathway_selection.csv")); sl <- sl[sl$model %in% c("M5", "L3", "L3-P"), ]
sl$feature <- gsub("_", " ", tolower(sub("REACTOME_", "", sl$feature))); sl$feature <- sub("^net:reactome ", "network: ", sub("^expr:reactome ", "expression: ", sl$feature))
p9 <- ggplot(sl, aes(model, feature, fill = selected)) + geom_tile(colour = "white") + geom_text(aes(label = sprintf("%.0f", 100 * selected)), size = 2.6) +
  facet_wrap(~ contrast, labeller = as_labeller(CLAB)) + scale_fill_gradient(low = "white", high = "#D55E00", limits = c(0, 1), name = "Selected\n(fraction of folds)") +
  labs(x = NULL, y = NULL) + theme(legend.position = "right")
ggsave(file.path(FIG, "figS4_selection.png"), p9, width = 11, height = 5, dpi = 300, bg = "white")
cat("figures written\n")
