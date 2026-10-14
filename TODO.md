# MarketLens Streamlit TODO

- [x] Diagnose and fix the current Streamlit startup/runtime failure.
- [x] Inspect marketlens-ai.com as the main product direction and record compatible UX decisions.
- [x] Keep catalogue data backend-managed; remove the public file-upload control.
- [x] Provide a non-fabricated 20,000+ catalogue loading path through an authorized backend source or `MARKETLENS_DATA_URL`.
- [x] Add a bounded free Open Beauty Facts fallback for identity search misses.
- [x] Implement a modern public search experience for product/category queries with clear product overview and current-data status.
- [x] Implement transparent Demand 40%, Profit 30%, Risk 20%, Competition Gap 10% scoring with GO, CAUTION, and PASS verdicts.
- [x] Add safe missing-data handling, provenance, source timestamps, trend recency, and exportable search results.
- [x] Ensure source-supplied scores are reference-only and the displayed score is recalculated into `calculated_final_market_score`.
- [x] Simplify Streamlit navigation and responsive presentation for public visitors.
- [x] Add regression tests for the calculated score column and Open Beauty Facts normalization.
- [x] Test locally, verify Streamlit deployment configuration, and push the repaired release to GitHub.

## Release note

The repository starter workbook is a small real sample. It must not be described as a live 20,000+ marketplace dataset. For public launch, connect an authorized, refreshable 20,000+ source through the backend-managed repository or `MARKETLENS_DATA_URL`, preserve source/licence metadata, and verify freshness in the Data source view.
