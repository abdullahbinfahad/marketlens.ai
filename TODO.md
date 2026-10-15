# MarketLens AI — Rebuild Checklist

- [x] Replace the single-source search flow with a five-layer live product intelligence architecture.
- [x] Add free DummyJSON, Fake Store API, and Open Beauty Facts adapters.
- [x] Add optional eBay Browse, Keepa, and Shopify connector boundaries without requiring credentials for local use.
- [x] Add concurrent provider fetching with independent failure isolation and provider health states.
- [x] Normalize and deduplicate heterogeneous provider records into the canonical MarketLens schema.
- [x] Preserve provider IDs, provider lists, source URLs, observed fields, and timestamps for provenance.
- [x] Keep the fixed Demand 40%, Profit 30%, Risk 20%, Competition Gap 10% scoring contract.
- [x] Add deterministic sentiment, trend, confidence, and risk analysis that works without a paid AI key.
- [x] Add optional DeepSeek JSON analysis through an environment-secret API key.
- [x] Add comparison visualization and profitability sensitivity simulations.
- [x] Add GO, CAUTION, and PASS decision support with transparent unavailable-data messaging.
- [x] Add unit tests for provider merging, normalization, analytics fallback, and simulation arithmetic.
- [ ] Configure authorized production credentials for eBay/Keepa/Shopify if real marketplace evidence is required.
- [ ] Complete a Streamlit Community Cloud browser walkthrough after deployment.
