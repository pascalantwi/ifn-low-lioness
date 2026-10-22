# GSE110169 — SLE, RA and healthy whole blood

Source: GEO [GSE110169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110169) (PMID 29534336), platform
[GPL13667](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL13667) (Affymetrix HG-U219).
Whole blood in PAXgene tubes; RMA-normalized log2 values supplied by the submitters; no batch correction.

## Folders

- `raw/` — files downloaded from GEO, unchanged: `GSE110169_series_matrix.txt.gz`, `GPL13667-15572.zip`
- `processed/` — output of `preprocess_gse110169.py`
- `preprocess_gse110169.py` — run from the repository root: `python3 data/GSE110169/preprocess_gse110169.py`

## processed/samples.tsv (243 rows, one per sample)

| Variable | Meaning | Values |
|---|---|---|
| `geo_accession` | GEO sample ID; matches the columns of the expression file | GSM2981057 … |
| `title` | array ID given by the submitters | |
| `group` | diagnosis | SLE 82, RA 84, HC (healthy control) 77 |
| `batch` | RNA extraction / array batch | batch1 64, batch2 77, batch3 59, batch4 43 |
| `glucocorticoids` | glucocorticoid use | TRUE 72, FALSE 89, missing 82 (76 of them HC) |
| `sex_reported` | sex given by the submitters | F 188, M 50, missing 5 |
| `y_score` | mean standardized expression of Y-chromosome genes (RPS4Y1, DDX3Y, KDM5D, UTY, EIF1AY) | |
| `sex_inferred` | sex inferred from `y_score` (Section 2.4) | F 192, M 51 |
| `sex_agrees` | reported sex = inferred sex (1 = yes; empty if sex not reported) | agrees in all 238 with reported sex |

## processed/probe_annotation.tsv

`probe_id`, `gene_symbol`, `chromosome_location`, `entrez_id` from the GEO platform table.
Only probes that map to exactly one gene symbol are kept (47,320 probes, 19,040 genes).

## processed/expression_probes.tsv.gz

log2 expression, 47,320 probes (rows) × 243 samples (columns), no missing values.
Probes are not yet collapsed to genes: collapsing (highest-variance probe), winsorizing and the IFN score and cutoff
depend on the training fold and are done inside cross-validation (Sections 2.2–2.3 of the manuscript).
