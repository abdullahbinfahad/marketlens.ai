"""
Scoring Algorithms for MarketLens AI
Perfect formulas for market opportunity analysis
Python 3.14+ compatible
"""

import pandas as pd
from typing import Dict, Any


def normalize_score(value: float, min_val: float = 0, max_val: float = 100) -> float:
    """Normalize a value to 0-100 scale."""
    if max_val == min_val:
        return 50.0
    normalized = ((value - min_val) / (max_val - min_val)) * 100
    return max(0, min(100, normalized))


def calculate_demand_score(product: Dict[str, Any]) -> float:
    """
    Calculate demand score (0-100).
    
    Formula: (Search_Volume × 0.35) + (Sales_Velocity × 0.40) + 
             (Reviews × 0.15) + (Trend × 0.10)
    """
    search_volume = normalize_score(
        product.get("search_volume_30d", 5000),
        min_val=1000,
        max_val=50000
    )
    
    sales_velocity = normalize_score(
        product.get("sales_velocity_weekly", 100),
        min_val=10,
        max_val=500
    )
    
    reviews = normalize_score(
        product.get("review_count", 1000),
        min_val=100,
        max_val=5000
    )
    
    trend = product.get("trend_score", 60)
    
    demand_score = (search_volume * 0.35) + (sales_velocity * 0.40) + (reviews * 0.15) + (trend * 0.10)
    
    return round(max(0, min(100, demand_score)), 1)


def calculate_profit_score(product: Dict[str, Any]) -> float:
    """
    Calculate profit score (0-100).
    
    Formula: (Price_Competitiveness × 0.40) + (Rating × 0.35) + 
             (Competition_Efficiency × 0.25)
    """
    # Price competitiveness (higher price = better margins, but lower demand)
    price = product.get("price", 50)
    price_score = normalize_score(price, min_val=10, max_val=300)
    
    # Rating (higher rating = better conversion)
    rating = product.get("avg_rating", 4.0)
    rating_score = normalize_score(rating, min_val=1.0, max_val=5.0)
    
    # Competition efficiency (fewer competitors = better margins)
    competitor_count = product.get("competitor_count", 50)
    competition_efficiency = normalize_score(
        100 - competitor_count,
        min_val=0,
        max_val=100
    )
    
    profit_score = (price_score * 0.40) + (rating_score * 0.35) + (competition_efficiency * 0.25)
    
    return round(max(0, min(100, profit_score)), 1)


def calculate_risk_score(product: Dict[str, Any]) -> float:
    """
    Calculate risk score (0-100).
    Higher score = higher risk.
    
    Formula: (Market_Saturation × 0.50) + (Competitor_Penalty × 0.35) + 
             (Rating_Risk × 0.15)
    """
    # Market saturation risk
    market_saturation = product.get("market_saturation", 50)
    saturation_score = normalize_score(market_saturation, min_val=0, max_val=100)
    
    # Competitor risk
    competitor_count = product.get("competitor_count", 50)
    competitor_penalty = normalize_score(competitor_count, min_val=10, max_val=200)
    
    # Rating risk (low rating = higher risk)
    rating = product.get("avg_rating", 4.0)
    rating_risk = 100 - normalize_score(rating, min_val=1.0, max_val=5.0)
    
    risk_score = (saturation_score * 0.50) + (competitor_penalty * 0.35) + (rating_risk * 0.15)
    
    return round(max(0, min(100, risk_score)), 1)


def calculate_competition_gap_score(gap_score_from_ai: float = 50) -> float:
    """
    Use AI-detected competition gap score.
    
    This comes from sentiment analysis of customer reviews.
    """
    return round(max(0, min(100, gap_score_from_ai)), 1)


def calculate_overall_score(
    demand_score: float,
    profit_score: float,
    risk_score: float,
    competition_gap_score: float
) -> float:
    """
    Calculate overall market opportunity score.
    
    Formula: (Demand × 0.40) + (Profit × 0.30) - (Risk × 0.20) + 
             (Competition_Gap × 0.10)
    """
    overall = (demand_score * 0.40) + (profit_score * 0.30) - (risk_score * 0.20) + (competition_gap_score * 0.10)
    
    return round(max(0, min(100, overall)), 1)


def get_verdict(overall_score: float) -> str:
    """Determine verdict based on overall score."""
    if overall_score >= 75:
        return "GO"
    elif overall_score >= 50:
        return "CAUTION"
    else:
        return "PASS"


def get_verdict_explanation(verdict: str, overall_score: float) -> str:
    """Get explanation for the verdict."""
    explanations = {
        "GO": f"Strong market opportunity detected (Score: {overall_score}/100). This product shows excellent potential with strong demand, good profit margins, and manageable risks. Proceed with confidence.",
        "CAUTION": f"Moderate market opportunity (Score: {overall_score}/100). This product has potential but requires careful risk management. Consider market conditions and competition before proceeding.",
        "PASS": f"High risk detected (Score: {overall_score}/100). This product faces significant market challenges. Consider pivoting to a different product or market segment.",
    }
    return explanations.get(verdict, "Unable to determine verdict.")


def calculate_all_scores(product: Dict[str, Any], gap_score_from_ai: float = 50) -> Dict[str, Any]:
    """
    Calculate all scores and verdicts for a product.
    
    Args:
        product: Product dictionary with all metrics
        gap_score_from_ai: Competition gap score from sentiment analysis
        
    Returns:
        Dictionary with all scores and verdict
    """
    demand_score = calculate_demand_score(product)
    profit_score = calculate_profit_score(product)
    risk_score = calculate_risk_score(product)
    competition_gap_score = calculate_competition_gap_score(gap_score_from_ai)
    overall_score = calculate_overall_score(demand_score, profit_score, risk_score, competition_gap_score)
    
    verdict = get_verdict(overall_score)
    verdict_explanation = get_verdict_explanation(verdict, overall_score)
    
    return {
        "demand_score": demand_score,
        "profit_score": profit_score,
        "risk_score": risk_score,
        "competition_gap_score": competition_gap_score,
        "overall_score": overall_score,
        "verdict": verdict,
        "verdict_explanation": verdict_explanation,
    }


def get_score_interpretation(score: float) -> str:
    """Get interpretation of a score."""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    else:
        return "Poor"


if __name__ == "__main__":
    # Test the algorithms
    test_product = {
        "product_name": "Wireless Earbuds Pro",
        "price": 89.99,
        "avg_rating": 4.3,
        "review_count": 2500,
        "search_volume_30d": 15000,
        "sales_velocity_weekly": 150,
        "trend_score": 75,
        "competitor_count": 45,
        "market_saturation": 65,
    }
    
    results = calculate_all_scores(test_product, gap_score_from_ai=72)
    
    print("Test Product Scores:")
    for key, value in results.items():
        print(f"  {key}: {value}")
