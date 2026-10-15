import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
S = ""
R = json.load(open(S + "study_results.json"))["auc"]["90 vs 77"]
scens = ["No difference", "Different levels", "More spread", "Hidden subgroups", "Rewired genes", "Treatment effect"]
subt = ["Nothing differs", "Some genes higher in patients", "Patients more variable",
        "Patients split up and down", "Genes connect differently", "60% of patients treated"]
meth = ["Simple gene levels", "Distance from healthy", "Quadratic classifier",
        "LIONESS network links", "LIONESS node strength", "Gene levels + LIONESS"]
col = {"Simple gene levels": "#eb6834", "Distance from healthy": "#eb6834", "Quadratic classifier": "#eb6834",
       "LIONESS network links": "#2a78d6", "LIONESS node strength": "#2a78d6", "Gene levels + LIONESS": "#1baf7a"}
surf, ink, ink2, grid = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
fig, axes = plt.subplots(2, 3, figsize=(17, 9.6), sharey=True, facecolor=surf)
for k, (ax, s) in enumerate(zip(axes.flat, scens)):
    ax.set_facecolor(surf); vals = [R[s][m][0] for m in meth]; best = max(vals)
    for i, m in enumerate(meth):
        v, e = R[s][m]; y = len(meth) - 1 - i
        ax.add_patch(FancyBboxPatch((0.3, y - 0.32), v - 0.3, 0.64, boxstyle="round,pad=0,rounding_size=0.04",
                                    linewidth=0, facecolor=col[m], mutation_aspect=0.5))
        win = best > 0.6 and v >= best - 0.025
        ax.text(v + 0.012, y, f"{v:.2f}" + ("  best" if win else ""), va="center", fontsize=10.5, color=ink,
                fontweight="bold" if win else "normal")
    ax.axvline(0.5, color=ink2, lw=1, ls=(0, (3, 3)))
    ax.set_xlim(0.3, 0.97); ax.set_ylim(-0.6, len(meth) - 0.4); ax.set_xticks([0.3, 0.5, 0.7, 0.9])
    ax.tick_params(colors=ink2, length=0); ax.grid(axis="x", color=grid, lw=0.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(f"{k+1}. {s}\n", fontsize=12.5, fontweight="bold", color=ink, loc="left")
    ax.text(0, 1.02, subt[k], transform=ax.transAxes, fontsize=10.5, color=ink2)
    if k >= 3: ax.set_xlabel("Score (AUC)", color=ink2)
for ax in axes[:, 0]:
    ax.set_yticks(range(len(meth))); ax.set_yticklabels(meth[::-1], color=ink)
fig.legend(handles=[Patch(color="#eb6834", label="Simple methods"), Patch(color="#2a78d6", label="LIONESS networks alone"),
                    Patch(color="#1baf7a", label="Gene levels + LIONESS (main hypothesis)")],
           loc="upper left", ncol=3, frameon=False, fontsize=11, bbox_to_anchor=(0.004, 0.955))
fig.suptitle("Simulation study: which method tells patients from healthy people?", x=0.01, ha="left",
             fontsize=15, fontweight="bold", color=ink, y=0.995)
fig.text(0.01, 0.965, "90 pretend patients vs 77 pretend healthy people (about the size of the real main dataset), 10 genes, 30 repeats, 5-fold cross-validation",
         fontsize=10.5, color=ink2)
fig.text(0.01, 0.005, "Score 0.5 = guessing (dashed line), 1.0 = perfect. Uncertainty on each score is about ±0.02.", fontsize=10, color=ink2)
plt.tight_layout(rect=(0, 0.025, 1, 0.915)); plt.savefig(S + "study_auc.png", dpi=150, facecolor=surf); print("ok")
