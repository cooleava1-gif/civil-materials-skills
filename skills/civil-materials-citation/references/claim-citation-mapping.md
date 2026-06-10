# Claim-Citation Mapping

Map citations by claim type.

| Claim type | Strong evidence | Weak evidence |
|---|---|---|
| Novelty | recent reviews plus directly related studies | uncited "few studies" statements |
| Mechanism | FTIR, SEM, fluorescence, rheology, hydration, microstructure | performance-only speculation |
| Performance | test matrix with controls and statistics | single value without repeatability |
| Durability | aging, moisture, freeze-thaw, service condition tests | short-term strength only |
| Engineering use | standard tests, constructability, cost or feasibility | lab mechanism with no application boundary |

For waterborne epoxy modified emulsified asphalt, keep citations for demulsification, epoxy curing, asphalt-resin compatibility, interface bonding, storage stability, viscosity, and moisture durability in separate rows.

## Citation Matrix Fields

For WER-EA and review-package work, use `assets/templates/citation-matrix-template.csv` and fill these screening fields before treating a source as reviewer-safe:

- `claim_id`: stable claim key such as `CIT-001`.
- `evidence_layer`: one WER-EA layer from `references/wer-ea-screening-and-source-quality.md`.
- `source_role`: `primary experimental evidence`, `review evidence`, `method evidence`, `standard/specification`, or `weak background`.
- `source_quality`: `high`, `medium`, `low`, or `screening needed`.
- `mechanism_directness`: whether mechanism support is direct, inferred, absent, or not applicable.
- `durability_relevance`: whether durability support is direct, adjacent, absent, or not applicable.
- `service_relevance`: whether service/field relevance is direct, lab-scale only, adjacent, or absent.
- `reader_anchor`: page, table, figure, DOI, or note anchor produced by `civil-materials-reader`.
- `figure_handoff`: panel or evidence row that can feed `civil-materials-figure`, or `not assessed`.
- `reviewer_risk`: `must-fix`, `strengthen`, or `optional`.

Do not upgrade a weak background source into a core mechanism, durability, or service claim. If the matrix row still says `screening needed`, send it to reader before using it in manuscript prose.
