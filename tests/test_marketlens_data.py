import pandas as pd

from algorithms import calculate_market_score
from marketlens_data import add_calculated_scores, _open_beauty_frame


def test_calculated_score_column_matches_engine():
    source = pd.DataFrame([{"product_id": "1", "product_name": "Test product", "monthly_unit_sales": 1000, "monthly_revenue": 25000, "average_rating": 4.5, "total_reviews_count": 500, "positive_review_percent": 80}])
    normalized = source.assign(**{column: pd.NA for column in ["product_sku", "product_description", "main_category", "sub_category", "brand", "target_platform", "target_region", "target_country", "currency", "sales_growth_rate_30d", "unit_cost_usd", "selling_price_usd", "gross_margin_percent", "platform_fee_percent", "shipping_cost_per_unit_usd", "net_profit_per_unit_usd", "negative_review_percent", "neutral_review_percent", "sentiment_score_overall", "top_customer_pain_points", "unmet_customer_needs", "total_active_sellers", "market_saturation_score", "top_3_sellers_market_share_percent", "average_competitor_rating", "price_gap_vs_average_competitor_percent", "demand_score", "profit_score", "risk_score", "competition_gap_score", "final_market_score", "product_verdict", "last_updated_timestamp"]})
    scored = add_calculated_scores(normalized)
    expected = calculate_market_score(scored.iloc[0].to_dict())["final_market_score"]
    assert scored.loc[0, "calculated_final_market_score"] == expected
    assert "calculated_product_verdict" in scored.columns


def test_open_beauty_facts_fallback_is_identity_only():
    frame = _open_beauty_frame([{"code": "123", "product_name": "Sample Shampoo", "brands": "Example", "categories": "Hair care, Shampoos", "ingredients_text": "Water", "countries": "France", "last_modified": "1700000000"}], "shampoo")
    assert len(frame) == 1
    assert frame.loc[0, "product_id"] == "OBF-123"
    assert frame.loc[0, "product_name"] == "Sample Shampoo"
    assert pd.isna(frame.loc[0, "monthly_unit_sales"])
    assert frame.attrs["source_label"].startswith("Free fallback: Open Beauty Facts")
