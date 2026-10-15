"""Simulation study mirroring the planned IFN-low LIONESS study (toy scale: one 10-gene pathway)."""
import numpy as np, json, warnings, sys
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
warnings.filterwarnings("ignore")
rng = np.random.default_rng(15)
G, LAM = 10, 0.2
A = np.eye(G) + np.diag(np.full(G-1, .4), 1) + np.diag(np.full(G-1, .4), -1)
def norm(S): return S/np.sqrt(np.outer(np.diag(S), np.diag(S)))
SIG = norm(np.linalg.inv(A))
B = A.copy(); B[0,1]=B[1,0]=-0.45; B[2,3]=B[3,2]=0.0; B[0,3]=B[3,0]=0.4; B[1,4]=B[4,1]=0.35
while np.min(np.linalg.eigvalsh(B)) <= 0.05: B += 0.05*np.eye(G)
SIGR = norm(np.linalg.inv(B))
SCENS = ["No difference", "Different levels", "More spread", "Hidden subgroups", "Rewired genes", "Treatment effect"]

def make(scen, nca, nhc):
    hc = rng.multivariate_normal(np.zeros(G), SIG, nhc)
    ca = rng.multivariate_normal(np.zeros(G), SIGR if scen == "Rewired genes" else SIG, nca)
    if scen == "Different levels": ca[:, :3] += 0.45
    if scen == "More spread": ca = ca*np.sqrt(1.8)
    if scen == "Hidden subgroups":
        s = np.where(rng.random(nca) < .5, 1, -1); sh = np.zeros(G); sh[:4] = 0.8; ca += np.outer(s, sh)
    if scen == "Treatment effect":   # 60% of patients treated: genes 7-9 shift together; no disease effect
        t = rng.random(nca) < 0.6; ca[np.ix_(t, [6, 7, 8])] += 0.7
    return np.vstack([hc, ca]), np.r_[np.zeros(nhc), np.ones(nca)]

IU = np.triu_indices(G, 1)
def pcor(X):
    Xc = X - X.mean(0); S = Xc.T @ Xc/len(X); S = (1-LAM)*S + LAM*np.diag(np.diag(S))
    O = np.linalg.inv(S); d = np.sqrt(np.diag(O)); P = -O/np.outer(d, d); np.fill_diagonal(P, 0); return P
def edges_loo(R):
    N = len(R); P = pcor(R); return np.array([(N*P - (N-1)*pcor(np.delete(R, i, 0)))[IU] for i in range(N)])
def edges_add(R, Q):
    N = len(R); P = pcor(R); return np.array([((N+1)*pcor(np.vstack([R, x])) - N*P)[IU] for x in Q])
def strength(E):
    W = np.zeros((len(E), G, G)); W[:, IU[0], IU[1]] = E; return (W + W.transpose(0, 2, 1)).sum(2)
def lr(): return make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=3000))

METHODS = ["Simple gene levels", "Distance from healthy", "Quadratic classifier",
           "LIONESS network links", "LIONESS node strength", "Gene levels + LIONESS"]
def balanced_ref(Xtr, ytr):
    i0, i1 = np.where(ytr == 0)[0], np.where(ytr == 1)[0]; m = min(len(i0), len(i1))
    return np.r_[rng.choice(i0, m, replace=False), rng.choice(i1, m, replace=False)]

def lioness_features(Xtr, ytr, Xte, B=5):
    """Symmetric, class-balanced, bagged reference: every sample (train or test) gets the same operation."""
    Etr = np.zeros((len(Xtr), len(IU[0]))); Ete = np.zeros((len(Xte), len(IU[0])))
    for _ in range(B):
        ref = balanced_ref(Xtr, ytr); R = Xtr[ref]; inref = np.zeros(len(Xtr), bool); inref[ref] = True
        Etr[ref] += edges_loo(R)
        if (~inref).any(): Etr[~inref] += edges_add(R, Xtr[~inref])
        Ete += edges_add(R, Xte)
    return Etr/B, Ete/B

def one_rep(scen, nca, nhc):
    X, y = make(scen, nca, nhc); p = {m: np.zeros(len(y)) for m in METHODS}
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=int(rng.integers(1e9))).split(X, y):
        Xtr, Xte, ytr = X[tr], X[te], y[tr]
        p["Simple gene levels"][te] = lr().fit(Xtr, ytr).predict_proba(Xte)[:, 1]
        hc = Xtr[ytr == 0]; mu = hc.mean(0); Ci = np.linalg.inv(np.cov(hc.T)*0.8 + 0.2*np.eye(G))
        dist = lambda Z: np.einsum('ij,jk,ik->i', Z-mu, Ci, Z-mu)[:, None]
        p["Distance from healthy"][te] = lr().fit(dist(Xtr), ytr).predict_proba(dist(Xte))[:, 1]
        p["Quadratic classifier"][te] = QDA(reg_param=0.3).fit(Xtr, ytr).predict_proba(Xte)[:, 1]
        Etr, Ete = lioness_features(Xtr, ytr, Xte)
        p["LIONESS network links"][te] = lr().fit(Etr, ytr).predict_proba(Ete)[:, 1]
        p["LIONESS node strength"][te] = lr().fit(strength(Etr), ytr).predict_proba(strength(Ete))[:, 1]
        p["Gene levels + LIONESS"][te] = lr().fit(np.c_[Xtr, Etr], ytr).predict_proba(np.c_[Xte, Ete])[:, 1]
    return {m: roc_auc_score(y, v) for m, v in p.items()}

def asymmetry_rep(nca, nhc):
    """No true difference. Wrong design: controls-only reference (controls leave-one-out, patients add-one-in)."""
    X, y = make("No difference", nca, nhc); p = np.zeros(len(y))
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=int(rng.integers(1e9))).split(X, y):
        Xtr, Xte, ytr = X[tr], X[te], y[tr]; R = Xtr[ytr == 0]
        Etr = np.zeros((len(Xtr), len(IU[0]))); Etr[ytr == 0] = edges_loo(R); Etr[ytr == 1] = edges_add(R, Xtr[ytr == 1])
        Ete = edges_add(R, Xte)  # all test samples: add-one-in (group unknown)
        p[te] = lr().fit(Etr, ytr).predict_proba(Ete)[:, 1]
    return roc_auc_score(y, p)

if __name__ == "__main__":
    REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    out = {"auc": {}, "asym": {}}
    for nca, nhc in [(40, 40), (90, 77)]:
        key = f"{nca} vs {nhc}"; out["auc"][key] = {}
        for s in SCENS:
            a = np.array([[r[m] for m in METHODS] for r in (one_rep(s, nca, nhc) for _ in range(REPS))])
            out["auc"][key][s] = {m: [float(a[:, j].mean()), float(1.96*a[:, j].std()/np.sqrt(REPS))] for j, m in enumerate(METHODS)}
            print(key, s, {m: round(out["auc"][key][s][m][0], 2) for m in METHODS}, flush=True)
        sym = [one_rep("No difference", nca, nhc)["LIONESS network links"] for _ in range(REPS)]
        asy = [asymmetry_rep(nca, nhc) for _ in range(REPS)]
        out["asym"][key] = {"symmetric": [float(np.mean(sym)), float(1.96*np.std(sym)/np.sqrt(REPS))],
                            "controls-only": [float(np.mean(asy)), float(1.96*np.std(asy)/np.sqrt(REPS))]}
        print(key, "asymmetry", out["asym"][key], flush=True)
    json.dump(out, open("study_results.json", "w"), indent=1)
