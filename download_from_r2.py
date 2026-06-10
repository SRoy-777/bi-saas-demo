
from dotenv import load_dotenv

load_dotenv()

import boto3
import os


# ---------------------------------------------------
# R2 Credentials
# ---------------------------------------------------

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("R2_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") or os.getenv("R2_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME") or "orient-analytics-snapshots"

R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")
if not R2_ENDPOINT_URL:
    ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
    if ACCOUNT_ID:
        R2_ENDPOINT_URL = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
    else:
        R2_ENDPOINT_URL = os.getenv("ENDPOINT_URL")

# ---------------------------------------------------
# Create Snapshot Folder
# ---------------------------------------------------

SNAPSHOT_DIR = os.getenv("SNAPSHOT_DIR")
if not SNAPSHOT_DIR:
    if os.getenv("SPACE_ID"):
        SNAPSHOT_DIR = "/tmp/snapshot"
    else:
        SNAPSHOT_DIR = "snapshot"

try:
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
except PermissionError:
    SNAPSHOT_DIR = "/tmp/snapshot"
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# ---------------------------------------------------
# R2 Client
# ---------------------------------------------------

if not ACCESS_KEY or not SECRET_KEY or not R2_ENDPOINT_URL:
    print("WARNING: R2 credentials missing in environment variables.")
    s3 = None
else:
    s3 = boto3.client(
        service_name='s3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )


# ---------------------------------------------------
# Files To Download
# ---------------------------------------------------

files = [

    "merged_sales.parquet",

    "rm_zm.parquet",

    "targets.parquet",

    "merged_scheme.parquet",

    "tag_list.parquet",

    "customer_list.parquet",

    "user_access.parquet",

    "tag_sold.parquet",

    "tag_received.parquet",

    "branch_daily_aggregate.parquet",

    "daily_targets.parquet",

    "old_gold_list.parquet"

]


# ---------------------------------------------------
# Download Files
# ---------------------------------------------------

if s3 is None:
    print("Skipping download from R2: R2 client not initialized. Will use local snapshots if available.")
else:
    for file_name in files:
        print(f"Downloading {file_name}...")
        try:
            s3.download_file(
                BUCKET_NAME,
                file_name,
                os.path.join(SNAPSHOT_DIR, file_name)
            )
            print(f"{file_name} downloaded.")
        except Exception as e:
            print(f"Failed to download {file_name}: {e}")
    print("All parquet snapshots downloaded from R2.")