---
name: civil-materials-response
version: "1.1.0"
stability: stable
description: Use when drafting, auditing, or strengthening point-by-point reviewer response letters for civil engineering and construction materials manuscripts.
---

# Civil Materials Response

Draft reviewer response letters that are complete, factual, and professional.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `response_task`, `comment_type`, and `journal_family`.
3. Load only the matching fragments.
4. Assign stable IDs to each reviewer comment.
5. Classify each comment and draft a point-by-point response.
6. Map action: ACCEPT_TEXT, ACCEPT_ANALYSIS, SOFTEN_CLAIM, or AUTHOR_INPUT_NEEDED.

## Gates

- Never invent data, experiments, or citations.
- Do not fabricate added experiments or supplementary figures.
- Responses must stand alone without the reviewer needing to re-read the manuscript.
