# Companion Modules

`materials-research` is the strategic router. Use companion skills for production-heavy work.

| Need | Companion skill | Use when |
|---|---|---|
| Full paper reading | `materials-reader` | reading PDFs, pasted papers, DOI/HTML, evidence-chain audits, literature matrices, journal-club notes |
| Literature search and citation mapping | `materials-citation` | building search strategies, citation matrices, reference gap audits, claim-source maps |
| From-scratch manuscript drafting | `materials-writing` | paper argument chains, abstracts, introductions, results/discussion drafting, review-paper outlines |
| English polishing | `materials-polishing` | polishing abstracts, introductions, results/discussions, cover letters, Chinese-to-English text, claim-strength audits |
| Reviewer response | `materials-response` | major/minor revision responses, rebuttal letters, response tables, revision summaries |
| Simulated peer review | `materials-reviewer` | referee-style reports, pre-submission reviewer-risk audits, two-reviewer simulations, cross-review synthesis |
| PPT outlines and slide logic | `materials-paper2ppt` | group meeting decks, journal-club slides, thesis/project reports, review talks, slide-ready Markdown |
| Real PPTX generation | `materials-pptx` | one-click `.pptx` generation, Markdown/JSON-to-PPTX conversion, PowerPoint deck scaffolds |
| Figures | `materials-figure` | figure plans, SVG plots, figure packages, data-to-caption work |
| Data and FAIR | `materials-data` | raw/processed data organization, metadata, FAIR audits, dataset packages, data availability statements |

Routing rule:

1. Use `materials-research` first when the user needs topic strategy, evidence-chain judgment, journal targeting, or experiment design.
2. Use a companion skill when the output format is already clear.
3. Return to `materials-research` for final reviewer-risk audit before submission.

Preferred handoff sequence for a full manuscript cycle:

1. `materials-reader` for source notes.
2. `materials-citation` for claim-source mapping.
3. `materials-writing` for argument chain and first complete draft.
4. `materials-research` for manuscript logic and journal fit.
5. `materials-polishing` for English.
6. `materials-data` for FAIR packaging and data availability statements.
7. `materials-figure` and `materials-pptx` for visual outputs.
8. `materials-reviewer` for simulated peer review before submission.
9. `materials-response` after peer review.
