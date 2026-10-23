## Performance summaries (Section 2.11): AUC per repeat (pooled out-of-fold predictions), Brier score,
## area under the precision-recall curve, paired AUC differences with the Nadeau-Bengio corrected
## standard error (equations 24-25), Holm correction within H1 and H2, and pathway selection frequencies.
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
OUT <- normalizePath(file.path(here, "../results"))
auc <- function(s, y) { r <- rank(s); n1 <- sum(y == 1); n0 <- sum(y == 0); (sum(r[y == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0) }
ap <- function(s, y) { o <- order(-s); y <- y[o]; tp <- cumsum(y); sum((tp / seq_along(y))[y == 1]) / sum(y) }
PAIRS <- list(H1a = c("L3", "M5"), H1b = c("L3-P", "M5"), H2a = c("L2", "M6"), H2b = c("L2-P", "M6"), H2c = c("L2", "M4"), H2d = c("L2-P", "M4"),
              E1 = c("M5", "M0a"), E2 = c("L3", "L2"), E3 = c("W2", "M5"))
perf <- list(); pairs <- list(); selr <- list(); sizes <- list()
for (cn in c("C1", "C2", "C3", "C4")) { f <- file.path(OUT, paste0("oof_", cn, ".rds")); if (!file.exists(f)) next
  R <- readRDS(f); models <- names(R[[1]]$pred); reps <- sort(unique(sapply(R, `[[`, "rep")))
  sizes[[cn]] <- data.frame(contrast = cn, mean_test_pos = mean(sapply(reps, function(r) sum(unlist(lapply(Filter(function(x) x$rep == r, R), `[[`, "y"))))),
    mean_test_neg = mean(sapply(reps, function(r) sum(1 - unlist(lapply(Filter(function(x) x$rep == r, R), `[[`, "y"))))),
    mean_train = mean(sapply(R, `[[`, "n_tr")), theta_mean = mean(sapply(R, `[[`, "theta")), theta_sd = sd(sapply(R, `[[`, "theta")))
  for (m in models) {
    a <- sapply(reps, function(r) { Rr <- Filter(function(x) x$rep == r, R); y <- unlist(lapply(Rr, `[[`, "y")); p <- unlist(lapply(Rr, function(x) x$pred[[m]])); c(auc(p, y), ap(p, y), if (all(p >= 0 & p <= 1)) mean((p - y)^2) else NA, mean(y)) })
    perf[[length(perf) + 1]] <- data.frame(contrast = cn, model = m, AUC = mean(a[1, ]), AUC_sd = sd(a[1, ]), AUC_min = min(a[1, ]), AUC_max = max(a[1, ]),
      AUPRC = mean(a[2, ]), prevalence = mean(a[4, ]), Brier = mean(a[3, ]))
  }
  ## paired differences: fold-level AUC differences, Nadeau-Bengio corrected variance
  fa <- function(m) sapply(R, function(x) auc(x$pred[[m]], x$y))
  ntr <- mean(sapply(R, `[[`, "n_tr")); nte <- mean(sapply(R, function(x) length(x$y)))
  for (h in names(PAIRS)) { a <- PAIRS[[h]][1]; b <- PAIRS[[h]][2]; d <- fa(a) - fa(b); J <- length(d)
    se <- sqrt((1 / J + nte / ntr) * var(d))
    dr <- mean(perf[[which(sapply(perf, function(p) p$contrast == cn && p$model == a))]]$AUC) - perf[[which(sapply(perf, function(p) p$contrast == cn && p$model == b))]]$AUC
    pairs[[length(pairs) + 1]] <- data.frame(contrast = cn, hypothesis = h, comparison = paste(a, "vs", b), delta_AUC = dr,
      delta_fold_mean = mean(d), SE = se, lo = dr - 1.96 * se, hi = dr + 1.96 * se, p = 2 * pnorm(-abs(dr / se))) }
  ## pathway selection frequencies in group-lasso models
  for (m in c("M2", "M5", "L2", "L2-P", "L3", "L3-P")) { v <- unlist(lapply(R, function(x) x$sel[[m]]))
    tb <- table(v) / length(R); selr[[length(selr) + 1]] <- data.frame(contrast = cn, model = m, feature = names(tb), selected = as.numeric(tb)) }
}
perf <- do.call(rbind, perf); pairs <- do.call(rbind, pairs); selr <- do.call(rbind, selr); sizes <- do.call(rbind, sizes)
pairs$p_holm <- NA
for (cn in unique(pairs$contrast)) for (h in c("H1", "H2")) { i <- pairs$contrast == cn & startsWith(pairs$hypothesis, h); pairs$p_holm[i] <- p.adjust(pairs$p[i], "holm") }
write.csv(perf, file.path(OUT, "performance.csv"), row.names = FALSE)
write.csv(pairs, file.path(OUT, "paired_differences.csv"), row.names = FALSE)
write.csv(selr, file.path(OUT, "pathway_selection.csv"), row.names = FALSE)
write.csv(sizes, file.path(OUT, "group_sizes.csv"), row.names = FALSE)
print(sizes); print(reshape(perf[, c("contrast", "model", "AUC")], idvar = "model", timevar = "contrast", direction = "wide"), digits = 3)
print(pairs[, c("contrast", "hypothesis", "comparison", "delta_AUC", "lo", "hi", "p", "p_holm")], digits = 3)
