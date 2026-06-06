# MarketLens AI v2.0 - Quick Start Guide 🚀

## 3-Step Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py/streamlit_app.py
```

### Step 3: Open Browser
Navigate to: **http://localhost:8501**

---

## That's It! 🎉

The app will automatically:
- ✅ Load 50 products
- ✅ Generate 1000 reviews
- ✅ Initialize all features
- ✅ Cache data for fast performance

---

## Optional: Add DeepSeek AI

For real sentiment analysis:

1. Get API key from https://platform.deepseek.com/
2. Create `.env` file:
   ```
   DEEPSEEK_API_KEY=sk-your-key-here
   ```
3. Restart the app

---

## Features

- **📊 50+ Products** with detailed metadata
- **📝 1000+ Reviews** with sentiment labels
- **🤖 AI Sentiment Analysis** via DeepSeek
- **📈 Perfect Algorithms** for scoring
- **🎯 GO/CAUTION/PASS Verdicts**
- **📱 Interactive Visualizations**
- **💾 Analysis History Tracking**

---

## Project Structure

```
MarketLens_AI_v2/
├── app.py/
│   └── streamlit_app.py          # Main app (all UI here)
├── data_generator.py              # 50 products, 1000 reviews
├── sentiment.py                   # DeepSeek integration
├── algorithms.py                  # Perfect scoring formulas
├── requirements.txt               # Dependencies
└── README.md                      # Full documentation
```

---

## Need Help?

- Check **README.md** for detailed documentation
- Visit https://www.marketlens-ai.com/
- Email: support@marketlens-ai.com

---

**Ready to analyze products? Let's go! 🎯**
