"""Runs the full simulation grid in parallel and appends one JSON line per analysed dataset."""
import json, sys, os, itertools, numpy as np
from multiprocessing import Pool
import simlib as L
SIZES = [10, 20, 30, 50, 60]; REPS = int(os.environ.get("REPS", 50))
OUT = "results.jsonl"

def calib_table():
    path = "calibration.json"
    if os.path.exists(path): return json.load(open(path))
    cal = {}
    for G in SIZES:
        st = L.Structure(G)
        for sc in ["S1", "S2", "S3", "S4"]:
            for c in [0.6, 0.7, 0.8]:
                if c != 0.7 and G != 20: continue
                e, a = L.calibrate(st, sc, c)
                cal[f"{G}|{sc}|{c}"] = [float(e), float(a)]; print("calibrated", G, sc, c, round(e, 3), round(a, 3), flush=True)
    json.dump(cal, open(path, "w"), indent=1); return cal

def tasks(cal):
    T = []
    for sc, G, r in itertools.product(["S0", "S1", "S2", "S3", "S4"], SIZES, range(REPS)):
        T.append(dict(grid="A", scen=sc, G=G, ceil=0.7, n=[90, 77], rep=r, models="main", variant="primary"))
    for sc, (c, n), r in itertools.product(["S0", "S1", "S2", "S3", "S4"], [(0.6, [90, 77]), (0.8, [90, 77]), (0.7, [40, 40])], range(REPS)):
        if sc == "S0" and c == 0.8: continue
        T.append(dict(grid="B", scen=sc, G=20, ceil=c, n=n, rep=r, models="core", variant="primary"))
    for sc, G, r in itertools.product(["S5", "S6"], SIZES, range(REPS)):
        T.append(dict(grid="C", scen=sc, G=G, ceil=None, n=[90, 77], rep=r, models="core", variant="all4"))
    for G, r in itertools.product(SIZES, range(REPS)):
        T.append(dict(grid="C", scen="S7", G=G, ceil=None, n=[90, 77], rep=r, models="core", variant="primary"))
    return T

CAL = None
def work(t):
    seed = abs(hash((t["grid"], t["scen"], t["G"], t["ceil"], tuple(t["n"]), t["rep"]))) % (2**32)
    rng = np.random.default_rng(seed); st = L.Structure(t["G"])
    eff = CAL[f'{t["G"]}|{t["scen"]}|{t["ceil"]}'][0] if t["scen"] in ("S1", "S2", "S3", "S4") else None
    X, I, y, tr = L.generate(st, t["scen"], eff, t["n"][0], t["n"][1], rng)
    out = []
    if t["variant"] == "all4":
        for v in ["none", "cond", "restrict", "both"]:
            cond = v in ("cond", "both"); idx = np.arange(len(y))
            if v in ("restrict", "both"):
                idx = np.where(~tr)[0] if t["scen"] == "S5" else L.match_on_ifn(I, y, rng)
            r = L.analyse(X[idx], I[idx], y[idx], rng, t["models"], cond=cond)
            out.append(dict(t, variant=v, n_used=[int((y[idx] == 1).sum()), int((y[idx] == 0).sum())], **r))
    else:
        r = L.analyse(X, I, y, rng, t["models"], cond=True)
        out.append(dict(t, **r))
    return out

def init(cal):
    global CAL; CAL = cal

if __name__ == "__main__":
    cal = calib_table(); T = tasks(cal)
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            d = json.loads(line); done.add((d["grid"], d["scen"], d["G"], d["ceil"], tuple(d["n"]), d["rep"]))
    T = [t for t in T if (t["grid"], t["scen"], t["G"], t["ceil"], tuple(t["n"]), t["rep"]) not in done]
    print("tasks to run:", len(T), flush=True)
    T.sort(key=lambda t: -t["G"])
    with Pool(4, initializer=init, initargs=(cal,)) as p, open(OUT, "a") as fh:
        for k, res in enumerate(p.imap_unordered(work, T, chunksize=1)):
            for d in res: fh.write(json.dumps(d) + "\n")
            fh.flush()
            if k % 50 == 0: print("done", k, flush=True)
    print("ALL DONE", flush=True)
