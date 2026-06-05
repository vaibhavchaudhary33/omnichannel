"""
config/settings.py
Centralised configuration loaded from environment / .env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ── API endpoints ────────────────────────────────────────────────────────────
SHOPIFY_API_URL   = os.getenv("SHOPIFY_API_URL",  "http://localhost:5001")
LOYALTY_API_URL   = os.getenv("LOYALTY_API_URL",  "http://localhost:5002")
POS_CSV_PATH      = os.getenv("POS_CSV_PATH",      str(BASE_DIR / "data" / "raw" / "pos_transactions.csv"))

# ── AWS S3 ───────────────────────────────────────────────────────────────────
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID",     "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_BUCKET_NAME       = os.getenv("AWS_BUCKET_NAME",       "cdp-unified-profiles")
AWS_REGION            = os.getenv("AWS_REGION",            "us-east-1")
S3_KEY_PREFIX         = os.getenv("S3_KEY_PREFIX",         "unified_profiles/")

# ── MySQL ────────────────────────────────────────────────────────────────────
MYSQL_HOST     = os.getenv("MYSQL_HOST",     "localhost")
MYSQL_PORT     = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER     = os.getenv("MYSQL_USER",     "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_DB       = os.getenv("MYSQL_DB",       "cdp")

# ── Local fallback output ────────────────────────────────────────────────────
LOCAL_OUTPUT_DIR = BASE_DIR / "data" / "processed"
LOCAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
