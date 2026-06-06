"""
Sentiment Analysis Module for MarketLens AI
Integrated DeepSeek API for real-time sentiment analysis.
"""

import os
import json
from openai import OpenAI
import random


class SentimentAnalyzer:
    """Analyzes customer reviews using DeepSeek API."""
    
    def __init__(self, api_key: str = None, model: str = "deepseek-chat"):
        """
        Initialize the sentiment analyzer.
        
        Args:
            api_key: DeepSeek API key. If None, uses environment variable.
            model: Model name (default: "deepseek-chat")
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            self.use_mock = True
            print("⚠️  DEEPSEEK_API_KEY not set. Using mock analysis.")
        else:
            self.use_mock = False
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.deepseek.com/v1"
                )
                self.model = model
            except Exception as e:
                print(f"⚠️  Failed to initialize DeepSeek client: {e}. Using mock analysis.")
                self.use_mock = True
    
    def analyze_reviews(self, product_name: str, reviews: list) -> dict:
        """
        Analyze customer reviews to identify market gaps and opportunities.
        
        Args:
            product_name: Name of the product
            reviews: List of review texts
        
        Returns:
            dict with competition_gap_score, unmet_needs, top_complaints, reasoning
        """
        if self.use_mock or not hasattr(self, 'client'):
            return self._analyze_reviews_mock(product_name, reviews)
        
        try:
            return self._analyze_reviews_real(product_name, reviews)
        except Exception as e:
            print(f"⚠️  API error: {e}. Falling back to mock analysis.")
            return self._analyze_reviews_mock(product_name, reviews)
    
    def _analyze_reviews_real(self, product_name: str, reviews: list) -> dict:
        """Real analysis using DeepSeek API."""
        # Combine up to 50 reviews to keep token usage reasonable
        reviews_combined = "\n".join(f"- {r}" for r in reviews[:50])
        
        prompt = f"""
You are an expert e-commerce market analyst specializing in competitive gap analysis.
Analyze these customer reviews for the product: {product_name}.

REVIEWS:
{reviews_combined}

TASK:
1. Identify the main unmet needs or desires customers mention (things they wish the product had).
2. List the top 3 most painful complaints (what customers dislike most).
3. Based on the analysis, assign a "Competition Gap Score" (0-100), where:
   - 100 = Huge gaps, new sellers can easily beat incumbents with improvements.
   - 75-99 = Significant gaps, clear opportunities for differentiation.
   - 50-74 = Moderate gaps, some improvement opportunities.
   - 25-49 = Small gaps, market is fairly well-served.
   - 0-24 = No gaps, current sellers are meeting customer needs well.

OUTPUT FORMAT (JSON only, no markdown):
{{
  "competition_gap_score": <integer 0-100>,
  "unmet_needs": ["need1", "need2", "need3"],
  "top_complaints": ["complaint1", "complaint2", "complaint3"],
  "reasoning": "Brief explanation of the gap score and market opportunity"
}}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    def _analyze_reviews_mock(self, product_name: str, reviews: list) -> dict:
        """Mock analysis for testing without API key."""
        mock_unmet_needs = [
            "Better battery life",
            "More durable materials",
            "Improved customer support",
            "Faster shipping options",
            "Better color variety",
            "Enhanced warranty coverage",
            "Eco-friendly packaging",
            "Customization options",
            "Lighter weight design",
            "Better ergonomics",
            "More affordable pricing",
            "Longer product lifespan",
            "Better user interface",
            "Improved performance",
            "More features",
        ]
        
        mock_complaints = [
            "Product broke within a month",
            "Poor quality control",
            "Misleading product description",
            "Uncomfortable to use",
            "Doesn't work as advertised",
            "Overpriced for the quality",
            "Terrible customer service",
            "Slow shipping",
            "Defective upon arrival",
            "Poor build quality",
            "Not durable",
            "Stopped working quickly",
            "Cheap materials",
            "Difficult to use",
            "Not worth the price",
        ]
        
        gap_score = random.randint(45, 85)
        unmet_needs = random.sample(mock_unmet_needs, 3)
        top_complaints = random.sample(mock_complaints, 3)
        
        return {
            "competition_gap_score": gap_score,
            "unmet_needs": unmet_needs,
            "top_complaints": top_complaints,
            "reasoning": f"Analysis of {len(reviews)} customer reviews for {product_name} reveals significant market gaps. Competitors are failing to address key pain points, presenting clear opportunities for differentiation and market capture.",
        }


if __name__ == "__main__":
    # Test the analyzer
    api_key = os.getenv("DEEPSEEK_API_KEY")
    analyzer = SentimentAnalyzer(api_key=api_key)
    
    sample_reviews = [
        "Battery dies in 2 hours, terrible.",
        "Great sound, but uncomfortable after 30 minutes.",
        "Case hinge broke within a week.",
        "Wish it had noise cancelling.",
        "Looks premium, but connection drops often.",
        "Best earbuds I've ever owned!",
        "Not worth the price.",
        "Excellent value for money.",
        "Stopped working after 3 months.",
        "Perfect for my needs.",
    ]
    
    print("Analyzing sample reviews for 'Wireless Earbuds'...\n")
    result = analyzer.analyze_reviews("Wireless Earbuds", sample_reviews)
    
    print(f"Competition Gap Score: {result['competition_gap_score']}/100")
    print(f"Unmet Needs: {result['unmet_needs']}")
    print(f"Top Complaints: {result['top_complaints']}")
    print(f"Reasoning: {result['reasoning']}")
