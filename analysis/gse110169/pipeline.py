"""Analysis pipeline for GSE110169 (Sections 2.2-2.12 of manuscript/progress_draft.md).

Everything that learns from data (probe choice, standardization, IFN cutoff, LIONESS references,
kappa, DN weights, tau, penalties) is estimated inside the training fold and applied unchanged
to the test fold.
"""
import gzip, numpy as np, pandas as pd, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, fcluster
warnings.filterwarnings("ignore")

ROOT = __file__.rsplit("/analysis/", 1)[0]
DATA = ROOT + "/data/GSE110169/"
IFN_GENES = ["IFI27", "IFI44", "IFI44L", "RSAD2"]
Y_GENES = {"RPS4Y1", "DDX3Y", "KDM5D", "UTY", "EIF1AY", "XIST", "TSIX"}
# cell-type marker sets (Section 2.4); canonical markers fixed before the analysis
CELL_MARKERS = {
    "neutrophils": ["FCGR3B", "CXCR2", "CSF3R", "FPR1", "MME", "CXCR1"],
    "monocytes": ["CD14", "LYZ", "CSF1R", "FCN1", "VCAN"],
    "B_cells": ["MS4A1", "CD79A", "CD79B", "CD19", "BANK1"],
    "plasmablasts": ["MZB1", "JCHAIN", "TNFRSF17", "TXNDC5"],
    "T_cells": ["CD3D", "CD3E", "CD3G", "CD2", "CD28"],
    "NK_cells": ["GNLY", "NKG7", "KLRD1", "PRF1", "KLRF1"],
    "eosinophils": ["CLC", "IL5RA", "CCR3", "SIGLEC8", "PRG2"],
}
B_REF = 20

# ------------------------------------------------------------------ data
def load():
    s = pd.read_csv(DATA + "processed/samples.tsv", sep="\t")
    ann = pd.read_csv(DATA + "processed/probe_annotation.tsv", sep="\t", index_col=0)
    e = pd.read_csv(DATA + "processed/expression_probes.tsv.gz", sep="\t", index_col=0)
    return s, ann, e

def read_gmt(path):
    return {l.split("\t")[0]: l.rstrip("\n").split("\t")[2:] for l in open(path)}

def subpathways(gmt, genes_present):
    """Section 2.5: sub-pathways of REACTOME_INTERFERON_SIGNALING (sets lying inside it),
    IFN-score genes removed, 15-50 genes (larger sets cut to 50 in-fold), Jaccard > 0.8 merged."""
    parent = set(gmt["REACTOME_INTERFERON_SIGNALING"])
    cand = {}
    for k, g in gmt.items():
        g = set(g)
        if k == "REACTOME_INTERFERON_SIGNALING" or len(g & parent) < 0.9*len(g): continue
        g = (g & genes_present) - set(IFN_GENES) - Y_GENES
        if len(g) >= 15: cand[k] = sorted(g)
    keep = []
    for k in sorted(cand, key=lambda k: -len(cand[k])):
        if all(len(set(cand[k]) & set(cand[j]))/len(set(cand[k]) | set(cand[j])) <= 0.8 for j in keep):
            keep.append(k)
    return {k: cand[k] for k in keep}

def singscore(Xr, idx):
    """Rank-based single-sample score (singscore-type, unidirectional): mean within-sample rank
    of the set genes scaled to [-0.5, 0.5]. Xr: samples x genes ranks (1..N)."""
    N = Xr.shape[1]; n = len(idx); r = Xr[:, idx].mean(1)
    lo, hi = (n + 1)/2, (2*N - n + 1)/2
    return (r - lo)/(hi - lo) - 0.5

# ------------------------------------------------------------------ association measures
def lam_ss(X):
    """Schaefer-Strimmer analytic shrinkage intensity (target: diagonal, on correlations)."""
    n = len(X); Z = (X - X.mean(0))/X.std(0, ddof=1)
    W = np.einsum('ni,nj->nij', Z, Z); S = W.mean(0)*n/(n - 1)
    v = n/(n - 1)**3*((W - W.mean(0))**2).sum(0)
    off = ~np.eye(X.shape[1], dtype=bool)
    return float(np.clip(v[off].sum()/(S[off]**2).sum(), 0, 1))

def pcor_mat(X, cond=None, lam=0.2):
    Z = X if cond is None else np.c_[X, cond]
    Zc = Z - Z.mean(0); S = Zc.T @ Zc/len(Z); S = (1 - lam)*S + lam*np.diag(np.diag(S))
    O = np.linalg.inv(S); d = np.sqrt(np.diag(O)); P = -O/np.outer(d, d)
    P = P[:X.shape[1], :X.shape[1]].copy(); np.fill_diagonal(P, 0); return P

def pear_mat(X, cond=None, lam=None):
    Xc = X - X.mean(0); S = Xc.T @ Xc/len(X); d = np.sqrt(np.diag(S))
    R = S/np.outer(d, d); np.fill_diagonal(R, 0); return R

def lioness(Xtr, ytr, Xte, f, ctr, cte, lam, rng):
    """Class-balanced bagged LIONESS (equations 13-14)."""
    G = Xtr.shape[1]; iu = np.triu_indices(G, 1)
    Etr = np.zeros((len(Xtr), len(iu[0]))); Ete = np.zeros((len(Xte), len(iu[0])))
    i0, i1 = np.where(ytr == 0)[0], np.where(ytr == 1)[0]; mm = min(len(i0), len(i1))
    for _ in range(B_REF):
        ref = np.r_[rng.choice(i0, mm, False), rng.choice(i1, mm, False)]
        R = Xtr[ref]; CR = None if ctr is None else ctr[ref]; N = len(R); P = f(R, CR, lam)
        inref = np.zeros(len(Xtr), bool); inref[ref] = True
        for k, idx in enumerate(ref):
            Etr[idx] += (N*P - (N - 1)*f(np.delete(R, k, 0), None if CR is None else np.delete(CR, k, 0), lam))[iu]
        for idx in np.where(~inref)[0]:
            Etr[idx] += ((N + 1)*f(np.vstack([R, Xtr[idx]]), None if CR is None else np.vstack([CR, ctr[idx]]), lam) - N*P)[iu]
        for t in range(len(Xte)):
            Ete[t] += ((N + 1)*f(np.vstack([R, Xte[t]]), None if CR is None else np.vstack([CR, cte[t]]), lam) - N*P)[iu]
    return Etr/B_REF, Ete/B_REF

def net_features(E, P, kappa, dP, G):
    """Primary (key4: DN, mean |w|, eta1, D; equations 16-19) and secondary (strengths, eq 20) features."""
    iu = np.triu_indices(G, 1); n = len(E)
    W = np.zeros((n, G, G)); W[:, iu[0], iu[1]] = E/kappa; W = W + W.transpose(0, 2, 1)
    e = W[:, iu[0], iu[1]]; pe = (P/kappa)[iu]
    key4 = np.c_[E @ dP, np.abs(e).mean(1), np.linalg.eigvalsh(W)[:, -1], np.sqrt(2*((e - pe)**2).sum(1))]
    strg = np.c_[np.clip(W, 0, None).sum(2), np.clip(-W, 0, None).sum(2)]
    return {"key4": key4, "sec": np.c_[strg, key4]}

# ------------------------------------------------------------------ group lasso (equation 22)
def _sig(z): return 1/(1 + np.exp(-np.clip(z, -30, 30)))
def gl_fit(X, y, groups, gam, n_iter=400):
    """Group-lasso logistic regression by FISTA; features standardized by caller."""
    n, p = X.shape; w = np.zeros(p); b = np.log((y.mean() + 1e-6)/(1 - y.mean() + 1e-6))
    v, vb, t = w.copy(), b, 1.0; L = 0.25*np.linalg.norm(X, 2)**2/n + 1e-8
    ug = np.unique(groups); gidx = [np.where(groups == g)[0] for g in ug]; sq = [np.sqrt(len(i)) for i in gidx]
    for _ in range(n_iter):
        r = _sig(X @ v + vb) - y; gw = X.T @ r/n; gb = r.mean()
        wn = v - gw/L; bn = vb - gb/L
        for i, s in zip(gidx, sq):
            nr = np.linalg.norm(wn[i]); wn[i] = 0 if nr <= gam*s/L else wn[i]*(1 - gam*s/L/nr)
        tn = (1 + np.sqrt(1 + 4*t*t))/2
        v = wn + (t - 1)/tn*(wn - w); vb = bn + (t - 1)/tn*(bn - b); w, b, t = wn, bn, tn
    return w, b

def gl_predict(A, y, B, groups, rng, n_gam=8):
    """Group lasso with gamma chosen by inner 5-fold CV (AUC); returns test probabilities and selected groups."""
    sc = StandardScaler().fit(A); A, B = sc.transform(A), sc.transform(B)
    r0 = (y - y.mean())/len(y)
    gmax = max(np.linalg.norm(A[:, groups == g].T @ r0)/np.sqrt((groups == g).sum()) for g in np.unique(groups))
    grid = gmax*np.logspace(0, -2, n_gam)[1:]
    skf = StratifiedKFold(5, shuffle=True, random_state=int(rng.integers(1e9)))
    sc_g = np.zeros(len(grid))
    for tr, te in skf.split(A, y):
        for k, g in enumerate(grid):
            w, b = gl_fit(A[tr], y[tr], groups, g, 200)
            p = A[te] @ w + b
            sc_g[k] += roc_auc_score(y[te], p) if len(np.unique(y[te])) > 1 else 0.5
    g = grid[int(np.argmax(sc_g))]; w, b = gl_fit(A, y, groups, g)
    sel = [gg for gg in np.unique(groups) if np.any(w[groups == gg] != 0)]
    return _sig(B @ w + b), sel

def lr_cv(A, y, B, rng, penalty="l2", Cs=(0.01, 0.1, 1.0)):
    best, bs = None, -1
    skf = StratifiedKFold(5, shuffle=True, random_state=int(rng.integers(1e9)))
    for C in Cs:
        s = 0
        for tr, te in skf.split(A, y):
            m = mk_lr(C, penalty).fit(A[tr], y[tr]); s += roc_auc_score(y[te], m.predict_proba(A[te])[:, 1])
        if s > bs: bs, best = s, C
    return mk_lr(best, penalty).fit(A, y).predict_proba(B)[:, 1]

def mk_lr(C, penalty="l2"):
    if penalty == "en":
        return make_pipeline(StandardScaler(), LogisticRegression(penalty="elasticnet", solver="saga", l1_ratio=0.5, C=C, max_iter=3000, tol=1e-3))
    return make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=5000))

def rqda_score(Xtr, ytr, Xte, reg=0.3):
    """Regularized QDA log-odds (Friedman); class covariances shrunk to the identity when needed."""
    ll = []
    for k in (0, 1):
        Z = Xtr[ytr == k]; mu = Z.mean(0); Sk = (1 - reg)*np.cov(Z.T) + reg*np.eye(Z.shape[1])
        _, logdet = np.linalg.slogdet(Sk); D = Xte - mu
        ll.append(-0.5*(logdet + np.einsum('ij,jk,ik->i', D, np.linalg.inv(Sk), D)) + np.log((ytr == k).mean()))
    return ll[1] - ll[0]

def wgcna_modules(Xtr, Xte, power=6):
    G = Xtr.shape[1]; A = np.abs(np.corrcoef(Xtr.T))**power
    Z = linkage((1 - A)[np.triu_indices(G, 1)], "average"); lab = fcluster(Z, max(2, G//10), "maxclust")
    ftr, fte, hubs = [], [], []
    for c in np.unique(lab):
        idx = np.where(lab == c)[0]
        k = A[np.ix_(idx, idx)].sum(1); hubs.append(idx[np.argmax(k)])
        if len(idx) == 1: ftr.append(Xtr[:, idx[0]]); fte.append(Xte[:, idx[0]]); continue
        p = PCA(1).fit(Xtr[:, idx]); ftr.append(p.transform(Xtr[:, idx])[:, 0]); fte.append(p.transform(Xte[:, idx])[:, 0])
    kall = A.sum(1); top = np.argsort(-kall)[:10]
    return np.array(ftr).T, np.array(fte).T, top
