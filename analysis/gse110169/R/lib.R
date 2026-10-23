## Functions for the GSE110169 analysis (Sections 2.2-2.12 of manuscript/progress_draft.md).
## Everything that learns from data is estimated in the training fold and applied unchanged to the test fold.
suppressPackageStartupMessages({library(glmnet); library(corpcor); library(e1071); library(gbm)
  library(pROC); library(mclust); library(dynamicTreeCut)})

IFN_GENES <- c("IFI27", "IFI44", "IFI44L", "RSAD2")
SEX_GENES <- c("RPS4Y1", "DDX3Y", "KDM5D", "UTY", "EIF1AY", "XIST", "TSIX")
## Reactome sub-pathways of Interferon Signaling (R-HSA-913531) and their children (Section 2.5)
IFN_SUBPATHWAYS <- paste0("REACTOME_", c("INTERFERON_ALPHA_BETA_SIGNALING", "INTERFERON_GAMMA_SIGNALING",
  "ANTIVIRAL_MECHANISM_BY_IFN_STIMULATED_GENES", "REGULATION_OF_IFNA_IFNB_SIGNALING",
  "REGULATION_OF_IFNG_SIGNALING", "ISG15_ANTIVIRAL_MECHANISM", "OAS_ANTIVIRAL_RESPONSE",
  "PKR_MEDIATED_SIGNALING", "IFNG_SIGNALING_ACTIVATES_MAPKS"))
## canonical cell-type markers, fixed before the analysis (Section 2.4)
CELL_MARKERS <- list(
  neutrophils = c("FCGR3B", "CXCR2", "CSF3R", "FPR1", "MME", "CXCR1"),
  monocytes = c("CD14", "LYZ", "CSF1R", "FCN1", "VCAN"),
  B_cells = c("MS4A1", "CD79A", "CD79B", "CD19", "BANK1"),
  plasmablasts = c("MZB1", "JCHAIN", "TNFRSF17", "TXNDC5"),
  T_cells = c("CD3D", "CD3E", "CD3G", "CD2", "CD28"),
  NK_cells = c("GNLY", "NKG7", "KLRD1", "PRF1", "KLRF1"),
  eosinophils = c("CLC", "IL5RA", "CCR3", "SIGLEC8", "PRG2"))
B_REF <- 20

read_gmt <- function(f) { l <- strsplit(readLines(f), "\t"); setNames(lapply(l, `[`, -(1:2)), sapply(l, `[`, 1)) }

subpathways <- function(gmt, present) {
  cand <- list()
  for (k in IFN_SUBPATHWAYS) {
    g <- setdiff(intersect(gmt[[k]], present), c(IFN_GENES, SEX_GENES))
    if (length(g) >= 15) cand[[k]] <- sort(g)
  }
  keep <- c()
  for (k in names(cand)[order(-lengths(cand))]) {
    jac <- sapply(keep, function(j) length(intersect(cand[[k]], cand[[j]])) / length(union(cand[[k]], cand[[j]])))
    if (all(jac <= 0.8)) keep <- c(keep, k)
  }
  cand[keep]
}

## singscore-type unidirectional score: mean within-sample rank of the set, scaled to [-0.5, 0.5]
singscore <- function(R, idx) { N <- ncol(R); n <- length(idx); r <- rowMeans(R[, idx, drop = FALSE])
  lo <- (n + 1) / 2; hi <- (2 * N - n + 1) / 2; (r - lo) / (hi - lo) - 0.5 }

## ---------------------------------------------------------------- association measures
pcor_mat <- function(X, C = NULL, lam) {
  Z <- if (is.null(C)) X else cbind(X, C); Z <- sweep(Z, 2, colMeans(Z))
  S <- crossprod(Z) / nrow(Z); S <- (1 - lam) * S; diag(S) <- diag(S) / (1 - lam)
  O <- solve(S); d <- sqrt(diag(O)); P <- -O / outer(d, d); G <- ncol(X)
  P <- P[1:G, 1:G, drop = FALSE]; diag(P) <- 0; P }
pear_mat <- function(X, C = NULL, lam = NULL) { R <- cor(X); diag(R) <- 0; R }
lam_ss <- function(X) attr(corpcor::cor.shrink(X, verbose = FALSE), "lambda")

## class-balanced bagged LIONESS (equations 13-14)
lioness <- function(Xtr, ytr, Xte, f, Ctr, Cte, lam) {
  G <- ncol(Xtr); ut <- upper.tri(diag(G)); m <- sum(ut)
  Etr <- matrix(0, nrow(Xtr), m); Ete <- matrix(0, nrow(Xte), m)
  i0 <- which(ytr == 0); i1 <- which(ytr == 1); mm <- min(length(i0), length(i1))
  for (b in 1:B_REF) {
    ref <- c(sample(i0, mm), sample(i1, mm)); R <- Xtr[ref, , drop = FALSE]
    CR <- if (is.null(Ctr)) NULL else Ctr[ref, , drop = FALSE]; N <- length(ref); P <- f(R, CR, lam)
    for (k in seq_along(ref)) Etr[ref[k], ] <- Etr[ref[k], ] +
      (N * P - (N - 1) * f(R[-k, , drop = FALSE], if (is.null(CR)) NULL else CR[-k, , drop = FALSE], lam))[ut]
    for (i in setdiff(seq_len(nrow(Xtr)), ref)) Etr[i, ] <- Etr[i, ] +
      ((N + 1) * f(rbind(R, Xtr[i, ]), if (is.null(CR)) NULL else rbind(CR, Ctr[i, ]), lam) - N * P)[ut]
    for (t in seq_len(nrow(Xte))) Ete[t, ] <- Ete[t, ] +
      ((N + 1) * f(rbind(R, Xte[t, ]), if (is.null(CR)) NULL else rbind(CR, Cte[t, ]), lam) - N * P)[ut]
  }
  list(tr = Etr / B_REF, te = Ete / B_REF)
}

## primary features (DN, mean |w|, eta1, D; equations 16-19) and secondary features (strengths, eq 20)
net_features <- function(E, P, kappa, dP, G) {
  ut <- upper.tri(diag(G)); pe <- (P / kappa)[ut]
  t(apply(E, 1, function(e) {
    W <- matrix(0, G, G); W[ut] <- e / kappa; W <- W + t(W); w <- W[ut]
    c(DN = sum(e * dP), meanw = mean(abs(w)), eta1 = max(eigen(W, symmetric = TRUE, only.values = TRUE)$values),
      D = sqrt(2 * sum((w - pe)^2)), pos = rowSums(pmax(W, 0)), neg = rowSums(pmax(-W, 0)))
  }))
}
key4 <- function(F) F[, 1:4, drop = FALSE]

## ---------------------------------------------------------------- group lasso (equation 22)
sig <- function(z) 1 / (1 + exp(-pmin(pmax(z, -30), 30)))
gl_fit <- function(X, y, grp, gam, n_iter = 400) {
  n <- nrow(X); p <- ncol(X); w <- rep(0, p); b <- qlogis(min(max(mean(y), 1e-6), 1 - 1e-6))
  v <- w; vb <- b; t <- 1; L <- 0.25 * norm(X, "2")^2 / n + 1e-8
  ug <- unique(grp); gi <- lapply(ug, function(g) which(grp == g)); sq <- sqrt(lengths(gi))
  for (it in 1:n_iter) {
    r <- sig(drop(X %*% v) + vb) - y; wn <- v - drop(crossprod(X, r)) / n / L; bn <- vb - mean(r) / L
    for (j in seq_along(gi)) { i <- gi[[j]]; nr <- sqrt(sum(wn[i]^2)); thr <- gam * sq[j] / L
      wn[i] <- if (nr <= thr) 0 else wn[i] * (1 - thr / nr) }
    tn <- (1 + sqrt(1 + 4 * t * t)) / 2; v <- wn + (t - 1) / tn * (wn - w); vb <- bn + (t - 1) / tn * (bn - b)
    w <- wn; b <- bn; t <- tn
  }
  list(w = w, b = b)
}
gl_predict <- function(A, y, B, grp, n_gam = 8) {
  mu <- colMeans(A); sdv <- apply(A, 2, sd); sdv[sdv == 0] <- 1
  A <- scale(A, mu, sdv); B <- scale(B, mu, sdv); r0 <- (y - mean(y)) / length(y)
  gmax <- max(sapply(unique(grp), function(g) sqrt(sum(crossprod(A[, grp == g, drop = FALSE], r0)^2)) / sqrt(sum(grp == g))))
  grid <- gmax * 10^seq(0, -2, length.out = n_gam)[-1]
  fid <- strat_folds(y, 5); sc <- numeric(length(grid))
  for (k in 1:5) { tr <- fid != k; te <- fid == k
    for (j in seq_along(grid)) { f <- gl_fit(A[tr, , drop = FALSE], y[tr], grp, grid[j], 200)
      sc[j] <- sc[j] + auc_fast(drop(A[te, , drop = FALSE] %*% f$w) + f$b, y[te]) } }
  f <- gl_fit(A, y, grp, grid[which.max(sc)])
  list(p = sig(drop(B %*% f$w) + f$b), sel = unique(grp[f$w != 0]))
}
strat_folds <- function(y, k) { f <- integer(length(y))
  for (c in unique(y)) { i <- which(y == c); f[i] <- sample(rep(1:k, length.out = length(i))) }; f }
auc_fast <- function(s, y) { if (length(unique(y)) < 2) return(0.5)
  r <- rank(s); n1 <- sum(y == 1); n0 <- sum(y == 0); (sum(r[y == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0) }

## penalized logistic regression with lambda chosen by inner 5-fold CV (AUC)
glmnet_cv <- function(A, y, B, alpha = 0) {
  A <- as.matrix(A); B <- as.matrix(B)
  if (ncol(A) == 1) { A <- cbind(A, 0); B <- cbind(B, 0) }
  m <- cv.glmnet(A, y, family = "binomial", alpha = alpha, nfolds = 5, type.measure = "auc", foldid = strat_folds(y, 5))
  drop(predict(m, B, s = "lambda.min", type = "response"))
}

## regularized QDA log-odds (Friedman 1989): class covariances shrunk towards the identity
rqda_score <- function(Xtr, ytr, Xte, reg = 0.3) {
  ll <- sapply(0:1, function(k) { Z <- Xtr[ytr == k, , drop = FALSE]; mu <- colMeans(Z)
    S <- (1 - reg) * cov(Z) + reg * diag(ncol(Z)); D <- sweep(Xte, 2, mu)
    -0.5 * (determinant(S)$modulus + rowSums((D %*% solve(S)) * D)) + log(mean(ytr == k)) })
  ll[, 2] - ll[, 1]
}

## WGCNA-type modules: soft-threshold adjacency, topological overlap, dynamic tree cut (Section 2.9)
wgcna_modules <- function(Xtr, Xte, power = 6) {
  A <- abs(cor(Xtr))^power; diag(A) <- 0; k <- rowSums(A)
  TOM <- (A %*% A + A) / (outer(k, k, pmin) + 1 - A); diag(TOM) <- 1
  h <- hclust(as.dist(1 - TOM), "average")
  lab <- cutreeDynamic(h, distM = 1 - TOM, deepSplit = 2, minClusterSize = 5, verbose = 0)
  if (all(lab == 0)) lab[] <- 1
  mods <- setdiff(unique(lab), 0)
  me <- lapply(mods, function(m) { i <- which(lab == m)
    if (length(i) == 1) return(list(tr = Xtr[, i], te = Xte[, i]))
    p <- prcomp(Xtr[, i]); list(tr = p$x[, 1], te = drop(scale(Xte[, i], p$center, FALSE) %*% p$rotation[, 1])) })
  hubs <- unlist(lapply(mods, function(m) { i <- which(lab == m); i[order(-k[i])][1:min(2, length(i))] }))
  list(tr = sapply(me, `[[`, "tr"), te = sapply(me, `[[`, "te"), hubs = hubs)
}
