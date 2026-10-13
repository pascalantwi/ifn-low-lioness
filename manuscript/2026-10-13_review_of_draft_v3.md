# Review of manuscript draft v3 (Introduction to Methods)

**Date:** 2026-10-13
**Draft reviewed:** `manuscript/draft_v3_intro_methods.md`
**Note:** NCBI and PubMed could not be reached; novelty checks used web search only. Claims marked *(unverified)* need checking.

---

## 1. Verdict

The Introduction and Methods are clear, logical and careful. The design (leakage control, confounder baselines, simulation, layered tests) is stronger than most papers in this area. But **the draft overclaims novelty in two places**, and a reviewer would catch both. Once these are corrected, the paper's honest contribution is moderate: a theory of what partial-correlation single-sample networks measure, plus a rigorous evaluation. That is enough for a good methods journal if the theory is correct and the predictions are tested.

## 2. Novelty: what is new and what is already known

| Part | Status | Action |
|---|---|---|
| LIONESS with partial correlation as a method | **Already known.** P-SSN (Huang 2021, *Brief Bioinform*) computes the change in partial correlation when a sample is added to a reference; by Result 3 this is a rescaled LIONESS-partial. | Do not claim as new. |
| SSN is a rescaled LIONESS (Result 3) | **Known empirically.** Deschildre 2024 [24] reported an almost perfect linear relationship, and the 2026 review [20] states the edge weights are perfectly correlated, differing only in magnitude. | Cite both. Present our part as the exact proof, valid for any association measure. |
| Pearson first-order formula, eq. (3) | **Already known** (Liu 2016 [15]). | Cite only. |
| Partial-correlation first-order formula, eq. (1) | **Probably new** (not found). | Keep as a main contribution. |
| Shrinkage first-order formula, eq. (2) | **Probably new** (not found). | Keep as a main contribution. |
| Predictions P2 (link to a quadratic classifier) and P4 (opposite signs for partial and Pearson) | **Probably new** (not found). | Lead with these. |
| Exact shrinkage implementation; symmetric, class-balanced reference | Modest novelty. | Present as design contributions. |
| Mechanism-matched baselines; layered tests with heterogeneity check | Partly new; differential-network testing itself exists [26]. | Present as an evaluation framework. |
| Single-sample networks in SLE; classifier results for IFN-low SLE | New application (none found). | Mention, but it cannot carry a BiB paper alone. |

"Probably new" means nothing was found in web searches; a full PubMed/arXiv search is still required.

## 3. Must fix

1. **Contribution 1 (Section 1.5).** Remove the claim that LIONESS with partial correlation was "not described previously". State that P-SSN already provides partial-correlation single-sample networks, and that we add an exact shrinkage implementation with a symmetric, balanced reference.
2. **Result 3 (Section 2.6) and Section 1.2.** Cite [20] and [24] for the observed SSN–LIONESS relationship. Describe Result 3 as the exact explanation, not as a new finding.
3. **Lead contribution.** Reorder Section 1.5, the Key Points and the Abstract so that the partial-correlation and shrinkage theory (eqs. 1–2, P2, P4) comes first.
4. **Confirm definitions.** Read P-SSN and SWEET in full and replace the [TBD] notes in Section 2.6 and Supplementary A.9 with their exact definitions.
5. **Check the theory.** Equation (2), Result 3 and predictions P1–P6 must be checked by Tyler or a statistician before submission.
6. **Verify references.** 18 of 43 references are marked "To verify" in `references.md`.

## 4. Should fix

1. **Strengthen the theory so it is clearly new.** For example, derive when topology features can outperform the quadratic baseline, or give a bound on the first-order approximation error.
2. **Settle the † defaults** (Supplementary Table S3) with Tyler before the stage 1 registration.
3. **Clinical check.** A rheumatologist should confirm the SLEDAI and lupus nephritis definitions (contrasts C4 and C5).
4. **Complete Table 1** after the go/no-go check.

## 5. Next steps, in order

1. Read P-SSN, SWEET and BONOBO in full.
2. Correct contribution 1, Result 3 and the order of contributions (items 1–3 above).
3. Ask Tyler to check Supplementary Appendix A and the † settings.
4. Run a full literature search for prior first-order or quadratic analyses of single-sample networks.
5. Verify the remaining references on NCBI.
