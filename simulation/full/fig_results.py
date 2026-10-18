"""Publication figures for the simulation results (Figures 2-4 and 6-9). Reads summary.json and results.jsonl."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
S = json.load(open("summary.json")); R = [json.loads(l) for l in open("results.jsonl")]
cal = S["oracle"]; FIG = "../../manuscript/figures/"
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e6e3"
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans", "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 200})
SEQ = LinearSegmentedColormap.from_list("seq", ["#f4f7fc", "#b9d1f1", "#5f9be3", "#2a78d6", "#123a6b"])
SIZES = [10, 20, 30, 50, 60]; SCEN = ["S0", "S1", "S2", "S3", "S4"]
FAM = [("Baseline", ["M0a"]), ("Expression", ["M1", "M2", "M3-score", "M3-boost", "M3-SVM", "M4", "M5", "M6"]),
       ("Network method", ["W2"]), ("LIONESS", ["L1", "L2", "L2-P", "L2-S", "L2-S-P", "L3", "L3-P", "L-explo", "L-sec+explo"])]
MODELS = [m for _, ms in FAM for m in ms]; FAMCOL = {"Baseline": MUTED, "Expression": ORANGE, "Network method": AQUA, "LIONESS": BLUE}
A = {tuple(k.split("|")): v for k, v in S["aucA"].items()}
def auc(G, sc, m): v = A.get((str(G), sc, m)); return (v[0], v[1]) if v else (np.nan, np.nan)
def rel(a, G, sc): return a if sc == "S0" else (a - 0.5)/(cal[f"{G}|{sc}|0.7"][1] - 0.5)

# ---------- Figure 2: performance map (model x scenario x pathway size), relative AUC
cols = [(sc, G) for sc in SCEN for G in SIZES]
M = np.array([[rel(auc(G, sc, m)[0], G, sc) if sc != "S0" else np.nan for sc, G in cols] for m in MODELS])
fig, ax = plt.subplots(figsize=(8.6, 5.6))
im = ax.imshow(M, cmap=SEQ, vmin=-0.2, vmax=1.0, aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if np.isfinite(M[i, j]): ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=5, color="white" if M[i, j] > 0.6 else INK)
S0 = np.array([auc(G, "S0", m)[0] for m in MODELS for G in SIZES]).reshape(len(MODELS), 5)
for i in range(len(MODELS)):
    for j in range(5): ax.text(j, i, f"{S0[i, j]:.2f}", ha="center", va="center", fontsize=5, color=MUTED)
for b in range(1, 5): ax.axvline(b*5 - 0.5, color="white", lw=3)
row = 0
for fam, ms in FAM:
    if row: ax.axhline(row - 0.5, color="white", lw=3)
    ax.text(-4.2, row + (len(ms) - 1)/2, fam, ha="right", va="center", fontsize=7, color=FAMCOL[fam], fontweight="bold")
    row += len(ms)
ax.set_yticks(range(len(MODELS))); ax.set_yticklabels(MODELS)
ax.set_xticks(range(len(cols))); ax.set_xticklabels([str(G) for _, G in cols], fontsize=6)
for k, sc in enumerate(SCEN):
    ax.text(k*5 + 2, -1.3, {"S0": "S0 null (AUC)", "S1": "S1 level", "S2": "S2 spread", "S3": "S3 subgroups", "S4": "S4 rewiring"}[sc], ha="center", fontsize=8, fontweight="bold")
ax.set_xlabel("Genes in pathway (60 = stress test)")
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
cb = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.01); cb.set_label("AUC relative to the best possible classifier")
fig.savefig(FIG + "fig2_performance_map.png", bbox_inches="tight"); plt.close()

# ---------- Figure 3: detection fingerprint (dot matrix)
P = {tuple(k.split("|")): v for k, v in S["pop"].items()}
tests = [("level", "Level\n(eq. 27)"), ("spread", "Spread\n(eq. 28)"), ("structure", "Structure,\npartial (eq. 29)"), ("structure-P", "Structure,\nPearson"), ("flag", "Subgroup\nflag (eq. 30)")]
scs = ["S0", "S1", "S2", "S3", "S4", "S7"]; names = {"S0": "S0 null", "S1": "S1 level", "S2": "S2 spread", "S3": "S3 subgroups", "S4": "S4 rewiring", "S7": "S7 positive control"}
fig, axs = plt.subplots(1, 2, figsize=(8.0, 3.4), gridspec_kw=dict(width_ratios=[1, 1]))
for a, G in zip(axs, [20, 50]):
    for i, sc in enumerate(scs):
        for j, (t, _) in enumerate(tests):
            v = P.get((str(G), sc), {}).get(t, [np.nan])[0]
            if not np.isfinite(v): continue
            a.scatter(j, i, s=20 + 600*v, color=BLUE, alpha=0.25 + 0.75*v, edgecolor="white", linewidth=1.0, zorder=3)
            a.text(j, i, f"{100*v:.0f}", ha="center", va="center", fontsize=6, color="white" if v > 0.45 else INK, zorder=4)
    a.set_xticks(range(len(tests))); a.set_xticklabels([l for _, l in tests], fontsize=6.5)
    a.set_yticks(range(len(scs))); a.set_yticklabels([names[s] for s in scs]); a.invert_yaxis()
    a.set_xlim(-0.6, len(tests) - 0.4); a.set_ylim(len(scs) - 0.5, -0.6); a.set_title(f"{G} genes", loc="left", fontsize=9)
    a.grid(color=GRID, lw=0.6); a.set_axisbelow(True)
    for s in a.spines.values(): s.set_visible(False)
    a.tick_params(length=0)
fig.text(0.5, -0.02, "Number in each circle: percentage of simulated datasets with p < 0.05 (circle area proportional)", ha="center", fontsize=7, color=MUTED)
fig.tight_layout(); fig.savefig(FIG + "fig3_detection_fingerprint.png", bbox_inches="tight"); plt.close()

# ---------- Figure 4: effect of pathway size (lines with Monte Carlo bands, direct labels)
show = [("L2", BLUE), ("L2-P", ORANGE), ("L1", AQUA), ("M6", YELLOW), ("M4", MAGENTA), ("M2", GREEN)]
fig, axs = plt.subplots(1, 4, figsize=(10.5, 3.0), sharey=True)
for k, sc in enumerate(["S1", "S2", "S3", "S4"]):
    a = axs[k]; a.axvspan(55, 63, color=GRID, zorder=0); a.text(59, 0.405, "stress\ntest", ha="center", fontsize=6, color=MUTED)
    a.axhline(0.5, color=MUTED, lw=0.8, ls=":"); a.plot(SIZES, [0.7]*5, color=INK, lw=0.8, ls="--"); a.text(10, 0.715, "best possible", fontsize=6, color=INK)
    for m, c in show:
        y = np.array([auc(G, sc, m)[0] for G in SIZES]); e = np.array([auc(G, sc, m)[1] for G in SIZES])
        a.fill_between(SIZES, y - 1.96*e, y + 1.96*e, color=c, alpha=0.15, linewidth=0); a.plot(SIZES, y, color=c, lw=2, marker="o", ms=3.5, markeredgecolor="white", markeredgewidth=0.8)
        if k == 3: a.text(63.5, y[-1], m, color=INK, fontsize=7, va="center")
    a.set_title({"S1": "S1 level", "S2": "S2 spread", "S3": "S3 subgroups", "S4": "S4 rewiring"}[sc], loc="left", fontsize=9)
    a.set_xticks(SIZES); a.set_xlabel("Genes in pathway"); a.set_xlim(7, 63); a.set_ylim(0.4, 0.92)
    if k == 0: a.set_ylabel("AUC")
fig.tight_layout(); fig.savefig(FIG + "fig4_pathway_size.png", bbox_inches="tight"); plt.close()

# ---------- Figure 6: model similarity map (PCA of AUC profiles across scenarios and sizes)
X = np.array([[auc(G, sc, m)[0] for sc in SCEN[1:] for G in SIZES] for m in MODELS])
Xc = X - X.mean(0); U, s, Vt = np.linalg.svd(Xc, full_matrices=False); Z = U[:, :2]*s[:2]; ve = s**2/np.sum(s**2)
fig, a = plt.subplots(figsize=(5.4, 4.2))
for fam, ms in FAM:
    idx = [MODELS.index(m) for m in ms]
    a.scatter(Z[idx, 0], Z[idx, 1], s=60, color=FAMCOL[fam], edgecolor="white", linewidth=1.5, label=fam, zorder=3)
for i, m in enumerate(MODELS): a.annotate(m, (Z[i, 0], Z[i, 1]), xytext=(4, 3), textcoords="offset points", fontsize=6.5, color=INK)
a.axhline(0, color=GRID, lw=0.8, zorder=0); a.axvline(0, color=GRID, lw=0.8, zorder=0)
a.set_xlabel(f"Component 1 ({100*ve[0]:.0f}% of variation)"); a.set_ylabel(f"Component 2 ({100*ve[1]:.0f}% of variation)")
a.legend(frameon=False, fontsize=7, loc="best")
fig.tight_layout(); fig.savefig(FIG + "fig6_model_map.png", bbox_inches="tight"); plt.close()
json.dump({"pca_var": ve[:3].tolist(), "loadings": {f"{sc}|{G}": [float(Vt[0, i]), float(Vt[1, i])] for i, (sc, G) in enumerate([(sc, G) for sc in SCEN[1:] for G in SIZES])}}, open("pca.json", "w"), indent=1)

# ---------- Figure 7: safeguards (dumbbell)
C = {tuple(k.split("|")): v for k, v in S["gc"].items()}
metrics = [("L3", "AUC, L3"), ("L3-P", "AUC, L3-P"), ("L2", "AUC, L2"), ("structure", "Structure test\nrejection rate"), ("L3vsM5_sig", "L3 > M5\n(significant)")]
vcol = {"none": RED, "cond": YELLOW, "restrict": AQUA, "both": BLUE}
vlab = {"none": "No safeguard", "cond": "IFN-score conditioning", "restrict": "Exclusion (S5) / matching (S6)", "both": "Both safeguards"}
fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.2), sharey=True)
for a, sc in zip(axs, ["S5", "S6"]):
    for i, (m, lab) in enumerate(metrics):
        vals = {v: C.get((sc, "20", v), {}).get(m, [np.nan])[0] for v in vcol}
        a.plot([vals["none"], vals["both"]], [i, i], color=GRID, lw=3, zorder=1)
        for v, c in vcol.items(): a.scatter(vals[v], i, s=45, color=c, edgecolor="white", linewidth=1.2, zorder=3, label=vlab[v] if i == 0 else None)
    a.set_yticks(range(len(metrics))); a.set_yticklabels([l for _, l in metrics]); a.invert_yaxis()
    a.axvline(0.5, color=MUTED, lw=0.8, ls=":"); a.axvline(0.05, color=MUTED, lw=0.8, ls="--")
    a.set_xlim(-0.02, 1.0); a.set_title({"S5": "S5 treatment (no true difference)", "S6": "S6 selection (no true difference)"}[sc], loc="left", fontsize=9)
    a.set_xlabel("Value (AUC or proportion)"); a.grid(axis="x", color=GRID, lw=0.6); a.set_axisbelow(True)
axs[0].legend(frameon=False, fontsize=6.5, loc="upper center", bbox_to_anchor=(1.05, 1.28), ncol=4)
fig.tight_layout(); fig.savefig(FIG + "fig7_safeguards.png", bbox_inches="tight"); plt.close()

# ---------- Figure 8: power curves for the primary comparison
Bp = {tuple(k.split("|")): v for k, v in S["gb"].items()}
fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
for a, sc in zip(axs, ["S3", "S4"]):
    for p, c in [("L3 vs M5", BLUE), ("L3-P vs M5", ORANGE)]:
        xs = [0.6, 0.7, 0.8]; ys = [Bp.get((sc, str(x), "90v77"), {}).get(p, {}).get("power", [np.nan])[0] for x in xs]
        a.plot(xs, ys, color=c, lw=2, marker="o", ms=4, markeredgecolor="white", label=f"{p} (90 vs 77)")
        y40 = Bp.get((sc, "0.7", "40v40"), {}).get(p, {}).get("power", [np.nan])[0]
        a.scatter([0.7], [y40], marker="D", s=30, facecolor="white", edgecolor=c, linewidth=1.5, zorder=4, label=f"{p} (40 vs 40)")
    a.axhline(0.8, color=MUTED, lw=0.8, ls="--"); a.text(0.6, 0.82, "80% power", fontsize=6, color=MUTED)
    a.set_xticks([0.6, 0.7, 0.8]); a.set_xlabel("AUC of the best possible classifier"); a.set_ylim(0, 1)
    a.set_title({"S3": "S3 subgroups", "S4": "S4 rewiring"}[sc], loc="left", fontsize=9)
axs[0].set_ylabel("Power (proportion significant)"); axs[1].legend(frameon=False, fontsize=6, loc="upper left", bbox_to_anchor=(1.0, 1.0))
fig.tight_layout(); fig.savefig(FIG + "fig8_power.png", bbox_inches="tight"); plt.close()

# ---------- Figure 9: distribution of AUC across simulated datasets (violin + points), S4, 20 genes
ms = [("M5", ORANGE), ("M6", YELLOW), ("L2", BLUE), ("L2-P", VIOLET), ("L3", AQUA), ("L3-P", MAGENTA)]
fig, axs = plt.subplots(1, 2, figsize=(8.0, 3.0), sharey=True)
rng = np.random.default_rng(0)
for a, sc in zip(axs, ["S0", "S4"]):
    for k, (m, c) in enumerate(ms):
        v = np.array([r["auc"][m] for r in R if r["grid"] == "A" and r["scen"] == sc and r["G"] == 20])
        if len(v) < 2: continue
        vp = a.violinplot(v, [k], widths=0.75, showextrema=False)
        for b in vp["bodies"]: b.set_facecolor(c); b.set_alpha(0.25); b.set_edgecolor("none")
        a.scatter(k + rng.uniform(-0.12, 0.12, len(v)), v, s=6, color=c, alpha=0.8, linewidth=0)
        a.plot([k - 0.25, k + 0.25], [np.median(v)]*2, color=INK, lw=1.5)
    a.axhline(0.5, color=MUTED, lw=0.8, ls=":")
    if sc == "S4": a.axhline(cal["20|S4|0.7"][1], color=INK, lw=0.8, ls="--"); a.text(5.4, cal["20|S4|0.7"][1] + 0.01, "best possible", fontsize=6, ha="right")
    a.set_xticks(range(len(ms))); a.set_xticklabels([m for m, _ in ms]); a.set_title({"S0": "S0 null", "S4": "S4 rewiring"}[sc] + ", 20 genes", loc="left", fontsize=9)
axs[0].set_ylabel("AUC per simulated dataset")
fig.tight_layout(); fig.savefig(FIG + "fig9_auc_distribution.png", bbox_inches="tight"); plt.close()
print("figures written")
