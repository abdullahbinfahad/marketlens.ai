"""Data loading and normalization for the public MarketLens Streamlit app."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from algorithms import calculate_market_score

ROOT = Path(__file__).resolve().parent
CANONICAL_COLUMNS = [
    "product_id", "product_sku", "product_name", "product_description", "main_category", "sub_category", "brand", "target_platform", "target_region", "target_country", "currency",
    "monthly_unit_sales", "monthly_revenue", "sales_growth_rate_30d", "average_rating", "total_reviews_count", "unit_cost_usd", "selling_price_usd", "gross_margin_percent", "platform_fee_percent", "shipping_cost_per_unit_usd", "net_profit_per_unit_usd",
    "positive_review_percent", "negative_review_percent", "neutral_review_percent", "sentiment_score_overall", "top_customer_pain_points", "unmet_customer_needs", "total_active_sellers", "market_saturation_score", "top_3_sellers_market_share_percent", "average_competitor_rating", "price_gap_vs_average_competitor_percent",
    "demand_score", "profit_score", "risk_score", "competition_gap_score", "final_market_score", "product_verdict", "last_updated_timestamp",
]
NUMERIC_COLUMNS = [column for column in CANONICAL_COLUMNS if column not in {"product_id", "product_sku", "product_name", "product_description", "main_category", "sub_category", "brand", "target_platform", "target_region", "target_country", "currency", "top_customer_pain_points", "unmet_customer_needs", "product_verdict", "last_updated_timestamp"}]
REFERENCE_SCORE_COLUMNS = {"demand_score", "profit_score", "risk_score", "competition_gap_score", "final_market_score", "product_verdict"}


def _normalize_column(value: Any) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def _read_bytes(payload: bytes, name: str) -> pd.DataFrame:
    suffix = Path(name).suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        raw = pd.read_excel(BytesIO(payload), sheet_name=0, header=None)
        return _detect_header(raw)
    return pd.read_csv(BytesIO(payload))


def _detect_header(raw: pd.DataFrame) -> pd.DataFrame:
    """Detect the real header row in workbooks with a blank leading column."""
    for index in range(min(len(raw), 12)):
        values = {_normalize_column(value) for value in raw.iloc[index].tolist()}
        if "product_sku" in values and ("product_id" in values or "product_name" in values):
            frame = raw.iloc[index + 1:].copy()
            frame.columns = [str(value).strip() for value in raw.iloc[index].tolist()]
            return frame.reset_index(drop=True)
    return raw


def _repair_shifted_headers(frame: pd.DataFrame) -> pd.DataFrame:
    columns = [_normalize_column(column) for column in frame.columns]
    frame = frame.copy()
    frame.columns = columns
    if "product_name" not in columns and "product_id" in columns and columns and columns[0] in {"", "nan", "__empty"}:
        leading = frame.columns[0]
        frame["__canonical_product_id"] = frame[leading]
        frame["__canonical_product_name"] = frame["product_id"]
        frame["product_id"] = frame["__canonical_product_id"]
        frame["product_name"] = frame["__canonical_product_name"]
    aliases = {"sku": "product_sku", "name": "product_name", "description": "product_description", "category": "main_category", "productid": "product_id", "productname": "product_name"}
    frame = frame.rename(columns={column: aliases.get(column, column) for column in frame.columns})
    return frame


def normalize_catalogue(frame: pd.DataFrame, source_label: str, source_url: str | None = None) -> pd.DataFrame:
    frame = _repair_shifted_headers(frame)
    for column in CANONICAL_COLUMNS:
        if column not in frame.columns:
            frame[column] = pd.NA
    frame = frame[CANONICAL_COLUMNS].copy()
    for column in NUMERIC_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["product_id"] = frame["product_id"].astype("string").str.strip()
    frame["product_sku"] = frame["product_sku"].astype("string").str.strip()
    frame["product_name"] = frame["product_name"].astype("string").str.strip()
    frame = frame[frame["product_id"].notna() & frame["product_name"].notna()].drop_duplicates("product_id").reset_index(drop=True)
    frame.attrs["source_label"] = source_label
    frame.attrs["source_url"] = source_url or ""
    frame.attrs["loaded_at"] = pd.Timestamp.utcnow().isoformat()
    return frame


def _empty(source_label: str, message: str) -> pd.DataFrame:
    frame = pd.DataFrame(columns=CANONICAL_COLUMNS)
    frame.attrs["source_label"] = source_label
    frame.attrs["message"] = message
    frame.attrs["loaded_at"] = pd.Timestamp.utcnow().isoformat()
    return frame


@__import__("streamlit").cache_data(show_spinner=False)
def load_catalogue(uploaded_bytes: bytes | None = None, uploaded_name: str = "", data_url: str = "") -> pd.DataFrame:
    if uploaded_bytes:
        return normalize_catalogue(_read_bytes(uploaded_bytes, uploaded_name), f"Uploaded: {uploaded_name}")
    if data_url:
        response = requests.get(data_url, timeout=30)
        response.raise_for_status()
        return normalize_catalogue(_read_bytes(response.content, data_url), f"Remote catalogue: {data_url}", data_url)
    for path in (ROOT / "data" / "catalogue.csv", ROOT / "data" / "catalogue.xlsx", ROOT / "data" / "products.csv"):
        if path.exists():
            return normalize_catalogue(_read_bytes(path.read_bytes(), path.name), f"Repository file: {path.name}")
    return _empty("No catalogue loaded", "Upload a CSV/XLSX or configure MARKETLENS_DATA_URL to enable public search.")


def add_calculated_scores(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame.copy()
    scored = frame.copy()
    results = scored.apply(lambda row: calculate_market_score(row.to_dict()), axis=1, result_type="expand")
    for source, target in (("demand_score", "calculated_demand_score"), ("profit_score", "calculated_profit_score"), ("risk_score", "calculated_risk_score"), ("competition_gap_score", "calculated_competition_gap_score"), ("final_market_score", "calculated_final_market_score"), ("verdict", "calculated_product_verdict"), ("confidence_score", "evidence_confidence"), ("risk_forecast_level", "risk_forecast_level")):
        scored[target] = results[source]
    scored.attrs = frame.attrs.copy()
    return scored


def search_catalogue(frame: pd.DataFrame, query: str = "", category: str = "All categories", verdict: str = "All verdicts", limit: int = 50) -> pd.DataFrame:
    result = frame
    if query.strip():
        term = query.strip().lower()
        searchable = result[["product_name", "product_sku", "product_description", "brand", "main_category", "sub_category"]].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
        result = result[searchable.str.contains(term, regex=False)]
    if category != "All categories":
        result = result[result["main_category"].fillna("") == category]
    if verdict != "All verdicts" and "calculated_product_verdict" in result:
        result = result[result["calculated_product_verdict"] == verdict]
    return result.head(limit)


def coverage_summary(frame: pd.DataFrame) -> dict[str, Any]:
    total = len(frame)
    evidence_columns = ["monthly_unit_sales", "monthly_revenue", "unit_cost_usd", "selling_price_usd", "average_rating", "total_reviews_count", "total_active_sellers"]
    observed_rows = int(frame[evidence_columns].notna().any(axis=1).sum()) if total else 0
    complete_rows = int(frame[evidence_columns].notna().all(axis=1).sum()) if total else 0
    return {"total_records": total, "records_with_observed_evidence": observed_rows, "records_with_complete_core_evidence": complete_rows, "coverage_percent": round(observed_rows / total * 100, 2) if total else 0.0, "source_label": frame.attrs.get("source_label", "Unknown source"), "source_url": frame.attrs.get("source_url", ""), "loaded_at": frame.attrs.get("loaded_at", "")}
