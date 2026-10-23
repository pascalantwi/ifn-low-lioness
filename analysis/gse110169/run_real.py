"""Run the three contrasts on GSE110169 with repeated nested cross-validation (Section 2.11).

python3 run_real.py [n_repeats]     (default 10 repeats x 5 outer folds)
Outputs: results/oof_<contrast>.pkl (out-of-fold predictions per repeat) and results/folds_<contrast>.json
"""
import sys, json, pickle, time, numpy as np, pandas as pd
from multiprocessing import Pool
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.decomposition import PCA
import pipeline as P

N_REP = int(sys.argv[1]) if len(sys.argv) > 1 else 10
OUT = P.ROOT + "/analysis/gse110169/results/"
s, ann, E = P.load()
gmt = P.read_gmt(P.DATA + "c2.cp.reactome.v2024.1.Hs.symbols.gmt")
genes_present = set(ann.gene_symbol)
PW = P.subpathways(gmt, genes_present)
probe_gene = ann.gene_symbol.reindex(E.index).values
Xall = E.values.T                        # samples x probes
group = s.group.values; sex = (s.sex_inferred == "M").astype(float).values
batch = pd.get_dummies(s.batch).values[:, 1:].astype(float)
gene_of = pd.Series(probe_gene)
probes_by_gene = gene_of.groupby(gene_of).indices        # gene -> probe column indices

CONTRASTS = {   # universe of samples, positive rule, negative rule
    "C1": dict(univ=["SLE", "HC"], pos=("SLE", "high"), neg=("HC", "low")),
    "C2": dict(univ=["SLE", "HC"], pos=("SLE", "low"), neg=("HC", "low")),
    "C3": dict(univ=["SLE", "RA", "HC"], pos=("SLE", "low"), neg=("RA", "low")),
}
MODELS = ["M0a", "M0c", "M1", "M2", "M3-score", "M3-boost", "M3-SVM", "M4", "M5", "M6",
          "W1", "W2", "L1", "L2", "L2-P", "L2-S", "L3", "L3-P"]

def collapse(tr_idx, genes):
    """Per gene, the probe with the highest variance in the training samples (Section 2.2)."""
    cols = []
    for g in genes:
        pc = probes_by_gene[g]
        cols.append(pc[np.argmax(Xall[np.ix_(tr_idx, pc)].var(0))] if len(pc) > 1 else pc[0])
    return np.array(cols)

def fold(args):
    cname, rep, k, tr_u, te_u = args
    c = CONTRASTS[cname]; rng = np.random.default_rng(1000*rep + k + hash(cname) % 997)
    # ---- IFN score and cutoff from training controls (Section 2.3)
    hc_tr = tr_u[group[tr_u] == "HC"]
    ic = collapse(tr_u, P.IFN_GENES); Xi = Xall[:, ic]
    Z = (Xi - Xi[hc_tr].mean(0))/Xi[hc_tr].std(0, ddof=1); I = Z.mean(1)
    theta = I[hc_tr].mean() + 2*I[hc_tr].std(ddof=1)
    status = np.where(I > theta, "high", "low")
    def pick(idx):
        p = idx[(group[idx] == c["pos"][0]) & (status[idx] == c["pos"][1])]
        n = idx[(group[idx] == c["neg"][0]) & (status[idx] == c["neg"][1])]
        return np.r_[p, n], np.r_[np.ones(len(p)), np.zeros(len(n))]
    tr, ytr = pick(tr_u); te, yte = pick(te_u)
    if len(np.unique(yte)) < 2 or len(np.unique(ytr)) < 2: return None
    # ---- gene-level data (in-fold probe choice), cell scores (Section 2.4)
    all_genes = sorted(probes_by_gene); gcols = collapse(tr_u, all_genes)
    Xg = Xall[:, gcols]; gidx = {g: i for i, g in enumerate(all_genes)}
    ranks = Xg.argsort(1).argsort(1) + 1.0
    cells = np.c_[[P.singscore(ranks, [gidx[g] for g in m if g in gidx]) for m in P.CELL_MARKERS.values()]].T
    cov_raw = np.c_[I, cells]
    cm, cs = cov_raw[tr].mean(0), cov_raw[tr].std(0); cov = (cov_raw - cm)/cs
    # ---- pathway matrices, standardized and winsorized in-fold
    pw = {}
    for name, genes in PW.items():
        cols = np.array([gidx[g] for g in genes])
        X = Xg[:, cols]
        if len(cols) > 50: cols = cols[np.argsort(-X[tr].var(0))[:50]]; X = Xg[:, cols]
        mu, sd = X[tr].mean(0), X[tr].std(0); pw[name] = np.clip((X - mu)/sd, -4, 4)
    names = list(pw); pr, sel = {}, {}
    Ytr = ytr
    def gl(blocks, key):
        A = np.hstack([b[tr] for b in blocks]); B = np.hstack([b[te] for b in blocks])
        groups = np.concatenate([np.full(b.shape[1], i) for i, b in enumerate(blocks)])
        p, sl = P.gl_predict(A, Ytr, B, groups, rng); pr[key] = p; sel[key] = sl
    # baselines
    pr["M0a"] = P.mk_lr(1.0).fit(I[tr, None], Ytr).predict_proba(I[te, None])[:, 1]
    pr["M0c"] = P.lr_cv(cells[tr], Ytr, cells[te], rng)
    # M1: all genes (top 5000 by training variance), elastic net
    v = Xg[tr].var(0); top = np.argsort(-v)[:5000]
    pr["M1"] = P.lr_cv(Xg[tr][:, top], Ytr, Xg[te][:, top], rng, penalty="en", Cs=(0.05, 0.5))
    # expression comparators
    gl([pw[n] for n in names], "M2")
    sc = []
    for n in names:
        pca = PCA(1).fit(pw[n][tr]); sc.append(np.c_[pw[n].mean(1), pca.transform(pw[n])[:, 0]])
    gl(sc, "M3-score")
    U = np.hstack([pw[n] for n in names]); _, uu = np.unique(U[tr].round(8), axis=1, return_index=True); U = U[:, np.sort(uu)]
    pr["M3-boost"] = GradientBoostingClassifier(n_estimators=100, max_depth=2, random_state=0).fit(U[tr], Ytr).predict_proba(U[te])[:, 1]
    pr["M3-SVM"] = SVC(kernel="rbf", C=1.0).fit(U[tr], Ytr).decision_function(U[te])
    dist = []
    for n in names:
        X = pw[n]; ref = X[tr][Ytr == 0]; S = np.cov(ref.T); S = 0.8*S + 0.2*np.diag(np.diag(S))
        Ci = np.linalg.inv(S); m = ref.mean(0); dist.append(np.einsum("ij,jk,ik->i", X - m, Ci, X - m)[:, None])
    gl(dist, "M4")
    Iz = cov[:, :1]
    gl([pw[n] for n in names] + [Iz], "M5")
    q = []
    for n in names:
        X = pw[n]; col = np.zeros(len(X)); trp = np.zeros(len(tr))
        from sklearn.model_selection import StratifiedKFold as SKF
        for a, b in SKF(5, shuffle=True, random_state=0).split(X[tr], Ytr):
            trp[b] = P.rqda_score(X[tr][a], Ytr[a], X[tr][b])
        col[tr] = trp; col[te] = P.rqda_score(X[tr], Ytr, X[te]); q.append(col[:, None])
    gl(q, "M6")
    # established network methods on the union of pathway genes
    mtr, mte, hubs = P.wgcna_modules(U[tr], U[te])
    pr["W1"] = P.lr_cv(U[tr][:, hubs], Ytr, U[te][:, hubs], rng)
    pr["W2"] = P.lr_cv(mtr, Ytr, mte, rng)
    # LIONESS networks (Sections 2.7-2.8)
    F = {"": {}, "-P": {}}; edges = []
    for n in names:
        X = pw[n]; G = X.shape[1]; iu = np.triu_indices(G, 1)
        lam = P.lam_ss(np.c_[X[tr], cov[tr]])
        for tag, f, ctr, cte in [("", P.pcor_mat, cov[tr], cov[te]), ("-P", P.pear_mat, None, None)]:
            Etr, Ete = P.lioness(X[tr], Ytr, X[te], f, ctr, cte, lam, rng)
            Pm = f(X[tr], ctr, lam); kappa = np.quantile(np.abs(Etr), 0.99)
            dP = (f(X[tr][Ytr == 1], None if ctr is None else ctr[Ytr == 1], lam) - f(X[tr][Ytr == 0], None if ctr is None else ctr[Ytr == 0], lam))[iu]
            Ftr = P.net_features(Etr, Pm, kappa, dP, G); Fte = P.net_features(Ete, Pm, kappa, dP, G)
            full = {key: np.zeros((len(Xall), Ftr[key].shape[1])) for key in Ftr}
            for key in Ftr: full[key][tr] = Ftr[key]; full[key][te] = Fte[key]
            F[tag][n] = full
            if tag == "":
                Ef = np.zeros((len(Xall), Etr.shape[1])); Ef[tr] = Etr; Ef[te] = Ete; edges.append(Ef)
    El = np.hstack(edges)
    pr["L1"] = P.lr_cv(El[tr], Ytr, El[te], rng)
    gl([F[""][n]["key4"] for n in names], "L2")
    gl([F["-P"][n]["key4"] for n in names], "L2-P")
    gl([F[""][n]["sec"] for n in names], "L2-S")
    gl([F[""][n]["key4"] for n in names] + [pw[n] for n in names] + [Iz], "L3")
    gl([F["-P"][n]["key4"] for n in names] + [pw[n] for n in names] + [Iz], "L3-P")
    return dict(contrast=cname, rep=rep, fold=k, te=te.tolist(), y=yte.tolist(), n_tr=len(tr),
                theta=float(theta), pred={m: np.asarray(pr[m]).tolist() for m in MODELS},
                sel={m: [names[i] if i < len(names) else ("IFN" if i == 2*len(names) else "expr:" + names[i - len(names)]) for i in v] for m, v in sel.items()})

def jobs(cname):
    c = CONTRASTS[cname]; univ = np.where(np.isin(group, c["univ"]))[0]
    strat = np.array([g + b for g, b in zip(group[univ], s.batch.values[univ])])
    out = []
    for rep in range(N_REP):
        skf = StratifiedKFold(5, shuffle=True, random_state=rep)
        for k, (a, b) in enumerate(skf.split(univ, strat)):
            out.append((cname, rep, k, univ[a], univ[b]))
    return out

if __name__ == "__main__":
    print("sub-pathways:", {k: len(v) for k, v in PW.items()}, flush=True)
    json.dump(PW, open(OUT + "subpathways.json", "w"), indent=1)
    for cname in (sys.argv[2].split(",") if len(sys.argv) > 2 else ["C1", "C2", "C3"]):
        t0 = time.time()
        with Pool(4) as pool: res = [r for r in pool.map(fold, jobs(cname)) if r is not None]
        pickle.dump(res, open(OUT + f"oof_{cname}.pkl", "wb"))
        print(cname, "folds:", len(res), "time: %.0f s" % (time.time() - t0), flush=True)
