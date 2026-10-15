"""AI analytics for sentiment, trends, risk, and explainable decision support."""
from __future__ import annotations

import json
import os
import re
from typing import Any

import requests

from algorithms import calculate_market_score

POSITIVE = {"good", "great", "excellent", "quality", "easy", "durable", "comfortable", "effective", "love", "best", "fast", "premium", "useful"}
NEGATIVE = {"bad", "poor", "broken", "difficult", "slow", "cheap", "waste", "problem", "issue", "hard", "disappointed", "limited", "risk"}


def sentiment_analysis(text: str) -> dict[str, Any]:
    words = re.findall(r"[a-z]+", (text or "").lower())
    positive = sum(word in POSITIVE for word in words)
    negative = sum(word in NEGATIVE for word in words)
    total = max(1, positive + negative)
    score = round(50 + (positive - negative) / total * 50, 2) if positive or negative else None
    label = "positive" if score is not None and score >= 60 else "negative" if score is not None and score <= 40 else "neutral"
    return {"score": score, "label": label, "positive_terms": positive, "negative_terms": negative, "method": "lexicon"}


def _deepseek(prompt: str) -> dict[str, Any] | None:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return None
    response = requests.post("https://api.deepseek.com/chat/completions", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json={"model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"), "temperature": 0.1, "messages": [{"role": "system", "content": "Return strict JSON only. You are the MarketLens analytics engine. Never invent unavailable evidence."}, {"role": "user", "content": prompt}]}, timeout=30)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    content = content[content.find("{"):content.rfind("}") + 1]
    return json.loads(content)


def analyze_product(product: dict[str, Any], comparable_count: int = 0) -> dict[str, Any]:
    description = str(product.get("product_description") or "")
    sentiment = sentiment_analysis(description)
    enriched = dict(product)
    if sentiment["score"] is not None and enriched.get("sentiment_score_overall") in (None, ""):
        enriched["sentiment_score_overall"] = sentiment["score"]
    score = calculate_market_score(enriched)
    trend_signal = "positive" if _number(product.get("discount_percent")) is not None and _number(product.get("discount_percent")) < 25 else "stable"
    if _number(product.get("provider_count")) and _number(product.get("provider_count")) >= 2:
        trend_signal = "cross-provider validation"
    risk_level = score["risk_forecast_level"]
    result = {"sentiment": sentiment, "trend_signal": trend_signal, "risk_level": risk_level, "score": score, "comparable_count": comparable_count, "ai_method": "deterministic fallback"}
    prompt = f"Analyze this product record without inventing missing values. Return JSON with keys trend_signal, risk_level, summary, next_steps. Record: {json.dumps(product, default=str)}. Existing score: {json.dumps(score)}."
    try:
        ai = _deepseek(prompt)
        if ai:
            result.update(ai)
            result["ai_method"] = "DeepSeek"
    except Exception as exc:
        result["ai_error"] = str(exc)
    return result


def _number(value: Any) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None
