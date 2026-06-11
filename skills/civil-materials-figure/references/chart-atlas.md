# Civil Materials Chart Atlas

Use this atlas when choosing a production figure family before coding. Each chart type links a civil-materials claim to a safe code pattern and a visual reference.

## Chart family index

| Chart family | Best use | Code pattern | Visual reference | Reviewer risk |
|---|---|---|---|---|
| bonding strength grouped bar | Control vs. modified tack coat under dry/wet states | `make_grouped_bar()` with SD bars | `rich-gallery/bonding_performance_matrix.svg`, `wer-ea-atlas/wer_ea_bonding_comparison.svg` | Missing replicate count or test condition |
| dosage-performance curve | Optimization trend across epoxy/modifier dosage | `make_line_trend()` with highlighted candidate range | `rich-gallery/dosage_workability_window.svg`, `wer-ea-atlas/wer_ea_dosage_window.svg` | Calling one dosage "optimal" without durability |
| FTIR overlay | Curing or chemical-change evidence | `make_ftir_overlay()` with peak labels | `rich-gallery/ftir_sem_evidence_pair.svg`, `wer-ea-atlas/wer_ea_ftir_card.svg` | Claiming full mechanism from FTIR alone |
| XRD stacked pattern | Hydration or crystalline phase comparison | `make_xrd_pattern()` with offset traces | `rich-gallery/cement_hydration_evidence.svg` | Unassigned peaks or no baseline correction |
| durability retention bar | Moisture, aging, freeze-thaw screening | Grouped retention bars with raw baseline noted | `rich-gallery/moisture_aging_retention.svg`, `wer-ea-atlas/wer_ea_durability_retention.svg` | Retention without original strength values |
| mechanical radar | Multi-index comparison for screening | `make_radar()` on normalized indices | `wer-ea-atlas/wer_ea_performance_boundary.svg` | Hiding weak raw indicators |
| SEM/fluorescence plate | Morphology and phase distribution | Assembled panel with scale bar | `rich-gallery/ftir_sem_evidence_pair.svg`, `wer-ea-atlas/wer_ea_sem_fluorescence.svg` | Representative image without field count |
| TG/DTG paired plot | Thermal stability and decomposition | Aligned mass-loss and derivative axes | `rich-gallery/cement_hydration_evidence.svg` | Overinterpreting small peak shifts |
| box/violin plot | Replicate-rich performance datasets | Raw points plus distribution shape | (generate with `scripts/civil_materials_plot_svg.py`) | Using distribution plots for n < 5 |
| mechanism schematic | Evidence-chain summary | Solid/dashed arrows by evidence confidence | `rich-gallery/interface_mechanism_map.svg`, `wer-ea-atlas/wer_ea_mechanism_map.svg` | Drawing unsupported causal links |
| evidence heatmap | Literature evidence coverage matrix | Rows=claims, cols=evidence layers, cells=confidence | `wer-ea-atlas/wer_ea_evidence_heatmap.svg`, `review-first/evidence_chain_map.svg` | Treating empty cells as "no evidence" vs "not searched" |
| research gap matrix | Gap identification for review papers | Rows=topics, cols=study counts, color=coverage | `wer-ea-atlas/wer_ea_research_gap.svg`, `review-first/research_gap_matrix.svg` | Confusing "few studies" with "no studies" |
| graphical abstract | Visual summary for journal submission | Schematic workflow with key result callout | `rich-gallery/lca_boundary_card.svg`, `wer-ea-atlas/wer_ea_graphical_abstract.svg` | Overclaiming in the visual summary |
| pavement layer diagram | Interface/tack coat positioning | Cross-section schematic with test locations | `rich-gallery/pavement_layer_tackcoat.svg` | Missing test location specification |

## Visual asset locations

- `assets/rich-gallery/generated/` — 10 general civil materials figures (SVG)
- `assets/wer-ea-atlas/generated/` — 20 WER-EA specific figures (SVG + PNG)
- `assets/review-first/generated/` — 10 review-oriented figures (SVG)
- `assets/showcase-proof/` — 4 proof board PNGs

## Usage rules

Start with the claim, then choose the chart. Do not start with the prettiest chart and retrofit a claim.

- Keep performance figures separate from mechanism figures unless both measurements exist.
- Do not use a mechanism schematic as proof of chemical reaction.
- Do not infer durability from short-term bonding strength.
- For waterborne epoxy modified emulsified asphalt, separate emulsion stability, epoxy curing, interface bonding, viscosity, storage stability, and moisture/aging evidence.
- Put control, dosage, temperature, curing condition, and test standard in the figure plan or caption when available.
