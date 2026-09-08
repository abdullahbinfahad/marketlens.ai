# MarketLens AI — Public Streamlit Product Intelligence

MarketLens AI is a public, search-first product intelligence tool for cross-border sellers. Visitors can load or connect an authorized catalogue, search any product or category, open a product overview, inspect observed market signals, and receive a transparent **GO / CAUTION / PASS** decision with confidence and provenance.

The main product direction is [marketlens-ai.com](https://marketlens-ai.com/). This repository is the Streamlit implementation and should remain the only codebase used for the Streamlit deployment.

## What the app does

The application follows a simple flow: **Explore → Inspect → Decide**. Search works across product name, SKU, description, brand, category, and sub-category. The product view separates overview data, observed market signals, decision score, and source provenance. A comparison view ranks loaded products without presenting the ranking as a sales guarantee.

The canonical formula is fixed:

> Market Score = Demand × 40% + Profit × 30% − Risk × 20% + Competition Gap × 10%

Verdicts are **GO** for scores of 70 or higher, **CAUTION** for 45–69.99, and **PASS** below 45. Confidence is calculated separately from evidence completeness. Missing data is left unavailable; the app does not generate replacement sales, revenue, review, competitor, or advertising values.

## Data and current-data behavior

The app accepts CSV and XLSX files using the 40-field MarketLens schema. It also supports a refreshable remote source through the `MARKETLENS_DATA_URL` Streamlit secret. A public deployment should connect an authorized source containing provenance, licence information, and update timestamps. The UI reports the loaded source and distinguishes identity-only catalogue rows from products with observed commercial evidence.

The repository includes the user-provided `data/catalogue.xlsx` starter workbook. It is a real 15-row sample, not a fabricated 20,000-row dataset. A 20,000+ catalogue can be connected by replacing it with an authorized `data/catalogue.csv` or `data/catalogue.xlsx`, or by configuring `MARKETLENS_DATA_URL`. Product identity fields alone are not treated as current market evidence.

The uploaded workbook variant with a blank leading column and a shifted header row is supported. Source-provided component scores and verdicts are treated as non-authoritative references; the app recalculates its own score from observed inputs.

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

Create a new app from `abdullahbinfahad/marketlens.ai`, select the `main` branch, and set the main file to `streamlit_app.py`. Add `MARKETLENS_DATA_URL` to Streamlit secrets if the catalogue should load from a refreshable remote CSV or XLSX source. If the source is private, use a secure authenticated data service instead of exposing a credential in the repository.

## Project structure

| File | Purpose |
|---|---|
| `streamlit_app.py` | Public search, product overview, comparison, data-source, and methodology UI |
| `marketlens_data.py` | CSV/XLSX/URL loading, shifted-header repair, schema normalization, search, coverage reporting, and score attachment |
| `algorithms.py` | Evidence-led scoring with fixed 40/30/20/10 weights, ratio normalization, confidence, and verdicts |
| `app.py/streamlit_app.py` | Compatibility wrapper for the alternate Streamlit Cloud path |
| `requirements.txt` | Reproducible runtime and test dependencies |
| `TODO.md` | Project acceptance checklist |
| `docs_reference.md` | Reference-site and judge-guide findings |

## Validation and limitations

The current-data label is only as strong as the connected source. The application can calculate a decision from a loaded workbook, but it cannot truthfully claim live marketplace trends without a refreshable source or API. Supplier verification, regulatory review, shipping validation, advertising cost validation, and real-time marketplace access remain necessary before a commercial launch decision.
