# Reference Gap Audit

Flag a citation gap when:

- a paragraph makes a broad field claim without a review or recent primary source,
- a mechanism is inferred without mechanism evidence,
- a test standard is used without naming the standard or precedent,
- a journal scope claim relies on memory,
- all citations are old while the topic is active,
- citations support adjacent materials but not the studied material system.

Suggested risk labels:

- `must-fix`: likely reviewer objection or desk-reject risk,
- `strengthen`: acceptable but thin,
- `optional`: useful for polish or positioning.

## WER-EA Reviewer-Safe Gap Checks

Use `references/wer-ea-screening-and-source-quality.md` before closing a WER-EA citation package.

Flag `must-fix` when:

- a formulation claim lacks `material_formulation` evidence from a directly matched WER-EA or emulsified asphalt system,
- an interface or tack-coat claim lacks `bonding_interface_performance` evidence,
- a mechanism claim relies only on strength or bonding values and lacks `curing_demulsification` or `microstructure_chemistry` evidence,
- a durability claim uses only short-term only bonding, viscosity, or fresh emulsion data,
- a service or field relevance claim lacks `service_field_relevance`, a standard/specification source, or an explicit engineering boundary,
- all mapped sources are `weak background`, `review evidence`, or `method evidence` for a claim that needs primary experimental evidence.

Flag `strengthen` when:

- source quality is still `screening needed`,
- the source has adjacent asphalt/epoxy evidence but not the studied WER-EA system,
- `reader_anchor` is missing for a claim that may enter Results, Discussion, or a review figure,
- `figure_handoff` is marked but the source has not been checked for measured-vs-inferred boundaries.
