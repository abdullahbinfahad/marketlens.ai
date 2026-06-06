"""
MarketLens AI - Complete Streamlit Application
Smart Cross-Border Product Intelligence Platform

Streamlit Cloud Compatible Version
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime
import os

# Import local modules
from data_generator import generate_products, generate_reviews, generate_trends
from sentiment import SentimentAnalyzer
from algorithms import calculate_all_scores, get_score_interpretation

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="MarketLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #333;
        margin: 20px 0 10px 0;
    }
    
    h1 {
        font-size: 36px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 24px;
        color: #667eea;
    }
    
    h3 {
        font-size: 18px;
        color: #764ba2;
    }
    
    /* Verdict Box */
    .verdict-box {
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        animation: slideIn 0.5s ease;
    }
    
    .verdict-go {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1a5f3f;
    }
    
    .verdict-caution {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #5f4a1a;
    }
    
    .verdict-pass {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

if "api_key" not in st.session_state:
    st.session_state.api_key = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# ============================================================================
# DATA LOADING (CACHED)
# ============================================================================

@st.cache_data
def load_all_data():
    """Load and cache all application data."""
    products = generate_products(50)
    reviews = generate_reviews(1000, 50)
    trends = generate_trends(12, 6)
    return products, reviews, trends

try:
    products_df, reviews_df, trends_df = load_all_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("### 🎯 MarketLens AI")
    st.markdown("**Smart Cross-Border Product Intelligence**")
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Select Page:",
        ["🏠 Home", "📊 Analysis", "📈 Trends", "👤 Profile", "📚 Research"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Products", len(products_df))
    with col2:
        st.metric("Reviews", len(reviews_df))
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    api_key_input = st.text_input(
        "DeepSeek API Key",
        type="password",
        value=st.session_state.get("api_key", ""),
        help="Optional: Leave empty for mock analysis"
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    st.markdown("---")
    st.caption("MarketLens AI v2.0 | Nanjing Tech University")

# ============================================================================
# PAGE: HOME
# ============================================================================

if "🏠" in page:
    st.markdown("# 🎯 MarketLens AI")
    st.markdown("### Smart Cross-Border Product Intelligence")
    
    st.markdown("""
    MarketLens AI is an intelligent decision-making agent for cross-border e-commerce.
    It answers: **Which products will perform best in targeted overseas markets?**
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Analyze Products
        Get instant insights on demand, profit, risk, and competition gaps.
        """)
        if st.button("Start Analysis →", key="btn_analysis", use_container_width=True):
            st.session_state.current_page = "Analysis"
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 📈 Explore Trends
        Visualize market trends and category performance.
        """)
        if st.button("View Trends →", key="btn_trends", use_container_width=True):
            st.session_state.current_page = "Trends"
            st.rerun()
    
    with col3:
        st.markdown("""
        ### 👤 Your Profile
        Track analyses and manage settings.
        """)
        if st.button("Go to Profile →", key="btn_profile", use_container_width=True):
            st.session_state.current_page = "Profile"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("## 🌟 Key Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        **🤖 AI-Powered Sentiment Analysis**
        - Analyzes 1000+ customer reviews
        - Identifies market gaps
        - Detects unmet needs
        
        **💰 Smart Scoring Engine**
        - Demand Score: Market appetite
        - Profit Score: Financial viability
        - Risk Score: Market saturation
        """)
    
    with feature_col2:
        st.markdown("""
        **📊 Real-time Market Intelligence**
        - Track 50+ products
        - Monitor 6 categories
        - Analyze seasonal patterns
        
        **🎯 Actionable Verdicts**
        - GO: Strong opportunity (≥75)
        - CAUTION: Moderate (50-74)
        - PASS: High risk (<50)
        """)
    
    st.markdown("---")
    
    st.markdown("## 📊 Market Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", len(products_df))
    with col2:
        st.metric("Total Reviews", len(reviews_df))
    with col3:
        st.metric("Categories", products_df["category"].nunique())
    with col4:
        st.metric("Avg Rating", f"{products_df['avg_rating'].mean():.1f}/5.0")

# ============================================================================
# PAGE: PRODUCT ANALYSIS
# ============================================================================

elif "📊" in page:
    st.markdown("# 📊 Product Analysis")
    st.markdown("Analyze any product and get instant insights on market opportunity.")
    
    st.markdown("---")
    
    # Tabs for input method
    tab1, tab2 = st.tabs(["📦 Select Existing Product", "✏️ Enter New Product"])
    
    with tab1:
        st.markdown("### Choose from our database (50 products)")
        
        product_options = products_df["product_name"].tolist()
        selected_product_name = st.selectbox(
            "Select a product:",
            product_options,
            label_visibility="collapsed"
        )
        
        selected_product = products_df[products_df["product_name"] == selected_product_name].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Price", f"${selected_product['price']:.2f}")
        with col2:
            st.metric("Rating", f"⭐ {selected_product['avg_rating']}/5.0")
        with col3:
            st.metric("Reviews", f"{selected_product['review_count']:,}")
        
        if st.button("Analyze This Product →", use_container_width=True, key="analyze_existing"):
            st.session_state.selected_product = selected_product.to_dict()
            st.session_state.analysis_mode = "existing"
    
    with tab2:
        st.markdown("### Enter product details manually")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("Product Name", placeholder="e.g., Wireless Earbuds")
            category = st.selectbox("Category", ["Electronics", "Fashion", "Home & Garden", "Sports", "Beauty"])
            price = st.number_input("Price ($)", min_value=1.0, max_value=10000.0, value=100.0)
        
        with col2:
            avg_rating = st.slider("Average Rating", 1.0, 5.0, 4.0, 0.1)
            review_count = st.number_input("Review Count", min_value=0, max_value=100000, value=1000, step=100)
            search_volume = st.number_input("Search Volume (30d)", min_value=0, max_value=100000, value=5000, step=100)
        
        if st.button("Analyze New Product →", use_container_width=True, key="analyze_new"):
            if not product_name:
                st.error("Please enter a product name")
            else:
                st.session_state.selected_product = {
                    "product_name": product_name,
                    "category": category,
                    "price": price,
                    "avg_rating": avg_rating,
                    "review_count": review_count,
                    "search_volume_30d": search_volume,
                    "sales_velocity_weekly": int(review_count / 10),
                    "trend_score": 60,
                    "competitor_count": 50,
                    "market_saturation": 55,
                }
                st.session_state.analysis_mode = "custom"
    
    # Display analysis results
    if "selected_product" in st.session_state:
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        product = st.session_state.selected_product
        
        # Get reviews for this product
        if st.session_state.analysis_mode == "existing":
            product_reviews = reviews_df[reviews_df["product_id"] == product.get("product_id", "PROD_001")]["review_text"].tolist()[:50]
        else:
            product_reviews = reviews_df["review_text"].tolist()[:50]
        
        if not product_reviews:
            product_reviews = ["Great product!", "Not as described", "Excellent quality"]
        
        # Sentiment analysis
        analyzer = SentimentAnalyzer(api_key=st.session_state.api_key)
        sentiment_result = analyzer.analyze_reviews(product["product_name"], product_reviews)
        
        # Calculate scores
        scores = calculate_all_scores(product, gap_score_from_ai=sentiment_result["competition_gap_score"])
        
        # Display verdict
        verdict_class = "verdict-go" if scores["verdict"] == "GO" else ("verdict-caution" if scores["verdict"] == "CAUTION" else "verdict-pass")
        st.markdown(f"""
        <div class="verdict-box {verdict_class}">
            <h2>{scores['verdict']}</h2>
            <p>{scores['verdict_explanation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Score breakdown
        st.markdown("## 📈 Score Breakdown")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Demand Score", f"{scores['demand_score']:.1f}/100")
        with col2:
            st.metric("Profit Score", f"{scores['profit_score']:.1f}/100")
        with col3:
            st.metric("Risk Score", f"{scores['risk_score']:.1f}/100")
        with col4:
            st.metric("Competition Gap", f"{scores['competition_gap_score']:.1f}/100")
        
        st.markdown("---")
        
        # Gauge charts
        st.markdown("## 📊 Visual Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=scores['demand_score'],
                title={'text': "Demand"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#667eea"}},
            ))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=scores['profit_score'],
                title={'text': "Profit"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#764ba2"}},
            ))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=scores['risk_score'],
                title={'text': "Risk"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#f5576c"}},
            ))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=scores['competition_gap_score'],
                title={'text': "Competition Gap"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#84fab0"}},
            ))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # AI Insights
        st.markdown("## 🤖 AI-Powered Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💡 Unmet Needs")
            for need in sentiment_result["unmet_needs"]:
                st.markdown(f"- {need}")
        
        with col2:
            st.markdown("### ⚠️ Top Complaints")
            for complaint in sentiment_result["top_complaints"]:
                st.markdown(f"- {complaint}")
        
        st.markdown("---")
        
        st.markdown("### 📝 Analysis Reasoning")
        st.info(sentiment_result["reasoning"])
        
        st.markdown("---")
        
        # Save to history
        if st.button("💾 Save to History", use_container_width=True):
            analysis_record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product_name": product["product_name"],
                "category": product.get("category", "Unknown"),
                "verdict": scores["verdict"],
                "overall_score": scores["overall_score"],
            }
            st.session_state.analysis_history.append(analysis_record)
            st.success("✅ Analysis saved to your history!")

# ============================================================================
# PAGE: TRENDS
# ============================================================================

elif "📈" in page:
    st.markdown("# 📈 Market Trends")
    st.markdown("Explore market trends across categories and time periods.")
    
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.selectbox("Select Category", ["All"] + trends_df["category"].unique().tolist())
    with col2:
        selected_metric = st.selectbox("Select Metric", ["search_volume", "sales_volume", "market_sentiment"])
    
    st.markdown("---")
    
    # Trend chart
    if selected_category == "All":
        trend_data = trends_df.groupby("date")[selected_metric].mean().reset_index()
    else:
        trend_data = trends_df[trends_df["category"] == selected_category]
    
    fig = px.line(
        trend_data,
        x="date",
        y=selected_metric,
        title=f"{selected_metric.replace('_', ' ').title()} Trend",
        markers=True,
    )
    fig.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Category comparison
    st.markdown("## 📊 Category Comparison")
    
    category_stats = trends_df.groupby("category")[selected_metric].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=category_stats.index,
        y=category_stats.values,
        title=f"Average {selected_metric.replace('_', ' ').title()} by Category",
        labels={'x': 'Category', 'y': selected_metric.replace('_', ' ').title()},
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Statistics table
    st.markdown("## 📈 Category Statistics")
    
    stats_df = trends_df.groupby("category").agg({
        "search_volume": ["mean", "max"],
        "sales_volume": ["mean", "max"],
        "market_sentiment": "mean",
    }).round(2)
    
    st.dataframe(stats_df, use_container_width=True)

# ============================================================================
# PAGE: PROFILE
# ============================================================================

elif "👤" in page:
    st.markdown("# 👤 User Profile")
    st.markdown("Track your analysis history and manage settings.")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 History", "⚙️ Settings", "📈 Statistics"])
    
    with tab1:
        st.markdown("## Analysis History")
        
        if st.session_state.analysis_history:
            history_df = pd.DataFrame(st.session_state.analysis_history)
            st.dataframe(history_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                csv = history_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="analysis_history.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col2:
                if st.button("🗑️ Clear History", use_container_width=True):
                    st.session_state.analysis_history = []
                    st.success("History cleared!")
                    st.rerun()
        else:
            st.info("No analysis history yet. Start analyzing products!")
    
    with tab2:
        st.markdown("## Settings")
        
        st.markdown("### API Configuration")
        st.info("Configure your DeepSeek API key in the sidebar for real sentiment analysis.")
        
        st.markdown("### Data & Privacy")
        st.markdown("""
        - All data is stored locally in your browser
        - Your API keys are never shared
        - You can clear your history anytime
        """)
    
    with tab3:
        st.markdown("## Statistics")
        
        if st.session_state.analysis_history:
            history = st.session_state.analysis_history
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Analyses", len(history))
            with col2:
                go_count = sum(1 for h in history if h.get("verdict") == "GO")
                st.metric("GO Verdicts", go_count)
            with col3:
                caution_count = sum(1 for h in history if h.get("verdict") == "CAUTION")
                st.metric("CAUTION Verdicts", caution_count)
            with col4:
                pass_count = sum(1 for h in history if h.get("verdict") == "PASS")
                st.metric("PASS Verdicts", pass_count)
        else:
            st.info("No statistics yet.")

# ============================================================================
# PAGE: RESEARCH
# ============================================================================

elif "📚" in page:
    st.markdown("# 📚 Market Research")
    st.markdown("Curated market insights and best practices.")
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📊 Market Overview", "🎯 Best Practices"])
    
    with tab1:
        st.markdown("## Market Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Products Analyzed", len(products_df))
        with col2:
            st.metric("Reviews Processed", len(reviews_df))
        with col3:
            st.metric("Categories", products_df["category"].nunique())
        with col4:
            st.metric("Avg Rating", f"{products_df['avg_rating'].mean():.1f}")
        
        st.markdown("---")
        
        st.markdown("### 🌍 Category Performance")
        
        category_perf = products_df.groupby("category").agg({
            "avg_rating": "mean",
            "review_count": "mean",
            "price": "mean",
        }).round(2)
        
        st.dataframe(category_perf, use_container_width=True)
    
    with tab2:
        st.markdown("## Best Practices")
        
        st.markdown("""
        ### 1️⃣ Product Selection
        - Focus on underserved niches
        - Look for unmet customer needs
        - Analyze competitor weaknesses
        - Validate demand with market data
        
        ### 2️⃣ Listing Optimization
        - Include primary keywords in title
        - Address customer pain points
        - Use high-quality images
        - Competitive pricing strategy
        
        ### 3️⃣ Marketing Strategy
        - Launch with competitive pricing
        - Leverage micro-influencers
        - Use paid advertising strategically
        - Build email list
        
        ### 4️⃣ Risk Management
        - Diversify across products
        - Monitor regulatory changes
        - Maintain cash reserves
        - Develop backup suppliers
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
    <p>MarketLens AI v2.0 | Nanjing Tech University | OPC Intelligent Agent Innovation Track</p>
    <p>🔗 <a href="https://www.marketlens-ai.com/">Website</a> | <a href="https://github.com/marketlens-ai">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
