"""
src/transformation/deduplicator.py
Merges duplicate customer profiles across sources using email as the
primary match key, with phone as a fallback.
"""
import uuid
import logging
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)


def _coalesce(*values):
    for v in values:
        if v is not None and str(v).strip() not in ("", "nan", "None", "NaN"):
            return v
    return None


def _merge_source_ids(*dicts) -> dict:
    merged = {}
    for d in dicts:
        if isinstance(d, dict):
            merged.update(d)
    return merged


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Deduplicator: starting with {len(df)} rows")

    email_groups: dict[str, list[int]] = {}
    phone_groups: dict[str, list[int]] = {}
    no_key_indices: list[int]          = []

    for idx, row in df.iterrows():
        email = row.get("email")
        phone = row.get("phone")
        if email:
            email_groups.setdefault(email, []).append(idx)
        elif phone:
            phone_groups.setdefault(phone, []).append(idx)
        else:
            no_key_indices.append(idx)

    merged_records = []

    def _merge_group(indices: list[int]) -> dict:
        rows = df.loc[indices]
        source_ids_list = [r for r in rows.get("source_ids", pd.Series(dtype=object)) if isinstance(r, dict)]
        return {
            "unified_id":         str(uuid.uuid4()),
            "email":              _coalesce(*rows["email"].tolist()),
            "phone":              _coalesce(*rows["phone"].tolist()),
            "first_name":         _coalesce(*rows["first_name"].tolist()),
            "last_name":          _coalesce(*rows["last_name"].tolist()),
            "date_of_birth":      _coalesce(*rows["date_of_birth"].tolist()),
            "total_orders":       int(rows["total_orders"].fillna(0).astype(float).sum()),
            "total_spend":        round(float(rows["total_spend"].fillna(0).astype(float).sum()), 2),
            "loyalty_points":     int(rows["loyalty_points"].fillna(0).astype(float).max()),
            "loyalty_tier":       _coalesce(*rows["loyalty_tier"].tolist()),
            "last_purchase_date": _most_recent(rows["last_purchase_date"].tolist()),
            "tags":               _merge_tags(rows["tags"].tolist()),
            "source_ids":         _merge_source_ids(*source_ids_list),
            "created_at":         pd.Timestamp.utcnow().isoformat(),
        }

    for email, indices in email_groups.items():
        merged_records.append(_merge_group(indices))

    for phone, indices in phone_groups.items():
        merged_records.append(_merge_group(indices))

    for idx in no_key_indices:
        merged_records.append(_merge_group([idx]))

    result = pd.DataFrame(merged_records)
    logger.info(f"Deduplicator: reduced to {len(result)} unique profiles "
                f"({len(df) - len(result)} duplicates removed)")
    return result


def _most_recent(dates: list) -> Optional[str]:
    valid = [d for d in dates if d and str(d).strip() not in ("", "nan", "None", "NaN")]
    if not valid:
        return None
    return max(valid)


def _merge_tags(tag_lists: list) -> list:
    merged = set()
    for item in tag_lists:
        if isinstance(item, list):
            merged.update(item)
        elif isinstance(item, str) and item:
            merged.update([t.strip() for t in item.split(",")])
    return sorted(merged)
