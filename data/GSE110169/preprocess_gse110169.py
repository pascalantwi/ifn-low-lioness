"""Pre-process GSE110169 (SLE, RA and healthy whole blood; Affymetrix HG-U219, GPL13667).

Input  (raw/):  GSE110169_series_matrix.txt.gz  - submitter RMA-normalized log2 data + sample information
                GPL13667-15572.zip              - GEO platform table (probe ID -> gene symbol)
Output (processed/):
    samples.tsv                 one row per sample: GEO ID, group, batch, glucocorticoids, reported and inferred sex
    probe_annotation.tsv        probe ID -> gene symbol, chromosome location, Entrez ID
    expression_probes.tsv.gz    log2 expression, probes (rows) x samples (columns), probes with one gene symbol only

Steps that depend on the training fold (collapsing probes to genes by highest variance, winsorizing,
IFN score and cutoff) are NOT done here; they are done inside cross-validation (Sections 2.2-2.3).
Run from the repository root:  python3 data/GSE110169/preprocess_gse110169.py
"""
import gzip, io, os, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "processed")
os.makedirs(OUT, exist_ok=True)

# ---- 1. sample information and expression matrix from the series matrix ----
meta, lines = {}, []
with gzip.open(os.path.join(RAW, "GSE110169_series_matrix.txt.gz"), "rt") as f:
    in_table = False
    for line in f:
        if line.startswith("!series_matrix_table_begin"):
            in_table = True; continue
        if line.startswith("!series_matrix_table_end"):
            break
        if in_table:
            lines.append(line); continue
        if line.startswith("!Sample_"):
            parts = [p.strip().strip('"') for p in line.rstrip("\n").split("\t")]
            key, vals = parts[0][8:], parts[1:]
            if key == "characteristics_ch1":
                key = vals[0].split(":")[0].strip()
                vals = [v.split(":", 1)[1].strip() if ":" in v else v for v in vals]
            meta.setdefault(key, vals)

expr = pd.read_csv(io.StringIO("".join(lines)), sep="\t", index_col=0)
expr.index = expr.index.astype(str)

samples = pd.DataFrame({
    "geo_accession": meta["geo_accession"],
    "title": meta["title"],
    "group": pd.Series(meta["disease"]).replace({"Normal": "HC"}).values,
    "batch": meta["batch"],
    "glucocorticoids": pd.Series(meta["glucocorticoids"]).replace({"NA": np.nan}).values,
    "sex_reported": pd.Series(meta["Sex"]).replace({"N/A": np.nan}).values,
})
assert list(samples.geo_accession) == list(expr.columns)

# ---- 2. probe annotation from the platform table ----
with zipfile.ZipFile(os.path.join(RAW, "GPL13667-15572.zip")) as z:
    name = [n for n in z.namelist() if n.endswith(".txt")][0]
    with z.open(name) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
        ann = pd.read_csv(text, sep="\t", comment="#", dtype=str,
                          usecols=["ID", "Gene Symbol", "Chromosomal Location", "Entrez Gene"])
ann.columns = ["probe_id", "gene_symbol", "chromosome_location", "entrez_id"]
ann = ann.set_index("probe_id")
ann["gene_symbol"] = ann["gene_symbol"].fillna("").str.strip()
# keep probes that map to exactly one gene ("A /// B" = several genes; "" or "---" = none)
one_gene = (ann.gene_symbol != "") & (ann.gene_symbol != "---") & (~ann.gene_symbol.str.contains("///"))
ann = ann[one_gene]
keep = expr.index.intersection(ann.index)
expr = expr.loc[keep]
ann = ann.loc[keep]

# ---- 3. inferred sex from Y-chromosome genes (Section 2.4) ----
Y_GENES = ["RPS4Y1", "DDX3Y", "KDM5D", "UTY", "EIF1AY"]
yprobes = ann.index[ann.gene_symbol.isin(Y_GENES)]
yz = expr.loc[yprobes]
yz = yz.sub(yz.mean(axis=1), axis=0).div(yz.std(axis=1), axis=0)
yscore = yz.mean(axis=0).values
# two-group split of the Y score (1-D k-means), M = high-Y group
c = np.array([yscore.min(), yscore.max()])
for _ in range(100):
    lab = np.abs(yscore[:, None] - c[None, :]).argmin(axis=1)
    c = np.array([yscore[lab == k].mean() for k in (0, 1)])
samples["y_score"] = np.round(yscore, 3)
samples["sex_inferred"] = np.where(lab == 1, "M", "F")
samples["sex_agrees"] = np.where(samples.sex_reported.isna(), np.nan,
                                 samples.sex_reported == samples.sex_inferred)

# ---- 4. write outputs ----
samples.to_csv(os.path.join(OUT, "samples.tsv"), sep="\t", index=False)
ann.to_csv(os.path.join(OUT, "probe_annotation.tsv"), sep="\t")
with gzip.open(os.path.join(OUT, "expression_probes.tsv.gz"), "wt", compresslevel=9) as f:
    expr.round(4).to_csv(f, sep="\t")

print("samples:", len(samples), "| probes kept:", expr.shape[0], "| genes:", ann.gene_symbol.nunique())
print("missing expression values:", int(expr.isna().sum().sum()),
      "| range: %.2f to %.2f" % (expr.min().min(), expr.max().max()))
print("Y-gene probes used:", len(yprobes))
