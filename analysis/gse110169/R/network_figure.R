## Figure 7: differential co-expression networks (LIONESS-paper style) for IFN-low SLE versus healthy
## controls and versus IFN-low RA, with partial and Pearson correlation. Descriptive.
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
source(file.path(here, "lib.R")); suppressPackageStartupMessages({library(ggplot2); library(patchwork); library(igraph)})
ROOT <- normalizePath(file.path(here, "../../..")); DATA <- file.path(ROOT, "data/GSE110169")
OUT <- file.path(ROOT, "analysis/gse110169/results"); FIG <- file.path(ROOT, "manuscript/figures")
s <- read.delim(file.path(DATA, "processed/samples.tsv"))
ann <- read.delim(file.path(DATA, "processed/probe_annotation.tsv"), row.names = 1)
E <- as.matrix(read.delim(gzfile(file.path(DATA, "processed/expression_probes.tsv.gz")), row.names = 1, check.names = FALSE))
Xall <- t(E); pg <- ann[colnames(Xall), "gene_symbol"]; pbg <- split(seq_along(pg), pg)
D <- readRDS(file.path(OUT, "descriptive.rds")); ic <- readRDS(file.path(OUT, "ifn_cells_all.rds"))
pwn <- grep("ALPHA_BETA", names(D), value = TRUE); genes <- D[[pwn]]$genes; grp <- D$group4
X <- Xall[, sapply(genes, function(g) { p <- pbg[[g]]; if (length(p) == 1) p else p[which.max(apply(Xall[, p, drop = FALSE], 2, var))] })]
colnames(X) <- genes; X <- scale(X); cov <- scale(cbind(ic$I, ic$cells))

assoc <- function(g, meas) { i <- which(grp == g)
  if (meas == "Partial correlation") { lam <- lam_ss(cbind(X[i, ], cov[i, ])); P <- pcor_mat(X[i, ], cov[i, ], lam) } else P <- pear_mat(X[i, ])
  dimnames(P) <- list(genes, genes); P }

panel <- function(comp, meas, compname, tag) {
  dA <- assoc("SLE IFN-low", meas) - assoc(comp, meas)
  ut <- which(upper.tri(dA), arr.ind = TRUE)
  ed <- data.frame(a = genes[ut[, 1]], b = genes[ut[, 2]], d = dA[ut]); ed <- ed[order(-abs(ed$d)), ][1:30, ]
  gr <- graph_from_data_frame(ed, directed = FALSE); set.seed(11)
  lay <- layout_components(gr, layout = layout_with_kk); lay <- apply(lay, 2, function(v) (v - min(v)) / diff(range(v)))
  n <- nrow(lay); dmin <- 0.12
  for (it in 1:300) { moved <- FALSE
    ## node-node separation
    for (i in 1:(n - 1)) for (j in (i + 1):n) { v <- lay[j, ] - lay[i, ]; dd <- sqrt(sum(v^2))
      if (dd < dmin) { u <- if (dd > 1e-9) v / dd else c(1, 0); sh <- (dmin - dd) / 2 + 1e-3
        lay[i, ] <- lay[i, ] - u * sh; lay[j, ] <- lay[j, ] + u * sh; moved <- TRUE } }
    ## node-edge separation (a node must not sit on an edge it is not part of)
    for (k in seq_len(nrow(ed))) { a <- match(ed$a[k], V(gr)$name); b <- match(ed$b[k], V(gr)$name)
      for (v in setdiff(1:n, c(a, b))) { P <- lay[v, ]; A <- lay[a, ]; B <- lay[b, ]; AB <- B - A
        u <- sum((P - A) * AB) / sum(AB^2); if (u <= 0.05 || u >= 0.95) next
        Q <- A + u * AB; dd <- sqrt(sum((P - Q)^2))
        if (dd < dmin / 2) { nrm <- if (dd > 1e-9) (P - Q) / dd else c(-AB[2], AB[1]) / sqrt(sum(AB^2)); lay[v, ] <- Q + nrm * (dmin / 2 + 0.005); moved <- TRUE } } }
    if (!moved) break }
  lay <- apply(lay, 2, function(v) (v - min(v)) / diff(range(v)))
  i1 <- grp == "SLE IFN-low" & !is.na(grp); i0 <- grp == comp & !is.na(grp)
  eff <- sapply(V(gr)$name, function(g) (mean(X[i1, g]) - mean(X[i0, g])) / sqrt((var(X[i1, g]) + var(X[i0, g])) / 2))
  nd <- data.frame(name = V(gr)$name, x = lay[, 1], y = lay[, 2], eff = eff)
  ed$x <- nd$x[match(ed$a, nd$name)]; ed$y <- nd$y[match(ed$a, nd$name)]; ed$xe <- nd$x[match(ed$b, nd$name)]; ed$ye <- nd$y[match(ed$b, nd$name)]
  ed$dir <- ifelse(ed$d > 0, "Stronger in IFN-low SLE", "Weaker in IFN-low SLE")
  ggplot() +
    geom_segment(data = ed, aes(x, y, xend = xe, yend = ye, colour = dir, linewidth = pmin(abs(d), 0.8)), lineend = "round", alpha = 0.85) +
    geom_point(data = nd, aes(x, y, fill = eff), size = 12, shape = 21, colour = "grey20", stroke = 0.7) +
    geom_text(data = nd, aes(x, y, label = name), size = 1.9, fontface = "bold", colour = "grey5") +
    scale_colour_manual(values = c(`Stronger in IFN-low SLE` = "#D55E00", `Weaker in IFN-low SLE` = "#0072B2"), name = "Edge", drop = FALSE) +
    scale_linewidth(range = c(0.4, 2.6), limits = c(0, 0.8), breaks = c(0.2, 0.4, 0.6), name = expression("|" * Delta * " correlation|")) +
    scale_fill_gradient2(low = "#9970AB", mid = "#F7F7F7", high = "#5AAE61", limits = c(-1.2, 1.2), oob = scales::squish,
      name = "Gene expression,\nIFN-low SLE vs comparator\n(standardized difference)") +
    coord_equal(clip = "off") + scale_x_continuous(expand = expansion(0.1)) + scale_y_continuous(expand = expansion(0.1)) +
    theme_void(base_size = 9) + theme(plot.title = element_text(face = "bold", size = 10, hjust = 0.5), plot.margin = margin(6, 6, 6, 6)) +
    labs(title = paste0(tag, "  IFN-low SLE vs ", compname, ": ", sub("Partial", "partial", meas)))
}
p <- (panel("HC", "Partial correlation", "HC", "A") | panel("HC", "Pearson correlation", "HC", "B")) /
     (panel("RA IFN-low", "Partial correlation", "IFN-low RA", "C") | panel("RA IFN-low", "Pearson correlation", "IFN-low RA", "D")) +
  plot_layout(guides = "collect") +
  plot_annotation(title = "Differential co-expression networks of interferon alpha/beta signalling",
    subtitle = "Edges: the 30 gene pairs with the largest change in correlation in each comparison (orange, stronger in IFN-low SLE; blue, weaker).\nNodes: genes, coloured by the difference in expression (green, higher in IFN-low SLE; purple, lower). Partial correlations are\nconditioned on the IFN score and cell-composition scores. Descriptive.",
    theme = theme(plot.title = element_text(face = "bold", size = 13), plot.subtitle = element_text(size = 9, colour = "grey30"))) &
  theme(legend.position = "right")
ggsave(file.path(FIG, "fig7_differential_network.png"), p, width = 13, height = 12.5, dpi = 300, bg = "white")
cat("figure 7 written\n")
