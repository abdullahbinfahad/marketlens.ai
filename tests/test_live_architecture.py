from marketlens_ai import analyze_product, sentiment_analysis
from marketlens_data import normalize_live_records
from marketlens_providers import ProviderResult, normalize_records
from marketlens_simulation import scenario_grid, simulate_profit


def test_provider_records_are_deduplicated_and_retain_sources():
    results = [
        ProviderResult("DummyJSON", "ok", [{"provider_product_id": "dummyjson:1", "product_name": "Phone", "brand": "A", "selling_price_usd": 10, "observed_fields": ["selling_price_usd"]}]),
        ProviderResult("eBay Browse API", "ok", [{"provider_product_id": "ebay:1", "product_name": "Phone", "brand": "A", "selling_price_usd": 12, "observed_fields": ["selling_price_usd"]}]),
    ]
    records = normalize_records(results)
    assert len(records) == 1
    assert records[0]["provider_count"] == 2
    assert set(records[0]["providers"]) == {"DummyJSON", "eBay Browse API"}


def test_live_records_enter_canonical_scoring_pipeline():
    frame = normalize_live_records([{"provider_product_id": "dummyjson:1", "product_name": "Phone", "brand": "A", "selling_price_usd": 100, "average_rating": 4.5}], "test")
    assert frame.loc[0, "product_id"] == "dummyjson:1"
    assert frame.loc[0, "product_name"] == "Phone"


def test_ai_fallback_is_deterministic_without_key():
    assert sentiment_analysis("great quality but slow and difficult")['label'] == "neutral"
    result = analyze_product({"product_name": "Test", "product_description": "great quality", "selling_price_usd": 20})
    assert result["ai_method"] == "deterministic fallback"
    assert result["score"]["verdict"] in {"GO", "CAUTION", "PASS"}


def test_profit_simulation_and_scenarios_are_numeric():
    result = simulate_profit({}, 100, 20, 8, 200, 15, 2)
    assert result["revenue"] == 2000
    assert result["net_profit"] == 500
    assert len(scenario_grid({"selling_price_usd": 20, "unit_cost_usd": 8})) == 3
