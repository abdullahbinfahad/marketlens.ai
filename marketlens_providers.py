"""Live product providers, resilient fetching, and canonical normalization."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
import os
from typing import Any, Callable

import requests


@dataclass
class ProviderResult:
    provider: str
    status: str
    records: list[dict[str, Any]] = field(default_factory=list)
    message: str = ""
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProviderError(RuntimeError):
    pass


def _get_json(url: str, *, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None, timeout: int = 12) -> Any:
    response = requests.get(url, params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()


def _text(value: Any) -> str:
    return str(value or "").strip()


def _number(value: Any) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def fetch_dummyjson(query: str) -> ProviderResult:
    """Free prototyping/search provider."""
    try:
        data = _get_json("https://dummyjson.com/products/search", params={"q": query, "limit": 30})
        products = data.get("products", []) if isinstance(data, dict) else []
        records = [{
            "provider_product_id": f"dummyjson:{item.get('id')}", "provider": "DummyJSON", "product_name": item.get("title"),
            "product_description": item.get("description"), "brand": item.get("brand"), "main_category": item.get("category"),
            "sub_category": item.get("category"), "selling_price_usd": item.get("price"), "average_rating": item.get("rating"),
            "inventory": item.get("stock"), "thumbnail": item.get("thumbnail"), "discount_percent": item.get("discountPercentage"),
            "observed_fields": ["product_name", "product_description", "brand", "main_category", "selling_price_usd", "average_rating"],
            "source_url": f"https://dummyjson.com/products/{item.get('id')}",
        } for item in products]
        return ProviderResult("DummyJSON", "ok", records, "Free prototyping catalogue")
    except Exception as exc:
        return ProviderResult("DummyJSON", "error", message=str(exc))


def fetch_fake_store(query: str) -> ProviderResult:
    """Free prototyping provider; locally filters its small catalogue."""
    try:
        products = _get_json("https://fakestoreapi.com/products")
        term = query.lower().strip()
        products = [item for item in products if not term or term in " ".join(str(item.get(key, "")) for key in ("title", "description", "category" )).lower()]
        records = [{
            "provider_product_id": f"fakestore:{item.get('id')}", "provider": "Fake Store API", "product_name": item.get("title"),
            "product_description": item.get("description"), "main_category": item.get("category"), "selling_price_usd": item.get("price"),
            "average_rating": (item.get("rating") or {}).get("rate"), "total_reviews_count": (item.get("rating") or {}).get("count"),
            "thumbnail": item.get("image"), "observed_fields": ["product_name", "product_description", "main_category", "selling_price_usd", "average_rating", "total_reviews_count"],
            "source_url": f"https://fakestoreapi.com/products/{item.get('id')}",
        } for item in products[:30]]
        return ProviderResult("Fake Store API", "ok", records, "Free sample catalogue")
    except Exception as exc:
        return ProviderResult("Fake Store API", "error", message=str(exc))


def fetch_open_beauty_facts(query: str) -> ProviderResult:
    """Free identity/ingredient provider."""
    try:
        data = _get_json("https://world.openbeautyfacts.org/cgi/search.pl", params={"search_terms": query, "search_simple": 1, "action": "process", "json": 1, "page_size": 30, "fields": "code,product_name,brands,categories,ingredients_text,countries,last_modified,nutrition_grades"})
        records = []
        for item in data.get("products", []):
            code, name = _text(item.get("code")), _text(item.get("product_name"))
            if not code or not name:
                continue
            categories = [_text(part) for part in _text(item.get("categories")).split(",") if _text(part)]
            records.append({
                "provider_product_id": f"openbeautyfacts:{code}", "provider": "Open Beauty Facts", "product_name": name,
                "product_description": item.get("ingredients_text"), "brand": item.get("brands"), "main_category": categories[0] if categories else "Beauty & personal care",
                "sub_category": categories[1] if len(categories) > 1 else "", "target_country": item.get("countries"), "nutrition_grade": item.get("nutrition_grades"),
                "last_updated_timestamp": item.get("last_modified"), "observed_fields": ["product_name", "product_description", "brand", "main_category", "target_country", "last_updated_timestamp"],
                "source_url": f"https://world.openbeautyfacts.org/product/{code}",
            })
        return ProviderResult("Open Beauty Facts", "ok", records, "Free identity and ingredient catalogue")
    except Exception as exc:
        return ProviderResult("Open Beauty Facts", "error", message=str(exc))


def fetch_ebay(query: str) -> ProviderResult:
    """Optional eBay Browse connector; disabled until EBAY_CLIENT_ID and EBAY_CLIENT_SECRET are configured."""
    token = os.getenv("EBAY_OAUTH_TOKEN")
    if not token:
        return ProviderResult("eBay Browse API", "not_configured", message="Set EBAY_OAUTH_TOKEN to enable marketplace listings.")
    try:
        data = _get_json("https://api.ebay.com/buy/browse/v1/item_summary/search", params={"q": query, "limit": 30}, headers={"Authorization": f"Bearer {token}", "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"})
        records = []
        for item in data.get("itemSummaries", []):
            price = (item.get("price") or {}).get("value")
            records.append({
                "provider_product_id": f"ebay:{item.get('itemId')}", "provider": "eBay Browse API", "product_name": item.get("title"),
                "product_description": item.get("shortDescription"), "main_category": item.get("categories", [{}])[0].get("categoryName") if item.get("categories") else "",
                "selling_price_usd": price, "currency": (item.get("price") or {}).get("currency"), "thumbnail": (item.get("image") or {}).get("imageUrl"),
                "source_url": item.get("itemWebUrl"), "observed_fields": ["product_name", "product_description", "selling_price_usd", "currency", "thumbnail"],
            })
        return ProviderResult("eBay Browse API", "ok", records, "Marketplace listing results")
    except Exception as exc:
        return ProviderResult("eBay Browse API", "error", message=str(exc))


def fetch_keepa(query: str) -> ProviderResult:
    """Optional Keepa connector; disabled until a Keepa key is configured."""
    if not os.getenv("KEEPA_API_KEY"):
        return ProviderResult("Keepa API", "not_configured", message="Set KEEPA_API_KEY to enable Amazon history data.")
    return ProviderResult("Keepa API", "not_implemented", message="Keepa requires a plan-specific request contract; configure it in the adapter before production use.")


def fetch_shopify(query: str) -> ProviderResult:
    """Optional Shopify connector; requires a participating store's Storefront endpoint/token."""
    endpoint, token = os.getenv("SHOPIFY_STOREFRONT_URL"), os.getenv("SHOPIFY_STOREFRONT_TOKEN")
    if not endpoint or not token:
        return ProviderResult("Shopify Storefront API", "not_configured", message="Set SHOPIFY_STOREFRONT_URL and SHOPIFY_STOREFRONT_TOKEN to enable a permitted store.")
    return ProviderResult("Shopify Storefront API", "not_implemented", message="Shopify access is store-specific; configure the permitted store's GraphQL query in the adapter.")


PROVIDERS: dict[str, Callable[[str], ProviderResult]] = {
    "DummyJSON": fetch_dummyjson, "Fake Store API": fetch_fake_store, "Open Beauty Facts": fetch_open_beauty_facts,
    "eBay Browse API": fetch_ebay, "Keepa API": fetch_keepa, "Shopify Storefront API": fetch_shopify,
}


def fetch_all(query: str, selected: list[str] | None = None) -> list[ProviderResult]:
    names = selected or list(PROVIDERS)
    names = [name for name in names if name in PROVIDERS]
    results: list[ProviderResult] = []
    with ThreadPoolExecutor(max_workers=min(6, max(1, len(names)))) as pool:
        futures = {pool.submit(PROVIDERS[name], query): name for name in names}
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda item: names.index(item.provider))


def normalize_records(results: list[ProviderResult]) -> list[dict[str, Any]]:
    """Deduplicate records while retaining provider/source evidence."""
    merged: dict[str, dict[str, Any]] = {}
    for result in results:
        for record in result.records:
            key = _text(record.get("product_name")).lower() + "|" + _text(record.get("brand")).lower()
            if not key.strip("|"):
                continue
            if key not in merged:
                merged[key] = dict(record)
                merged[key]["providers"] = [result.provider]
                merged[key]["provider_count"] = 1
            else:
                target = merged[key]
                target["providers"].append(result.provider)
                target["provider_count"] += 1
                for field, value in record.items():
                    if target.get(field) in (None, "", []) and value not in (None, "", []):
                        target[field] = value
                target["observed_fields"] = sorted(set(target.get("observed_fields", [])) | set(record.get("observed_fields", [])))
    return list(merged.values())
