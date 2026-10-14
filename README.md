# MarketLens AI — Public Streamlit Product Intelligence

MarketLens AI is a public, search-first product intelligence tool for cross-border sellers. Visitors search the backend-managed catalogue, inspect a product overview, and receive a transparent **GO / CAUTION / PASS** decision with confidence and provenance.

The main product direction is [marketlens-ai.com](https://marketlens-ai.com/). This repository is the Streamlit implementation for `abdullahbinfahad/marketlens.ai`.

## Product flow

**Search → Inspect → Decide.** Search works across product name, SKU, description, brand, category, and sub-category. A product view separates overview data, observed market signals, decision score, and provenance. Public file uploads are intentionally disabled: catalogue files are loaded by the backend from the repository or from `MARKETLENS_DATA_URL`.

If a search misses the managed catalogue, the app makes a free, bounded lookup against [Open Beauty Facts](https://world.openbeautyfacts.org/). Those fallback records are identity-only unless the API explicitly supplies commercial evidence, so sales, revenue, price, reviews, and competitor fields remain **Unavailable** rather than being invented.

## Scoring contract

The canonical formula is fixed:

> Market Score = Demand × 40% + Profit × 30% − Risk × 20% + Competition Gap × 10%

Verdicts are **GO** for scores of 70 or higher, **CAUTION** for 45–69.99, and **PASS** below 45. Confidence is calculated separately from evidence completeness. Missing data is left unavailable; the app does not generate replacement sales, revenue, review, competitor, or advertising values.

## Data and freshness

The backend accepts CSV and XLSX files using the 40-field MarketLens schema and can read a refreshable remote source through the `MARKETLENS_DATA_URL` Streamlit secret. A production deployment should connect an authorized source containing a source URL, licence/attribution details, and update timestamps. The UI reports the loaded source and distinguishes identity-only catalogue rows from products with observed commercial evidence.

The repository includes `data/catalogue.xlsx` as a small real starter workbook. It is not presented as a 20,000-row live dataset. For 20,000+ records, replace it through the backend-managed repository/data URL path with an authorized catalogue. Do not fabricate rows or treat the free identity fallback as current marketplace performance.

## Run locally

```bash
git clone https://github.com/abdullahbinfahad/marketlens.ai.git
cd marketlens.ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open `http://localhost:8501`. The `app.py/streamlit_app.py` path is retained as a compatibility entry point, but `streamlit_app.py` in the repository root is the recommended Streamlit Cloud entry point.

## Deploy on Streamlit Community Cloud

1. Create a new app from `abdullahbinfahad/marketlens.ai`.
2. Select branch `main` and main file `streamlit_app.py`.
3. Add `MARKETLENS_DATA_URL` to Streamlit Secrets if a refreshable remote CSV/XLSX source should be used.
4. Keep the source authorized, traceable, and licensed. Do not put private credentials in the repository or expose private URLs without an authenticated service.
5. Verify a managed-catalogue search, a no-match Open Beauty Facts fallback search, the Data source page, and the Methodology page.

## Project structure

| File | Purpose |
|---|---|
| `streamlit_app.py` | Search-first UI, product overview, comparison, provenance, and methodology |
| `marketlens_data.py` | Backend catalogue loading, schema normalization, free Open Beauty Facts fallback, search, and coverage reporting |
| `algorithms.py` | Evidence-led scoring with fixed 40/30/20/10 weights, confidence, and verdicts |
| `app.py/streamlit_app.py` | Compatibility wrapper for alternate Streamlit Cloud configurations |
| `data/catalogue.xlsx` | Small real starter workbook; replace through the backend-managed path for a larger catalogue |
| `tests/` | Scoring, calculated-column, and fallback normalization tests |
| `requirements.txt` | Runtime and test dependencies |
| `TODO.md` | Acceptance checklist |

## Validation and limitations

Run:

```bash
pytest -q
python -m py_compile algorithms.py marketlens_data.py streamlit_app.py app.py/streamlit_app.py
```

The current-data label is only as strong as the connected source. The application can calculate a decision from a loaded workbook, but it cannot truthfully claim live marketplace trends without a refreshable source or API. Supplier verification, regulatory review, shipping validation, advertising-cost validation, and real-time marketplace access remain necessary before a commercial launch decision.
