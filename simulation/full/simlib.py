"""Full simulation for the IFN-low LIONESS study (Section 2.13, Supplementary Section S1).

Synthetic stand-in: the real GSE319130 controls could not be downloaded in the environment
where this code was run, so all data are generated from a synthetic Gaussian model with the
structure described in Section 2.13 (interferon activity factor, equation 32; correlated
gene-specific variation, equation 31 with normal margins).
"""
import numpy as np, warnings
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, fcluster
import networkx as nx
warnings.filterwarnings("ignore")
LAM = 0.2          # fixed shrinkage intensity (equation 4)
B_REF = 5          # balanced reference subsets (Section 2.7 specifies 20; 5 used for computation)
N_PERM = 199       # permutations for population-level tests (Section 2.12 specifies 10,000)

# ---------------------------------------------------------------- structure
class Structure:
    """Synthetic interferon sub-pathway with G genes plus four IFN-score genes."""
    def __init__(self, G, seed=1):
        r = np.random.default_rng(seed)
        O = np.eye(G)
        for i in range(G - 1): O[i, i+1] = O[i+1, i] = 0.3
        extra = r.choice(len(np.triu_indices(G, 2)[0]), size=max(1, G // 2), replace=False)
        iu2 = np.triu_indices(G, 2)
        for k in extra:
            i, j = iu2[0][k], iu2[1][k]; O[i, j] = O[j, i] = r.choice([-0.25, 0.25])
        while np.linalg.eigvalsh(O).min() < 0.1: O += 0.05*np.eye(G)
        self.G, self.O0 = G, O
        self.R0 = corr(np.linalg.inv(O))                 # gene-specific correlation
        self.l = r.uniform(0.2, 0.5, G)                  # loadings on IFN activity (eq 32)
        self.Sig = self.R0 + np.outer(self.l, self.l)    # total covariance, var(f)=1
        self.lev = np.arange(int(np.ceil(0.2*G)))        # genes shifted in S1 and S3
        # rewiring target for S4: 10% of gene pairs
        iu = np.triu_indices(G, 1); m = int(np.ceil(0.1*len(iu[0])))
        sel = r.choice(len(iu[0]), m, replace=False); T = O.copy()
        for k in sel:
            i, j = iu[0][k], iu[1][k]
            if O[i, j] != 0: T[i, j] = T[j, i] = -O[i, j] if r.random() < 0.5 else 0.0
            else: T[i, j] = T[j, i] = r.choice([-0.3, 0.3])
        self.Tdir = T - O
        self.rewired = sel

def corr(S): d = np.sqrt(np.diag(S)); return S/np.outer(d, d)

def rewired_R(st, t):
    O = st.O0 + t*st.Tdir
    if np.linalg.eigvalsh(O).min() <= 0.05: return None
    return corr(np.linalg.inv(O))

# ---------------------------------------------------------------- oracle calibration (S1-S4)
def oracle_auc(st, scen, eff, rng, n=200000):
    G, Sig = st.G, st.Sig
    if scen == "S1":
        d = np.zeros(G); d[st.lev] = eff; D2 = d @ np.linalg.solve(Sig, d)
        return stats.norm.cdf(np.sqrt(D2)/np.sqrt(2))
    if scen == "S2":
        return stats.f.cdf(eff**2, G, G)
    if scen == "S3":
        d = np.zeros(G); d[st.lev] = eff; D2 = d @ np.linalg.solve(Sig, d)
        a0 = rng.normal(0, np.sqrt(D2), n); s = rng.choice([-1, 1], n); a1 = s*D2 + rng.normal(0, np.sqrt(D2), n)
        return auc_fast(np.abs(a1), np.abs(a0))
    if scen == "S4":
        RR = rewired_R(st, eff)
        if RR is None: return np.nan
        S0, S1 = Sig, RR + np.outer(st.l, st.l)
        L = np.linalg.cholesky
        x0 = rng.standard_normal((n, G)) @ L(S0).T; x1 = rng.standard_normal((n, G)) @ L(S1).T
        A = np.linalg.inv(S0) - np.linalg.inv(S1)
        q = lambda x: np.einsum('ij,jk,ik->i', x, A, x)
        return auc_fast(q(x1), q(x0))

def auc_fast(p, c):
    s = np.r_[p, c]; rk = stats.rankdata(s)
    return (rk[:len(p)].sum() - len(p)*(len(p)+1)/2)/(len(p)*len(c))

def calibrate(st, scen, target, seed=0):
    rng = np.random.default_rng(seed)
    lo, hi = {"S1": (0, 3), "S2": (1, 3), "S3": (0, 3), "S4": (0, 1)}[scen]
    if scen == "S4":                          # largest valid rewiring strength
        while rewired_R(st, hi*1.5) is not None and hi < 6: hi *= 1.5
        while rewired_R(st, hi) is None: hi *= 0.95
    if oracle_auc(st, scen, hi, rng) < target: return hi, oracle_auc(st, scen, hi, rng)
    for _ in range(30):
        mid = (lo+hi)/2
        if oracle_auc(st, scen, mid, rng) < target: lo = mid
        else: hi = mid
    return hi, oracle_auc(st, scen, hi, rng)

# ---------------------------------------------------------------- data generation
def draw(st, n, rng, f_mean=0.0, f_sd=1.0, R=None):
    """Equation 32: pathway genes x = l f + eps; score genes s = 0.9 f + 0.3 e."""
    R = st.R0 if R is None else R
    f = rng.normal(f_mean, f_sd, n)
    eps = rng.standard_normal((n, st.G)) @ np.linalg.cholesky(R).T
    X = np.outer(f, st.l) + eps
    Sg = 0.9*f[:, None] + 0.3*rng.standard_normal((n, 4))
    return X, Sg, f

def ifn_score(Sg, ctrl):
    mu, sd = Sg[ctrl].mean(0), Sg[ctrl].std(0); return ((Sg - mu)/sd).mean(1)

def generate(st, scen, eff, n_pat, n_con, rng):
    """Returns pathway expression X, IFN score I, labels y (1 = patient), treated flag."""
    G = st.G; m = 2*max(n_pat, n_con)
    Xc, Sc, _ = draw(st, m, rng)
    treated = np.zeros(m, bool)
    if scen in ("S0", "S1", "S2", "S3"):
        Xp, Sp, _ = draw(st, m, rng)
        if scen == "S1": Xp[:, st.lev] += eff
        if scen == "S2": Xp = Xp*eff; Sp = Sp
        if scen == "S3":
            s = np.where(rng.random(m) < .5, 1, -1); sh = np.zeros(G); sh[st.lev] = eff; Xp = Xp + np.outer(s, sh)
    elif scen == "S4":
        Xp, Sp, _ = draw(st, m, rng, R=rewired_R(st, eff))
    elif scen == "S5":       # half treated IFN-high (deviations x 0.3), half untreated control-like
        Xa, Sa, _ = draw(st, m, rng, f_mean=3.0); Xa, Sa = 0.3*Xa, 0.3*Sa
        Xb, Sb, _ = draw(st, m, rng)
        Xp, Sp = np.vstack([Xa, Xb]), np.vstack([Sa, Sb]); treated = np.r_[np.ones(m, bool), np.zeros(m, bool)]
    elif scen == "S6":       # SLE population: 75% IFN-high, 25% IFN-low; no other disease effect
        hi = rng.random(4*m) < 0.75
        Xp, Sp, _ = draw(st, 4*m, rng); Xh, Shh, _ = draw(st, 4*m, rng, f_mean=3.0)
        Xp[hi], Sp[hi] = Xh[hi], Shh[hi]
    elif scen == "S7":       # IFN-high patients vs all controls (no cutoff for controls)
        Xp, Sp, _ = draw(st, m, rng, f_mean=3.0)
    ctrl_ref = np.r_[np.zeros(len(Sp), bool), np.ones(len(Sc), bool)]
    Iall = ifn_score(np.vstack([Sp, Sc]), ctrl_ref); Ip, Ic = Iall[:len(Sp)], Iall[len(Sp):]
    theta = Ic.mean() + 2*Ic.std()
    if scen == "S7":
        kp = np.where(Ip > theta)[0]; kc = np.arange(len(Ic))
    else:
        kp = np.where(Ip <= theta)[0]; kc = np.where(Ic <= theta)[0]
    if scen == "S5":   # equal numbers of treated and untreated among selected patients
        kt, ku = kp[treated[kp]], kp[~treated[kp]]
        h = n_pat//2; kp = np.r_[rng.choice(kt, h, False), rng.choice(ku, n_pat-h, False)]
    else:
        kp = rng.choice(kp, n_pat, replace=False)
    kc = rng.choice(kc, n_con, replace=False)
    X = np.vstack([Xp[kp], Xc[kc]]); I = np.r_[Ip[kp], Ic[kc]]
    y = np.r_[np.ones(n_pat), np.zeros(n_con)]
    tr = np.r_[treated[kp] if scen == "S5" else np.zeros(n_pat, bool), np.zeros(n_con, bool)]
    return X, I, y, tr

# ---------------------------------------------------------------- association measures
def shrink(S): return (1-LAM)*S + LAM*np.diag(np.diag(S))
def pcor_mat(X, cond=None):
    """Partial correlation among the columns of X, optionally also conditioning on cond (eq 4-5)."""
    Z = X if cond is None else np.c_[X, cond]
    Zc = Z - Z.mean(0); S = shrink(Zc.T @ Zc/len(Z)); O = np.linalg.inv(S)
    d = np.sqrt(np.diag(O)); P = -O/np.outer(d, d); P = P[:X.shape[1], :X.shape[1]]
    np.fill_diagonal(P, 0); return P
def pear_mat(X, cond=None):
    Xc = X - X.mean(0); S = Xc.T @ Xc/len(X); R = corr(S); np.fill_diagonal(R, 0); return R

def lioness(Xtr, ytr, Xte, f, ctr, cte, rng):
    """Class-balanced, bagged LIONESS (equations 13-14); every sample treated by the same rule."""
    G = Xtr.shape[1]; iu = np.triu_indices(G, 1)
    Etr = np.zeros((len(Xtr), len(iu[0]))); Ete = np.zeros((len(Xte), len(iu[0])))
    i0, i1 = np.where(ytr == 0)[0], np.where(ytr == 1)[0]; mm = min(len(i0), len(i1))
    cc = (lambda idx: None) if ctr is None else (lambda idx: ctr[idx])
    for _ in range(B_REF):
        ref = np.r_[rng.choice(i0, mm, False), rng.choice(i1, mm, False)]
        R = Xtr[ref]; CR = None if ctr is None else ctr[ref]; N = len(R); P = f(R, CR)
        inref = np.zeros(len(Xtr), bool); inref[ref] = True
        for k, idx in enumerate(ref):
            Rm = np.delete(R, k, 0); Cm = None if CR is None else np.delete(CR, k, 0)
            Etr[idx] += (N*P - (N-1)*f(Rm, Cm))[iu]
        for idx in np.where(~inref)[0]:
            Ra = np.vstack([R, Xtr[idx]]); Ca = None if CR is None else np.r_[CR, ctr[idx]]
            Etr[idx] += ((N+1)*f(Ra, Ca) - N*P)[iu]
        for t in range(len(Xte)):
            Ra = np.vstack([R, Xte[t]]); Ca = None if CR is None else np.r_[CR, cte[t]]
            Ete[t] += ((N+1)*f(Ra, Ca) - N*P)[iu]
    return Etr/B_REF, Ete/B_REF

# ---------------------------------------------------------------- network features (Section 2.8)
def net_features(E, P, kappa, dP, G, explo=False, tau=None):
    iu = np.triu_indices(G, 1); n = len(E)
    W = np.zeros((n, G, G)); W[:, iu[0], iu[1]] = E/kappa; W = W + W.transpose(0, 2, 1)
    e = W[:, iu[0], iu[1]]; pe = (P/kappa)[iu]
    key4 = np.c_[E @ dP, np.abs(e).mean(1), np.linalg.eigvalsh(W)[:, -1], np.sqrt(2*((e - pe)**2).sum(1))]
    strg = np.c_[np.clip(W, 0, None).sum(2), np.clip(-W, 0, None).sum(2)]
    out = {"key4": key4, "sec": np.c_[strg, key4]}
    if explo:
        A = np.abs(W); m = len(iu[0])
        num = np.einsum('nij,njk,nki->ni', W, W, W); den = A.sum(2)**2 - (A**2).sum(2)
        clus = num/np.where(den == 0, 1, den)
        ae = np.abs(e); pp = ae/ae.sum(1, keepdims=True)
        H = -(pp*np.log(pp + 1e-300)).sum(1)/np.log(m); pipos = (e > 0).mean(1)
        Rr = np.array([np.corrcoef(x, pe)[0, 1] for x in e])
        g_feats = []
        for s in range(n):
            a = ae[s]; keep = a > tau
            g = nx.Graph(); g.add_nodes_from(range(G))
            g.add_weighted_edges_from([(iu[0][k], iu[1][k], 1/a[k]) for k in np.where(keep)[0]])
            lcc = g.subgraph(max(nx.connected_components(g), key=len))
            diam = nx.diameter(lcc) if lcc.number_of_nodes() > 1 else 0
            bt = nx.betweenness_centrality(g, weight='weight')
            g_feats.append(np.r_[keep.sum(), diam, nx.transitivity(g), [g.degree(i) for i in range(G)], [bt[i] for i in range(G)]])
        out["explo"] = np.c_[np.array(g_feats), clus, pipos, H, Rr]
    return out

# ---------------------------------------------------------------- models and evaluation
def lr(C=0.5): return make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=3000))
def fitpred(m, A, y, B):
    m.fit(A, y)
    return m.predict_proba(B)[:, 1] if hasattr(m, "predict_proba") else m.decision_function(B)

MAIN_MODELS = ["M0a", "M1", "M2", "M3-score", "M3-boost", "M3-SVM", "M4", "M5", "M6", "W2",
               "L1", "L2", "L2-P", "L2-S", "L2-S-P", "L3", "L3-P", "L-explo", "L-sec+explo"]
CORE_MODELS = ["M0a", "M2", "M4", "M5", "M6", "L2", "L2-P", "L3", "L3-P"]
PAIRS = [("L3", "M5"), ("L3-P", "M5"), ("L2", "M6"), ("L2-P", "M6"), ("L2", "M4"), ("L2-P", "M4")]

def wgcna_like(Xtr, Xte, G):
    A = np.abs(np.corrcoef(Xtr.T))**6; D = 1 - A
    k = max(2, G//10); Z = linkage(D[np.triu_indices(G, 1)], 'average'); lab = fcluster(Z, k, 'maxclust')
    ftr, fte = [], []
    for c in np.unique(lab):
        idx = lab == c
        if idx.sum() == 1: ftr.append(Xtr[:, idx][:, 0]); fte.append(Xte[:, idx][:, 0]); continue
        p = PCA(1).fit(Xtr[:, idx]); ftr.append(p.transform(Xtr[:, idx])[:, 0]); fte.append(p.transform(Xte[:, idx])[:, 0])
    return np.c_[ftr].T if len(ftr) > 1 else np.array(ftr).T, np.c_[fte].T if len(fte) > 1 else np.array(fte).T

def analyse(X, I, y, rng, models="main", cond=True, tests=True):
    """One simulated dataset: out-of-fold predictions (one repeat of 5-fold CV), paired AUC
    differences with the Nadeau-Bengio corrected variance, population-level tests, subgroup check."""
    G = X.shape[1]; names = MAIN_MODELS if models == "main" else CORE_MODELS
    explo = models == "main"
    oof = {k: np.zeros(len(y)) for k in names}; fold_auc = {k: [] for k in names}; folds = []
    skf = StratifiedKFold(5, shuffle=True, random_state=int(rng.integers(1e9)))
    for tr, te in skf.split(X, y):
        mu, sd = X[tr].mean(0), X[tr].std(0); Xs = np.clip((X - mu)/sd, -4, 4)
        Xtr, Xte, ytr = Xs[tr], Xs[te], y[tr]; Itr, Ite = I[tr], I[te]
        pr = {}
        pr["M0a"] = fitpred(lr(), Itr[:, None], ytr, Ite[:, None])
        pr["M2"] = fitpred(lr(), Xtr, ytr, Xte)
        pr["M5"] = fitpred(lr(), np.c_[Xtr, Itr], ytr, np.c_[Xte, Ite])
        hc = Xtr[ytr == 0]; Ci = np.linalg.inv(shrink(np.cov(hc.T))); mh = hc.mean(0)
        dist = lambda Z: np.einsum('ij,jk,ik->i', Z - mh, Ci, Z - mh)[:, None]
        pr["M4"] = fitpred(lr(), dist(Xtr), ytr, dist(Xte))
        pr["M6"] = fitpred(QDA(reg_param=0.3), Xtr, ytr, Xte)
        if models == "main":
            pr["M1"] = fitpred(make_pipeline(StandardScaler(), LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5, C=0.5, max_iter=2000, tol=1e-3)), np.c_[Xtr, Itr], ytr, np.c_[Xte, Ite])
            pc = PCA(1).fit(Xtr); sc = lambda Z: np.c_[Z.mean(1), pc.transform(Z)[:, 0]]
            pr["M3-score"] = fitpred(lr(), sc(Xtr), ytr, sc(Xte))
            pr["M3-boost"] = fitpred(GradientBoostingClassifier(n_estimators=100, max_depth=2, random_state=0), Xtr, ytr, Xte)
            pr["M3-SVM"] = fitpred(make_pipeline(StandardScaler(), SVC(kernel='rbf', C=1.0)), Xtr, ytr, Xte)
            a, b = wgcna_like(Xtr, Xte, G); pr["W2"] = fitpred(lr(), a, ytr, b)
        feats = {}
        for tag, f, ctr, cte in [("", pcor_mat, Itr if cond else None, Ite if cond else None), ("-P", pear_mat, None, None)]:
            Etr, Ete = lioness(Xtr, ytr, Xte, f, ctr, cte, rng)
            P = f(Xtr, Itr if (cond and tag == "") else None)
            kappa = np.quantile(np.abs(Etr), 0.99)
            iu = np.triu_indices(G, 1)
            c1 = f(Xtr[ytr == 1], Itr[ytr == 1] if (cond and tag == "") else None)
            c0 = f(Xtr[ytr == 0], Itr[ytr == 0] if (cond and tag == "") else None)
            dP = (c1 - c0)[iu]
            tau = np.quantile(np.abs(Etr/kappa), 0.90)
            do_ex = explo and tag == ""
            Ftr = net_features(Etr, P, kappa, dP, G, do_ex, tau); Fte = net_features(Ete, P, kappa, dP, G, do_ex, tau)
            feats[tag] = (Ftr, Fte)
            if models == "main" and tag == "":
                pr["L1"] = fitpred(lr(), Etr, ytr, Ete)
        for tag in ["", "-P"]:
            Ftr, Fte = feats[tag]
            pr["L2" + tag] = fitpred(lr(), Ftr["key4"], ytr, Fte["key4"])
            pr["L3" + tag] = fitpred(lr(), np.c_[Ftr["key4"], Xtr, Itr], ytr, np.c_[Fte["key4"], Xte, Ite])
            if models == "main":
                pr["L2-S" + tag] = fitpred(lr(), Ftr["sec"], ytr, Fte["sec"])
        if models == "main":
            Ftr, Fte = feats[""]
            pr["L-explo"] = fitpred(lr(), Ftr["explo"], ytr, Fte["explo"])
            pr["L-sec+explo"] = fitpred(lr(), np.c_[Ftr["sec"], Ftr["explo"]], ytr, np.c_[Fte["sec"], Fte["explo"]])
        for k in names:
            oof[k][te] = pr[k]; fold_auc[k].append(roc_auc_score(y[te], pr[k]))
        folds.append((len(tr), len(te)))
    res = {"auc": {k: float(roc_auc_score(y, oof[k])) for k in names}, "pairs": {}}
    ntr, nte = folds[0]
    for a, b in PAIRS:
        d = np.array(fold_auc[a]) - np.array(fold_auc[b]); K = len(d)
        se = np.sqrt((1/K + nte/ntr)*d.var(ddof=1))      # Nadeau-Bengio corrected variance
        res["pairs"][f"{a} vs {b}"] = [float(d.mean()), float(se)]
    if tests: res.update(pop_tests(X, I, y, rng, cond))
    return res

def pop_tests(X, I, y, rng, cond=True):
    """Layered tests (equations 27-29) on expression adjusted for the IFN score, label permutation
    of the adjusted data (Freedman-Lane-type), and the subgroup check (equation 30)."""
    Z = (X - X.mean(0))/X.std(0)
    if cond:
        Zd = np.c_[np.ones(len(I)), I]; Z = Z - Zd @ np.linalg.lstsq(Zd, Z, rcond=None)[0]
    def st(lab):
        a, b = Z[lab == 1], Z[lab == 0]
        V = shrink(np.cov(np.vstack([a - a.mean(0), b - b.mean(0)]).T)); Vi = np.linalg.inv(V)
        dm = a.mean(0) - b.mean(0)
        da = np.einsum('ij,jk,ik->i', a - a.mean(0), Vi, a - a.mean(0)).mean()
        db = np.einsum('ij,jk,ik->i', b - b.mean(0), Vi, b - b.mean(0)).mean()
        return np.array([dm @ Vi @ dm, abs(da - db), np.linalg.norm(pcor_mat(a) - pcor_mat(b)), np.linalg.norm(pear_mat(a) - pear_mat(b))])
    obs = st(y); c = np.zeros(4)
    for _ in range(N_PERM): c += st(rng.permutation(y)) >= obs
    p = (c + 1)/(N_PERM + 1)
    def dbic(M):
        P3 = PCA(3).fit_transform(M - M.mean(0))
        b = [GaussianMixture(k, n_init=3, random_state=0).fit(P3).bic(P3) for k in (1, 2)]
        return b[0] - b[1]
    flag = bool(dbic(Z[y == 1]) > 2 and dbic(Z[y == 0]) <= 2)
    return {"p": {"level": float(p[0]), "spread": float(p[1]), "structure": float(p[2]), "structure-P": float(p[3])}, "subgroup_flag": flag}

def match_on_ifn(I, y, rng):
    """1:1 nearest-neighbour matching of patients to controls on the IFN score, without replacement."""
    pts = np.where(y == 1)[0]; cons = list(np.where(y == 0)[0]); keep = []
    for i in rng.permutation(pts):
        if not cons: break
        j = min(cons, key=lambda c: abs(I[c] - I[i])); cons.remove(j); keep += [i, j]
    return np.array(sorted(keep))
