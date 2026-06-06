# MarketLens AI v2.0 🎯

**Smart Cross-Border Product Intelligence Platform**

MarketLens AI is an intelligent decision-making agent for cross-border e-commerce. It analyzes **50+ products** with **1000+ customer reviews** using **DeepSeek AI** to identify market gaps and opportunities.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run app.py/streamlit_app.py
```

### 3. Open Browser
Navigate to: `http://localhost:8501`

---

## 📊 Project Structure

```
MarketLens_AI_v2/
├── app.py/
│   └── streamlit_app.py          # Main Streamlit application
├── data_generator.py              # Generates 50+ products, 1000+ reviews
├── sentiment.py                   # DeepSeek sentiment analysis
├── algorithms.py                  # Perfect scoring algorithms
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
└── README.md                      # This file
```

---

## 🎯 Key Features

### ✅ 50+ Detailed Products
- 10 Electronics
- 10 Fashion items
- 10 Home & Garden
- 10 Sports
- 10 Beauty products

### ✅ 1000+ Rich Reviews
- 60% Positive reviews
- 20% Negative reviews
- 20% Neutral reviews
- Verified purchase tracking
- Helpful count metrics

### ✅ AI-Powered Sentiment Analysis
- **DeepSeek API Integration**: Real sentiment analysis
- **Mock Fallback**: Works without API key
- **Gap Detection**: Identifies unmet customer needs
- **Complaint Analysis**: Top 3 complaints per product

### ✅ Perfect Scoring Algorithms

**Demand Score (0-100)**
```
Formula: (Search_Volume × 0.35) + (Sales_Velocity × 0.40) + (Reviews × 0.15) + (Trend × 0.10)
```

**Profit Score (0-100)**
```
Formula: (Price_Competitiveness × 0.40) + (Rating × 0.35) + (Competition_Efficiency × 0.25)
```

**Risk Score (0-100)**
```
Formula: (Market_Saturation × 0.50) + (Competitor_Penalty × 0.35) + (Rating_Risk × 0.15)
```

**Overall Score (0-100)**
```
Formula: (Demand × 0.40) + (Profit × 0.30) - (Risk × 0.20) + (Competition × 0.10)
```

### ✅ Intelligent Verdicts
- **GO (≥75)**: Strong opportunity. Proceed with confidence.
- **CAUTION (50-74)**: Moderate opportunity. Requires careful risk management.
- **PASS (<50)**: High risk. Consider pivoting.

### ✅ Interactive Visualizations
- Gauge charts for each score
- Trend analysis charts
- Category comparison charts
- Sentiment distribution
- Price vs. rating scatter plots

---

## 🤖 DeepSeek Integration

### Optional: Add Real AI Analysis

1. **Get API Key**
   - Visit: https://platform.deepseek.com/
   - Create account and get API key

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your key
   DEEPSEEK_API_KEY=sk-your-key-here
   ```

3. **Restart App**
   ```bash
   streamlit run app.py/streamlit_app.py
   ```

### Without API Key
- App uses mock sentiment analysis
- All features remain fully functional
- Perfect for testing and demos

---

## 📖 Usage Guide

### 1. **Product Analysis Page**
- Select from 50 pre-loaded products OR enter custom details
- Get instant demand, profit, risk, and competition scores
- View AI-identified unmet needs and complaints
- Save analyses to history

### 2. **Trends Page**
- Explore 12 months of market data
- Compare 6 product categories
- Analyze search volume, sales, and sentiment trends
- View category performance statistics

### 3. **Profile Page**
- Track all analyses in history
- Export data as CSV
- View statistics and insights
- Manage API key and settings

### 4. **Research Page**
- Market overview and statistics
- Category performance analysis
- Best practices for success
- Risk management strategies

---

## 🔧 Technical Details

### Data Generation
- **Products**: 50 realistic e-commerce products with metadata
- **Reviews**: 1000 reviews with sentiment labels and ratings
- **Trends**: 12 months of market data across 6 categories
- All data is cached for fast performance

### Sentiment Analysis
- Analyzes up to 50 reviews per product
- Identifies unmet needs and pain points
- Generates competition gap scores (0-100)
- Provides actionable reasoning

### Algorithms
- Normalized scoring (0-100 scale)
- Weighted formulas for accuracy
- Market opportunity index calculation
- Market viability scoring

---

## 📊 Data Sample

### Products Include:
- Wireless Earbuds Pro ($89.99, 4.3★)
- Noise Cancelling Headphones ($199.99, 4.6★)
- Smart Watch Series 5 ($299.99, 4.4★)
- Cotton T-Shirt Pack ($34.99, 4.4★)
- Yoga Mat Non-Slip ($24.99, 4.6★)
- And 45 more...

### Reviews Include:
- "Excellent product! Exceeded my expectations."
- "Poor quality. Broke after a week."
- "It's okay, nothing special."
- And 997 more...

---

## 🎨 UI/UX Features

- **Modern Design**: Gradient backgrounds, rounded cards
- **Responsive Layout**: Works on desktop and tablet
- **Interactive Charts**: Plotly-powered visualizations
- **Smooth Animations**: Hover effects and transitions
- **Color Palette**: Purple, pink, green, and red gradients

---

## 🔐 Security & Privacy

- All data stored locally in browser session
- No cloud uploads or external storage
- API keys stored locally, never transmitted
- Open source codebase for transparency

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
streamlit run app.py/streamlit_app.py --server.port 8502
```

### Clear Cache
```bash
streamlit cache clear
```

### API Key Issues
- Verify key is correct in `.env`
- Check API has sufficient credits
- App will fall back to mock analysis if key fails

---

## 📈 Performance

- **Page Load**: <2 seconds (with caching)
- **Analysis Time**: <1 second
- **Memory Usage**: <300MB
- **Data Size**: 50 products, 1000 reviews, 72 trend records

---

## 🚀 Deployment

### Local Deployment
```bash
streamlit run app.py/streamlit_app.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Configure environment variables
4. Deploy with one click

### Docker
```bash
docker build -t marketlens-ai .
docker run -p 8501:8501 marketlens-ai
```

---

## 📝 License

MarketLens AI v2.0 - Nanjing Tech University

**Team:**
- Abdullah Bin Fahad (Team Captain)
- Rokeya Zaman (Data Scientist & AI)
- Shayne Lorraine (Full-Stack Developer)
- Revy Syawal Rizki (Backend Engineer)
- Brian Mavenrich (Frontend & Data Analytics)

---

## 📧 Support

- **Website**: https://www.marketlens-ai.com/
- **Email**: support@marketlens-ai.com
- **GitHub**: https://github.com/marketlens-ai

---

**Built with ❤️ for global e-commerce sellers**

*MarketLens AI - Smart decisions, better products, global success.*
