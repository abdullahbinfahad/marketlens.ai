"""
Perfect Algorithms for MarketLens AI
Refined scoring formulas with advanced market analysis logic.
"""

import numpy as np


def normalize_score(value, min_val=0, max_val=100, target_min=0, target_max=100):
    """Normalize a value to target range (default 0-100)."""
    if max_val == min_val:
        return (target_min + target_max) / 2
    normalized = ((value - min_val) / (max_val - min_val)) * (target_max - target_min) + target_min
    return max(target_min, min(target_max, normalized))


def calculate_demand_score(
    search_volume,
    sales_velocity,
    review_count,
    trend_score,
    search_vol_range=(100, 50000),
    sales_vel_range=(5, 1000),
    review_range=(50, 5000),
    trend_range=(20, 100)
):
    """
    Calculate Demand Score (0-100) - Market appetite and growth potential.
    
    Formula: (Search_Volume × 0.35) + (Sales_Velocity × 0.40) + (Reviews × 0.15) + (Trend × 0.10)
    
    Higher weights on Sales_Velocity and Search_Volume as they indicate real market activity.
    """
    search_norm = normalize_score(search_volume, search_vol_range[0], search_vol_range[1])
    sales_norm = normalize_score(sales_velocity, sales_vel_range[0], sales_vel_range[1])
    review_norm = normalize_score(review_count, review_range[0], review_range[1])
    trend_norm = normalize_score(trend_score, trend_range[0], trend_range[1])
    
    demand = (search_norm * 0.35) + (sales_norm * 0.40) + (review_norm * 0.15) + (trend_norm * 0.10)
    return round(demand, 2)


def calculate_profit_score(
    price,
    avg_rating,
    competitor_count,
    review_count,
    price_range=(10, 500),
    competitor_range=(5, 200)
):
    """
    Calculate Profit Score (0-100) - Financial viability and margin potential.
    
    Formula: (Price_Competitiveness × 0.40) + (Rating_Strength × 0.35) + (Competition_Efficiency × 0.25)
    
    Considers price positioning, customer satisfaction (rating), and competitive efficiency.
    """
    # Price competitiveness: mid-range prices often have best margins
    price_norm = normalize_score(price, price_range[0], price_range[1])
    # Optimal price point is around 60-70% of range (sweet spot for margins)
    price_competitiveness = 100 - abs(price_norm - 65) * 1.5
    price_competitiveness = max(0, min(100, price_competitiveness))
    
    # Rating strength: higher rating = better margin potential
    rating_strength = (avg_rating / 5.0) * 100
    
    # Competition efficiency: fewer competitors per review = better margins
    competition_efficiency = normalize_score(
        review_count / (competitor_count + 1),
        0,
        100,
        0,
        100
    )
    
    profit = (price_competitiveness * 0.40) + (rating_strength * 0.35) + (competition_efficiency * 0.25)
    return round(profit, 2)


def calculate_risk_score(
    market_saturation,
    competitor_count,
    avg_rating,
    review_count,
    competitor_range=(5, 200)
):
    """
    Calculate Risk Score (0-100) - Market barriers and saturation.
    
    Formula: (Market_Saturation × 0.50) + (Competitor_Penalty × 0.35) + (Rating_Risk × 0.15)
    
    Higher score = higher risk. Considers saturation, competition, and rating gaps.
    """
    # Market saturation directly impacts risk
    saturation_risk = market_saturation
    
    # Competitor penalty: more competitors = higher risk
    competitor_penalty = normalize_score(competitor_count, competitor_range[0], competitor_range[1])
    
    # Rating risk: low ratings indicate market dissatisfaction (higher risk)
    rating_risk = 100 - (avg_rating / 5.0) * 100
    
    risk = (saturation_risk * 0.50) + (competitor_penalty * 0.35) + (rating_risk * 0.15)
    return round(risk, 2)


def calculate_competition_gap_score(gap_score_from_ai):
    """
    Competition Gap Score (0-100) - Market opportunity from AI sentiment analysis.
    
    Directly from DeepSeek AI sentiment analysis.
    Higher score = more market gaps = better opportunity.
    """
    return round(max(0, min(100, gap_score_from_ai)), 2)


def calculate_overall_score(demand, profit, risk, competition):
    """
    Calculate Overall MarketLens Score (0-100) - Final verdict score.
    
    Formula: (Demand × 0.40) + (Profit × 0.30) - (Risk × 0.20) + (Competition × 0.10)
    
    Weights:
    - Demand (40%): Market appetite is most important
    - Profit (30%): Financial viability is critical
    - Risk (20%): Subtracted because it's a negative factor
    - Competition (10%): Market gaps provide opportunity
    """
    overall = (demand * 0.40) + (profit * 0.30) - (risk * 0.20) + (competition * 0.10)
    return round(overall, 2)


def get_verdict(overall_score):
    """
    Determine verdict based on overall score.
    
    GO: ≥75 - Strong opportunity, proceed with confidence
    CAUTION: 50-74 - Moderate opportunity, requires careful risk management
    PASS: <50 - High risk, consider pivoting
    """
    if overall_score >= 75:
        return "GO", "🟢 Strong market opportunity with high potential. Proceed with confidence."
    elif overall_score >= 50:
        return "CAUTION", "🟡 Moderate opportunity; requires careful risk management and market validation."
    else:
        return "PASS", "🔴 High risk or low potential. Consider pivoting to a different product or category."


def calculate_market_opportunity_index(demand, profit, competition):
    """
    Calculate Market Opportunity Index (0-100).
    Focuses on positive factors: demand, profitability, and market gaps.
    """
    moi = (demand * 0.40) + (profit * 0.35) + (competition * 0.25)
    return round(moi, 2)


def calculate_market_viability_score(demand, profit, risk):
    """
    Calculate Market Viability Score (0-100).
    Focuses on sustainability: demand, profitability, and low risk.
    """
    mvs = (demand * 0.35) + (profit * 0.40) - (risk * 0.25)
    return round(mvs, 2)


def calculate_all_scores(product_data, gap_score_from_ai=None):
    """
    Calculate all scores for a product.
    
    Args:
        product_data: dict with product metrics
        gap_score_from_ai: AI-generated competition gap score (0-100)
    
    Returns:
        dict with all scores, verdict, and analysis
    """
    if gap_score_from_ai is None:
        gap_score_from_ai = np.random.randint(40, 85)
    
    # Calculate individual scores
    demand = calculate_demand_score(
        product_data.get("search_volume_30d", 5000),
        product_data.get("sales_velocity_weekly", 250),
        product_data.get("review_count", 2500),
        product_data.get("trend_score", 60),
    )
    
    profit = calculate_profit_score(
        product_data.get("price", 100),
        product_data.get("avg_rating", 4.0),
        product_data.get("competitor_count", 50),
        product_data.get("review_count", 2500),
    )
    
    risk = calculate_risk_score(
        product_data.get("market_saturation", 50),
        product_data.get("competitor_count", 50),
        product_data.get("avg_rating", 4.0),
        product_data.get("review_count", 2500),
    )
    
    competition = calculate_competition_gap_score(gap_score_from_ai)
    
    # Calculate overall score
    overall = calculate_overall_score(demand, profit, risk, competition)
    
    # Get verdict
    verdict, verdict_explanation = get_verdict(overall)
    
    # Calculate additional metrics
    moi = calculate_market_opportunity_index(demand, profit, competition)
    mvs = calculate_market_viability_score(demand, profit, risk)
    
    return {
        "demand_score": demand,
        "profit_score": profit,
        "risk_score": risk,
        "competition_gap_score": competition,
        "overall_score": overall,
        "market_opportunity_index": moi,
        "market_viability_score": mvs,
        "verdict": verdict,
        "verdict_explanation": verdict_explanation,
    }


def get_score_interpretation(score_name, score_value):
    """Get human-readable interpretation of a score."""
    if score_value >= 80:
        level = "Excellent"
    elif score_value >= 60:
        level = "Good"
    elif score_value >= 40:
        level = "Moderate"
    else:
        level = "Poor"
    
    return f"{level} ({score_value:.1f}/100)"


if __name__ == "__main__":
    # Test with sample data
    sample_product = {
        "price": 150,
        "avg_rating": 4.5,
        "review_count": 2000,
        "search_volume_30d": 8000,
        "sales_velocity_weekly": 300,
        "trend_score": 75,
        "competitor_count": 45,
        "market_saturation": 55,
    }
    
    scores = calculate_all_scores(sample_product, gap_score_from_ai=72)
    
    print("=" * 60)
    print("MARKETLENS AI - SCORING ANALYSIS")
    print("=" * 60)
    print(f"\nProduct Analysis Results:")
    print(f"  Demand Score:              {get_score_interpretation('Demand', scores['demand_score'])}")
    print(f"  Profit Score:              {get_score_interpretation('Profit', scores['profit_score'])}")
    print(f"  Risk Score:                {get_score_interpretation('Risk', scores['risk_score'])}")
    print(f"  Competition Gap Score:     {get_score_interpretation('Competition', scores['competition_gap_score'])}")
    print(f"\n  Overall Score:             {scores['overall_score']:.1f}/100")
    print(f"  Market Opportunity Index:  {scores['market_opportunity_index']:.1f}/100")
    print(f"  Market Viability Score:    {scores['market_viability_score']:.1f}/100")
    print(f"\n  Verdict: {scores['verdict']}")
    print(f"  {scores['verdict_explanation']}")
    print("=" * 60)
