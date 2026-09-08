import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from algorithms import calculate_market_score


def test_fixed_weights_and_verdict_contract():
    result = calculate_market_score({
        "monthly_unit_sales": 2000, "monthly_revenue": 50000, "sales_growth_rate_30d": 10,
        "average_rating": 5, "total_reviews_count": 5000, "positive_review_percent": 90,
        "gross_margin_percent": 80, "unit_cost_usd": 20, "selling_price_usd": 100,
        "platform_fee_percent": 15, "shipping_cost_per_unit_usd": 5, "net_profit_per_unit_usd": 40,
        "advertising_cost_of_sale": 10, "advertising_spend_usd": 2000, "ad_click_through_rate": 2.5, "ad_conversion_rate": 8,
        "market_saturation_score": 30, "total_active_sellers": 100, "negative_review_percent": 5,
        "neutral_review_percent": 5, "top_3_sellers_market_share_percent": 20,
        "average_competitor_rating": 4, "price_gap_vs_average_competitor_percent": -10,
        "unmet_customer_needs": "Longer battery life", "sentiment_score_overall": 90,
    })
    expected = result["demand_score"] * 0.40 + result["profit_score"] * 0.30 - result["risk_score"] * 0.20 + result["competition_gap_score"] * 0.10
    assert result["final_market_score"] == round(expected, 2)
    assert result["confidence_score"] == 100.0
    assert result["verdict"] in {"GO", "CAUTION", "PASS"}


def test_missing_evidence_is_not_invented():
    result = calculate_market_score({"product_name": "Unknown product"})
    assert result["final_market_score"] == 0.0
    assert result["confidence_score"] == 0.0
    assert result["verdict"] == "PASS"
    assert result["risk_forecast_level"] == "UNKNOWN"


def test_ratio_and_percent_inputs_are_equivalent():
    ratio = calculate_market_score({"market_saturation_score": 0.65, "negative_review_percent": 0.18, "neutral_review_percent": 0.09, "sentiment_score_overall": 0.78, "positive_review_percent": 0.73})
    percent = calculate_market_score({"market_saturation_score": 65, "negative_review_percent": 18, "neutral_review_percent": 9, "sentiment_score_overall": 78, "positive_review_percent": 73})
    assert ratio["risk_score"] == percent["risk_score"]
    assert ratio["competition_gap_score"] == percent["competition_gap_score"]
