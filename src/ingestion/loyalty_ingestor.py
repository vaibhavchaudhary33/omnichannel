"""
src/ingestion/loyalty_ingestor.py
Fetches loyalty members from the Loyalty Program (mock) REST API.
"""
import logging
import requests
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)


class LoyaltyIngestor:
    """
    Pulls all members from the Loyalty Program API.

    Usage:
        ingestor = LoyaltyIngestor(base_url="http://localhost:5002")
        df = ingestor.fetch_all()
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None, page_size: int = 50):
        self.base_url  = base_url.rstrip("/")
        self.page_size = page_size
        self.session   = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    # ── Public ────────────────────────────────────────────────────────────────

    def fetch_all(self) -> pd.DataFrame:
        logger.info("LoyaltyIngestor: starting fetch")
        members = self._paginate("/api/v1/members", "members", "meta")
        logger.info(f"LoyaltyIngestor: fetched {len(members)} members")
        return pd.DataFrame(members)

    # ── Private ───────────────────────────────────────────────────────────────

    def _paginate(self, endpoint: str, data_key: str, meta_key: str) -> list[dict]:
        results = []
        page    = 1
        while True:
            url    = f"{self.base_url}{endpoint}"
            params = {"page": page, "limit": self.page_size}
            try:
                resp = self.session.get(url, params=params, timeout=10)
                resp.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"LoyaltyIngestor: request failed — {e}")
                break

            data        = resp.json()
            records     = data.get(data_key, [])
            results.extend(records)

            meta        = data.get(meta_key, {})
            total_pages = meta.get("total_pages", 1)
            logger.debug(f"LoyaltyIngestor: page {page}/{total_pages} — {len(records)} records")

            if page >= total_pages:
                break
            page += 1

        return results
