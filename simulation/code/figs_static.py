"""Figure 1 (synthetic data check) and Figure 9 (exact vs first-order LIONESS edges)."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import simlib as L
BLUE, ORANGE, AQUA, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
rng = np.random.default_rng(42); out = {}
# ---- Figure 1: synthetic stand-in
st = L.Structure(20); X, Sg, f = L.draw(st, 5000, rng)
target = L.corr(st.Sig)[np.triu_indices(20, 1)]; emp = np.corrcoef(X.T)[np.triu_indices(20, 1)]
Xc, Sc, _ = L.draw(st, 20000, rng); hi = rng.random(20000) < 0.75
Xp, Sp, _ = L.draw(st, 20000, rng); Xh, Sh, _ = L.draw(st, 20000, rng, f_mean=3.0); Sp[hi] = Sh[hi]
I = L.ifn_score(np.vstack([Sp, Sc]), np.r_[np.zeros(20000, bool), np.ones(20000, bool)]); Ip, Ic = I[:20000], I[20000:]
theta = Ic.mean() + 2*Ic.std()
out["fig1"] = {"max_abs_corr_error": float(np.abs(emp - target).max()), "corr_of_corr": float(np.corrcoef(emp, target)[0, 1]),
               "controls_below_cutoff": float((Ic <= theta).mean()), "patients_below_cutoff": float((Ip <= theta).mean())}
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.8))
ax[0].scatter(target, emp, s=10, color=BLUE, edgecolor="white", linewidth=0.5)
lim = [min(target.min(), emp.min()) - .05, max(target.max(), emp.max()) + .05]; ax[0].plot(lim, lim, color=MUTED, lw=1, ls="--")
ax[0].set_xlabel("Target correlation (model)"); ax[0].set_ylabel("Correlation in simulated data")
ax[0].set_title("a  Gene–gene correlations (20 genes)", loc="left", fontsize=9)
bins = np.linspace(-3, 8, 70)
ax[1].hist(Ic, bins, color=BLUE, alpha=.75, label="Controls", density=True)
ax[1].hist(Ip, bins, color=ORANGE, alpha=.65, label="SLE patients", density=True)
ax[1].axvline(theta, color=INK, lw=1); ax[1].text(theta + .15, ax[1].get_ylim()[1]*.45, "cutoff θ", fontsize=8, color=INK)
ax[1].set_xlabel("IFN score (equation 2)"); ax[1].set_ylabel("Density"); ax[1].legend(frameon=False, fontsize=8, loc="upper right")
ax[1].set_title("b  IFN score distributions", loc="left", fontsize=9)
fig.tight_layout(); fig.savefig("../../manuscript/figures/fig1_synthetic_check.png"); plt.close()
# ---- Figure 9: exact vs first-order edges
def exact_vs_approx(G, lam, n=167, nq=30):
    st = L.Structure(G); X, _, _ = L.draw(st, n, rng); iu = np.triu_indices(G, 1)
    def pc(Z):
        Zc = Z - Z.mean(0); S = Zc.T @ Zc/len(Z); S = (1-lam)*S + lam*np.diag(np.diag(S)); O = np.linalg.inv(S)
        d = np.sqrt(np.diag(O)); P = -O/np.outer(d, d); np.fill_diagonal(P, 1); return P, O
    P, O = pc(X); mu = X.mean(0); ex, ap = [], []
    for q in range(nq):
        Pm, _ = pc(np.delete(X, q, 0)); e = (n*P - (n-1)*Pm)[iu]
        d = X[q] - mu; u = O @ d; sq = np.sqrt(np.diag(O))
        M = (1-lam)*np.outer(u, u) + lam*O @ np.diag(d**2) @ O; Mt = M/np.outer(sq, sq)
        a = (P + Mt + P*(np.diag(Mt)[:, None] + np.diag(Mt)[None, :])/2)[iu]
        ex.append(e); ap.append(a)
    ex, ap = np.concatenate(ex), np.concatenate(ap)
    return ex, ap
out["fig5"] = {}
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0))
for k, G in enumerate([10, 20, 30, 50, 60]):
    for lam in (0.0, 0.2):
        if lam == 0.0 and G >= 167: continue
        ex, ap = exact_vs_approx(G, lam)
        out["fig5"][f"G{G}_lam{lam}"] = {"r": float(np.corrcoef(ex, ap)[0, 1]), "median_abs_err": float(np.median(np.abs(ex - ap))),
                                        "p95_abs_err": float(np.quantile(np.abs(ex - ap), .95)), "sd_exact": float(ex.std())}
        if lam == 0.2 and G in (20, 60):
            a = ax[0 if G == 20 else 1]; a.scatter(ex, ap, s=3, color=BLUE, alpha=.35, linewidth=0)
            lim = [ex.min(), ex.max()]; a.plot(lim, lim, color=MUTED, lw=1, ls="--")
            a.set_title(f"{'a' if G == 20 else 'b'}  {G} genes, λ = 0.2 (r = {np.corrcoef(ex, ap)[0, 1]:.3f})", loc="left", fontsize=9)
            a.set_xlabel("Exact LIONESS edge (equation 6)"); a.set_ylabel("First-order edge (equation 9)")
fig.tight_layout(); fig.savefig("../../manuscript/figures/fig9_first_order.png"); plt.close()
json.dump(out, open("static_results.json", "w"), indent=1); print(json.dumps(out, indent=1))
