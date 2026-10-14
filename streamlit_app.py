"""MarketLens AI public search-first Streamlit application."""
from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from algorithms import WEIGHTS, get_verdict_explanation
from marketlens_data import add_calculated_scores, coverage_summary, load_catalogue, search_catalogue, search_open_beauty_facts

st.set_page_config(page_title="MarketLens AI", page_icon="◎", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
:root { --ink:#101828; --muted:#667085; --line:#e4e7ec; --blue:#175cd3; --blue-soft:#eff8ff; }
.block-container { max-width: 1360px; padding-top: 2rem; padding-bottom: 4rem; }
[data-testid="stSidebar"] { background:#f8fafc; border-right:1px solid #eaecf0; }
.hero { border:1px solid #d0d5dd; border-radius:24px; padding:32px; background:radial-gradient(circle at 90% 10%,#dbeafe 0,transparent 35%),linear-gradient(135deg,#fff,#f8fbff); margin-bottom:24px; }
.hero h1 { font-size:clamp(2rem,4vw,3.6rem); letter-spacing:-.06em; color:var(--ink); margin:8px 0; }
.hero p { color:var(--muted); max-width:760px; font-size:1.05rem; line-height:1.7; }
.pill { display:inline-block; border:1px solid #b2ddff; background:var(--blue-soft); color:var(--blue); border-radius:999px; padding:5px 10px; font-size:.78rem; font-weight:700; }
.verdict { border-radius:16px; padding:16px 20px; font-weight:700; margin:10px 0 18px; }
.verdict-go { background:#ecfdf3; color:#027a48; border:1px solid #abefc6; }
.verdict-caution { background:#fffaeb; color:#b54708; border:1px solid #fedf89; }
.verdict-pass { background:#fef3f2; color:#b42318; border:1px solid #fecdca; }
.small-note { color:var(--muted); font-size:.83rem; line-height:1.55; }
[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:16px; padding:16px; }
</style>
""", unsafe_allow_html=True)


def source_config() -> str:
    try:
        return str(st.secrets.get("MARKETLENS_DATA_URL", os.getenv("MARKETLENS_DATA_URL", "")))
    except Exception:
        return os.getenv("MARKETLENS_DATA_URL", "")


def verdict_class(verdict: str) -> str:
    return {"GO": "verdict-go", "CAUTION": "verdict-caution", "PASS": "verdict-pass"}.get(verdict, "verdict-pass")


def display_number(value: object, suffix: str = "") -> str:
    if pd.isna(value) if not isinstance(value, str) else not value.strip():
        return "Unavailable"
    return f"{value:,.2f}{suffix}" if isinstance(value, float) else f"{value}{suffix}"


def render_score_card(row: pd.Series) -> None:
    verdict = str(row.get("calculated_product_verdict", "PASS"))
    score = float(row.get("calculated_final_market_score", 0) or 0)
    confidence = float(row.get("evidence_confidence", 0) or 0)
    st.markdown(f'<div class="verdict {verdict_class(verdict)}"><span>{verdict}</span> · {score:.1f}/100 · Evidence confidence {confidence:.1f}%</div>', unsafe_allow_html=True)
    st.caption(get_verdict_explanation(verdict, score))
    chart = pd.DataFrame({"Component": ["Demand 40%", "Profit 30%", "Risk 20%", "Competition gap 10%"], "Score": [row.get("calculated_demand_score", 0), row.get("calculated_profit_score", 0), row.get("calculated_risk_score", 0), row.get("calculated_competition_gap_score", 0)]})
    st.bar_chart(chart.set_index("Component"), height=220, color="#175cd3")
    st.markdown(f"**Method:** fixed weights — Demand {WEIGHTS['demand']:.0%}, Profit {WEIGHTS['profit']:.0%}, Risk {WEIGHTS['risk']:.0%}, Competition Gap {WEIGHTS['competition_gap']:.0%}.")


def render_product(row: pd.Series, coverage: dict[str, object]) -> None:
    st.markdown(f"## {row.get('product_name', 'Unnamed product')}")
    st.caption(f"{row.get('brand') or 'Brand unavailable'} · {row.get('main_category') or 'Category unavailable'} · ID {row.get('product_id')}")
    tabs = st.tabs(["Decision", "Product overview", "Market signals", "Provenance"])
    with tabs[0]:
        render_score_card(row)
        if row.get("calculated_product_verdict") == "PASS":
            st.warning("PASS means the available evidence does not support a confident launch decision. It is not a claim that the product cannot sell.")
    with tabs[1]:
        st.write(row.get("product_description") or "No product description was supplied.")
        left, right = st.columns(2)
        with left:
            st.metric("Selling price", display_number(row.get("selling_price_usd"), f" {row.get('currency') or 'USD'}"))
            st.metric("Monthly revenue", display_number(row.get("monthly_revenue"), " USD"))
            st.metric("Average rating", display_number(row.get("average_rating"), " / 5"))
        with right:
            st.metric("Monthly unit sales", display_number(row.get("monthly_unit_sales")))
            st.metric("Net profit / unit", display_number(row.get("net_profit_per_unit_usd"), " USD"))
            st.metric("Active sellers", display_number(row.get("total_active_sellers")))
    with tabs[2]:
        signals = pd.DataFrame({"Signal": ["30-day sales growth", "Positive reviews", "Negative reviews", "Saturation", "Competitor price gap", "Customer pain points", "Unmet needs"], "Observed value": [display_number(row.get("sales_growth_rate_30d"), "%"), display_number(row.get("positive_review_percent"), "%"), display_number(row.get("negative_review_percent"), "%"), display_number(row.get("market_saturation_score")), display_number(row.get("price_gap_vs_average_competitor_percent"), "%"), row.get("top_customer_pain_points") or "Unavailable", row.get("unmet_customer_needs") or "Unavailable"]})
        st.dataframe(signals, hide_index=True, use_container_width=True)
        st.info("Signals are displayed only when present in the source. Identity-only fallback results intentionally show commercial metrics as unavailable.")
    with tabs[3]:
        st.write(f"**Source:** {coverage['source_label']}")
        st.write(f"**Loaded at:** {coverage['loaded_at'] or 'Unavailable'}")
        st.write(f"**Source URL:** {coverage['source_url'] or 'Not supplied'}")
        st.write(f"**Product update:** {row.get('last_updated_timestamp') or 'Not supplied'}")
        st.write("Source-supplied component scores and verdicts are reference fields only; the displayed decision is recalculated by MarketLens.")


def main() -> None:
    with st.sidebar:
        st.markdown("## ◎ MarketLens AI")
        st.caption("Public product intelligence")
        page = st.radio("Navigate", ["Explore products", "Compare opportunities", "Data source", "Methodology"], label_visibility="collapsed")
        st.divider()
        st.caption("Catalogue data is backend-managed. Public file uploads are disabled.")
        st.caption("Free fallback: Open Beauty Facts identity search when the managed catalogue has no match.")
        st.divider()
        st.caption("Current-data claims require a source URL and update timestamp. Identity-only records remain clearly marked.")

    configured_url = source_config()
    try:
        frame = load_catalogue(configured_url)
    except Exception as error:
        st.error(f"The backend catalogue could not be loaded: {error}")
        frame = load_catalogue()
    scored = add_calculated_scores(frame)
    coverage = coverage_summary(scored)
    categories = ["All categories"] + sorted(str(item) for item in scored["main_category"].dropna().unique()) if not scored.empty else ["All categories"]

    st.markdown('<div class="hero"><span class="pill">SOURCE-AWARE PRODUCT INTELLIGENCE</span><h1>Find products you can explain.</h1><p>Search a backend-managed catalogue, inspect the product overview, and receive a transparent market decision based on observed demand, profit, risk, competition, and evidence confidence.</p></div>', unsafe_allow_html=True)
    metric_cols = st.columns(4)
    metric_cols[0].metric("Catalogue records", f"{coverage['total_records']:,}")
    metric_cols[1].metric("Observed evidence", f"{coverage['coverage_percent']}%")
    metric_cols[2].metric("Core evidence complete", f"{coverage['records_with_complete_core_evidence']:,}")
    metric_cols[3].metric("Source", str(coverage['source_label'])[:22])

    if page == "Explore products":
        st.markdown("<h2>Explore products</h2><p class='small-note'>Search by name, SKU, brand, description, category, or sub-category. If the managed catalogue has no match, MarketLens checks the free Open Beauty Facts API.</p>", unsafe_allow_html=True)
        query_col, category_col, verdict_col = st.columns([2.2, 1, 1])
        with query_col:
            query = st.text_input("Search", placeholder="Try: wireless earbuds, skincare, kitchen, SKU…")
        with category_col:
            category = st.selectbox("Category", categories)
        with verdict_col:
            verdict = st.selectbox("Decision", ["All verdicts", "GO", "CAUTION", "PASS"])
        results = search_catalogue(scored, query, category, verdict, limit=100)
        source_for_result = coverage
        if results.empty and query.strip() and category == "All categories" and verdict == "All verdicts":
            try:
                fallback = add_calculated_scores(search_open_beauty_facts(query, limit=25))
                if not fallback.empty:
                    results, source_for_result = fallback, coverage_summary(fallback)
                    st.info("No managed-catalogue match. Showing identity results from the free Open Beauty Facts API; commercial evidence is unavailable unless explicitly supplied by a source.")
            except requests.RequestException:
                st.warning("The free fallback source is temporarily unavailable. Try again later or search another term.")
        st.caption(f"Showing {len(results):,} matching products")
        if results.empty:
            st.warning("No matching products. Try a broader search or another category.")
        else:
            table = results[["product_name", "brand", "main_category", "calculated_final_market_score", "calculated_product_verdict", "evidence_confidence"]].rename(columns={"product_name": "Product", "brand": "Brand", "main_category": "Category", "calculated_final_market_score": "Score", "calculated_product_verdict": "Decision", "evidence_confidence": "Confidence %"})
            st.dataframe(table, hide_index=True, use_container_width=True)
            options = results["product_id"].astype(str).tolist()
            chosen = st.selectbox("Open product overview", options, format_func=lambda key: str(results.loc[results["product_id"].astype(str) == key, "product_name"].iloc[0]))
            render_product(results[results["product_id"].astype(str) == chosen].iloc[0], source_for_result)
            st.download_button("Download search results (CSV)", results.to_csv(index=False).encode("utf-8"), "marketlens-search-results.csv", "text/csv")
    elif page == "Compare opportunities":
        st.markdown("<h2>Compare opportunities</h2><p class='small-note'>This ranking is calculated from the backend-managed source and is not a promise of future sales.</p>", unsafe_allow_html=True)
        ranking = scored.sort_values(["calculated_final_market_score", "evidence_confidence"], ascending=False).head(25)
        st.dataframe(ranking[["product_name", "main_category", "calculated_final_market_score", "calculated_product_verdict", "evidence_confidence"]].rename(columns={"product_name": "Product", "main_category": "Category", "calculated_final_market_score": "Score", "calculated_product_verdict": "Decision", "evidence_confidence": "Confidence %"}), hide_index=True, use_container_width=True)
        if not ranking.empty:
            st.plotly_chart(px.bar(ranking.head(10), x="calculated_final_market_score", y="product_name", color="calculated_product_verdict", orientation="h", title="Top observed opportunities"), use_container_width=True)
    elif page == "Data source":
        st.markdown("<h2>Data source and freshness</h2><p class='small-note'>The catalogue is loaded by the backend from the repository or MARKETLENS_DATA_URL. Visitors cannot upload files. A free Open Beauty Facts lookup is used only when a search misses the managed catalogue.</p>", unsafe_allow_html=True)
        st.json(coverage)
        st.info("For Streamlit Community Cloud, set MARKETLENS_DATA_URL in Secrets to an authorized, refreshable CSV/XLSX source containing provenance and update timestamps. Open Beauty Facts is free and identity-focused; it is not a substitute for live sales, price, advertising, or competitor evidence.")
    else:
        st.markdown("<h2>Methodology</h2><p class='small-note'>Every displayed number is either observed from the source or calculated from observed inputs. Missing data remains unavailable.</p>", unsafe_allow_html=True)
        st.markdown("### Fixed decision formula")
        st.latex(r"MarketScore = Demand \times 0.40 + Profit \times 0.30 - Risk \times 0.20 + CompetitionGap \times 0.10")
        st.table(pd.DataFrame({"Dimension": ["Demand", "Profit", "Risk", "Competition Gap"], "Weight": ["40%", "30%", "20%", "10%"], "Interpretation": ["Sales, revenue, growth, reviews, rating, positive review share", "Margin, cost, fees, shipping, net profit, advertising efficiency", "Saturation, sellers, negative/neutral reviews, concentration, acquisition cost", "Competitor rating/price, unmet needs, sentiment, seller gap"]}))
        st.write("**GO** means at least 70. **CAUTION** means 45–69.99. **PASS** means below 45. Confidence is reported separately and falls when evidence is missing.")
        st.warning("A product identity is not the same as current market evidence. Connect authorized current sources before making purchasing, inventory, or launch decisions.")


if __name__ == "__main__":
    main()
