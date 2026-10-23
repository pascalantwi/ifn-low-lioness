## Repeated nested cross-validation of all models for contrasts C1-C3 in GSE110169 (Sections 2.10-2.11).
## Rscript run_real.R [n_repeats=10] [contrasts=C1,C2,C3]
args <- commandArgs(TRUE); N_REP <- if (length(args) >= 1) as.integer(args[1]) else 10
CONTR <- if (length(args) >= 2) strsplit(args[2], ",")[[1]] else c("C1", "C2", "C3")
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
source(file.path(here, "lib.R")); suppressPackageStartupMessages(library(parallel))
ROOT <- normalizePath(file.path(here, "../../..")); DATA <- file.path(ROOT, "data/GSE110169")
OUT <- file.path(ROOT, "analysis/gse110169/results"); dir.create(OUT, FALSE)

s <- read.delim(file.path(DATA, "processed/samples.tsv"))
ann <- read.delim(file.path(DATA, "processed/probe_annotation.tsv"), row.names = 1)
E <- as.matrix(read.delim(gzfile(file.path(DATA, "processed/expression_probes.tsv.gz")), row.names = 1, check.names = FALSE))
Xall <- t(E); pg <- ann[colnames(Xall), "gene_symbol"]
gmt <- read_gmt(file.path(DATA, "c2.cp.reactome.v2024.1.Hs.symbols.gmt"))
PW <- subpathways(gmt, unique(pg)); pw_names <- names(PW)
cat("sub-pathways:", paste0(sub("REACTOME_", "", pw_names), " (", lengths(PW), ")", collapse = "; "), "\n")
jsonlite::write_json(PW, file.path(OUT, "subpathways.json"), pretty = TRUE)
probes_by_gene <- split(seq_along(pg), pg); all_genes <- names(probes_by_gene)
group <- s$group; batch <- model.matrix(~ batch, s)[, -1]

CONTRASTS <- list(C1 = list(univ = c("SLE", "HC"), pos = c("SLE", "high"), neg = c("HC", "low")),
                  C2 = list(univ = c("SLE", "HC"), pos = c("SLE", "low"), neg = c("HC", "low")),
                  C3 = list(univ = c("SLE", "RA", "HC"), pos = c("SLE", "low"), neg = c("RA", "low")))
MODELS <- c("M0a", "M0c", "M1", "M2", "M3-score", "M3-boost", "M3-SVM", "M4", "M5", "M6",
            "W1", "W2", "L1", "L2", "L2-P", "L2-S", "L3", "L3-P")

collapse <- function(tr, genes) sapply(genes, function(g) { p <- probes_by_gene[[g]]
  if (length(p) == 1) p else p[which.max(apply(Xall[tr, p, drop = FALSE], 2, var))] })

run_fold <- function(job) {
  cn <- job$c; ct <- CONTRASTS[[cn]]; tru <- job$tr; teu <- job$te
  set.seed(1000 * job$rep + job$k)
  ## IFN score and cutoff from the training controls (Section 2.3)
  hc <- tru[group[tru] == "HC"]; Xi <- Xall[, collapse(tru, IFN_GENES)]
  Z <- sweep(sweep(Xi, 2, colMeans(Xi[hc, ])), 2, apply(Xi[hc, ], 2, sd), "/"); I <- rowMeans(Z)
  theta <- mean(I[hc]) + 2 * sd(I[hc]); status <- ifelse(I > theta, "high", "low")
  pick <- function(idx) { p <- idx[group[idx] == ct$pos[1] & status[idx] == ct$pos[2]]
    n <- idx[group[idx] == ct$neg[1] & status[idx] == ct$neg[2]]; list(i = c(p, n), y = c(rep(1, length(p)), rep(0, length(n)))) }
  a <- pick(tru); b <- pick(teu); tr <- a$i; y <- a$y; te <- b$i
  if (length(unique(b$y)) < 2) return(NULL)
  ## gene-level data with in-fold probe choice; cell-composition scores (Section 2.4)
  Xg <- Xall[, collapse(tru, all_genes)]; colnames(Xg) <- all_genes
  Rk <- t(apply(Xg, 1, rank))
  cells <- sapply(CELL_MARKERS, function(m) singscore(Rk, match(intersect(m, all_genes), all_genes)))
  cov <- scale(cbind(IFN = I, cells), colMeans(cbind(I, cells)[tr, ]), apply(cbind(I, cells)[tr, ], 2, sd))
  ## pathway matrices: top 50 genes by training variance, standardized and winsorized in-fold
  pw <- lapply(PW, function(g) { X <- Xg[, g, drop = FALSE]
    if (ncol(X) > 50) X <- X[, order(-apply(X[tr, ], 2, var))[1:50]]
    pmin(pmax(scale(X, colMeans(X[tr, ]), apply(X[tr, ], 2, sd)), -4), 4) })
  K <- length(pw); pr <- list(); sel <- list()
  gl <- function(blocks, key) { A <- do.call(cbind, lapply(blocks, function(x) x[tr, , drop = FALSE]))
    B <- do.call(cbind, lapply(blocks, function(x) x[te, , drop = FALSE]))
    grp <- unlist(lapply(seq_along(blocks), function(i) rep(i, ncol(blocks[[i]]))))
    r <- gl_predict(A, y, B, grp); pr[[key]] <<- r$p; sel[[key]] <<- r$sel }
  ## baselines
  pr$M0a <- predict(glm(y ~ I, data = data.frame(y = y, I = I[tr]), family = binomial), data.frame(I = I[te]), type = "response")
  pr$M0c <- glmnet_cv(cells[tr, ], y, cells[te, ])
  ## M1: all genes (5,000 most variable in training), elastic net
  top <- order(-apply(Xg[tr, ], 2, var))[1:5000]
  pr$M1 <- glmnet_cv(Xg[tr, top], y, Xg[te, top], alpha = 0.5)
  ## expression comparators
  gl(pw, "M2")
  gl(lapply(pw, function(X) { p <- prcomp(X[tr, ]); cbind(rowMeans(X), scale(X, p$center, FALSE) %*% p$rotation[, 1]) }), "M3-score")
  U <- do.call(cbind, pw); U <- U[, !duplicated(colnames(U))]
  d <- data.frame(y = y, U[tr, ]); colnames(d) <- c("y", paste0("g", seq_len(ncol(U))))
  gb <- gbm(y ~ ., data = d, distribution = "bernoulli", n.trees = 100, interaction.depth = 2, shrinkage = 0.1, bag.fraction = 1, verbose = FALSE)
  nd <- data.frame(U[te, , drop = FALSE]); colnames(nd) <- colnames(d)[-1]
  pr$`M3-boost` <- predict(gb, nd, n.trees = 100, type = "response")
  sv <- svm(U[tr, ], factor(y), kernel = "radial", cost = 1, scale = FALSE)
  dv <- attr(predict(sv, U[te, , drop = FALSE], decision.values = TRUE), "decision.values")
  pr$`M3-SVM` <- if (colnames(dv)[1] == "1/0") dv[, 1] else -dv[, 1]
  gl(lapply(pw, function(X) { R <- X[tr, ][y == 0, ]; S <- cov(R); S <- 0.8 * S + 0.2 * diag(diag(S))
    D <- sweep(X, 2, colMeans(R)); matrix(rowSums((D %*% solve(S)) * D)) }), "M4")
  Iz <- cov[, "IFN", drop = FALSE]
  gl(c(pw, list(Iz)), "M5")
  gl(lapply(pw, function(X) { col <- numeric(nrow(X)); f <- strat_folds(y, 5); v <- numeric(length(tr))
    for (k in 1:5) v[f == k] <- rqda_score(X[tr, ][f != k, ], y[f != k], X[tr, ][f == k, , drop = FALSE])
    col[tr] <- v; col[te] <- rqda_score(X[tr, ], y, X[te, , drop = FALSE]); matrix(col) }), "M6")
  ## established network methods on the union of pathway genes
  wm <- wgcna_modules(U[tr, ], U[te, , drop = FALSE])
  pr$W1 <- glmnet_cv(U[tr, wm$hubs], y, U[te, wm$hubs, drop = FALSE])
  pr$W2 <- glmnet_cv(as.matrix(wm$tr), y, matrix(wm$te, nrow = length(te)))
  ## LIONESS (Sections 2.7-2.8); partial correlations conditioned on IFN score and cell scores
  Fp <- list(); Fq <- list(); edges <- list()
  for (n in names(pw)) { X <- pw[[n]]; G <- ncol(X); ut <- upper.tri(diag(G))
    lam <- lam_ss(cbind(X[tr, ], cov[tr, ]))
    for (meas in c("partial", "pearson")) {
      f <- if (meas == "partial") pcor_mat else pear_mat
      C <- if (meas == "partial") cov else NULL
      Ct <- if (is.null(C)) NULL else C[tr, , drop = FALSE]; Cs <- if (is.null(C)) NULL else C[te, , drop = FALSE]
      L <- lioness(X[tr, ], y, X[te, , drop = FALSE], f, Ct, Cs, lam)
      Pm <- f(X[tr, ], Ct, lam); kappa <- quantile(abs(L$tr), 0.99)
      dP <- (f(X[tr, ][y == 1, ], if (is.null(Ct)) NULL else Ct[y == 1, ], lam) - f(X[tr, ][y == 0, ], if (is.null(Ct)) NULL else Ct[y == 0, ], lam))[ut]
      Ft <- net_features(L$tr, Pm, kappa, dP, G); Fs <- net_features(L$te, Pm, kappa, dP, G)
      ## cross-fitted DN score for training samples: weights estimated without the sample's inner fold
      cf <- strat_folds(y, 5)
      for (k in 1:5) { a <- cf != k
        dPk <- (f(X[tr, ][a & y == 1, ], if (is.null(Ct)) NULL else Ct[a & y == 1, ], lam) - f(X[tr, ][a & y == 0, ], if (is.null(Ct)) NULL else Ct[a & y == 0, ], lam))[ut]
        Ft[cf == k, "DN"] <- L$tr[cf == k, , drop = FALSE] %*% dPk }
      full <- matrix(0, nrow(Xall), ncol(Ft)); full[tr, ] <- Ft; full[te, ] <- Fs
      if (meas == "partial") { Fp[[n]] <- full; e <- matrix(0, nrow(Xall), ncol(L$tr)); e[tr, ] <- L$tr; e[te, ] <- L$te; edges[[n]] <- e } else Fq[[n]] <- full
    } }
  El <- do.call(cbind, edges); pr$L1 <- glmnet_cv(El[tr, ], y, El[te, , drop = FALSE])
  gl(lapply(Fp, key4), "L2"); gl(lapply(Fq, key4), "L2-P"); gl(Fp, "L2-S")
  gl(c(lapply(Fp, key4), pw, list(Iz)), "L3"); gl(c(lapply(Fq, key4), pw, list(Iz)), "L3-P")
  lab <- function(v, key) { nm <- if (key %in% c("L3", "L3-P")) c(paste0("net:", names(pw)), paste0("expr:", names(pw)), "IFN")
    else if (key == "M5") c(paste0("expr:", names(pw)), "IFN") else names(pw); nm[v] }
  list(contrast = cn, rep = job$rep, fold = job$k, te = te, y = b$y, n_tr = length(tr), n_pos_tr = sum(y),
       theta = theta, pred = lapply(pr[MODELS], as.numeric), sel = mapply(lab, sel, names(sel), SIMPLIFY = FALSE))
}

N_PERM <- if (length(args) >= 3) as.integer(args[3]) else 0
if (N_PERM > 0) {   # leakage check (Section 2.11): group labels permuted within the contrast universe, one repeat each
  group0 <- group; auc <- function(p, y) { r <- rank(p); n1 <- sum(y); n0 <- sum(1 - y); (sum(r[y == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0) }
  for (cn in CONTR) { univ <- which(group0 %in% CONTRASTS[[cn]]$univ); out <- list()
    for (b in 1:N_PERM) { set.seed(50000 + b); group <<- group0; group[univ] <<- sample(group0[univ])
      f <- integer(length(univ)); strat <- group[univ]
      for (sg in unique(strat)) { i <- which(strat == sg); f[i] <- sample(rep(1:5, length.out = length(i))) }
      jobs <- lapply(1:5, function(k) list(c = cn, rep = 1000 + b, k = k, tr = univ[f != k], te = univ[f == k]))
      res <- Filter(function(x) !is.null(x) && is.null(x$error), mclapply(jobs, function(j) tryCatch(run_fold(j), error = function(e) list(error = conditionMessage(e))), mc.cores = 4))
      y <- unlist(lapply(res, `[[`, "y"))
      out[[b]] <- sapply(MODELS, function(m) auc(unlist(lapply(res, function(x) x$pred[[m]])), y))
      cat(cn, "perm", b, round(out[[b]][c("M5", "L3", "L3-P")], 3), "\n") }
    saveRDS(do.call(rbind, out), file.path(OUT, paste0("perm_", cn, ".rds"))) }
  quit(save = "no") }

for (cn in CONTR) {
  t0 <- Sys.time(); ct <- CONTRASTS[[cn]]; univ <- which(group %in% ct$univ)
  ## folds stratified by group, batch and approximate IFN status (cutoff from all controls; used only to balance folds)
  Iall <- local({ Xi <- Xall[, sapply(IFN_GENES, function(g) probes_by_gene[[g]][1])]; hc <- group == "HC"
    rowMeans(sweep(sweep(Xi, 2, colMeans(Xi[hc, ])), 2, apply(Xi[hc, ], 2, sd), "/")) })
  st0 <- ifelse(Iall > mean(Iall[group == "HC"]) + 2 * sd(Iall[group == "HC"]), "high", "low")
  strat <- paste(group[univ], st0[univ], s$batch[univ])
  jobs <- list()
  for (r in 1:N_REP) { set.seed(r); f <- integer(length(univ))
    for (sg in unique(strat)) { i <- which(strat == sg); f[i] <- sample(rep(1:5, length.out = length(i))) }
    for (k in 1:5) jobs[[length(jobs) + 1]] <- list(c = cn, rep = r, k = k, tr = univ[f != k], te = univ[f == k]) }
  res <- mclapply(jobs, function(j) tryCatch(run_fold(j), error = function(e) list(error = conditionMessage(e))), mc.cores = 4)
  err <- Filter(function(x) !is.null(x$error), res); if (length(err)) print(err[[1]])
  res <- Filter(function(x) !is.null(x) && is.null(x$error), res)
  saveRDS(res, file.path(OUT, paste0("oof_", cn, ".rds")))
  cat(cn, "folds:", length(res), "time:", round(as.numeric(difftime(Sys.time(), t0, units = "secs"))), "s\n")
}
