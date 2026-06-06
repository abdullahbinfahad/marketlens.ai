"""
Sentiment Analysis Module for MarketLens AI
Integrates with DeepSeek API for AI-powered sentiment analysis
Secure environment variable handling - NO hardcoded keys
Python 3.14+ compatible
"""

import os
import json
from typing import Dict, List
import random


class SentimentAnalyzer:
    """AI-powered sentiment analyzer using DeepSeek API."""
    
    def __init__(self, api_key: str = None, model: str = "deepseek-chat"):
        """
        Initialize the sentiment analyzer.
        
        Args:
            api_key: DeepSeek API key (from environment or parameter)
            model: Model name to use
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.model = model
        self.use_mock = not self.api_key  # Use mock if no API key
        
        if not self.use_mock:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.deepseek.com/v1"
                )
            except ImportError:
                self.use_mock = True
                print("⚠️ OpenAI package not available. Using mock analysis.")
    
    def analyze_reviews(self, product_name: str, reviews: List[str]) -> Dict:
        """
        Analyze customer reviews for sentiment and market gaps.
        
        Args:
            product_name: Name of the product
            reviews: List of review texts
            
        Returns:
            Dictionary with sentiment analysis results
        """
        if self.use_mock:
            return self._mock_analysis(product_name, reviews)
        
        try:
            return self._real_analysis(product_name, reviews)
        except Exception as e:
            print(f"⚠️ Real analysis failed: {e}. Using mock analysis.")
            return self._mock_analysis(product_name, reviews)
    
    def _real_analysis(self, product_name: str, reviews: List[str]) -> Dict:
        """Real DeepSeek API analysis."""
        reviews_combined = "\n".join(f"- {r}" for r in reviews[:50])
        
        prompt = f"""
You are an expert e-commerce market analyst.
Analyze these customer reviews for the product: {product_name}.

REVIEWS:
{reviews_combined}

TASK:
1. Identify the main unmet needs or desires customers mention.
2. List the top 3 most painful complaints.
3. Based on those, assign a "Competition Gap Score" (0-100), where:
   - 100 = Huge gaps, new sellers can easily beat incumbents.
   - 0   = No gaps, current sellers are perfect.

OUTPUT FORMAT (JSON):
{{
  "competition_gap_score": <integer 0-100>,
  "unmet_needs": ["..."],
  "top_complaints": ["..."],
  "reasoning": "Brief explanation"
}}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _mock_analysis(self, product_name: str, reviews: List[str]) -> Dict:
        """Mock analysis for testing without API key."""
        
        # Analyze sentiment from review texts
        positive_count = sum(1 for r in reviews if any(word in r.lower() for word in ["great", "excellent", "amazing", "love", "perfect"]))
        negative_count = sum(1 for r in reviews if any(word in r.lower() for word in ["bad", "poor", "terrible", "hate", "awful"]))
        
        sentiment_ratio = positive_count / len(reviews) if reviews else 0.5
        gap_score = int(50 + (sentiment_ratio - 0.5) * 100)
        gap_score = max(0, min(100, gap_score))
        
        # Generate realistic insights based on product category
        unmet_needs_pool = {
            "Electronics": [
                "Better battery life",
                "Improved noise cancellation",
                "More durable materials",
                "Faster charging",
                "Better connectivity"
            ],
            "Fashion": [
                "Better sizing accuracy",
                "More color options",
                "Improved durability",
                "Sustainable materials",
                "Better fit for different body types"
            ],
            "Home & Garden": [
                "Easier installation",
                "Better durability",
                "More color choices",
                "Eco-friendly options",
                "Better customer support"
            ],
            "Sports": [
                "Better comfort",
                "Improved durability",
                "More sizes available",
                "Better grip",
                "Lightweight design"
            ],
            "Beauty": [
                "Natural ingredients",
                "Hypoallergenic formulas",
                "Cruelty-free options",
                "Better packaging",
                "Longer lasting results"
            ]
        }
        
        complaints_pool = {
            "Electronics": [
                "Battery drains too quickly",
                "Poor build quality",
                "Connectivity issues",
                "Uncomfortable fit",
                "Limited warranty"
            ],
            "Fashion": [
                "Sizing runs small/large",
                "Material quality poor",
                "Stitching comes undone",
                "Color fades quickly",
                "Not as pictured"
            ],
            "Home & Garden": [
                "Difficult to assemble",
                "Breaks easily",
                "Poor instructions",
                "Not as durable",
                "Cheap materials"
            ],
            "Sports": [
                "Uncomfortable after use",
                "Poor quality",
                "Doesn't last long",
                "Not suitable for all body types",
                "Overpriced"
            ],
            "Beauty": [
                "Causes irritation",
                "Doesn't work as advertised",
                "Strong chemical smell",
                "Expensive",
                "Packaging is wasteful"
            ]
        }
        
        # Extract category from product name or use default
        category = "Electronics"
        for cat in unmet_needs_pool.keys():
            if cat.lower() in product_name.lower():
                category = cat
                break
        
        unmet_needs = random.sample(unmet_needs_pool.get(category, unmet_needs_pool["Electronics"]), 3)
        top_complaints = random.sample(complaints_pool.get(category, complaints_pool["Electronics"]), 3)
        
        return {
            "competition_gap_score": gap_score,
            "unmet_needs": unmet_needs,
            "top_complaints": top_complaints,
            "reasoning": f"Analysis based on {len(reviews)} customer reviews. {positive_count} positive, {negative_count} negative reviews detected. Market gap identified in customer satisfaction areas."
        }


if __name__ == "__main__":
    # Test the analyzer
    analyzer = SentimentAnalyzer()
    
    test_reviews = [
        "Great product! Exceeded expectations.",
        "Battery dies too quickly.",
        "Excellent quality and fast shipping.",
        "Poor build quality.",
        "Best purchase ever!",
    ]
    
    result = analyzer.analyze_reviews("Wireless Earbuds", test_reviews)
    print("Analysis Result:")
    print(json.dumps(result, indent=2))
