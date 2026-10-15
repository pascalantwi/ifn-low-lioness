"""Step 5: layered population tests (level, spread, structure) and the hidden-subgroup check."""
import numpy as np, json, warnings
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
import study
warnings.filterwarnings("ignore")
rng = np.random.default_rng(7); study.rng = rng
G, LAM = study.G, study.LAM
def shrink_cov(X):
    S = np.cov(X.T); return (1-LAM)*S + LAM*np.diag(np.diag(S))
def stats(X, y):
    a, b = X[y == 1], X[y == 0]
    W = shrink_cov(np.vstack([a - a.mean(0), b - b.mean(0)])); Wi = np.linalg.inv(W)
    dm = a.mean(0) - b.mean(0); t1 = dm @ Wi @ dm
    da = np.einsum('ij,jk,ik->i', a - a.mean(0), Wi, a - a.mean(0)); db = np.einsum('ij,jk,ik->i', b - b.mean(0), Wi, b - b.mean(0))
    t2 = abs(da.mean() - db.mean())
    t3 = np.linalg.norm(study.pcor(a) - study.pcor(b))
    return np.array([t1, t2, t3])
def perm_p(X, y, B=99):
    obs = stats(X, y); c = np.zeros(3)
    for _ in range(B): c += stats(X, rng.permutation(y)) >= obs
    return (c + 1)/(B + 1)
def subgroups(Z):
    Z = PCA(3).fit_transform(Z - Z.mean(0))
    b = [GaussianMixture(k, n_init=3, random_state=0).fit(Z).bic(Z) for k in (1, 2)]; return b[0] - b[1] > 2
REPS = 30; out = {}
for s in study.SCENS:
    sig = np.zeros(3); flag = 0
    for _ in range(REPS):
        X, y = study.make(s, 90, 77); p = perm_p(X, y); sig += p < 0.05
        if p[2] < 0.05 and subgroups(X[y == 1]) and not subgroups(X[y == 0]): flag += 1
    out[s] = {"level": sig[0]/REPS, "spread": sig[1]/REPS, "structure": sig[2]/REPS, "subgroup flag": flag/REPS}
    print(s, out[s], flush=True)
json.dump(out, open("tests_results.json", "w"), indent=1)
