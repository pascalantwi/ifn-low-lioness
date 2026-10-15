import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
S = ""
R = json.load(open(S + "ifn_results.json"))
keys = ["IFN-low vs healthy | No real difference", "IFN-low vs healthy | Gene levels differ",
        "IFN-low vs healthy | Genes rewired", "IFN-high vs healthy | No real difference"]
titles = ["1. IFN-low: no real difference", "2. IFN-low: gene levels differ", "3. IFN-low: genes rewired", "4. Check: IFN-high vs healthy"]
subt = ["Only leftover interferon differs", "Some genes higher in IFN-low patients", "Genes connect differently in IFN-low patients", "Everything should work here"]
meth = ["Leftover IFN score", "Gene levels", "Gene levels + IFN score", "Quadratic classifier", "LIONESS links", "Gene levels + LIONESS + IFN score"]
col = {m: "#eb6834" for m in meth[:4]}; col["LIONESS links"] = "#2a78d6"; col["Gene levels + LIONESS + IFN score"] = "#1baf7a"
surf, ink, ink2, grid = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
fig, axes = plt.subplots(1, 4, figsize=(19, 5.9), sharey=True, facecolor=surf)
for k, (ax, key) in enumerate(zip(axes, keys)):
    ax.set_facecolor(surf); A = R[key]["auc"]; best = max(A[m][0] for m in meth)
    for i, m in enumerate(meth):
        v = A[m][0]; y = len(meth) - 1 - i
        ax.add_patch(FancyBboxPatch((0.3, y - 0.32), v - 0.3, 0.64, boxstyle="round,pad=0,rounding_size=0.04",
                                    linewidth=0, facecolor=col[m], mutation_aspect=0.5))
        win = v >= best - 0.025
        ax.text(v + 0.012, y, f"{v:.2f}" + ("  best" if win else ""), va="center", fontsize=10.5, color=ink, fontweight="bold" if win else "normal")
    ax.axvline(0.5, color=ink2, lw=1, ls=(0, (3, 3)))
    ax.set_xlim(0.3, 1.12); ax.set_ylim(-0.6, len(meth) - 0.4); ax.set_xticks([0.3, 0.5, 0.7, 0.9])
    ax.tick_params(colors=ink2, length=0); ax.grid(axis="x", color=grid, lw=0.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(titles[k] + "\n", fontsize=12.5, fontweight="bold", color=ink, loc="left")
    ax.text(0, 1.02, subt[k], transform=ax.transAxes, fontsize=10.5, color=ink2)
    ax.set_xlabel("Score (AUC)", color=ink2)
axes[0].set_yticks(range(len(meth))); axes[0].set_yticklabels(meth[::-1], color=ink)
fig.suptitle("Simulation of the full IFN-low pipeline: does LIONESS add anything beyond the leftover interferon signal?",
             x=0.01, ha="left", fontsize=14.5, fontweight="bold", color=ink, y=0.99)
fig.text(0.01, 0.925, "360 pretend lupus patients (25% IFN-low) and 77 healthy people; IFN-low chosen by the cutoff inside each training fold; IFN genes removed from features; 30 repeats",
         fontsize=10.5, color=ink2)
fig.legend(handles=[Patch(color="#eb6834", label="Simple methods"), Patch(color="#2a78d6", label="LIONESS networks alone"),
                    Patch(color="#1baf7a", label="Main hypothesis: gene levels + LIONESS + IFN score")],
           loc="upper left", ncol=3, frameon=False, fontsize=11, bbox_to_anchor=(0.004, 0.91))
fig.text(0.01, 0.005, "Score 0.5 = guessing (dashed line), 1.0 = perfect. Uncertainty on each score is about ±0.02.", fontsize=10, color=ink2)
plt.tight_layout(rect=(0, 0.03, 1, 0.84)); plt.savefig(S + "ifn_auc.png", dpi=150, facecolor=surf); print("ok")
