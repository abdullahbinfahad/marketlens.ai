"""Evidence-led MarketLens scoring for the Streamlit application.

The engine never substitutes invented defaults. Each component is calculated from
available fields, while confidence reports how much of the evidence contract was observed.
The baseline formula is fixed: Demand 40%, Profit 30%, Risk 20%, Competition Gap 10%.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import math

WEIGHTS = {"demand": 0.40, "profit": 0.30, "risk": 0.20, "competition_gap": 0.10}
VERDICTS = {"GO": 70.0, "CAUTION": 45.0, "PASS": 0.0}


def _number(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _pct(value: Any) -> float | None:
    """Normalize ratio-form values such as 0.78 and percent-form values such as 78."""
    number = _number(value)
    if number is None:
        return None
    if 0 <= number <= 1:
        number *= 100
    return max(0.0, min(100.0, number))


def _cap(value: float) -> float:
    return max(0.0, min(100.0, value))


def _scale(value: Any, upper: float) -> float | None:
    number = _number(value)
    return None if number is None else _cap(number / upper * 100)


def _weighted(parts: list[tuple[Any, float, Any]], missing: list[str]) -> tuple[float, int, int]:
    total_weight = 0.0
    score = 0.0
    observed = 0
    for value, weight, transform in parts:
        number = transform(value) if callable(transform) else _number(value)
        if number is None:
            continue
        score += _cap(number) * weight
        total_weight += weight
        observed += 1
    return (_cap(score / total_weight) if total_weight else 0.0, observed, len(parts))


def calculate_market_score(product: Mapping[str, Any]) -> dict[str, Any]:
    """Calculate a transparent MarketLens result from one normalized product row."""
    missing: list[str] = []

    demand_parts = [
        (product.get("monthly_unit_sales"), 0.22, lambda v: _scale(v, 2000)),
        (product.get("monthly_revenue"), 0.18, lambda v: _scale(v, 50000)),
        (product.get("sales_growth_rate_30d"), 0.18, lambda v: _cap((_number(v) or 0) + 10) * 5 if _number(v) is not None else None),
        (product.get("total_reviews_count"), 0.14, lambda v: _scale(v, 5000)),
        (product.get("average_rating"), 0.14, lambda v: _scale(v, 5)),
        (product.get("positive_review_percent"), 0.14, _pct),
    ]
    profit_margin = product.get("gross_margin_percent")
    if _number(profit_margin) is None and _number(product.get("selling_price_usd")) and _number(product.get("unit_cost_usd")):
        price = _number(product.get("selling_price_usd")) or 0
        cost = _number(product.get("unit_cost_usd")) or 0
        profit_margin = ((price - cost) / price * 100) if price > 0 else None
    contribution_margin = None
    price = _number(product.get("selling_price_usd"))
    cost = _number(product.get("unit_cost_usd"))
    if price and price > 0 and cost is not None:
        fee = (_pct(product.get("platform_fee_percent")) or 0) * price / 100
        shipping = _number(product.get("shipping_cost_per_unit_usd")) or 0
        contribution_margin = (price - cost - fee - shipping) / price * 100
    net_margin = None
    net_profit = _number(product.get("net_profit_per_unit_usd"))
    if net_profit is not None and price and price > 0:
        net_margin = net_profit / price * 100
    ad_efficiency = None
    acos = _pct(product.get("advertising_cost_of_sale"))
    if acos is not None:
        ad_efficiency = 100 - acos
    profit_parts = [
        (profit_margin, 0.22, _pct), (contribution_margin, 0.22, _pct), (net_margin, 0.18, lambda v: None if _number(v) is None else _cap((_number(v) or 0) * 2)),
        (product.get("monthly_revenue"), 0.10, lambda v: _scale(v, 50000)), (ad_efficiency, 0.10, _pct),
        (product.get("advertising_spend_usd"), 0.06, lambda v: (100 - (_number(v) or 0) / (_number(product.get("monthly_revenue")) or 1) * 100) if _number(product.get("monthly_revenue")) else None),
        (product.get("ad_click_through_rate"), 0.06, lambda v: _scale(_pct(v), 5)), (product.get("ad_conversion_rate"), 0.06, lambda v: _scale(_pct(v), 15)),
    ]
    risk_parts = [
        (product.get("market_saturation_score"), 0.28, _pct), (product.get("total_active_sellers"), 0.16, lambda v: _scale(v, 500)),
        (product.get("negative_review_percent"), 0.20, lambda v: None if _pct(v) is None else _cap((_pct(v) or 0) * 2)), (product.get("neutral_review_percent"), 0.08, _pct),
        (product.get("top_3_sellers_market_share_percent"), 0.14, _pct), (acos, 0.14, _pct),
    ]
    rating_gap = None
    rating = _number(product.get("average_rating")); competitor_rating = _number(product.get("average_competitor_rating"))
    if rating is not None and competitor_rating is not None:
        rating_gap = _cap(50 + (rating - competitor_rating) * 25)
    price_gap = _number(product.get("price_gap_vs_average_competitor_percent"))
    needs_gap = 100 if str(product.get("unmet_customer_needs") or "").strip() else 60 if str(product.get("top_customer_pain_points") or "").strip() else None
    sentiment = _pct(product.get("sentiment_score_overall"))
    if sentiment is None:
        sentiment = _pct(product.get("positive_review_percent"))
    competition_parts = [
        (rating_gap, 0.25, _number), (None if price_gap is None else 50 - price_gap, 0.20, _number), (needs_gap, 0.20, _number),
        (sentiment, 0.15, _number), (None if _number(product.get("total_active_sellers")) is None else 100 - (_scale(product.get("total_active_sellers"), 500) or 0), 0.10, _number),
        (product.get("positive_review_percent"), 0.10, _pct),
    ]

    component_parts = {"demand": demand_parts, "profit": profit_parts, "risk": risk_parts, "competition_gap": competition_parts}
    scores: dict[str, float] = {}
    observed_total = 0
    expected_total = 0
    for name, parts in component_parts.items():
        score, observed, expected = _weighted(parts, missing)
        scores[name] = round(score, 2)
        observed_total += observed
        expected_total += expected
        if observed == 0:
            missing.append(name)

    final_score = round(_cap(scores["demand"] * WEIGHTS["demand"] + scores["profit"] * WEIGHTS["profit"] - scores["risk"] * WEIGHTS["risk"] + scores["competition_gap"] * WEIGHTS["competition_gap"]), 2)
    confidence = round(observed_total / expected_total * 100, 2) if expected_total else 0.0
    verdict = "GO" if final_score >= 70 else "CAUTION" if final_score >= 45 else "PASS"
    category = str(product.get("main_category") or "").lower()
    risk_adjustment = 7 if any(term in category for term in ("beauty", "cosmetic", "personal care")) else 6 if any(term in category for term in ("electronics", "computer", "mobile")) else 10 if any(term in category for term in ("food", "beverage", "grocery")) else 4 if any(term in category for term in ("fashion", "apparel", "clothing", "shoes")) else 0
    forecast_score = round(_cap(scores["risk"] + risk_adjustment), 2) if observed_total else None
    forecast_level = "UNKNOWN" if forecast_score is None else "HIGH" if forecast_score >= 75 else "ELEVATED" if forecast_score >= 55 else "MODERATE" if forecast_score >= 30 else "LOW"
    return {
        "scoring_version": "marketlens-streamlit-1.2", "demand_score": scores["demand"], "profit_score": scores["profit"], "risk_score": scores["risk"],
        "competition_gap_score": scores["competition_gap"], "final_market_score": final_score, "confidence_score": confidence, "verdict": verdict,
        "risk_forecast_score": forecast_score, "risk_forecast_level": forecast_level, "category_risk_adjustment": risk_adjustment,
        "observed_metric_count": observed_total, "expected_metric_count": expected_total,
        "missing_evidence": missing, "rationale": f"Fixed weighting: Demand 40%, Profit 30%, Risk 20%, Competition Gap 10%. {expected_total - observed_total} component inputs remain unavailable." if expected_total else "No scoring evidence is available.",
    }


def calculate_all_scores(product: Mapping[str, Any], gap_score_from_ai: float | None = None) -> dict[str, Any]:
    """Backward-compatible wrapper for existing Streamlit callers."""
    row = dict(product)
    if gap_score_from_ai is not None and row.get("sentiment_score_overall") in (None, ""):
        row["sentiment_score_overall"] = gap_score_from_ai
    return calculate_market_score(row)


def get_verdict_explanation(verdict: str, overall_score: float) -> str:
    return {"GO": f"GO — the observed baseline score is {overall_score:.1f}/100; validate suppliers and regulations before committing inventory.", "CAUTION": f"CAUTION — the observed baseline score is {overall_score:.1f}/100; investigate the missing evidence and market risks.", "PASS": f"PASS — the observed baseline score is {overall_score:.1f}/100; current evidence does not support a confident launch decision."}.get(verdict, "Decision unavailable.")
