"""
src/transformation/transformer.py
Orchestrates the full transformation pipeline.
"""
import logging
import pandas as pd
from typing import Optional

from src.transformation.cleaner import (
    clean_email, clean_phone, clean_name,
    parse_date, parse_datetime,
    clean_float, clean_int, clean_bool,
    split_full_name,
)
from src.transformation.deduplicator import deduplicate

logger = logging.getLogger(__name__)

CANONICAL_COLS = [
    "unified_id", "email", "phone",
    "first_name", "last_name", "date_of_birth",
    "total_orders", "total_spend",
    "loyalty_points", "loyalty_tier",
    "last_purchase_date", "tags", "source_ids", "created_at",
]


class Transformer:
    def __init__(
        self,
        shopify_customers: pd.DataFrame,
        shopify_orders: pd.DataFrame,
        pos_df: pd.DataFrame,
        loyalty_df: pd.DataFrame,
    ):
        self.shopify_customers = shopify_customers
        self.shopify_orders    = shopify_orders
        self.pos_df            = pos_df
        self.loyalty_df        = loyalty_df

    def run(self) -> pd.DataFrame:
        logger.info("Transformer: starting normalisation")

        shopify_norm = self._normalise_shopify()
        pos_norm     = self._normalise_pos()
        loyalty_norm = self._normalise_loyalty()

        combined = pd.concat([shopify_norm, pos_norm, loyalty_norm], ignore_index=True)
        logger.info(f"Transformer: combined {len(combined)} raw records before dedup")

        result = deduplicate(combined)
        if result.empty:
            return pd.DataFrame(columns=CANONICAL_COLS)
        return result[CANONICAL_COLS]

    def _normalise_shopify(self) -> pd.DataFrame:
        df = self.shopify_customers.copy()
        if df.empty:
            return pd.DataFrame(columns=CANONICAL_COLS)

        order_stats = self._aggregate_shopify_orders()

        records = []
        for _, row in df.iterrows():
            sid   = str(row.get("id", ""))
            email = clean_email(row.get("email"))
            phone = clean_phone(row.get("phone"))

            addresses = row.get("addresses") or []
            addr = addresses[0] if isinstance(addresses, list) and addresses else {}

            stats = order_stats.get(sid, {"orders": 0, "spend": 0.0, "last_date": None})

            records.append({
                "email":              email,
                "phone":              phone,
                "first_name":         clean_name(row.get("first_name")),
                "last_name":          clean_name(row.get("last_name")),
                "date_of_birth":      None,
                "total_orders":       stats["orders"],
                "total_spend":        stats["spend"],
                "loyalty_points":     0,
                "loyalty_tier":       None,
                "last_purchase_date": stats["last_date"],
                "tags":               row.get("tags") or [],
                "source_ids":         {"shopify_id": sid},
            })

        out = pd.DataFrame(records)
        logger.info(f"Transformer: normalised {len(out)} Shopify customers")
        return out

    def _aggregate_shopify_orders(self) -> dict:
        stats = {}
        for _, o in self.shopify_orders.iterrows():
            cid   = str(o.get("customer_id", ""))
            price = clean_float(o.get("total_price", 0))
            date  = parse_date(o.get("created_at"))
            if cid not in stats:
                stats[cid] = {"orders": 0, "spend": 0.0, "last_date": None}
            stats[cid]["orders"] += 1
            stats[cid]["spend"]  += price
            if date and (stats[cid]["last_date"] is None or date > stats[cid]["last_date"]):
                stats[cid]["last_date"] = date
        return stats

    def _normalise_pos(self) -> pd.DataFrame:
        df = self.pos_df.copy()
        if df.empty:
            return pd.DataFrame(columns=CANONICAL_COLS)

        groups: dict[str, dict] = {}

        for _, row in df.iterrows():
            email  = clean_email(row.get("customer_email"))
            phone  = clean_phone(row.get("customer_phone"))
            key    = email or phone
            if not key:
                key = f"__pos_{row.get('transaction_id', id(row))}__"

            amount = clean_float(row.get("amount", 0))
            date   = parse_date(row.get("transaction_date"))

            name_raw          = str(row.get("customer_name", "") or "")
            first_n, last_n   = split_full_name(name_raw)

            if key not in groups:
                groups[key] = {
                    "email":              email,
                    "phone":              phone,
                    "first_name":         first_n,
                    "last_name":          last_n,
                    "date_of_birth":      None,
                    "total_orders":       0,
                    "total_spend":        0.0,
                    "loyalty_points":     0,
                    "loyalty_tier":       None,
                    "last_purchase_date": None,
                    "tags":               [],
                    "source_ids":         {"pos_transactions": []},
                }

            g = groups[key]
            g["total_orders"] += 1
            g["total_spend"]  += amount
            g["source_ids"]["pos_transactions"].append(row.get("transaction_id", ""))
            if date and (g["last_purchase_date"] is None or date > g["last_purchase_date"]):
                g["last_purchase_date"] = date
            if g["first_name"] is None and first_n:
                g["first_name"] = first_n
            if g["last_name"] is None and last_n:
                g["last_name"] = last_n

        out = pd.DataFrame(list(groups.values()))
        logger.info(f"Transformer: normalised {len(out)} unique PoS customers from {len(df)} transactions")
        return out

    def _normalise_loyalty(self) -> pd.DataFrame:
        df = self.loyalty_df.copy()
        if df.empty:
            return pd.DataFrame(columns=CANONICAL_COLS)

        records = []
        for _, row in df.iterrows():
            email = clean_email(row.get("email_address") or row.get("email"))
            phone = clean_phone(row.get("mobile_number") or row.get("phone"))
            first = clean_name(row.get("given_name")  or row.get("first_name"))
            last  = clean_name(row.get("surname")     or row.get("last_name"))
            dob   = parse_date(row.get("birth_date")  or row.get("date_of_birth"))

            records.append({
                "email":              email,
                "phone":              phone,
                "first_name":         first,
                "last_name":          last,
                "date_of_birth":      dob,
                "total_orders":       0,
                "total_spend":        0.0,
                "loyalty_points":     clean_int(row.get("points_balance", 0)),
                "loyalty_tier":       str(row.get("tier", "") or "").strip() or None,
                "last_purchase_date": parse_date(row.get("last_activity")),
                "tags":               [],
                "source_ids":         {"loyalty_id": str(row.get("member_id", ""))},
            })

        out = pd.DataFrame(records)
        logger.info(f"Transformer: normalised {len(out)} Loyalty members")
        return out
