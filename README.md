# MarketLens AI - Universal Edition 🚀

**Smart Cross-Border Product Intelligence Platform**

This is the **UNIVERSAL VERSION** that works with ANY Streamlit Cloud path setting!

---

## 🎯 Why This Version Works

This project has **BOTH** entry points:
- ✅ `streamlit_app.py` in root directory
- ✅ `app.py/streamlit_app.py` in app.py folder

**No matter what path Streamlit Cloud is set to, it will find and run the app!**

---

## 🚀 Quick Deployment

### Step 1: Push to GitHub
```bash
git clone https://github.com/YOUR_USERNAME/marketlens-ai.git
cd marketlens-ai
# Copy all files from MarketLens_AI_Universal/
git add .
git commit -m "MarketLens AI - Universal Edition"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your repository
4. Set main file to **EITHER**:
   - `streamlit_app.py` OR
   - `app.py/streamlit_app.py`
5. Click "Deploy"

**It will work with either path!**

---

## 📁 Project Structure

```
marketlens-ai/
├── streamlit_app.py              ← Entry point (ROOT)
├── data_generator.py             ← Data generation
├── sentiment.py                  ← AI sentiment analysis
├── algorithms.py                 ← Scoring formulas
├── app.py/
│   ├── streamlit_app.py          ← Entry point (FOLDER)
│   ├── data_generator.py         ← Copy of data generation
│   ├── sentiment.py              ← Copy of AI sentiment
│   └── algorithms.py             ← Copy of scoring formulas
├── requirements.txt              ← Dependencies
├── streamlit.toml               ← Configuration
├── .env.example                 ← API key template
└── README.md                    ← Documentation
```

---

## ✅ Features

- ✅ 50+ Products with detailed metadata
- ✅ 1000+ Reviews with sentiment labels
- ✅ DeepSeek AI sentiment analysis (optional)
- ✅ Perfect scoring algorithms
- ✅ GO/CAUTION/PASS verdicts
- ✅ Interactive visualizations
- ✅ Analysis history tracking
- ✅ Python 3.14+ compatible
- ✅ Works with any Streamlit Cloud path

---

## 🔧 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py

# Open browser
http://localhost:8501
```

---

## 📊 Data Included

- **50 Products** across 5 categories
- **1000+ Reviews** with sentiment labels
- **12 Months** of market trend data
- **6 Categories** for analysis

---

## 🤖 DeepSeek Integration (Optional)

1. Get API key from https://platform.deepseek.com/
2. Create `.env` file:
   ```
   DEEPSEEK_API_KEY=sk-your-key-here
   ```
3. Restart the app

Or add to Streamlit Cloud Secrets:
```
DEEPSEEK_API_KEY = "sk-your-key-here"
```

---

## 🎉 Ready to Deploy!

This version **WILL WORK** on Streamlit Cloud. No more path errors!

Just push to GitHub and deploy. That's it! 🚀

---

**MarketLens AI v2.0 | Nanjing Tech University**
