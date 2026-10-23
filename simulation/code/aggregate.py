"""Aggregates results.jsonl into result tables (Markdown + JSON) and Figures 2-4."""
import json, numpy as np, collections, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = [json.loads(l) for l in open("results.jsonl")]
cal = json.load(open("calibration.json"))
SIZES = [10, 20, 30, 50, 60]; SCEN = ["S0", "S1", "S2", "S3", "S4"]
def sel(**kw): return [r for r in R if all(r.get(k) == v for k, v in kw.items())]
def mse(v): v = np.asarray(v, float); return v.mean(), v.std(ddof=1)/np.sqrt(len(v)) if len(v) > 1 else np.nan
def pse(b): b = np.asarray(b, float); p = b.mean(); return p, np.sqrt(p*(1-p)/len(b))
def fmt(m, s, d=2): return f"{m:.{d}f} ({s:.{d}f})" if np.isfinite(s) else f"{m:.{d}f}"
def rel(auc, ceil): return (auc - 0.5)/(ceil - 0.5)
out = {}
# ---- Table: AUC by model x scenario (grid A) for each size
models = ["M0a", "M1", "M2", "M3-score", "M3-boost", "M3-SVM", "M4", "M5", "M6", "W2", "L1", "L2", "L2-P", "L2-S", "L2-S-P", "L3", "L3-P", "L-explo", "L-sec+explo"]
aucA = {}
for G in SIZES:
    for sc in SCEN:
        rs = sel(grid="A", scen=sc, G=G)
        if not rs: continue
        for m in models: aucA[(G, sc, m)] = mse([r["auc"][m] for r in rs]) + (len(rs),)
out["aucA"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in aucA.items()}
out["oracle"] = cal
def table_auc(G):
    hdr = "| Model | " + " | ".join(SCEN) + " |\n|---|" + "---|"*len(SCEN) + "\n"
    rows = ""
    for m in models:
        cells = []
        for sc in SCEN:
            if (G, sc, m) not in aucA: cells.append("–"); continue
            a, s, n = aucA[(G, sc, m)]
            if sc == "S0": cells.append(fmt(a, s))
            else:
                c = cal[f"{G}|{sc}|0.7"][1]; cells.append(f"{fmt(a, s)} [{rel(a, c):.2f}]")
        rows += f"| {m} | " + " | ".join(cells) + " |\n"
    return hdr + rows
out["table_auc_md"] = {G: table_auc(G) for G in SIZES}
# ---- pairs: false positives and coverage under S0; power under S1-S4
pairs = ["L3 vs M5", "L3-P vs M5", "L2 vs M6", "L2-P vs M6", "L2 vs M4", "L2-P vs M4"]
def sig_pos(r, p): d, se = r["pairs"][p]; return d - 1.96*se > 0
def covers0(r, p): d, se = r["pairs"][p]; return abs(d) <= 1.96*se
fp = {}
for G in SIZES:
    rs = sel(grid="A", scen="S0", G=G)
    for p in pairs: fp[(G, p)] = (pse([sig_pos(r, p) for r in rs]), pse([covers0(r, p) for r in rs]), len(rs))
out["fp"] = {f"{k[0]}|{k[1]}": v for k, v in fp.items()}
# ---- population tests (grid A)
layers = ["level", "spread", "structure", "structure-P"]
pop = {}
for G in SIZES:
    for sc in SCEN:
        rs = sel(grid="A", scen=sc, G=G)
        if not rs: continue
        pop[(G, sc)] = {l: pse([r["p"][l] < 0.05 for r in rs]) for l in layers}
        pop[(G, sc)]["flag"] = pse([r["subgroup_flag"] for r in rs])
for sc in ["S7"]:
    for G in SIZES:
        rs = sel(grid="C", scen=sc, G=G)
        if rs:
            pop[(G, sc)] = {l: pse([r["p"][l] < 0.05 for r in rs]) for l in layers}; pop[(G, sc)]["flag"] = pse([r["subgroup_flag"] for r in rs])
out["pop"] = {f"{k[0]}|{k[1]}": v for k, v in pop.items()}
# ---- grid C: S5 / S6 variants, S7
gc = {}
for sc in ["S5", "S6"]:
    for G in SIZES:
        for v in ["none", "cond", "restrict", "both"]:
            rs = sel(grid="C", scen=sc, G=G, variant=v)
            if not rs: continue
            d = {m: mse([r["auc"][m] for r in rs]) for m in ["M0a", "M5", "L2", "L2-P", "L3", "L3-P"]}
            d.update({l: pse([r["p"][l] < 0.05 for r in rs]) for l in layers})
            d["L3vsM5_sig"] = pse([sig_pos(r, "L3 vs M5") for r in rs]); d["n_used"] = np.mean([r["n_used"] for r in rs], 0).tolist()
            gc[(sc, G, v)] = d
for G in SIZES:
    rs = sel(grid="C", scen="S7", G=G)
    if rs: gc[("S7", G, "primary")] = {m: mse([r["auc"][m] for r in rs]) for m in ["M0a", "M2", "M4", "M5", "M6", "L2", "L2-P", "L3", "L3-P"]}
out["gc"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in gc.items()}
# ---- grid B: smallest detectable difference (MDD = 2.80 x median SE) and power
gb = {}
for sc in SCEN:
    for c, n in [(0.6, [90, 77]), (0.7, [40, 40]), (0.8, [90, 77])]:
        rs = sel(grid="B", scen=sc, ceil=c, n=n)
        if not rs: continue
        gb[(sc, c, tuple(n))] = {p: dict(mdd=float(2.80*np.median([r["pairs"][p][1] for r in rs])),
                                        delta=mse([r["pairs"][p][0] for r in rs]), power=pse([sig_pos(r, p) for r in rs])) for p in ["L3 vs M5", "L3-P vs M5"]}
for sc in SCEN:   # add the main setting from grid A at 20 genes
    rs = sel(grid="A", scen=sc, G=20)
    if rs: gb[(sc, 0.7, (90, 77))] = {p: dict(mdd=float(2.80*np.median([r["pairs"][p][1] for r in rs])),
                                             delta=mse([r["pairs"][p][0] for r in rs]), power=pse([sig_pos(r, p) for r in rs])) for p in ["L3 vs M5", "L3-P vs M5"]}
out["gb"] = {f"{k[0]}|{k[1]}|{k[2][0]}v{k[2][1]}": v for k, v in gb.items()}
json.dump(out, open("summary.json", "w"), indent=1, default=float)

# ---------------- figures
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"
INK, MUTED = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
# Figure 2: heatmaps of AUC (model x scenario) for each pathway size
fig, axes = plt.subplots(1, 5, figsize=(11, 5.2), sharey=True)
for k, G in enumerate(SIZES):
    M = np.array([[aucA[(G, sc, m)][0] if (G, sc, m) in aucA else np.nan for sc in SCEN] for m in models])
    ax = axes[k]; im = ax.imshow(M, cmap="Blues", vmin=0.4, vmax=0.85, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if np.isfinite(M[i, j]): ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=6, color="white" if M[i, j] > 0.7 else INK)
    ax.set_xticks(range(len(SCEN))); ax.set_xticklabels(SCEN); ax.set_title(f"{G} genes" + (" (stress test)" if G == 60 else ""), fontsize=8)
    if k == 0: ax.set_yticks(range(len(models))); ax.set_yticklabels(models)
    for s in ax.spines.values(): s.set_visible(False)
cb = fig.colorbar(im, ax=axes, fraction=0.015, pad=0.01); cb.set_label("AUC")
fig.savefig("../../manuscript/figures/fig2_auc_heatmap.png", bbox_inches="tight"); plt.close()
# Figure 6: rejection rates of population tests and subgroup flag at 20 genes
labs = ["Level", "Spread", "Structure (partial)", "Structure (Pearson)", "Subgroup flag"]; keys = layers + ["flag"]
cols = [BLUE, ORANGE, AQUA, YELLOW, VIOLET]; scs = SCEN + ["S7"]
fig, ax = plt.subplots(figsize=(7.2, 3.0)); w = 0.15
for i, (lab, key, col) in enumerate(zip(labs, keys, cols)):
    vals = [pop[(20, sc)][key][0] if (20, sc) in pop else np.nan for sc in scs]
    ax.bar(np.arange(len(scs)) + (i - 2)*w, vals, w*0.9, color=col, label=lab)
ax.axhline(0.05, color=MUTED, lw=1, ls="--"); ax.text(len(scs) - 0.45, 0.07, "5%", color=MUTED, fontsize=7)
ax.set_xticks(range(len(scs))); ax.set_xticklabels(scs); ax.set_ylabel("Proportion of datasets with p < 0.05"); ax.set_ylim(0, 1.05)
ax.legend(frameon=False, ncol=5, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, 1.15))
fig.tight_layout(); fig.savefig("../../manuscript/figures/fig3_population_tests.png", bbox_inches="tight"); plt.close()
# Figure 4: effect of pathway size, S1-S4
show = [("L2", BLUE), ("L2-P", ORANGE), ("L1", AQUA), ("M6", YELLOW), ("M4", MAGENTA), ("M2", GREEN)]
fig, axes = plt.subplots(1, 4, figsize=(11, 2.9), sharey=True)
for k, sc in enumerate(["S1", "S2", "S3", "S4"]):
    ax = axes[k]
    for m, col in show:
        ys = [aucA[(G, sc, m)][0] if (G, sc, m) in aucA else np.nan for G in SIZES]
        es = [aucA[(G, sc, m)][1] if (G, sc, m) in aucA else np.nan for G in SIZES]
        ax.errorbar(SIZES, ys, yerr=es, color=col, lw=2, marker="o", ms=4, capsize=0, label=m)
    ax.axvspan(55, 62, color="#e6e6e3", zorder=0); ax.text(57.5, 0.42, "stress\ntest", ha="center", fontsize=6, color=MUTED)
    ax.set_title(sc, fontsize=9, loc="left"); ax.set_xticks(SIZES); ax.set_xlabel("Genes in pathway"); ax.axhline(0.5, color=MUTED, lw=.8, ls=":")
    if k == 0: ax.set_ylabel("AUC")
axes[-1].legend(frameon=False, fontsize=7, loc="center left", bbox_to_anchor=(1.0, 0.5))
fig.tight_layout(); fig.savefig("../../manuscript/figures/fig4_pathway_size.png", bbox_inches="tight"); plt.close()
print("ok", len(R), "rows")
