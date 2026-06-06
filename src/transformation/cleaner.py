"""
src/transformation/cleaner.py
Low-level cleaning utilities used by the transformer.
"""
import re
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

DATE_FORMATS = [
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%m/%d/%Y",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d %b %Y",
    "%d %B %Y",
    "%B %d, %Y",
    "%b %d, %Y",
]


def clean_email(value) -> Optional[str]:
    if not value or str(value).strip() in ("", "nan", "None", "NaN"):
        return None
    email = str(value).strip().lower()
    if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return email
    logger.debug(f"clean_email: invalid format discarded — '{email}'")
    return None


def clean_phone(value) -> Optional[str]:
    if not value or str(value).strip() in ("", "nan", "None", "NaN"):
        return None
    digits = re.sub(r"\D", "", str(value))
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    if len(digits) >= 7:
        return f"+{digits}"
    return None


def clean_name(value) -> Optional[str]:
    if not value or str(value).strip() in ("", "nan", "None", "NaN"):
        return None
    return " ".join(str(value).strip().split()).title()


def parse_date(value, output_fmt: str = "%Y-%m-%d") -> Optional[str]:
    if not value or str(value).strip() in ("", "nan", "None", "NaN"):
        return None
    raw = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).strftime(output_fmt)
        except ValueError:
            continue
    try:
        import pandas as pd
        return pd.to_datetime(raw, infer_datetime_format=True).strftime(output_fmt)
    except Exception:
        logger.debug(f"parse_date: could not parse '{raw}'")
        return None


def parse_datetime(value) -> Optional[str]:
    return parse_date(value, output_fmt="%Y-%m-%dT%H:%M:%S")


def clean_float(value, default: float = 0.0) -> float:
    if value is None or str(value).strip() in ("", "nan", "None", "NaN"):
        return default
    cleaned = re.sub(r"[^\d.]", "", str(value))
    try:
        return float(cleaned)
    except ValueError:
        return default


def clean_int(value, default: int = 0) -> int:
    try:
        return int(float(str(value)))
    except (ValueError, TypeError):
        return default


def clean_bool(value) -> Optional[bool]:
    if value is None:
        return None
    v = str(value).strip().lower()
    if v in ("true", "1", "yes", "y"):
        return True
    if v in ("false", "0", "no", "n"):
        return False
    return None


def split_full_name(full_name: str) -> tuple[Optional[str], Optional[str]]:
    if not full_name:
        return None, None
    if "," in full_name:
        parts = [p.strip() for p in full_name.split(",", 1)]
        return clean_name(parts[1]), clean_name(parts[0])
    parts = full_name.strip().split(None, 1)
    if len(parts) == 2:
        return clean_name(parts[0]), clean_name(parts[1])
    return clean_name(parts[0]), None
