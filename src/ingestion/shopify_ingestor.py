"""
src/ingestion/shopify_ingestor.py
Fetches customers and orders from the Shopify (mock) REST API with pagination.
"""
import logging
import requests
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)


class ShopifyIngestor:
    """
    Pulls all customers and orders from the Shopify API.

    Usage:
        ingestor = ShopifyIngestor(base_url="http://localhost:5001")
        customers_df, orders_df = ingestor.fetch_all()
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None, page_size: int = 50):
        self.base_url  = base_url.rstrip("/")
        self.page_size = page_size
        self.session   = requests.Session()
        if api_key:
            self.session.headers.update({"X-Shopify-Access-Token": api_key})

    # ── Public ────────────────────────────────────────────────────────────────

    def fetch_all(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Return (customers_df, orders_df)."""
        logger.info("ShopifyIngestor: starting fetch")
        customers = self._paginate("/admin/api/2024-01/customers.json", "customers")
        orders    = self._paginate("/admin/api/2024-01/orders.json",    "orders")
        logger.info(f"ShopifyIngestor: fetched {len(customers)} customers, {len(orders)} orders")
        return pd.DataFrame(customers), pd.DataFrame(orders)

    # ── Private ───────────────────────────────────────────────────────────────

    def _paginate(self, endpoint: str, key: str) -> list[dict]:
        """Walk through all pages and return a flat list of records."""
        results = []
        page    = 1
        while True:
            url    = f"{self.base_url}{endpoint}"
            params = {"page": page, "limit": self.page_size}
            try:
                resp = self.session.get(url, params=params, timeout=10)
                resp.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"ShopifyIngestor: request failed — {e}")
                break

            data       = resp.json()
            records    = data.get(key, [])
            results.extend(records)

            pagination   = data.get("pagination", {})
            total_pages  = pagination.get("total_pages", 1)
            logger.debug(f"ShopifyIngestor: page {page}/{total_pages} — {len(records)} {key}")

            if page >= total_pages:
                break
            page += 1

        return results
