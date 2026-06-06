"""
src/ingestion/pos_ingestor.py
Reads PoS transaction CSVs.  Handles encoding issues and schema validation.
"""
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

EXPECTED_COLUMNS = {
    "transaction_id",
    "customer_email",
    "customer_phone",
    "customer_name",
    "transaction_date",
    "amount",
    "payment_method",
    "store_id",
    "items_count",
    "discount_applied",
}


class PosIngestor:
    """
    Reads one or more PoS CSV files and returns a combined DataFrame.

    Usage:
        ingestor = PosIngestor(csv_path="data/raw/pos_transactions.csv")
        df = ingestor.fetch_all()
    """

    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)

    # ── Public ────────────────────────────────────────────────────────────────

    def fetch_all(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            logger.error(f"PosIngestor: file not found — {self.csv_path}")
            return pd.DataFrame()

        logger.info(f"PosIngestor: reading {self.csv_path}")
        try:
            df = pd.read_csv(self.csv_path, dtype=str, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(self.csv_path, dtype=str, encoding="latin-1")

        self._validate_schema(df)
        logger.info(f"PosIngestor: loaded {len(df)} rows")
        return df

    # ── Private ───────────────────────────────────────────────────────────────

    def _validate_schema(self, df: pd.DataFrame) -> None:
        missing = EXPECTED_COLUMNS - set(df.columns)
        if missing:
            logger.warning(f"PosIngestor: missing expected columns: {missing}")
        extra = set(df.columns) - EXPECTED_COLUMNS
        if extra:
            logger.debug(f"PosIngestor: extra columns (will keep): {extra}")
