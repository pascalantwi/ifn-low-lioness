# Pilot simulation study

**Date:** 2026-10-15
**Purpose:** a small pilot of the simulation study in the refined plan. It checks, on pretend data where the truth is known, whether the planned design gives the right answer before any real lupus data are analysed.

**Scale:** one pathway of 10 genes (plus 4 interferon genes in the IFN pipeline), Gaussian data, 30 repeats per setting, 5-fold cross-validation. The full simulation in the plan will use more genes, realistic (plasmode) data and more repeats.

## How it follows the refined plan

| Refined plan step | What the simulation did |
|---|---|
| IFN-low definition | Cutoff = healthy mean + 2 SD, fitted inside each training fold, same filter for patients and controls |
| Leftover IFN as a baseline | IFN genes removed from features; IFN score kept as its own model |
| Symmetric, balanced reference | Equal patients and healthy people, 5 bagged subsets, same rule for every sample (leave-one-out if in the reference, add-one-in otherwise) |
| Mechanism-matched baselines | Gene levels, distance from healthy, regularised quadratic classifier |
| Main hypothesis H1 | Gene levels + LIONESS + IFN score vs gene levels + IFN score |
| Layered direct tests | Level, spread and structure permutation tests, plus the hidden-subgroup check |
| Validation | 5-fold cross-validation, 30 repeats, real-data size (about 90 vs 77) and 40 vs 40 |

## Results

### 1. Which method separates the groups? (90 vs 77, AUC; ±0.02)

| Planted difference | Gene levels | Distance from healthy | Quadratic classifier | LIONESS links | LIONESS strength | Gene levels + LIONESS |
|---|---|---|---|---|---|---|
| None | 0.48 | 0.49 | 0.47 | 0.49 | 0.50 | 0.48 |
| Gene levels | **0.77** | 0.56 | 0.71 | 0.50 | 0.50 | 0.68 |
| More spread | 0.50 | **0.80** | 0.70 | 0.48 | 0.49 | 0.48 |
| Hidden subgroups | 0.49 | 0.73 | **0.79** | 0.69 | 0.66 | 0.68 |
| Rewired genes | 0.48 | 0.54 | **0.71** | 0.69 | 0.54 | 0.67 |
| Treatment effect | **0.69** | 0.58 | 0.65 | 0.51 | 0.51 | 0.60 |

**Finding:** LIONESS only detects differences in how genes connect (subgroups, rewiring), and even then the quadratic classifier matches or beats it. With a balanced reference, LIONESS does not detect level or spread differences.

### 2. Direct tests (share of 30 datasets called "different", 90 vs 77)

| Planted difference | Level test | Spread test | Structure test | Subgroup check |
|---|---|---|---|---|
| None | 0% | 10% | 3% | 0% |
| Gene levels | **100%** | 3% | 7% | 0% |
| More spread | 0% | **100%** | 3% | 0% |
| Hidden subgroups | 10% | 47% | **100%** | **80%** |
| Rewired genes | 3% | 3% | **97%** | 0% |
| Treatment effect | **100%** | 7% | 3% | 0% |

**Finding:** each test detects its own kind of difference, and the subgroup check separates hidden subgroups from true rewiring.

### 3. Full interferon pipeline (360 patients, 25% IFN-low; 77 controls; AUC)

| Scenario | Leftover IFN score | Gene levels | Gene levels + IFN score | Quadratic classifier | LIONESS links | Gene levels + LIONESS + IFN score |
|---|---|---|---|---|---|---|
| IFN-low: no real difference | **0.69** | 0.55 | 0.66 | 0.53 | 0.49 | 0.59 |
| IFN-low: gene levels differ | 0.69 | 0.67 | **0.75** | 0.63 | 0.51 | 0.67 |
| IFN-low: genes rewired | **0.70** | 0.56 | 0.68 | 0.64 | 0.59 | 0.68 |
| Check: IFN-high vs healthy | **1.00** | 0.76 | **1.00** | 0.73 | 0.51 | 0.99 |

**Findings:**
- The leftover IFN score alone separates IFN-low patients from healthy people (AUC about 0.70), even when nothing else differs. About 120 patients passed the cutoff although only about 90 were truly IFN-low.
- H1: adding LIONESS to gene levels and the IFN score did not help in any scenario, and lowered the score when no structure difference was planted.

### 4. Safeguards

- With no planted difference, every method scored about 0.50 (no fake results).
- A healthy-only LIONESS reference did not create fake separation (AUC 0.50 at 90 vs 77; 0.49 at 40 vs 40), so the balanced reference should be justified as fairer rather than as preventing fake results.
- At 40 vs 40, all scores were lower (e.g. LIONESS on rewired genes 0.62 vs 0.69).

## What this changes in the plan

1. Correct prediction P3: with a balanced reference, networks do not detect level or spread differences.
2. Keep the leftover IFN score as the baseline every model must beat.
3. Re-justify the balanced reference.
4. Report the direct tests as the main way to describe how IFN-low lupus differs.
5. Scale up the full simulation (more genes, plasmode data, more repeats).

## Files

| File | What it does |
|---|---|
| `study.py` | Six planted-difference scenarios; method comparison; safety check of the reference design |
| `tests.py` | Layered direct tests and the hidden-subgroup check |
| `ifn_study.py` | Full IFN-low pipeline with the in-fold interferon cutoff |
| `plot_study.py`, `plot_ifn.py` | Draw the charts |
| `*_results.json`, `*.png` | Saved results and charts |

**To rerun** (needs Python with numpy, scikit-learn and matplotlib), from inside `simulation/`:
```
python3 study.py 30
python3 tests.py
python3 ifn_study.py 30
python3 plot_study.py
python3 plot_ifn.py
```
Results vary slightly between runs because the data are random; the fixed seeds in the scripts make each run repeatable on the same machine.
