"""
Data Generator for MarketLens AI
Generates 50 products, 1000+ reviews, and market trends
Python 3.14+ compatible
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_products(count: int = 50) -> pd.DataFrame:
    """Generate realistic e-commerce products."""
    
    categories = ["Electronics", "Fashion", "Home & Garden", "Sports", "Beauty"]
    products_per_category = count // len(categories)
    
    products = []
    product_id = 1
    
    # Product templates
    electronics = [
        ("Wireless Earbuds Pro", 89.99),
        ("Noise Cancelling Headphones", 199.99),
        ("Smart Watch Series 5", 299.99),
        ("USB-C Fast Charger", 29.99),
        ("Portable Power Bank 20000mAh", 39.99),
        ("Bluetooth Speaker", 49.99),
        ("4K Webcam", 79.99),
        ("Gaming Mouse", 59.99),
        ("Mechanical Keyboard RGB", 99.99),
        ("Phone Stand Adjustable", 19.99),
    ]
    
    fashion = [
        ("Cotton T-Shirt Pack", 34.99),
        ("Slim Fit Jeans", 54.99),
        ("Running Sneakers", 89.99),
        ("Casual Jacket", 79.99),
        ("Yoga Leggings", 44.99),
        ("Sports Bra", 39.99),
        ("Winter Beanie", 19.99),
        ("Sunglasses UV Protection", 49.99),
        ("Athletic Socks Pack", 24.99),
        ("Casual Hoodie", 59.99),
    ]
    
    home_garden = [
        ("LED Smart Bulb", 24.99),
        ("Non-Stick Cookware Set", 79.99),
        ("Air Purifier", 129.99),
        ("Desk Lamp LED", 34.99),
        ("Bedding Set Queen", 69.99),
        ("Shower Head High Pressure", 29.99),
        ("Plant Pot Set", 39.99),
        ("Curtain Rod Adjustable", 44.99),
        ("Door Mat Anti-Slip", 19.99),
        ("Pillow Memory Foam", 49.99),
    ]
    
    sports = [
        ("Yoga Mat Non-Slip", 24.99),
        ("Dumbbell Set", 89.99),
        ("Resistance Bands Set", 19.99),
        ("Jump Rope", 14.99),
        ("Foam Roller", 29.99),
        ("Yoga Blocks", 19.99),
        ("Kettlebell", 34.99),
        ("Push-Up Bars", 24.99),
        ("Gym Bag", 39.99),
        ("Water Bottle 1L", 19.99),
    ]
    
    beauty = [
        ("Facial Cleanser", 24.99),
        ("Moisturizer Cream", 34.99),
        ("Vitamin C Serum", 44.99),
        ("Face Mask Sheet", 14.99),
        ("Lip Balm SPF 30", 9.99),
        ("Hair Shampoo", 19.99),
        ("Body Lotion", 24.99),
        ("Sunscreen SPF 50", 29.99),
        ("Eye Cream", 39.99),
        ("Makeup Brush Set", 29.99),
    ]
    
    templates = {
        "Electronics": electronics,
        "Fashion": fashion,
        "Home & Garden": home_garden,
        "Sports": sports,
        "Beauty": beauty,
    }
    
    for category in categories:
        for name, price in templates[category]:
            products.append({
                "product_id": f"PROD_{product_id:04d}",
                "product_name": name,
                "category": category,
                "price": price,
                "avg_rating": round(random.uniform(3.5, 5.0), 1),
                "review_count": random.randint(100, 5000),
                "search_volume_30d": random.randint(1000, 50000),
                "sales_velocity_weekly": random.randint(10, 500),
                "trend_score": random.randint(30, 95),
                "competitor_count": random.randint(20, 200),
                "market_saturation": random.randint(20, 90),
            })
            product_id += 1
    
    return pd.DataFrame(products)


def generate_reviews(count: int = 1000, product_count: int = 50) -> pd.DataFrame:
    """Generate realistic customer reviews."""
    
    positive_reviews = [
        "Excellent product! Exceeded my expectations.",
        "Great quality and fast shipping.",
        "Highly recommend! Best purchase ever.",
        "Amazing value for money.",
        "Perfect! Exactly what I needed.",
        "Outstanding customer service.",
        "Five stars! Very satisfied.",
        "Fantastic product, will buy again.",
        "Superb quality and durability.",
        "Absolutely love it!",
        "Best in class product.",
        "Impressive performance.",
        "Excellent build quality.",
        "Worth every penny.",
        "Highly satisfied customer.",
    ]
    
    negative_reviews = [
        "Poor quality. Broke after a week.",
        "Not as described in the listing.",
        "Terrible customer support.",
        "Waste of money.",
        "Defective product received.",
        "Very disappointed.",
        "Cheap materials.",
        "Doesn't work as advertised.",
        "Horrible experience.",
        "Would not recommend.",
        "Quality is subpar.",
        "Overpriced for what you get.",
        "Arrived damaged.",
        "Stopped working after a month.",
        "Complete disappointment.",
    ]
    
    neutral_reviews = [
        "It's okay, nothing special.",
        "Average product.",
        "Does what it's supposed to do.",
        "Not bad, not great.",
        "Decent for the price.",
        "It's fine.",
        "Meets expectations.",
        "Could be better.",
        "Acceptable quality.",
        "Mediocre.",
        "Neither good nor bad.",
        "Satisfactory.",
        "Adequate.",
        "Fair product.",
        "So-so.",
    ]
    
    reviews = []
    
    for i in range(count):
        # Distribute: 60% positive, 20% negative, 20% neutral
        rand = random.random()
        if rand < 0.6:
            review_text = random.choice(positive_reviews)
            rating = random.randint(4, 5)
            sentiment = "positive"
        elif rand < 0.8:
            review_text = random.choice(negative_reviews)
            rating = random.randint(1, 2)
            sentiment = "negative"
        else:
            review_text = random.choice(neutral_reviews)
            rating = 3
            sentiment = "neutral"
        
        reviews.append({
            "review_id": f"REV_{i+1:05d}",
            "product_id": f"PROD_{random.randint(1, product_count):04d}",
            "rating": rating,
            "review_text": review_text,
            "helpful_count": random.randint(0, 500),
            "verified_purchase": random.choice([True, True, True, False]),
            "sentiment": sentiment,
            "date": datetime.now() - timedelta(days=random.randint(0, 365)),
        })
    
    return pd.DataFrame(reviews)


def generate_trends(months: int = 12, categories: int = 6) -> pd.DataFrame:
    """Generate market trend data."""
    
    category_names = ["Electronics", "Fashion", "Home & Garden", "Sports", "Beauty", "Other"][:categories]
    
    trends = []
    base_date = datetime.now() - timedelta(days=30*months)
    
    for month in range(months):
        current_date = base_date + timedelta(days=30*month)
        
        for category in category_names:
            trends.append({
                "date": current_date.strftime("%Y-%m"),
                "category": category,
                "search_volume": random.randint(10000, 100000),
                "sales_volume": random.randint(5000, 50000),
                "market_sentiment": round(random.uniform(0.3, 0.9), 2),
                "growth_rate": round(random.uniform(-0.2, 0.3), 2),
            })
    
    return pd.DataFrame(trends)


if __name__ == "__main__":
    print("Generating test data...")
    
    products = generate_products(50)
    print(f"✓ Generated {len(products)} products")
    print(products.head())
    
    reviews = generate_reviews(1000, 50)
    print(f"\n✓ Generated {len(reviews)} reviews")
    print(reviews.head())
    
    trends = generate_trends(12, 6)
    print(f"\n✓ Generated {len(trends)} trend records")
    print(trends.head())
