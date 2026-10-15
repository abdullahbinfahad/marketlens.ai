# MarketLens AI — Live Product Intelligence

MarketLens AI is a search-first product intelligence dashboard built around five layers:

1. **Live Product APIs** — DummyJSON, Fake Store API, and Open Beauty Facts work without paid credentials. Optional eBay Browse, Keepa, and Shopify connectors are included for authorized accounts.
2. **API Integration and Normalization** — provider adapters fetch independently, isolate failures, deduplicate overlapping products, preserve provider evidence, and map results into one canonical scoring schema.
3. **AI Analytics Engine** — deterministic sentiment, trend, risk, and confidence analysis always works locally. Optional DeepSeek JSON analysis activates with `DEEPSEEK_API_KEY`; the app never invents unavailable evidence.
4. **MarketLens Dashboard** — live search, provider health, comparison maps, source evidence, and profitability simulations.
5. **Product Decision Support** — fixed Demand 40%, Profit 30%, Risk 20%, Competition Gap 10% scoring with GO, CAUTION, and PASS outcomes.

## Decision model

```text
MarketScore = Demand × 0.40 + Profit × 0.30 − Risk × 0.20 + CompetitionGap × 0.10
```

- **GO:** 70 or higher
- **CAUTION:** 45–69.99
- **PASS:** below 45

Confidence is separate from the score. Provider fields are observed evidence; missing sales, revenue, advertising, competitor, or margin values remain unavailable.

## Provider matrix

| Provider | Default | Role | Limitation |
|---|---:|---|---|
| DummyJSON | Yes | Free product search and prototype integration | Sample data, not market intelligence |
| Fake Store API | Yes | Free catalogue, price, rating, and review-count integration | Sample data, not live marketplace data |
| Open Beauty Facts | Yes | Free beauty identity and ingredient discovery | Mostly identity/ingredient evidence |
| eBay Browse API | Optional | Authorized live marketplace listings and prices | Requires OAuth token and eBay access |
| Keepa API | Optional | Amazon history and sales-rank analysis | Requires Keepa key and plan-specific contract |
| Shopify Storefront API | Optional | Data from a permitted participating store | Requires store endpoint and token |
| DeepSeek | Optional | AI-generated trend/risk summary and next steps | Requires API key; deterministic fallback remains available |

## Optional Streamlit Secrets

```toml
DEEPSEEK_API_KEY = "..."
DEEPSEEK_MODEL = "deepseek-chat"
EBAY_OAUTH_TOKEN = "..."
KEEPA_API_KEY = "..."
SHOPIFY_STOREFRONT_URL = "https://your-store.myshopify.com/api/2025-01/graphql.json"
SHOPIFY_STOREFRONT_TOKEN = "..."
```

Never commit these values. Free providers work with no secrets.

## Run locally

```bash
git clone https://github.com/abdullahbinfahad/marketlens.ai.git
cd marketlens.ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open `http://localhost:8501` and use **Live search**. Select the free providers in the sidebar, search a broad term such as `phone`, `laptop`, or `shampoo`, and open a normalized product record.

## Deploy on Streamlit Community Cloud

Create an app from `abdullahbinfahad/marketlens.ai`, branch `main`, with `streamlit_app.py` as the main file. Add only the optional secrets you are authorized to use. The app does not require paid credentials for its default live providers.

The repository also retains a backend-managed starter workbook for the catalogue route. It is not presented as current marketplace intelligence. Live provider results are the primary path in the rebuilt application.

## Validation

```bash
pytest -q
python -m py_compile algorithms.py marketlens_data.py marketlens_providers.py marketlens_ai.py marketlens_simulation.py streamlit_app.py app.py/streamlit_app.py
```

The test suite covers fixed scoring, provider deduplication, canonical normalization, fallback AI analytics, and profitability simulations. Live API smoke checks should use broad provider-native terms and can return zero results for unsupported phrases without indicating an application failure.
