"""Simulation of the full IFN-low pipeline: IFN cutoff inside folds, IFN genes excluded, LIONESS vs leftover IFN."""
import numpy as np, json, warnings, sys
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import study
warnings.filterwarnings("ignore")
rng = np.random.default_rng(42); study.rng = rng
G = study.G; K = 4                                   # 4 IFN panel genes + 10 pathway genes
N_SLE, N_HC = 360, 77                                # ~25% IFN-low -> ~90 IFN-low women vs 77 women controls
RIFN = 0.6*np.ones((K, K)) + 0.4*np.eye(K)

def make(truth):
    # latent IFN activity: controls 0; patients 75% high (mean 3), 25% low (mean 0.5 = mildly raised)
    hi = rng.random(N_SLE) < 0.75
    lat = np.r_[np.zeros(N_HC), np.where(hi, rng.normal(3, 1, N_SLE), rng.normal(0.5, 0.5, N_SLE))]
    ifn = rng.multivariate_normal(np.zeros(K), RIFN, N_HC + N_SLE) + lat[:, None]
    path = rng.multivariate_normal(np.zeros(G), study.SIG, N_HC + N_SLE)
    low = np.r_[np.zeros(N_HC, bool), ~hi]
    if truth == "Genes rewired":
        path[low] = rng.multivariate_normal(np.zeros(G), study.SIGR, low.sum())
    if truth == "Gene levels differ":
        path[np.ix_(low, [0, 1, 2])] += 0.45
    path[:, 9] += 0.35*lat                           # one pathway gene partly driven by IFN (outside the panel)
    X = np.c_[ifn, path]; y = np.r_[np.zeros(N_HC), np.ones(N_SLE)]
    return X, y, np.r_[np.zeros(N_HC, bool), hi]

def ifn_score(X, hc):
    m, s = hc[:, :K].mean(0), hc[:, :K].std(0); return ((X[:, :K] - m)/s).mean(1)

METHODS = ["Leftover IFN score", "Gene levels", "Gene levels + IFN score", "Quadratic classifier",
           "LIONESS links", "Gene levels + LIONESS + IFN score"]
def lr(): return study.lr()

def one_rep(truth, contrast="IFN-low vs healthy"):
    X, y, hi = make(truth); preds = {m: [] for m in METHODS}; ys = []; nlow = []
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=int(rng.integers(1e9))).split(X, y):
        Xtr, Xte, ytr, yte = X[tr], X[te], y[tr], y[te]
        hc = Xtr[ytr == 0]; s_tr, s_te = ifn_score(Xtr, hc), ifn_score(Xte, hc)
        sc = ifn_score(hc, hc); cut = sc.mean() + 2*sc.std()          # cutoff fitted on training controls only
        if contrast == "IFN-low vs healthy":
            ktr, kte = s_tr <= cut, s_te <= cut                        # same filter for patients and controls
        else:                                                          # positive control: IFN-high vs healthy
            ktr = (ytr == 0) & (s_tr <= cut) | (ytr == 1) & (s_tr > cut)
            kte = (yte == 0) & (s_te <= cut) | (yte == 1) & (s_te > cut)
        Atr, Ate, atr = Xtr[ktr][:, K:], Xte[kte][:, K:], ytr[ktr]     # features exclude IFN panel genes
        str_, ste = s_tr[ktr][:, None], s_te[kte][:, None]
        nlow.append((atr == 1).sum())
        Etr, Ete = study.lioness_features(Atr, atr, Ate)
        f = {"Leftover IFN score": (str_, ste), "Gene levels": (Atr, Ate),
             "Gene levels + IFN score": (np.c_[Atr, str_], np.c_[Ate, ste]),
             "LIONESS links": (Etr, Ete), "Gene levels + LIONESS + IFN score": (np.c_[Atr, Etr, str_], np.c_[Ate, Ete, ste])}
        for m, (a, b) in f.items(): preds[m] += list(lr().fit(a, atr).predict_proba(b)[:, 1])
        preds["Quadratic classifier"] += list(QDA(reg_param=0.3).fit(Atr, atr).predict_proba(Ate)[:, 1])
        ys += list(yte[kte])
    return {m: roc_auc_score(ys, preds[m]) for m in METHODS}, float(np.mean(nlow))*5/4, int(sum(ys))

if __name__ == "__main__":
    REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    runs = [("No real difference", "IFN-low vs healthy"), ("Gene levels differ", "IFN-low vs healthy"),
            ("Genes rewired", "IFN-low vs healthy"), ("No real difference", "IFN-high vs healthy")]
    out = {}
    for truth, con in runs:
        r = [one_rep(truth, con) for _ in range(REPS)]
        a = np.array([[x[0][m] for m in METHODS] for x in r])
        key = f"{con} | {truth}"
        out[key] = {"auc": {m: [float(a[:, j].mean()), float(1.96*a[:, j].std()/np.sqrt(REPS))] for j, m in enumerate(METHODS)},
                    "patients_in_analysis": float(np.mean([x[2] for x in r]))}
        print(key, {m: round(out[key]['auc'][m][0], 2) for m in METHODS}, "patients:", round(out[key]["patients_in_analysis"]), flush=True)
    json.dump(out, open("ifn_results.json", "w"), indent=1)
