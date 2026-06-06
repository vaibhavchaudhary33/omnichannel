"""
src/output/mysql_writer.py
Writes the unified customer profiles DataFrame to a MySQL table.
"""
import json
import logging
import pandas as pd

logger = logging.getLogger(__name__)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS unified_customer_profiles (
    unified_id          VARCHAR(36)     PRIMARY KEY,
    email               VARCHAR(255)    UNIQUE,
    phone               VARCHAR(30),
    first_name          VARCHAR(100),
    last_name           VARCHAR(100),
    date_of_birth       DATE,
    total_orders        INT             DEFAULT 0,
    total_spend         DECIMAL(12, 2)  DEFAULT 0.00,
    loyalty_points      INT             DEFAULT 0,
    loyalty_tier        VARCHAR(50),
    last_purchase_date  DATE,
    tags                JSON,
    source_ids          JSON,
    created_at          DATETIME
);
"""

UPSERT_SQL = """
INSERT INTO unified_customer_profiles
    (unified_id, email, phone, first_name, last_name, date_of_birth,
     total_orders, total_spend, loyalty_points, loyalty_tier,
     last_purchase_date, tags, source_ids, created_at)
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    email              = VALUES(email),
    phone              = COALESCE(VALUES(phone),          phone),
    first_name         = COALESCE(VALUES(first_name),     first_name),
    last_name          = COALESCE(VALUES(last_name),      last_name),
    date_of_birth      = COALESCE(VALUES(date_of_birth),  date_of_birth),
    total_orders       = total_orders + VALUES(total_orders),
    total_spend        = total_spend  + VALUES(total_spend),
    loyalty_points     = GREATEST(loyalty_points, VALUES(loyalty_points)),
    loyalty_tier       = COALESCE(VALUES(loyalty_tier),   loyalty_tier),
    last_purchase_date = GREATEST(
                            COALESCE(last_purchase_date, '1970-01-01'),
                            COALESCE(VALUES(last_purchase_date), '1970-01-01')
                         ),
    tags               = VALUES(tags),
    source_ids         = VALUES(source_ids);
"""


class MySQLWriter:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.config = {
            "host":     host,
            "port":     port,
            "user":     user,
            "password": password,
            "database": database,
        }

    def write(self, df: pd.DataFrame) -> int:
        try:
            import mysql.connector
        except ImportError:
            logger.error("MySQLWriter: mysql-connector-python is not installed")
            raise

        conn   = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        try:
            cursor.execute(CREATE_TABLE_SQL)
            conn.commit()
            rows     = self._prepare_rows(df)
            cursor.executemany(UPSERT_SQL, rows)
            conn.commit()
            affected = cursor.rowcount
            logger.info(f"MySQLWriter: {affected} rows upserted")
            return affected
        except Exception as e:
            conn.rollback()
            logger.error(f"MySQLWriter: write failed — {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def _prepare_rows(df: pd.DataFrame) -> list[tuple]:
        rows = []
        for _, r in df.iterrows():
            rows.append((
                r.get("unified_id"),
                r.get("email")    or None,
                r.get("phone")    or None,
                r.get("first_name") or None,
                r.get("last_name")  or None,
                r.get("date_of_birth") or None,
                int(r.get("total_orders") or 0),
                float(r.get("total_spend") or 0),
                int(r.get("loyalty_points") or 0),
                r.get("loyalty_tier") or None,
                r.get("last_purchase_date") or None,
                json.dumps(r.get("tags") or []),
                json.dumps(r.get("source_ids") or {}),
                r.get("created_at") or None,
            ))
        return rows
