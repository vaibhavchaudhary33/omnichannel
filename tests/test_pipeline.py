"""
tests/test_pipeline.py
Unit tests for cleaning utilities, deduplicator, and transformer.
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.transformation.cleaner import (
    clean_email, clean_phone, clean_name, parse_date,
    clean_float, clean_int, clean_bool, split_full_name,
)
from src.transformation.deduplicator import deduplicate


class TestCleanEmail:
    def test_valid_lowercase(self):
        assert clean_email("User@Example.COM") == "user@example.com"

    def test_strips_whitespace(self):
        assert clean_email("  hello@world.io  ") == "hello@world.io"

    def test_invalid_returns_none(self):
        assert clean_email("not-an-email") is None

    def test_empty_returns_none(self):
        assert clean_email("") is None
        assert clean_email(None) is None
        assert clean_email("nan") is None


class TestCleanPhone:
    def test_ten_digits(self):
        assert clean_phone("5551234567") == "+15551234567"

    def test_formatted_us(self):
        assert clean_phone("(555) 123-4567") == "+15551234567"

    def test_e164(self):
        assert clean_phone("+15551234567") == "+15551234567"

    def test_empty_returns_none(self):
        assert clean_phone(None) is None
        assert clean_phone("") is None

    def test_too_short_returns_none(self):
        assert clean_phone("123") is None


class TestCleanName:
    def test_title_case(self):
        assert clean_name("JOHN DOE") == "John Doe"
        assert clean_name("jane smith") == "Jane Smith"

    def test_strips_extra_spaces(self):
        assert clean_name("  Alice   ") == "Alice"

    def test_none_returns_none(self):
        assert clean_name(None) is None
        assert clean_name("") is None


class TestParseDate:
    def test_iso(self):
        assert parse_date("2023-07-15") == "2023-07-15"

    def test_us_format(self):
        assert parse_date("07/15/2023") == "2023-07-15"

    def test_eu_format(self):
        assert parse_date("15-07-2023") == "2023-07-15"

    def test_long_format(self):
        assert parse_date("July 15, 2023") == "2023-07-15"

    def test_unknown_returns_none(self):
        assert parse_date("not-a-date") is None

    def test_empty_returns_none(self):
        assert parse_date(None) is None


class TestCleanFloat:
    def test_plain_number(self):
        assert clean_float("123.45") == 123.45

    def test_currency_string(self):
        assert clean_float("$1,234.56") == 1234.56

    def test_none_default(self):
        assert clean_float(None) == 0.0


class TestCleanBool:
    def test_truthy(self):
        for v in ("true", "1", "yes", "y", True, 1):
            assert clean_bool(v) is True

    def test_falsy(self):
        for v in ("false", "0", "no", "n", False, 0):
            assert clean_bool(v) is False

    def test_none(self):
        assert clean_bool(None) is None


class TestSplitFullName:
    def test_standard(self):
        assert split_full_name("John Smith") == ("John", "Smith")

    def test_comma_format(self):
        first, last = split_full_name("Smith, John")
        assert first == "John"
        assert last == "Smith"

    def test_single_name(self):
        first, last = split_full_name("Madonna")
        assert first == "Madonna"
        assert last is None

    def test_empty(self):
        assert split_full_name("") == (None, None)


class TestDeduplicator:
    def test_merges_by_email(self):
        rows = [
            {"email": "alice@x.com", "phone": None, "first_name": "Alice",
             "last_name": None, "date_of_birth": None, "total_orders": 3,
             "total_spend": 100.0, "loyalty_points": 0, "loyalty_tier": None,
             "last_purchase_date": None, "tags": [], "source_ids": {"shopify_id": "S1"}},
            {"email": "alice@x.com", "phone": None, "first_name": None,
             "last_name": "Smith", "date_of_birth": None, "total_orders": 2,
             "total_spend": 50.0, "loyalty_points": 500, "loyalty_tier": None,
             "last_purchase_date": None, "tags": [], "source_ids": {"loyalty_id": "L1"}},
        ]
        df = deduplicate(pd.DataFrame(rows))
        assert len(df) == 1
        assert df.iloc[0]["total_orders"] == 5
        assert df.iloc[0]["total_spend"] == 150.0
        assert df.iloc[0]["loyalty_points"] == 500

    def test_no_duplicate_keeps_both(self):
        rows = [
            {"email": "alice@x.com", "phone": None, "first_name": None,
             "last_name": None, "date_of_birth": None, "total_orders": 1,
             "total_spend": 0.0, "loyalty_points": 0, "loyalty_tier": None,
             "last_purchase_date": None, "tags": [], "source_ids": {}},
            {"email": "bob@x.com", "phone": None, "first_name": None,
             "last_name": None, "date_of_birth": None, "total_orders": 2,
             "total_spend": 0.0, "loyalty_points": 0, "loyalty_tier": None,
             "last_purchase_date": None, "tags": [], "source_ids": {}},
        ]
        df = deduplicate(pd.DataFrame(rows))
        assert len(df) == 2

    def test_unified_id_assigned(self):
        rows = [
            {"email": "z@z.com", "phone": None, "first_name": None,
             "last_name": None, "date_of_birth": None, "total_orders": 0,
             "total_spend": 0.0, "loyalty_points": 0, "loyalty_tier": None,
             "last_purchase_date": None, "tags": [], "source_ids": {}},
        ]
        df  = deduplicate(pd.DataFrame(rows))
        uid = df.iloc[0]["unified_id"]
        assert uid and len(uid) == 36
