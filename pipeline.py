"""
pipeline.py
Main entry point for the Omnichannel Data Ingestion Engine.

Usage:
    python pipeline.py                  # output to local CSV + JSON
    python pipeline.py --output s3      # output to AWS S3
    python pipeline.py --output mysql   # output to MySQL
    python pipeline.py --output all     # all three
    python pipeline.py --dry-run        # transform only, no write
"""
import sys
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd
from colorama import Fore, Style, init as colorama_init

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import (
    SHOPIFY_API_URL, LOYALTY_API_URL, POS_CSV_PATH,
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, AWS_REGION, S3_KEY_PREFIX,
    MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB,
    LOCAL_OUTPUT_DIR,
)
from src.ingestion.shopify_ingestor import ShopifyIngestor
from src.ingestion.pos_ingestor     import PosIngestor
from src.ingestion.loyalty_ingestor import LoyaltyIngestor
from src.transformation.transformer import Transformer

colorama_init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("pipeline")

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║       Omnichannel Data Ingestion Engine  v1.0            ║
║       ERP · PoS · CRM  →  Unified Customer Profile       ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""


def _step(msg: str) -> None:
    print(f"\n{Fore.YELLOW}▶{Style.RESET_ALL}  {msg}")

def _ok(msg: str) -> None:
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL}  {msg}")

def _warn(msg: str) -> None:
    print(f"  {Fore.RED}✗{Style.RESET_ALL}  {msg}")


def ingest(args):
    _step("INGESTION")
    shopify = ShopifyIngestor(SHOPIFY_API_URL)
    shp_customers, shp_orders = shopify.fetch_all()
    _ok(f"Shopify: {len(shp_customers)} customers, {len(shp_orders)} orders")

    pos    = PosIngestor(POS_CSV_PATH)
    pos_df = pos.fetch_all()
    _ok(f"PoS CSV: {len(pos_df)} transactions")

    loyalty = LoyaltyIngestor(LOYALTY_API_URL)
    loy_df  = loyalty.fetch_all()
    _ok(f"Loyalty API: {len(loy_df)} members")

    return shp_customers, shp_orders, pos_df, loy_df


def transform(shp_customers, shp_orders, pos_df, loy_df):
    _step("TRANSFORMATION")
    t      = Transformer(shp_customers, shp_orders, pos_df, loy_df)
    result = t.run()
    _ok(f"Unified profiles generated: {len(result)}")
    return result


def output_local(df: pd.DataFrame) -> None:
    ts        = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    csv_path  = LOCAL_OUTPUT_DIR / f"unified_profiles_{ts}.csv"
    json_path = LOCAL_OUTPUT_DIR / f"unified_profiles_{ts}.json"
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2,
               default_handler=lambda o: list(o) if isinstance(o, set) else str(o))
    _ok(f"CSV  → {csv_path}")
    _ok(f"JSON → {json_path}")


def output_s3(df: pd.DataFrame) -> None:
    from src.output.s3_uploader import S3Uploader
    uploader = S3Uploader(
        bucket=AWS_BUCKET_NAME,
        key_prefix=S3_KEY_PREFIX,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    uri = uploader.upload(df)
    _ok(f"S3 → {uri}")


def output_mysql(df: pd.DataFrame) -> None:
    from src.output.mysql_writer import MySQLWriter
    writer   = MySQLWriter(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    affected = writer.write(df)
    _ok(f"MySQL → {affected} rows upserted")


def print_summary(df: pd.DataFrame) -> None:
    _step("SUMMARY")
    print(f"\n  {'Metric':<35} {'Value':>10}")
    print(f"  {'─'*45}")
    print(f"  {'Total unified profiles':<35} {len(df):>10,}")
    print(f"  {'Profiles with email':<35} {df['email'].notna().sum():>10,}")
    print(f"  {'Profiles with phone':<35} {df['phone'].notna().sum():>10,}")
    print(f"  {'Profiles with loyalty data':<35} {(df['loyalty_tier'].notna()).sum():>10,}")
    print(f"  {'Profiles with DOB':<35} {df['date_of_birth'].notna().sum():>10,}")
    print(f"  {'Total orders (all sources)':<35} {int(df['total_orders'].sum()):>10,}")
    print(f"  {'Total revenue tracked':<35} {'${:>10,.2f}'.format(df['total_spend'].sum())}")
    print(f"  {'Total loyalty points':<35} {int(df['loyalty_points'].sum()):>10,}")
    print()


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="Omnichannel Data Ingestion Engine")
    parser.add_argument("--output", choices=["local", "s3", "mysql", "all"],
                        default="local")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        shp_customers, shp_orders, pos_df, loy_df = ingest(args)
        df = transform(shp_customers, shp_orders, pos_df, loy_df)

        if args.dry_run:
            _step("DRY RUN — skipping output")
            print_summary(df)
            return

        _step("OUTPUT")
        dest = args.output

        if dest in ("local", "all"):
            output_local(df)
        if dest in ("s3", "all"):
            try:
                output_s3(df)
            except Exception as e:
                _warn(f"S3 upload failed: {e}")
        if dest in ("mysql", "all"):
            try:
                output_mysql(df)
            except Exception as e:
                _warn(f"MySQL write failed: {e}")

        print_summary(df)
        print(f"\n{Fore.GREEN}Pipeline completed successfully.{Style.RESET_ALL}\n")

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        print(f"\n{Fore.RED}Pipeline failed: {e}{Style.RESET_ALL}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
