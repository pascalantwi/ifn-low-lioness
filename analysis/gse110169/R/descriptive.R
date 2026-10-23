## Descriptive network summaries for the figures (not used for model evaluation):
## group-level partial correlations (adjusted residuals) and full-data LIONESS features by group.
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
source(file.path(here, "lib.R"))
ROOT <- normalizePath(file.path(here, "../../..")); DATA <- file.path(ROOT, "data/GSE110169")
OUT <- file.path(ROOT, "analysis/gse110169/results"); set.seed(7)
s <- read.delim(file.path(DATA, "processed/samples.tsv"))
ann <- read.delim(file.path(DATA, "processed/probe_annotation.tsv"), row.names = 1)
E <- as.matrix(read.delim(gzfile(file.path(DATA, "processed/expression_probes.tsv.gz")), row.names = 1, check.names = FALSE))
Xall <- t(E); pg <- ann[colnames(Xall), "gene_symbol"]; pbg <- split(seq_along(pg), pg); genes <- names(pbg)
Xg <- Xall[, sapply(genes, function(g) { p <- pbg[[g]]; if (length(p) == 1) p else p[which.max(apply(Xall[, p, drop = FALSE], 2, var))] })]; colnames(Xg) <- genes
PW <- jsonlite::read_json(file.path(OUT, "subpathways.json"), simplifyVector = TRUE)
ic <- readRDS(file.path(OUT, "ifn_cells_all.rds")); I <- ic$I; st <- ic$status; cells <- ic$cells
grp4 <- ifelse(s$group == "HC", ifelse(st == "low", "HC", NA), paste(s$group, ifelse(st == "low", "IFN-low", "IFN-high")))
cov <- scale(cbind(IFN = I, cells))
out <- list(group4 = grp4)
for (n in names(PW)) {
  X <- Xg[, PW[[n]]]; if (ncol(X) > 50) X <- X[, order(-apply(X[!is.na(grp4), ], 2, var))[1:50]]
  X <- pmin(pmax(scale(X), -4), 4)
  ## group-level partial correlations conditioned on IFN score and cell scores
  pc <- lapply(c("HC", "SLE IFN-low", "SLE IFN-high", "RA IFN-low"), function(g) { i <- which(grp4 == g)
    lam <- lam_ss(cbind(X[i, ], cov[i, ])); P <- pcor_mat(X[i, ], cov[i, ], lam); dimnames(P) <- list(colnames(X), colnames(X)); P })
  names(pc) <- c("HC", "SLE IFN-low", "SLE IFN-high", "RA IFN-low")
  ## full-data LIONESS, balanced reference of HC and IFN-low SLE; other groups added one at a time
  ref <- which(grp4 %in% c("HC", "SLE IFN-low")); y <- as.numeric(grp4[ref] == "SLE IFN-low"); oth <- which(!is.na(grp4) & !(seq_along(grp4) %in% ref))
  lam <- lam_ss(cbind(X[ref, ], cov[ref, ])); G <- ncol(X); ut <- upper.tri(diag(G))
  feats <- list()
  for (meas in c("partial", "pearson")) { f <- if (meas == "partial") pcor_mat else pear_mat; C <- if (meas == "partial") cov else NULL
    L <- lioness(X[ref, ], y, X[oth, , drop = FALSE], f, if (is.null(C)) NULL else C[ref, ], if (is.null(C)) NULL else C[oth, ], lam)
    Pm <- f(X[ref, ], if (is.null(C)) NULL else C[ref, ], lam); kappa <- quantile(abs(L$tr), 0.99)
    dP <- (f(X[ref, ][y == 1, ], if (is.null(C)) NULL else C[ref, ][y == 1, ], lam) - f(X[ref, ][y == 0, ], if (is.null(C)) NULL else C[ref, ][y == 0, ], lam))[ut]
    Ft <- net_features(L$tr, Pm, kappa, dP, G); cf <- strat_folds(y, 5)
    for (k in 1:5) { a <- cf != k; Cr <- if (is.null(C)) NULL else C[ref, ]
      dPk <- (f(X[ref, ][a & y == 1, ], if (is.null(Cr)) NULL else Cr[a & y == 1, ], lam) - f(X[ref, ][a & y == 0, ], if (is.null(Cr)) NULL else Cr[a & y == 0, ], lam))[ut]
      Ft[cf == k, "DN"] <- L$tr[cf == k, , drop = FALSE] %*% dPk }
    Fm <- rbind(Ft, net_features(L$te, Pm, kappa, dP, G))[, 1:4]
    feats[[meas]] <- data.frame(sample = c(ref, oth), group = grp4[c(ref, oth)], measure = meas, Fm) }
  out[[n]] <- list(pcor = pc, features = do.call(rbind, feats), genes = colnames(X))
  cat(n, "done\n")
}
saveRDS(out, file.path(OUT, "descriptive.rds"))
