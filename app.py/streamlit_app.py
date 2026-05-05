import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai

# ------------------- API Keys -------------------
ALIBABA_API_KEY = "ok_f8d69264b35fbdc6a3b35086d763874c"
ALIBABA_BASE_URL = "https://alibaba-scraper.omkar.cloud/alibaba/products/search"

GEMINI_API_KEY = "AIzaSyCSUkWRunK7RfHy-4P2uKgLHNF4TwaHxHE"
genai.configure(api_key=GEMINI_API_KEY)

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="MarketLens AI | Alibaba + MarketLens Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- Custom CSS -------------------
st.markdown("""
<style>
    .main { background-color: #0b1020; }
    .sidebar { background-color: #111827; }
    h1 { color: #4fc3f7; }
    h2, h3 { color: #e0f2fe; }
    .stButton>button { background-color: #0284c7; color: white; border-radius: 8px; }
    .card {
        background: #1e293b;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0px;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# ------------------- 1. Fetch Alibaba Data -------------------
def get_alibaba_data(search_query):
    headers = {"API-Key": ALIBABA_API_KEY}
    params = {"search_query": search_query}
    try:
        res = requests.get(ALIBABA_BASE_URL, headers=headers, params=params, timeout=20)
        if res.status_code == 200:
            return res.json()
        else:
            return {"error": f"Alibaba API Error: {res.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# ------------------- 2. Trim Alibaba Data (Only Useful Info) -------------------
def trim_alibaba_for_ai(alibaba_data):
    summary = []
    products = alibaba_data.get("products", [])[:3]

    for p in products:
        title = p.get("title", "")
        price_range = p.get("pricing", {}).get("range_formatted", "")
        moq = p.get("pricing", {}).get("minimum_order_label", "")
        supplier = p.get("supplier", {})
        sup_name = supplier.get("name", "")
        country = supplier.get("country", "")
        gold = supplier.get("is_gold_supplier", False)
        ta = supplier.get("has_trade_assurance", False)

        summary.append(f"""
Product: {title}
Price Range: {price_range}
MOQ: {moq}
Supplier: {sup_name}, {country}
Gold Supplier: {gold}
Trade Assurance: {ta}
""")
    return "\n".join(summary)

# ------------------- 3. Analyze Trimmed Data with Gemini -------------------
def gemini_market_analysis(trimmed_data, target_market):
    prompt = f"""
You are a professional cross-border e-commerce business analyst.
Analyze this Alibaba product data and give a clear structured report:
1. Is this product profitable & good for selling in {target_market}?
2. Price range evaluation & profit potential
3. MOQ risk for small importers
4. Supplier reliability (Gold Supplier / Trade Assurance)
5. Competition level
6. Final clear recommendation

Alibaba Product Data:
{trimmed_data}
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# ------------------- Sidebar -------------------
with st.sidebar:
    st.title("📊 MarketLens AI")
    st.markdown("---")
    st.markdown("### Menu")
    st.write("🏠 Home")
    st.write("🔎 Product Market Analysis")
    st.write("📈 Market Data")
    st.write("👥 Team")
    st.markdown("---")
    st.success("Alibaba + Gemini AI")

# ------------------- Main UI -------------------
st.title("MarketLens AI")
st.subheader("Alibaba Live Data → MarketLens AI Analysis")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔎 Product Analysis", "📈 Market Data", "👥 Team"])

with tab1:
    st.markdown("### Project Workflow")
    st.markdown("""
    <div class="card">
    1. Fetch live Alibaba product data<br>
    2. Auto trim only useful info<br>
    3. Send clean summary to Gemini<br>
    4. Get professional market analysis report
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔎 Product Market Analyzer")
    product_query = st.text_input("Enter product name:", value="wireless headphones")
    target_market = st.selectbox("Target Market", ["India", "ASEAN", "Middle East", "Europe", "Global"])

    if st.button("Run AI Analysis"):
        with st.spinner("Fetching Alibaba data..."):
            alibaba_data = get_alibaba_data(product_query)

        if "error" in alibaba_data:
            st.error(alibaba_data["error"])
        else:
            # Trim big JSON to small summary
            trimmed = trim_alibaba_for_ai(alibaba_data)
            with st.spinner("MarketLens AI analyzing..."):
                report = gemini_market_analysis(trimmed, target_market)
            st.markdown("## 📋 MarketLens AI Final Analysis Report")
            st.success(report)

with tab3:
    st.markdown("### Global Market Demand Dashboard")
    data = {
        "Market": ["China", "ASEAN", "Middle East", "Europe", "India"],
        "Electronics": [92, 88, 85, 80, 94],
        "Home Goods": [85, 90, 83, 78, 72],
        "Apparel": [70, 75, 80, 88, 86]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("Market"), height=350)

with tab4:
    st.markdown("### Our Team")
    st.write("**Abdullah Bin Fahad** | 阿卜杜拉 | Project Leader")
    st.write("**Rokeya Zaman** | 罗基亚 | AI Researcher")
    st.write("**Shayne Lorraine** | 谢恩 | UI/UX Designer")
    st.write("**Revy Syawal Rizki** | 雷维 | Data Engineer")
    st.write("**Brian Mavenrich** | 布莱恩 | Market Specialist")
    st.markdown("### Advisors")
    st.write("Liu Liu | 刘琬")
    st.write("Zhang Junqiang | 张军强")

st.divider()
st.markdown("<p style='text-align:center; color:#888;'>© 2026 MarketLens AI | Alibaba + Gemini Integrated</p>", unsafe_allow_html=True)
