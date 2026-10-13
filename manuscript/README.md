# Manuscript

Working drafts of paper 2 (single-sample networks in interferon-low SLE). Nothing has been analysed yet; results are placeholders.

- `draft_v3_intro_methods.md`: Title, Key Points, Abstract, Introduction and Methods, plus draft Table 1, Supplementary Appendix A (derivations), Supplementary Sections S2 and S4, Supplementary Tables S2 and S3, and the reference list.
- `references.md`: the 43 references in citation order, with verification status and where each is cited.
- `checks/`: small Python scripts behind the numerical claims in the draft (needs `numpy`; the heterogeneity check also needs `scikit-learn`):
  - `ssn_lioness_equivalence.py`: SSN equals (LIONESS − reference)/(n + 1) exactly (Result 3).
  - `layer3_structure_test.py`: false-positive rate of the layer-3 structure test under no difference, spread-only differences and hidden subgroups (Section 2.12).
  - `heterogeneity_check.py`: how often the mixture-model check flags null, subgroup and rewiring scenarios (Section 2.12).
- The Appendix A checks for equations (1)–(2) are in `../reviews/2026-10-06_appendixA_checks.py`.

Before submission: confirm the † settings with Tyler, verify the references marked "To verify", read P-SSN, SWEET and BONOBO in full, and fill in the go/no-go counts.
