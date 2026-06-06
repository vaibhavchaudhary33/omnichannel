"""
src/output/s3_uploader.py
Uploads the unified customer profiles DataFrame to AWS S3.
"""
import io
import json
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


class S3Uploader:
    def __init__(
        self,
        bucket: str,
        key_prefix: str = "unified_profiles/",
        aws_access_key_id: str = "",
        aws_secret_access_key: str = "",
        region_name: str = "us-east-1",
    ):
        self.bucket     = bucket
        self.key_prefix = key_prefix.rstrip("/") + "/"
        self._init_client(aws_access_key_id, aws_secret_access_key, region_name)

    def upload(self, df: pd.DataFrame) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        key       = f"{self.key_prefix}run={timestamp}/profiles.parquet"

        logger.info(f"S3Uploader: uploading {len(df)} profiles → s3://{self.bucket}/{key}")

        buffer = io.BytesIO()
        df_serialisable = self._make_serialisable(df)

        try:
            df_serialisable.to_parquet(buffer, index=False, engine="pyarrow")
            buffer.seek(0)
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=buffer.getvalue(),
                ContentType="application/octet-stream",
            )
            uri = f"s3://{self.bucket}/{key}"
            logger.info(f"S3Uploader: upload complete → {uri}")
            return uri
        except ImportError:
            return self._upload_json(df_serialisable, timestamp)
        except Exception as e:
            logger.error(f"S3Uploader: upload failed — {e}")
            raise

    def _init_client(self, key_id: str, secret: str, region: str) -> None:
        try:
            import boto3
            session       = boto3.Session(
                aws_access_key_id     = key_id  or None,
                aws_secret_access_key = secret  or None,
                region_name           = region,
            )
            self.client = session.client("s3")
        except ImportError:
            logger.warning("S3Uploader: boto3 not installed — S3 uploads will fail")
            self.client = None

    def _upload_json(self, df: pd.DataFrame, timestamp: str) -> str:
        key = f"{self.key_prefix}run={timestamp}/profiles.json"
        payload = df.to_json(orient="records", indent=2)
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=payload.encode("utf-8"),
            ContentType="application/json",
        )
        uri = f"s3://{self.bucket}/{key}"
        logger.info(f"S3Uploader: JSON upload complete → {uri}")
        return uri

    @staticmethod
    def _make_serialisable(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for col in out.columns:
            if out[col].dtype == object:
                sample = out[col].dropna().head(1)
                if len(sample) > 0 and isinstance(sample.iloc[0], (list, dict)):
                    out[col] = out[col].apply(
                        lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
                    )
        return out
