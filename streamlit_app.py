"""MarketLens AI: live provider search, normalization, AI analytics, dashboard, and decisions."""
from __future__ import annotations

import os
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from algorithms import WEIGHTS
from marketlens_ai import analyze_product
from marketlens_data import add_calculated_scores, load_catalogue, normalize_live_records, search_catalogue
from marketlens_providers import PROVIDERS, fetch_all, normalize_records
from marketlens_simulation import scenario_grid, simulate_profit

st.set_page_config(page_title="MarketLens AI", page_icon="◎", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
:root { --ink:#0f172a; --muted:#64748b; --line:#e2e8f0; --blue:#2563eb; --navy:#0b1220; }
.block-container { max-width: 1440px; padding: 1.4rem 2rem 4rem; }
[data-testid="stSidebar"] { background:#0b1220; }
[data-testid="stSidebar"] * { color:#dbeafe !important; }
.hero { border-radius:26px; padding:38px; color:white; background:linear-gradient(135deg,#0b1220 0%,#102d5c 55%,#2563eb 100%); margin-bottom:24px; box-shadow:0 20px 50px #0f172a22; }
.hero h1 { font-size:clamp(2rem,4vw,4rem); letter-spacing:-.065em; margin:8px 0 10px; }
.hero p { color:#bfdbfe; max-width:780px; font-size:1.05rem; line-height:1.7; }
.pill { display:inline-block; border:1px solid #93c5fd66; background:#ffffff14; border-radius:999px; padding:6px 12px; font-size:.75rem; letter-spacing:.1em; font-weight:700; }
.card { border:1px solid var(--line); border-radius:18px; padding:18px; background:white; }
.verdict { border-radius:16px; padding:18px 22px; font-weight:800; font-size:1.15rem; margin:8px 0 18px; }
.verdict-go { background:#ecfdf3; color:#027a48; border:1px solid #abefc6; }
.verdict-caution { background:#fffaeb; color:#b54708; border:1px solid #fedf89; }
.verdict-pass { background:#fef3f2; color:#b42318; border:1px solid #fecdca; }
.small { color:var(--muted); font-size:.83rem; line-height:1.55; }
[data-testid="stMetric"] { border:1px solid var(--line); border-radius:16px; padding:14px; background:#fff; }
</style>
""", unsafe_allow_html=True)


def _secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, os.getenv(name, default)))
    except Exception:
        return os.getenv(name, default)


@st.cache_data(ttl=600, show_spinner=False)
def live_search(query: str, providers: tuple[str, ...]):
    results = fetch_all(query, list(providers))
    records = normalize_records(results)
    return results, records


def verdict_class(verdict: str) -> str:
    return {"GO": "verdict-go", "CAUTION": "verdict-caution", "PASS": "verdict-pass"}.get(verdict, "verdict-pass")


def metric_value(value: Any, suffix: str = "") -> str:
    if value is None or pd.isna(value) if not isinstance(value, str) else not value.strip():
        return "Unavailable"
    return f"{value:,.2f}{suffix}" if isinstance(value, float) else f"{value}{suffix}"


def render_decision(row: pd.Series, raw: dict[str, Any] | None = None) -> dict[str, Any]:
    product = {**(raw or {}), **row.to_dict()}
    analysis = analyze_product(product)
    score = analysis["score"]
    verdict = score["verdict"]
    st.markdown(f'<div class="verdict {verdict_class(verdict)}">{verdict} · {score["final_market_score"]:.1f}/100 · Evidence confidence {score["confidence_score"]:.1f}%</div>', unsafe_allow_html=True)
    st.caption({"GO": "Strong observed opportunity signal. Validate suppliers, regulations, and unit economics before committing inventory.", "CAUTION": "Mixed or incomplete evidence. Investigate demand, margin, and risk signals before launch.", "PASS": "Current evidence does not support a confident launch decision. This is not a claim that the product cannot sell."}[verdict])
    chart = pd.DataFrame({"Dimension": ["Demand", "Profit", "Risk", "Competition gap"], "Score": [score["demand_score"], score["profit_score"], score["risk_score"], score["competition_gap_score"]]})
    st.plotly_chart(px.bar(chart, x="Dimension", y="Score", range_y=[0, 100], color="Dimension", title="Fixed 40/30/20/10 score components"), use_container_width=True)
    st.write(f"**AI analytics:** {analysis['ai_method']} · **Sentiment:** {analysis['sentiment']['label']} · **Trend:** {analysis['trend_signal']} · **Risk outlook:** {analysis['risk_level']}")
    return analysis


def render_product(row: pd.Series, raw: dict[str, Any] | None = None) -> None:
    product = {**(raw or {}), **row.to_dict()}
    st.markdown(f"### {product.get('product_name', 'Unnamed product')}")
    st.caption(f"{product.get('brand') or 'Brand unavailable'} · {product.get('main_category') or 'Category unavailable'} · {product.get('provider') or 'Managed catalogue'}")
    tabs = st.tabs(["Decision", "Overview", "Market evidence", "Profit simulation", "Provenance"])
    with tabs[0]:
        render_decision(row, raw)
    with tabs[1]:
        st.write(product.get("product_description") or "No product description supplied.")
        a, b, c, d = st.columns(4)
        a.metric("Price", metric_value(product.get("selling_price_usd"), " USD"))
        b.metric("Rating", metric_value(product.get("average_rating"), " / 5"))
        c.metric("Reviews", metric_value(product.get("total_reviews_count")))
        d.metric("Providers", metric_value(product.get("provider_count"), " sources"))
    with tabs[2]:
        st.dataframe(pd.DataFrame({"Signal": ["Sentiment", "Trend", "Risk outlook", "Observed fields", "Provider count"], "Value": [str(analyze_product(product)["sentiment"]), analyze_product(product)["trend_signal"], analyze_product(product)["risk_level"], ", ".join(product.get("observed_fields", [])) or "Unavailable", product.get("provider_count", 1)]}), hide_index=True, use_container_width=True)
        st.info("Provider values are displayed as observed. Missing commercial fields remain unavailable and are not guessed.")
    with tabs[3]:
        st.caption("Scenario outputs are sensitivity simulations, not guaranteed forecasts.")
        scenarios = scenario_grid(product)
        st.dataframe(pd.DataFrame(scenarios)[["Scenario", "units", "revenue", "net_profit", "net_margin_percent", "break_even_units"]], hide_index=True, use_container_width=True)
        st.plotly_chart(px.bar(pd.DataFrame(scenarios), x="Scenario", y="net_profit", color="Scenario", title="Scenario net profit"), use_container_width=True)
    with tabs[4]:
        st.write(f"**Source provider:** {product.get('provider') or 'Managed catalogue'}")
        st.write(f"**All providers matched:** {', '.join(product.get('providers', [])) or product.get('provider', 'Managed source')}")
        st.write(f"**Source URL:** {product.get('source_url') or 'Not supplied'}")
        st.write(f"**Provider record ID:** {product.get('provider_product_id') or product.get('product_id')}")
        st.write(f"**Fetched/updated:** {product.get('last_updated_timestamp') or 'Fetched live; provider timestamp unavailable'}")


def main() -> None:
    with st.sidebar:
        st.markdown("## ◎ MarketLens AI")
        st.caption("Live product intelligence")
        page = st.radio("Workspace", ["Live search", "Compare", "Simulation", "API health", "Methodology"], label_visibility="collapsed")
        st.divider()
        st.markdown("**Live providers**")
        default = ["DummyJSON", "Fake Store API", "Open Beauty Facts", "eBay Browse API", "Keepa API", "Shopify Storefront API"]
        selected = [name for name in default if st.checkbox(name, value=name in {"DummyJSON", "Fake Store API", "Open Beauty Facts"}, key=f"provider_{name}")]
        st.divider()
        st.caption("Free providers work without keys. eBay, Keepa, Shopify, and DeepSeek activate only when their credentials are configured in Streamlit Secrets.")

    st.markdown('<div class="hero"><span class="pill">LIVE PRODUCT APIs · AI ANALYTICS · DECISION SUPPORT</span><h1>Know what to launch next.</h1><p>MarketLens combines live product discovery, provider normalization, transparent analytics, profitability scenarios, and a GO · CAUTION · PASS decision in one focused workspace.</p></div>', unsafe_allow_html=True)

    if page == "Live search":
        query = st.text_input("Search products across live providers", placeholder="Try: wireless earbuds, skincare, running shoes…")
        if not query.strip():
            st.info("Enter a product or category to query the selected live providers.")
            return
        with st.spinner("Fetching and normalizing live provider data…"):
            results, raw_records = live_search(query, tuple(selected))
        normalized = normalize_live_records(raw_records, f"Live providers: {', '.join(selected)}")
        scored = add_calculated_scores(normalized)
        st.caption(f"{len(raw_records)} normalized products from {sum(item.status == 'ok' for item in results)} working provider(s)")
        if scored.empty:
            st.warning("No products were returned. Try another query or enable more providers.")
            return
        st.dataframe(scored[["product_name", "brand", "main_category", "calculated_final_market_score", "calculated_product_verdict", "evidence_confidence"]].rename(columns={"product_name": "Product", "brand": "Brand", "main_category": "Category", "calculated_final_market_score": "Score", "calculated_product_verdict": "Decision", "evidence_confidence": "Confidence %"}), hide_index=True, use_container_width=True)
        chosen = st.selectbox("Open product intelligence", scored["product_id"].astype(str).tolist(), format_func=lambda key: str(scored.loc[scored["product_id"].astype(str) == key, "product_name"].iloc[0]))
        selected_row = scored[scored["product_id"].astype(str) == chosen].iloc[0]
        raw = next((record for record in raw_records if record.get("provider_product_id") == chosen), None)
        render_product(selected_row, raw)
    elif page == "Compare":
        query = st.text_input("Search a comparison set", placeholder="Try: laptops, handbags, moisturizer…")
        if query.strip():
            _, records = live_search(query, tuple(selected))
            scored = add_calculated_scores(normalize_live_records(records, "Live provider comparison"))
            if not scored.empty:
                st.plotly_chart(px.scatter(scored, x="calculated_demand_score", y="calculated_profit_score", size="evidence_confidence", color="calculated_product_verdict", hover_name="product_name", title="Demand vs profit opportunity map", labels={"calculated_demand_score": "Demand score", "calculated_profit_score": "Profit score"}), use_container_width=True)
                st.dataframe(scored[["product_name", "main_category", "calculated_final_market_score", "calculated_product_verdict", "evidence_confidence"]].sort_values("calculated_final_market_score", ascending=False), hide_index=True, use_container_width=True)
    elif page == "Simulation":
        st.markdown("### Profitability simulation")
        st.caption("Select a live product first in Live search, or enter a scenario manually.")
        units = st.number_input("Monthly units", min_value=1, value=500, step=50)
        price = st.number_input("Selling price (USD)", min_value=0.01, value=29.99, step=1.0)
        cost = st.number_input("Unit cost (USD)", min_value=0.0, value=12.0, step=1.0)
        ads = st.number_input("Monthly advertising spend (USD)", min_value=0.0, value=500.0, step=50.0)
        fee = st.slider("Platform fee (%)", 0.0, 40.0, 15.0)
        shipping = st.number_input("Shipping per unit (USD)", min_value=0.0, value=2.0, step=0.5)
        simulation = simulate_profit({}, int(units), price, cost, ads, fee, shipping)
        a, b, c = st.columns(3)
        a.metric("Revenue", f"${simulation['revenue']:,.2f}")
        b.metric("Net profit", f"${simulation['net_profit']:,.2f}")
        c.metric("Break-even units", f"{simulation['break_even_units']:,.0f}")
    elif page == "API health":
        st.markdown("### Provider health and configuration")
        rows = []
        for name in ["DummyJSON", "Fake Store API", "Open Beauty Facts", "eBay Browse API", "Keepa API", "Shopify Storefront API"]:
            configured = name in {"DummyJSON", "Fake Store API", "Open Beauty Facts"} or (name == "eBay Browse API" and bool(_secret("EBAY_OAUTH_TOKEN"))) or (name == "Keepa API" and bool(_secret("KEEPA_API_KEY"))) or (name == "Shopify Storefront API" and bool(_secret("SHOPIFY_STOREFRONT_URL")))
            rows.append({"Provider": name, "Status": "Ready" if configured else "Optional / not configured", "Role": PROVIDERS[name].__doc__ or "Provider adapter"})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        st.info("Fake Store API and DummyJSON are useful integration sources, not real market intelligence. eBay and Keepa are the production marketplace connectors once authorized credentials and usage plans are available.")
    else:
        st.markdown("### Five-layer architecture")
        st.markdown("**1. Live Product APIs** — DummyJSON, Fake Store API, Open Beauty Facts, and optional eBay/Keepa/Shopify adapters. **2. Integration & Normalization** — common product schema, deduplication, provider evidence, timestamps, and failure isolation. **3. AI Analytics** — deterministic sentiment/trend/risk fallback with optional DeepSeek JSON analysis. **4. Dashboard** — search, comparison map, provider health, evidence, and profitability scenarios. **5. Decision Support** — fixed Demand 40%, Profit 30%, Risk 20%, Competition Gap 10% scoring with GO, CAUTION, PASS thresholds.")
        st.latex(r"MarketScore = Demand \times 0.40 + Profit \times 0.30 - Risk \times 0.20 + CompetitionGap \times 0.10")
        st.warning("Live provider data varies in coverage and freshness. A decision is a research aid, not a guarantee of sales, profit, or compliance.")


if __name__ == "__main__":
    main()
