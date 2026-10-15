"""Transparent profitability simulations; outputs are scenarios, not forecasts."""
from __future__ import annotations

from typing import Any


def _num(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def simulate_profit(product: dict[str, Any], units: int, selling_price: float, unit_cost: float, ad_spend: float, platform_fee_percent: float, shipping_cost: float) -> dict[str, Any]:
    revenue = max(0, units) * max(0, selling_price)
    fees = revenue * max(0, platform_fee_percent) / 100
    variable_cost = max(0, units) * (max(0, unit_cost) + max(0, shipping_cost))
    net_profit = revenue - fees - variable_cost - max(0, ad_spend)
    margin = (net_profit / revenue * 100) if revenue else 0.0
    return {"units": units, "revenue": round(revenue, 2), "fees": round(fees, 2), "variable_cost": round(variable_cost, 2), "ad_spend": round(max(0, ad_spend), 2), "net_profit": round(net_profit, 2), "net_margin_percent": round(margin, 2), "break_even_units": round((max(0, ad_spend)) / max(0.01, selling_price - unit_cost - selling_price * platform_fee_percent / 100 - shipping_cost), 1)}


def scenario_grid(product: dict[str, Any]) -> list[dict[str, Any]]:
    units = max(1, int(_num(product.get("inventory"), _num(product.get("monthly_unit_sales"), 100))))
    price = max(0.01, _num(product.get("selling_price_usd"), 0))
    cost = max(0.0, _num(product.get("unit_cost_usd"), price * 0.55))
    fee = max(0.0, _num(product.get("platform_fee_percent"), 15))
    shipping = max(0.0, _num(product.get("shipping_cost_per_unit_usd"), 0))
    revenue_anchor = _num(product.get("monthly_revenue"), units * price)
    ad_anchor = _num(product.get("advertising_spend_usd"), revenue_anchor * 0.1)
    scenarios = []
    for label, unit_multiplier, price_multiplier, ad_multiplier in [("Conservative", 0.65, 0.95, 1.25), ("Base", 1.0, 1.0, 1.0), ("Upside", 1.35, 1.05, 0.85)]:
        scenarios.append({"Scenario": label, **simulate_profit(product, int(units * unit_multiplier), price * price_multiplier, cost, ad_anchor * ad_multiplier, fee, shipping)})
    return scenarios
