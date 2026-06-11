# Figure Contract

## Core Conclusion

Stress-Strain figures must show mechanical response under loading as material-specific and condition-dependent rather than universal.

## Evidence Chain

| Panel | Evidence source | Source anchor | What it supports | Boundary |
|---|---|---|---|---|
| a | source_data.csv | D001 | stress-strain curve | template only |
| b | source_data.csv | D002 | elastic modulus | template only |
| c | source_data.csv | D003 | failure strain | template only |

## Archetype

curve

## Backend

- Selected backend: Python
- Runtime/package status: generated as template-only package
- Backend exclusivity note: all plotting, previews, exports, and QA renders use Python.

## Journal/Export Contract

- Target journal family: CBM/CCC/RMPD/JBE-ready review figure template
- Width: double-column template
- Font size: readable at final size
- Vector formats: SVG, PDF
- Raster formats: PNG, TIFF
- DPI: 300+

## Statistics And Image Integrity

- n definition: not applicable for template-only package
- replicate definition: not applicable for template-only package
- center/spread: not applicable for template-only package
- test/correction: not applicable for template-only package
- image provenance: no raw microscopy image in this package
- scale bars: not applicable
- crop/contrast notes: not applicable

## WER-EA Boundary

- Performance evidence: template only until real source rows are inserted
- Direct mechanism evidence: template only until FTIR/rheology/microscopy anchors are inserted
- Inferred mechanism: must be styled separately from direct evidence
- Durability/service evidence: must remain lab/service-condition specific
- Unsupported or missing evidence: no field-life claim can be made from this template alone

## Reviewer Risk

- Replace template values with source-grounded evidence before manuscript use.
