## Population-level tests T1-T3 (equations 26-28) with Freedman-Lane permutation and the subgroup check
## (equation 29), for each sub-pathway and contrast (Section 2.12). IFN status from all controls.
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
source(file.path(here, "lib.R"))
ROOT <- normalizePath(file.path(here, "../../..")); DATA <- file.path(ROOT, "data/GSE110169")
OUT <- file.path(ROOT, "analysis/gse110169/results")
N_PERM <- 10000; set.seed(2026)
s <- read.delim(file.path(DATA, "processed/samples.tsv"))
ann <- read.delim(file.path(DATA, "processed/probe_annotation.tsv"), row.names = 1)
E <- as.matrix(read.delim(gzfile(file.path(DATA, "processed/expression_probes.tsv.gz")), row.names = 1, check.names = FALSE))
Xall <- t(E); pg <- ann[colnames(Xall), "gene_symbol"]; group <- s$group
pbg <- split(seq_along(pg), pg); genes <- names(pbg)
Xg <- Xall[, sapply(genes, function(g) { p <- pbg[[g]]; if (length(p) == 1) p else p[which.max(apply(Xall[, p, drop = FALSE], 2, var))] })]
colnames(Xg) <- genes
PW <- jsonlite::read_json(file.path(OUT, "subpathways.json"), simplifyVector = TRUE)
hc <- group == "HC"; Z <- scale(Xg[, IFN_GENES], colMeans(Xg[hc, IFN_GENES]), apply(Xg[hc, IFN_GENES], 2, sd))
I <- rowMeans(Z); theta <- mean(I[hc]) + 2 * sd(I[hc]); status <- ifelse(I > theta, "high", "low")
Rk <- t(apply(Xg, 1, rank)); cells <- sapply(CELL_MARKERS, function(m) singscore(Rk, match(intersect(m, genes), genes)))
saveRDS(list(I = I, theta = theta, status = status, cells = cells), file.path(OUT, "ifn_cells_all.rds"))

CONTR <- list(C1 = c("SLE", "high", "HC", "low"), C2 = c("SLE", "low", "HC", "low"), C3 = c("SLE", "low", "RA", "low"))
stat <- function(Za, Zb, lam) {
  Ra <- sweep(Za, 2, colMeans(Za)); Rb <- sweep(Zb, 2, colMeans(Zb)); V <- cov(rbind(Ra, Rb))
  V <- (1 - lam) * V + lam * diag(diag(V)); Vi <- solve(V); dm <- colMeans(Za) - colMeans(Zb)
  c(T1 = drop(dm %*% Vi %*% dm), T2 = abs(mean(rowSums((Ra %*% Vi) * Ra)) - mean(rowSums((Rb %*% Vi) * Rb))),
    T3 = norm(pcor_mat(Za, NULL, lam) - pcor_mat(Zb, NULL, lam), "F"), T3P = norm(cor(Za) - cor(Zb), "F"))
}
dbic <- function(M) { P3 <- prcomp(M)$x[, 1:3]
  b <- sapply(1:2, function(k) { m <- Mclust(P3, G = k, modelNames = "VVV", verbose = FALSE); if (is.null(m)) NA else -m$bic }); b[1] - b[2] }
rows <- list()
for (cn in names(CONTR)) { cc <- CONTR[[cn]]
  i1 <- which(group == cc[1] & status == cc[2]); i0 <- which(group == cc[3] & status == cc[4]); idx <- c(i1, i0); y <- c(rep(1, length(i1)), rep(0, length(i0)))
  covs <- cbind(sex = as.numeric(s$sex_inferred[idx] == "M"), model.matrix(~ batch, s[idx, ])[, -1], cells[idx, ], IFN = I[idx])
  D <- cbind(1, covs)
  for (n in names(PW)) { X <- Xg[idx, PW[[n]]]; if (ncol(X) > 50) X <- X[, order(-apply(X, 2, var))[1:50]]
    X <- scale(X); R <- X - D %*% qr.solve(D, X)            # Freedman-Lane: residuals of the covariate-only model
    lam <- lam_ss(R); obs <- stat(R[y == 1, ], R[y == 0, ], lam); cnt <- 0
    for (b in 1:N_PERM) { yp <- sample(y); cnt <- cnt + (stat(R[yp == 1, ], R[yp == 0, ], lam) >= obs) }
    p <- (cnt + 1) / (N_PERM + 1)
    db <- c(pat = dbic(R[y == 1, ]), con = dbic(R[y == 0, ]))
    rows[[length(rows) + 1]] <- data.frame(contrast = cn, pathway = sub("REACTOME_", "", n), n_pos = length(i1), n_neg = length(i0), genes = ncol(X),
      T1 = obs[1], T2 = obs[2], T3 = obs[3], T3P = obs[4], p_T1 = p[1], p_T2 = p[2], p_T3 = p[3], p_T3P = p[4],
      dBIC_pat = db[1], dBIC_con = db[2])
    cat(cn, n, round(p, 4), "\n") } }
res <- do.call(rbind, rows)
for (v in c("p_T1", "p_T2", "p_T3", "p_T3P")) res[[sub("p_", "q_", v)]] <- ave(res[[v]], res$contrast, FUN = function(p) p.adjust(p, "BH"))
res$subgroup_flag <- res$dBIC_pat > 2 & res$dBIC_con <= 2
write.csv(res, file.path(OUT, "population_tests.csv"), row.names = FALSE)
