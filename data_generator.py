"""
Enhanced Data Generator for MarketLens AI
Generates 50+ realistic products and 1000+ detailed reviews with rich metadata.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Comprehensive product database
PRODUCTS_DATA = [
    # Electronics
    {"name": "Wireless Earbuds Pro", "category": "Electronics", "base_price": 89.99, "base_rating": 4.3},
    {"name": "Noise Cancelling Headphones", "category": "Electronics", "base_price": 199.99, "base_rating": 4.6},
    {"name": "Smart Watch Series 5", "category": "Electronics", "base_price": 299.99, "base_rating": 4.4},
    {"name": "USB-C Fast Charger", "category": "Electronics", "base_price": 29.99, "base_rating": 4.7},
    {"name": "Portable Power Bank 30000mAh", "category": "Electronics", "base_price": 49.99, "base_rating": 4.5},
    {"name": "4K Webcam with Microphone", "category": "Electronics", "base_price": 79.99, "base_rating": 4.2},
    {"name": "Bluetooth Speaker Waterproof", "category": "Electronics", "base_price": 59.99, "base_rating": 4.4},
    {"name": "Phone Tripod Stand", "category": "Electronics", "base_price": 19.99, "base_rating": 4.6},
    {"name": "Wireless Mouse and Keyboard Set", "category": "Electronics", "base_price": 39.99, "base_rating": 4.3},
    {"name": "USB Hub 7-Port", "category": "Electronics", "base_price": 24.99, "base_rating": 4.5},
    
    # Fashion
    {"name": "Cotton T-Shirt Pack (5)", "category": "Fashion", "base_price": 34.99, "base_rating": 4.4},
    {"name": "Slim Fit Jeans Blue", "category": "Fashion", "base_price": 49.99, "base_rating": 4.3},
    {"name": "Casual Sneakers White", "category": "Fashion", "base_price": 69.99, "base_rating": 4.5},
    {"name": "Winter Puffer Jacket", "category": "Fashion", "base_price": 129.99, "base_rating": 4.6},
    {"name": "Yoga Leggings High Waist", "category": "Fashion", "base_price": 39.99, "base_rating": 4.7},
    {"name": "Sports Bra Set (3 Pack)", "category": "Fashion", "base_price": 44.99, "base_rating": 4.4},
    {"name": "Leather Belt Brown", "category": "Fashion", "base_price": 24.99, "base_rating": 4.5},
    {"name": "Hoodie Sweatshirt", "category": "Fashion", "base_price": 44.99, "base_rating": 4.3},
    {"name": "Socks Bundle (12 Pairs)", "category": "Fashion", "base_price": 19.99, "base_rating": 4.6},
    {"name": "Baseball Cap Adjustable", "category": "Fashion", "base_price": 14.99, "base_rating": 4.4},
    
    # Home & Garden
    {"name": "LED Smart Light Bulbs (4-Pack)", "category": "Home & Garden", "base_price": 39.99, "base_rating": 4.5},
    {"name": "Bamboo Cutting Board Set", "category": "Home & Garden", "base_price": 29.99, "base_rating": 4.6},
    {"name": "Stainless Steel Cookware Set", "category": "Home & Garden", "base_price": 99.99, "base_rating": 4.4},
    {"name": "Non-Stick Frying Pan", "category": "Home & Garden", "base_price": 24.99, "base_rating": 4.5},
    {"name": "Microfiber Cleaning Cloth (10-Pack)", "category": "Home & Garden", "base_price": 12.99, "base_rating": 4.7},
    {"name": "Bamboo Shelf Organizer", "category": "Home & Garden", "base_price": 34.99, "base_rating": 4.4},
    {"name": "Air Purifier HEPA Filter", "category": "Home & Garden", "base_price": 79.99, "base_rating": 4.3},
    {"name": "Humidifier Ultrasonic", "category": "Home & Garden", "base_price": 44.99, "base_rating": 4.5},
    {"name": "Plant Pot Set (6)", "category": "Home & Garden", "base_price": 19.99, "base_rating": 4.6},
    {"name": "Kitchen Knife Set (8-Piece)", "category": "Home & Garden", "base_price": 49.99, "base_rating": 4.4},
    
    # Sports
    {"name": "Yoga Mat Non-Slip", "category": "Sports", "base_price": 24.99, "base_rating": 4.6},
    {"name": "Dumbbell Set Adjustable", "category": "Sports", "base_price": 79.99, "base_rating": 4.5},
    {"name": "Resistance Bands Set (5)", "category": "Sports", "base_price": 19.99, "base_rating": 4.7},
    {"name": "Jump Rope Speed", "category": "Sports", "base_price": 14.99, "base_rating": 4.4},
    {"name": "Push-Up Bars Pair", "category": "Sports", "base_price": 16.99, "base_rating": 4.5},
    {"name": "Foam Roller 36 inch", "category": "Sports", "base_price": 29.99, "base_rating": 4.6},
    {"name": "Kettlebell 20lb", "category": "Sports", "base_price": 34.99, "base_rating": 4.5},
    {"name": "Yoga Block 2-Pack", "category": "Sports", "base_price": 14.99, "base_rating": 4.7},
    {"name": "Ab Wheel Roller", "category": "Sports", "base_price": 19.99, "base_rating": 4.4},
    {"name": "Bicycle Helmet Safety", "category": "Sports", "base_price": 39.99, "base_rating": 4.6},
    
    # Beauty
    {"name": "Facial Cleanser Gel", "category": "Beauty", "base_price": 14.99, "base_rating": 4.5},
    {"name": "Moisturizer Cream 50ml", "category": "Beauty", "base_price": 24.99, "base_rating": 4.6},
    {"name": "Vitamin C Serum", "category": "Beauty", "base_price": 19.99, "base_rating": 4.7},
    {"name": "Face Mask Sheet (10-Pack)", "category": "Beauty", "base_price": 12.99, "base_rating": 4.4},
    {"name": "Lipstick Set (6 Colors)", "category": "Beauty", "base_price": 16.99, "base_rating": 4.5},
    {"name": "Makeup Brush Set", "category": "Beauty", "base_price": 19.99, "base_rating": 4.6},
    {"name": "Hair Shampoo & Conditioner", "category": "Beauty", "base_price": 12.99, "base_rating": 4.4},
    {"name": "Eye Cream Anti-Aging", "category": "Beauty", "base_price": 22.99, "base_rating": 4.7},
    {"name": "Face Sunscreen SPF 50", "category": "Beauty", "base_price": 14.99, "base_rating": 4.5},
    {"name": "Nail Polish Set (12 Colors)", "category": "Beauty", "base_price": 13.99, "base_rating": 4.6},
]

# Comprehensive review templates
POSITIVE_REVIEWS = [
    "Excellent product! Exceeded my expectations.",
    "Great quality and fast shipping. Highly recommend!",
    "Perfect! Exactly what I was looking for.",
    "Amazing value for money. Will buy again.",
    "Outstanding! Better than expected.",
    "Love it! Great customer service too.",
    "Fantastic product. Very satisfied.",
    "Best purchase I've made in a while.",
    "Highly impressed with the quality.",
    "Worth every penny. Highly recommended.",
    "Exceeded expectations. Very happy!",
    "Great product at a great price.",
    "Perfect quality and delivery.",
    "Absolutely love this product!",
    "Best in its class. Highly satisfied.",
    "Excellent craftsmanship and design.",
    "Fantastic! Arrived quickly and in perfect condition.",
    "Amazing quality for the price.",
    "Highly recommend to everyone!",
    "Perfect! No complaints whatsoever.",
]

NEGATIVE_REVIEWS = [
    "Poor quality. Broke after a week.",
    "Not as described. Very disappointed.",
    "Terrible customer service.",
    "Waste of money. Don't buy.",
    "Defective product received.",
    "Overpriced for what you get.",
    "Shipping took forever.",
    "Doesn't work as advertised.",
    "Very poor quality control.",
    "Extremely disappointed with this purchase.",
    "Not worth the price at all.",
    "Cheap materials. Won't last long.",
    "Misleading product description.",
    "Arrived damaged and seller won't help.",
    "Worst purchase ever.",
    "Quality is terrible.",
    "Stopped working after 2 weeks.",
    "Complete waste of money.",
    "Regret buying this.",
    "Avoid this product!",
]

NEUTRAL_REVIEWS = [
    "It's okay, nothing special.",
    "Average product for the price.",
    "Does what it says, nothing more.",
    "Decent quality.",
    "Acceptable, but could be better.",
    "Standard product.",
    "Not bad, but not great either.",
    "It works as expected.",
    "Satisfactory purchase.",
    "Fine for the price.",
    "Meets basic expectations.",
    "Adequate quality.",
    "Reasonable value.",
    "Gets the job done.",
    "Decent for everyday use.",
    "Works fine most of the time.",
    "Not the best, not the worst.",
    "Acceptable quality.",
    "Decent alternative.",
    "Fair value for money.",
]

def generate_products(num_products=50):
    """Generate 50+ detailed products."""
    products = []
    
    for i, product_data in enumerate(PRODUCTS_DATA[:num_products]):
        product = {
            "product_id": f"PROD_{i+1:03d}",
            "product_name": product_data["name"],
            "category": product_data["category"],
            "price": round(product_data["base_price"] + np.random.normal(0, 5), 2),
            "avg_rating": round(product_data["base_rating"] + np.random.normal(0, 0.3), 1),
            "review_count": np.random.randint(100, 5000),
            "search_volume_30d": np.random.randint(500, 50000),
            "sales_velocity_weekly": np.random.randint(10, 1000),
            "trend_score": np.random.randint(20, 100),
            "competitor_count": np.random.randint(10, 200),
            "market_saturation": round(np.random.uniform(20, 95), 2),
            "description": f"High-quality {product_data['name']} designed for modern consumers.",
        }
        products.append(product)
    
    return pd.DataFrame(products)


def generate_reviews(num_reviews=1000, num_products=50):
    """Generate 1000+ detailed reviews."""
    reviews = []
    
    for i in range(num_reviews):
        product_id = f"PROD_{np.random.randint(1, num_products+1):03d}"
        sentiment = np.random.choice(["positive", "negative", "neutral"], p=[0.6, 0.2, 0.2])
        
        if sentiment == "positive":
            text = np.random.choice(POSITIVE_REVIEWS)
            rating = np.random.uniform(4.0, 5.0)
        elif sentiment == "negative":
            text = np.random.choice(NEGATIVE_REVIEWS)
            rating = np.random.uniform(1.0, 2.5)
        else:
            text = np.random.choice(NEUTRAL_REVIEWS)
            rating = np.random.uniform(2.5, 4.0)
        
        review = {
            "review_id": f"REV_{i+1:05d}",
            "product_id": product_id,
            "review_text": text,
            "rating": round(rating, 1),
            "sentiment": sentiment,
            "date": (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime("%Y-%m-%d"),
            "verified_purchase": np.random.choice([True, False], p=[0.85, 0.15]),
            "helpful_count": np.random.randint(0, 500),
        }
        reviews.append(review)
    
    return pd.DataFrame(reviews)


def generate_trends(num_months=12, num_categories=6):
    """Generate market trend data."""
    categories = ["Electronics", "Fashion", "Home & Garden", "Sports", "Beauty", "Toys"][:num_categories]
    trends = []
    
    base_date = datetime.now() - timedelta(days=30*num_months)
    
    for month in range(num_months):
        current_date = base_date + timedelta(days=30*month)
        for category in categories:
            trend = {
                "date": current_date.strftime("%Y-%m"),
                "category": category,
                "search_volume": np.random.randint(5000, 100000),
                "sales_volume": np.random.randint(500, 10000),
                "avg_price": round(np.random.uniform(30, 300), 2),
                "market_sentiment": round(np.random.uniform(40, 95), 2),
                "growth_rate": round(np.random.uniform(-10, 30), 2),
            }
            trends.append(trend)
    
    return pd.DataFrame(trends)


if __name__ == "__main__":
    products = generate_products(50)
    reviews = generate_reviews(1000, 50)
    trends = generate_trends(12, 6)
    
    print(f"✅ Generated {len(products)} products")
    print(f"✅ Generated {len(reviews)} reviews")
    print(f"✅ Generated {len(trends)} trend records")
    print(f"\nProducts: {products.shape}")
    print(f"Reviews: {reviews.shape}")
    print(f"Trends: {trends.shape}")
