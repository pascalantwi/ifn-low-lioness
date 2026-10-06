"""Numerical checks supporting reviews/2026-10-06_initial_critique.md (Section 2.3, Appendix R1).

Run: python3 reviews/2026-10-06_appendixA_checks.py   (needs numpy)

Check 1: exact leave-one-out LIONESS on (shrinkage) partial correlation vs
         (a) the plan's first-order formula (Appendix A), and
         (b) the shrinkage-corrected first-order formula derived in the review.
Check 2: residual-based features (M5, M7a) computed with an in-sample reference are on a
         different scale for training vs new (test) samples.
Check 3: exact LIONESS edges are on the same scale for training (leave-one-out) and
         test (add-one-in) samples, so the plan's symmetry claim holds.
Check 4: under heavy shrinkage (large pathways), LIONESS-partial and LIONESS-Pearson edges
         become strongly correlated across patients.
Shrinkage model throughout: Sigma_lam = (1-lam) S + lam diag(S), lam fixed (corpcor-style
correlation shrinkage with variances not shrunk). Data: Gaussian, tridiagonal precision.
"""
import numpy as np


def cov(X):
    mu = X.mean(0)
    D = X - mu
    return D.T @ D / X.shape[0], mu


def shrink(S, lam):
    return (1 - lam) * S + lam * np.diag(np.diag(S))


def pcor(S):
    O = np.linalg.inv(S)
    d = np.sqrt(np.diag(O))
    P = -O / np.outer(d, d)
    np.fill_diagonal(P, 1)
    return P, O


def pearson(S):
    d = np.sqrt(np.diag(S))
    return S / np.outer(d, d)


def chain_sigma(G):
    A = np.eye(G) + np.diag(np.full(G - 1, 0.4), 1) + np.diag(np.full(G - 1, 0.4), -1)
    return np.linalg.inv(A)


def check1(rng):
    print("Check 1: exact LIONESS-partial vs first-order formulas")
    for N, G, lam in [(100, 12, 0), (300, 12, 0), (100, 40, 0), (100, 40, 0.2),
                      (300, 12, 0.2), (100, 40, 0.5), (130, 100, 0.5), (130, 150, 0.7)]:
        X = rng.multivariate_normal(np.zeros(G), chain_sigma(G), size=N)
        S, mu = cov(X)
        P, O = pcor(shrink(S, lam))
        s = np.sqrt(np.diag(O))
        iu = np.triu_indices(G, 1)
        ex, plan, fix = [], [], []
        for q in range(N):
            Pm, _ = pcor(shrink(cov(np.delete(X, q, 0))[0], lam))
            ex.append((N * P - (N - 1) * Pm)[iu])
            d = X[q] - mu
            u = O @ d
            ut = u / s
            plan.append((np.outer(ut, ut) + P * (1 + (ut[:, None] ** 2 + ut[None, :] ** 2) / 2))[iu])
            M = (1 - lam) * np.outer(u, u) + lam * O @ np.diag(d ** 2) @ O
            Mt = M / np.outer(s, s)
            dm = np.diag(Mt)
            fix.append((P + Mt + P * (dm[:, None] + dm[None, :]) / 2)[iu])
        ex, plan, fix = map(np.concatenate, (ex, plan, fix))
        print(f"  N={N:3d} G={G:3d} lam={lam}: cor(exact, plan formula)={np.corrcoef(ex, plan)[0, 1]:.4f}  "
              f"cor(exact, shrinkage-corrected)={np.corrcoef(ex, fix)[0, 1]:.4f}")


def check2(rng):
    print("Check 2: mean sum(u~^2)/G, in-sample (training) vs new (test) samples, same reference")
    for N, G, lam in [(130, 15, 0.1), (130, 50, 0.3), (130, 100, 0.5), (130, 150, 0.7)]:
        Sig = chain_sigma(G)
        X = rng.multivariate_normal(np.zeros(G), Sig, size=N)
        T = rng.multivariate_normal(np.zeros(G), Sig, size=200)
        S, mu = cov(X)
        O = np.linalg.inv(shrink(S, lam))
        s = np.sqrt(np.diag(O))
        f = lambda x: np.sum(((O @ (x - mu)) / s) ** 2) / G
        tr = np.mean([f(x) for x in X])
        te = np.mean([f(x) for x in T])
        print(f"  N={N} G={G:3d} lam={lam}: train {tr:.2f}  test {te:.2f}  ratio {te / tr:.2f}")


def check3(rng):
    print("Check 3: SD of exact LIONESS edge deviations, training (LOO) vs test (add-one-in)")
    for N, G, lam in [(130, 15, 0.1), (130, 50, 0.3), (130, 100, 0.5), (130, 150, 0.7)]:
        Sig = chain_sigma(G)
        X = rng.multivariate_normal(np.zeros(G), Sig, size=N)
        T = rng.multivariate_normal(np.zeros(G), Sig, size=60)
        iu = np.triu_indices(G, 1)
        P = pcor(shrink(cov(X)[0], lam))[0]
        tr = np.array([(N * P - (N - 1) * pcor(shrink(cov(np.delete(X, q, 0))[0], lam))[0])[iu]
                       for q in range(0, N, 2)])
        te = np.array([((N + 1) * pcor(shrink(cov(np.vstack([X, t]))[0], lam))[0] - N * P)[iu] for t in T])
        a, b = np.std(tr - P[iu]), np.std(te - P[iu])
        print(f"  N={N} G={G:3d} lam={lam}: train {a:.3f}  test {b:.3f}  ratio {b / a:.2f}")


def check4(rng):
    print("Check 4: mean per-edge across-patient correlation, LIONESS-partial vs LIONESS-Pearson")
    for N, G, lam in [(130, 15, 0.1), (130, 50, 0.3), (130, 100, 0.6), (130, 150, 0.8)]:
        X = rng.multivariate_normal(np.zeros(G), chain_sigma(G), size=N)
        iu = np.triu_indices(G, 1)
        S = cov(X)[0]
        Pp, Pr = pcor(shrink(S, lam))[0], pearson(S)
        a, b = [], []
        for q in range(0, N, 5):
            Sm = cov(np.delete(X, q, 0))[0]
            a.append((N * Pp - (N - 1) * pcor(shrink(Sm, lam))[0])[iu])
            b.append((N * Pr - (N - 1) * pearson(Sm))[iu])
        a, b = np.array(a), np.array(b)
        c = np.nanmean([np.corrcoef(a[:, k], b[:, k])[0, 1] for k in range(a.shape[1])])
        print(f"  N={N} G={G:3d} lam={lam}: {c:.2f}")


if __name__ == "__main__":
    check1(np.random.default_rng(1))
    check2(np.random.default_rng(2))
    check3(np.random.default_rng(3))
    check4(np.random.default_rng(2))
