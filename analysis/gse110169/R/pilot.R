## Pilot (exploratory): (a) LIONESS with a healthy-control reference, (b) immune pathways outside interferon.
## One repeat of 5-fold cross-validation, contrasts C2 and C3. Rscript pilot.R [n_repeats=1]
args <- commandArgs(TRUE); N_REP <- if (length(args) >= 1) as.integer(args[1]) else 1
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
source(file.path(here, "lib.R")); suppressPackageStartupMessages(library(parallel))
ROOT <- normalizePath(file.path(here, "../../..")); DATA <- file.path(ROOT, "data/GSE110169"); OUT <- file.path(ROOT, "analysis/gse110169/results")
s <- read.delim(file.path(DATA, "processed/samples.tsv")); ann <- read.delim(file.path(DATA, "processed/probe_annotation.tsv"), row.names = 1)
E <- as.matrix(read.delim(gzfile(file.path(DATA, "processed/expression_probes.tsv.gz")), row.names = 1, check.names = FALSE))
Xall <- t(E); pg <- ann[colnames(Xall), "gene_symbol"]; gmt <- read_gmt(file.path(DATA, "c2.cp.reactome.v2024.1.Hs.symbols.gmt"))
probes_by_gene <- split(seq_along(pg), pg); all_genes <- names(probes_by_gene); group <- s$group
PW_IFN <- subpathways(gmt, unique(pg))
IMM <- paste0("REACTOME_", c("SIGNALING_BY_THE_B_CELL_RECEPTOR_BCR", "TCR_SIGNALING", "NEUTROPHIL_DEGRANULATION", "TOLL_LIKE_RECEPTOR_CASCADES", "SIGNALING_BY_INTERLEUKINS"))
PW_IMM <- lapply(setNames(IMM, IMM), function(k) sort(setdiff(intersect(gmt[[k]], unique(pg)), c(IFN_GENES, SEX_GENES))))
CONTRASTS <- list(C2 = list(univ = c("SLE", "HC"), pos = c("SLE", "low"), neg = c("HC", "low")),
                  C3 = list(univ = c("SLE", "RA", "HC"), pos = c("SLE", "low"), neg = c("RA", "low")))
collapse <- function(tr, genes) sapply(genes, function(g) { p <- probes_by_gene[[g]]
  if (length(p) == 1) p else p[which.max(apply(Xall[tr, p, drop = FALSE], 2, var))] })

## LIONESS with one fixed reference set (healthy controls): leave-one-out for reference members, add-one-in otherwise
lioness_ref <- function(R, CR, Xs, Cs, inR, f, lam) {
  G <- ncol(R); ut <- upper.tri(diag(G)); N <- nrow(R); P <- f(R, CR, lam)
  t(sapply(seq_len(nrow(Xs)), function(i) { k <- inR[i]
    if (!is.na(k)) (N * P - (N - 1) * f(R[-k, , drop = FALSE], if (is.null(CR)) NULL else CR[-k, , drop = FALSE], lam))[ut]
    else ((N + 1) * f(rbind(R, Xs[i, ]), if (is.null(CR)) NULL else rbind(CR, Cs[i, ]), lam) - N * P)[ut] }))
}

run_fold <- function(job) {
  ct <- CONTRASTS[[job$c]]; tru <- job$tr; teu <- job$te; set.seed(7000 + 10 * job$rep + job$k)
  hc <- tru[group[tru] == "HC"]; Xi <- Xall[, collapse(tru, IFN_GENES)]
  I <- rowMeans(sweep(sweep(Xi, 2, colMeans(Xi[hc, ])), 2, apply(Xi[hc, ], 2, sd), "/"))
  theta <- mean(I[hc]) + 2 * sd(I[hc]); st <- ifelse(I > theta, "high", "low")
  pick <- function(idx) { p <- idx[group[idx] == ct$pos[1] & st[idx] == ct$pos[2]]; n <- idx[group[idx] == ct$neg[1] & st[idx] == ct$neg[2]]
    list(i = c(p, n), y = c(rep(1, length(p)), rep(0, length(n)))) }
  a <- pick(tru); b <- pick(teu); tr <- a$i; y <- a$y; te <- b$i; if (length(unique(b$y)) < 2) return(NULL)
  href <- hc[st[hc] == "low"]                                   # healthy reference: IFN-low training controls
  Xg <- Xall[, collapse(tru, all_genes)]; colnames(Xg) <- all_genes; Rk <- t(apply(Xg, 1, rank))
  cells <- sapply(CELL_MARKERS, function(m) singscore(Rk, match(intersect(m, all_genes), all_genes)))
  cr <- cbind(I, cells); cov <- scale(cr, colMeans(cr[tr, ]), apply(cr[tr, ], 2, sd)); Iz <- cov[, 1, drop = FALSE]
  pr <- list()
  gl <- function(blocks, key) { A <- do.call(cbind, lapply(blocks, function(x) x[tr, , drop = FALSE])); B <- do.call(cbind, lapply(blocks, function(x) x[te, , drop = FALSE]))
    grp <- unlist(lapply(seq_along(blocks), function(i) rep(i, ncol(blocks[[i]])))); pr[[key]] <<- gl_predict(A, y, B, grp)$p }
  pr$M0a <- predict(glm(y ~ I, data = data.frame(y = y, I = I[tr]), family = binomial), data.frame(I = I[te]), type = "response")
  for (set in c("IFN", "IMM")) {
    PW <- if (set == "IFN") PW_IFN else PW_IMM
    pw <- lapply(PW, function(g) { X <- Xg[, g, drop = FALSE]; if (ncol(X) > 50) X <- X[, order(-apply(X[tr, ], 2, var))[1:50]]
      pmin(pmax(scale(X, colMeans(X[tr, ]), apply(X[tr, ], 2, sd)), -4), 4) })
    gl(pw, paste0("M2|", set)); gl(c(pw, list(Iz)), paste0("M5|", set))
    gl(lapply(pw, function(X) { R <- X[tr, ][y == 0, ]; S <- cov(R); S <- 0.8 * S + 0.2 * diag(diag(S)); D <- sweep(X, 2, colMeans(R)); matrix(rowSums((D %*% solve(S)) * D)) }), paste0("M4|", set))
    refs <- if (set == "IFN") c("balanced", "healthy") else c("balanced", "healthy")
    for (ref in refs) { F <- list(partial = list(), pearson = list())
      for (n in names(pw)) { X <- pw[[n]]; G <- ncol(X); ut <- upper.tri(diag(G)); lam <- lam_ss(cbind(X[tr, ], cov[tr, ]))
        for (meas in c("partial", "pearson")) { f <- if (meas == "partial") pcor_mat else pear_mat; C <- if (meas == "partial") cov else NULL
          sub <- function(i) if (is.null(C)) NULL else C[i, , drop = FALSE]
          if (ref == "balanced") { L <- lioness(X[tr, ], y, X[te, , drop = FALSE], f, sub(tr), sub(te), lam); Etr <- L$tr; Ete <- L$te }
          else { R <- X[href, , drop = FALSE]; all <- c(tr, te); inR <- match(all, href)
            Eall <- lioness_ref(R, sub(href), X[all, , drop = FALSE], sub(all), inR, f, lam); Etr <- Eall[seq_along(tr), , drop = FALSE]; Ete <- Eall[-seq_along(tr), , drop = FALSE] }
          Pm <- if (ref == "balanced") f(X[tr, ], sub(tr), lam) else f(X[href, ], sub(href), lam); kappa <- quantile(abs(Etr), 0.99)
          dP <- (f(X[tr, ][y == 1, ], if (is.null(C)) NULL else C[tr, ][y == 1, ], lam) - f(X[tr, ][y == 0, ], if (is.null(C)) NULL else C[tr, ][y == 0, ], lam))[ut]
          Ft <- net_features(Etr, Pm, kappa, dP, G); Fs <- net_features(Ete, Pm, kappa, dP, G); cf <- strat_folds(y, 5)
          for (k in 1:5) { a2 <- cf != k
            dPk <- (f(X[tr, ][a2 & y == 1, ], if (is.null(C)) NULL else C[tr, ][a2 & y == 1, ], lam) - f(X[tr, ][a2 & y == 0, ], if (is.null(C)) NULL else C[tr, ][a2 & y == 0, ], lam))[ut]
            Ft[cf == k, "DN"] <- Etr[cf == k, , drop = FALSE] %*% dPk }
          full <- matrix(0, nrow(Xall), 4); full[tr, ] <- Ft[, 1:4]; full[te, ] <- Fs[, 1:4]; F[[meas]][[n]] <- full } }
      tag <- paste0("|", set, "|", ref)
      gl(F$partial, paste0("L2", tag)); gl(F$pearson, paste0("L2-P", tag))
      gl(c(F$partial, pw, list(Iz)), paste0("L3", tag)); gl(c(F$pearson, pw, list(Iz)), paste0("L3-P", tag)) } }
  list(contrast = job$c, rep = job$rep, fold = job$k, y = b$y, pred = lapply(pr, as.numeric))
}

jobs <- list()
for (cn in names(CONTRASTS)) { univ <- which(group %in% CONTRASTS[[cn]]$univ)
  Xi <- Xall[, sapply(IFN_GENES, function(g) probes_by_gene[[g]][1])]; h <- group == "HC"
  Ia <- rowMeans(sweep(sweep(Xi, 2, colMeans(Xi[h, ])), 2, apply(Xi[h, ], 2, sd), "/")); s0 <- ifelse(Ia > mean(Ia[h]) + 2 * sd(Ia[h]), "high", "low")
  strat <- paste(group[univ], s0[univ], s$batch[univ])
  for (r in 1:N_REP) { set.seed(r); f <- integer(length(univ))
    for (sg in unique(strat)) { i <- which(strat == sg); f[i] <- sample(rep(1:5, length.out = length(i))) }
    for (k in 1:5) jobs[[length(jobs) + 1]] <- list(c = cn, rep = r, k = k, tr = univ[f != k], te = univ[f == k]) } }
cat("immune pathways:", paste0(sub("REACTOME_", "", names(PW_IMM)), " (", lengths(PW_IMM), ")", collapse = "; "), "\n")
res <- mclapply(jobs, function(j) tryCatch(run_fold(j), error = function(e) list(error = conditionMessage(e))), mc.cores = 4)
err <- Filter(function(x) !is.null(x$error), res); if (length(err)) print(err[[1]]$error)
res <- Filter(function(x) !is.null(x) && is.null(x$error), res); saveRDS(res, file.path(OUT, "pilot.rds"))
auc <- function(p, y) { r <- rank(p); n1 <- sum(y); n0 <- sum(1 - y); (sum(r[y == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0) }
tab <- do.call(rbind, lapply(c("C2", "C3"), function(cn) { R <- Filter(function(x) x$contrast == cn, res)
  do.call(rbind, lapply(names(R[[1]]$pred), function(m) data.frame(contrast = cn, model = m,
    AUC = mean(sapply(unique(sapply(R, `[[`, "rep")), function(r) { Rr <- Filter(function(x) x$rep == r, R)
      auc(unlist(lapply(Rr, function(x) x$pred[[m]])), unlist(lapply(Rr, `[[`, "y"))) }))))) }))
write.csv(tab, file.path(OUT, "pilot_auc.csv"), row.names = FALSE)
print(reshape(tab, idvar = "model", timevar = "contrast", direction = "wide"), digits = 3, row.names = FALSE)
