import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import boto3
import pandas as pd
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# ====================================================
# R2 CLIENT SETUP
# ====================================================
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

s3 = None
if ACCESS_KEY and SECRET_KEY and R2_ENDPOINT_URL:
    s3 = boto3.client(
        service_name='s3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
else:
    print("WARNING: R2 credentials not found in env. Snapshots will only be saved locally.")

# Ensure snapshot directory exists
SNAPSHOT_DIR = os.getenv("SNAPSHOT_DIR", "snapshot")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Helper to upload file to R2
def upload_to_r2(local_path):
    if s3 is None:
        print(f"Skipping R2 upload for {local_path} (R2 client not initialized)")
        return
    
    file_name = os.path.basename(local_path)
    print(f"Uploading {file_name} to R2 bucket '{BUCKET_NAME}'...")
    try:
        s3.upload_file(local_path, BUCKET_NAME, file_name)
        print(f"Uploaded {file_name} successfully.")
    except Exception as e:
        print(f"ERROR: Failed to upload {file_name}: {e}")

# ====================================================
# PIPELINE FUNCTIONS
# ====================================================

def run_pipeline(source_type="synthetic"):
    print(f"Starting ETL Pipeline in {source_type.upper()} mode...\n")
    
    # 1. Acquire dataframes
    if source_type == "synthetic":
        from etl.generate_synthetic_data import generate_all_dfs
        raw_dfs = generate_all_dfs()
    else:
        # Load from local Excel files in data/
        print("Reading local Excel files...")
        raw_dfs = {}
        try:
            raw_dfs['rm_zm'] = pd.read_excel("data/raw/rm_zm.xlsx")
            raw_dfs['targets'] = pd.read_excel("data/raw/targets.xlsx")
            raw_dfs['daily_targets'] = pd.read_excel("data/processed/daily_targets.xlsx")
            raw_dfs['branch_daily_aggregate'] = pd.read_excel("data/processed/branch_daily_aggregate.xlsx")
            raw_dfs['customer_list'] = pd.read_excel("data/processed/processed_customer.xlsx", dtype={'Phone No.': str, 'Customer No.': str})
            raw_dfs['tag_list'] = pd.read_excel("data/processed/processed_tags.xlsx")
            raw_dfs['tag_received'] = pd.read_excel("data/processed/tag_received.xlsx")
            raw_dfs['tag_sold'] = pd.read_excel("data/processed/tag_sold.xlsx")
            raw_dfs['old_gold_list'] = pd.read_excel("data/processed/processed_old_gold.xlsx")
            raw_dfs['merged_scheme'] = pd.read_excel("data/processed/merged_scheme_joining_report.xlsx")
            raw_dfs['merged_sales'] = pd.read_excel("data/processed/merged_sales.xlsx")
            raw_dfs['user_access'] = pd.read_excel("data/processed/user_access.xlsx")
        except Exception as e:
            print(f"ERROR: Failed to read local Excel files: {e}")
            print("Make sure files exist under 'data/raw/' and 'data/processed/' or run with '--synthetic'")
            return

    # 2. Process and write snapshots
    
    # --- rm_zm ---
    print("\nProcessing rm_zm...")
    df_rm_zm = raw_dfs['rm_zm'].copy()
    df_rm_zm.to_parquet(f"{SNAPSHOT_DIR}/rm_zm.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/rm_zm.parquet")
    
    # --- user_access ---
    print("\nProcessing user_access...")
    df_ua = raw_dfs['user_access'].copy()
    df_ua.columns = [c.strip().lower().replace(" ", "_") for c in df_ua.columns]
    df_ua.to_parquet(f"{SNAPSHOT_DIR}/user_access.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/user_access.parquet")
    
    # --- targets ---
    print("\nProcessing targets...")
    df_targets = raw_dfs['targets'].copy()
    df_targets['month'] = pd.to_datetime(df_targets['month'], errors='coerce')
    df_targets.to_parquet(f"{SNAPSHOT_DIR}/targets.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/targets.parquet")
    
    # --- daily_targets ---
    print("\nProcessing daily_targets...")
    df_dt = raw_dfs['daily_targets'].copy()
    df_dt['Date'] = pd.to_datetime(df_dt['Date'], errors='coerce')
    df_dt.to_parquet(f"{SNAPSHOT_DIR}/daily_targets.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/daily_targets.parquet")
    
    # --- customer_list ---
    print("\nProcessing customer_list...")
    df_cust = raw_dfs['customer_list'].copy()
    df_cust.columns = [c.strip().lower().replace(" ", "_") for c in df_cust.columns]
    df_cust['phone_no.'] = df_cust['phone_no.'].astype(str).str.replace('.0', '', regex=False).str.strip()
    df_cust['customer_no.'] = df_cust['customer_no.'].astype(str).str.replace('.0', '', regex=False).str.strip()
    df_cust['birth_date'] = pd.to_datetime(df_cust['birth_date'], errors='coerce')
    df_cust['anniversary_date'] = pd.to_datetime(df_cust['anniversary_date'], errors='coerce')
    df_cust.to_parquet(f"{SNAPSHOT_DIR}/customer_list.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/customer_list.parquet")
    
    # --- tag_list ---
    print("\nProcessing tag_list...")
    df_tag = raw_dfs['tag_list'].copy()
    df_tag.columns = [c.strip().lower().replace(" ", "_") for c in df_tag.columns]
    for col in ['tag_generated_date', 'tag_received_date']:
        if col in df_tag.columns:
            df_tag[col] = pd.to_datetime(df_tag[col], errors='coerce')
    df_tag.to_parquet(f"{SNAPSHOT_DIR}/tag_list.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/tag_list.parquet")
    
    # --- tag_received ---
    print("\nProcessing tag_received...")
    df_tr = raw_dfs['tag_received'].copy()
    df_tr.columns = [c.strip().lower().replace(" ", "_") for c in df_tr.columns]
    if 'tag_received_date' in df_tr.columns:
        df_tr['tag_received_date'] = pd.to_datetime(df_tr['tag_received_date'], errors='coerce')
    df_tr.to_parquet(f"{SNAPSHOT_DIR}/tag_received.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/tag_received.parquet")
    
    # --- tag_sold ---
    print("\nProcessing tag_sold...")
    df_ts = raw_dfs['tag_sold'].copy()
    df_ts.columns = [c.strip().lower().replace(" ", "_") for c in df_ts.columns]
    if 'invoice_date' in df_ts.columns:
        df_ts['invoice_date'] = pd.to_datetime(df_ts['invoice_date'], errors='coerce')
    df_ts.to_parquet(f"{SNAPSHOT_DIR}/tag_sold.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/tag_sold.parquet")
    
    # --- old_gold_list ---
    print("\nProcessing old_gold_list...")
    df_og = raw_dfs['old_gold_list'].copy()
    df_og.columns = [c.strip().lower().replace(" ", "_") for c in df_og.columns]
    if 'posting_date' in df_og.columns:
        df_og['posting_date'] = pd.to_datetime(df_og['posting_date'], errors='coerce')
    df_og.to_parquet(f"{SNAPSHOT_DIR}/old_gold_list.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/old_gold_list.parquet")
    
    # --- branch_daily_aggregate ---
    print("\nProcessing branch_daily_aggregate...")
    df_ba = raw_dfs['branch_daily_aggregate'].copy()
    df_ba['Date'] = pd.to_datetime(df_ba['Date'], errors='coerce')
    df_ba.to_parquet(f"{SNAPSHOT_DIR}/branch_daily_aggregate.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/branch_daily_aggregate.parquet")
    
    # --- merged_scheme ---
    print("\nProcessing merged_scheme...")
    df_scheme = raw_dfs['merged_scheme'].copy()
    df_scheme["LocationName"] = df_scheme["LocationName"].astype(str).str.strip()
    for col in ['SCHEMEOPENINGDATE', 'schemefirstpaydate', 'MATURITYDATE']:
        if col in df_scheme.columns:
            df_scheme[col] = pd.to_datetime(df_scheme[col], errors='coerce')
    df_scheme.to_parquet(f"{SNAPSHOT_DIR}/merged_scheme.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/merged_scheme.parquet")
    
    # --- merged_sales ---
    print("\nProcessing merged_sales...")
    df_sales = raw_dfs['merged_sales'].copy()
    for col in ['Invoice Date', 'Posting Date']:
        if col in df_sales.columns:
            df_sales[col] = pd.to_datetime(df_sales[col], errors='coerce')
    df_sales.to_parquet(f"{SNAPSHOT_DIR}/merged_sales.parquet", index=False)
    upload_to_r2(f"{SNAPSHOT_DIR}/merged_sales.parquet")
    
    print("\n====================================================")
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("All Parquet snapshots generated locally and uploaded to R2.")
    print("====================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Central ETL pipeline runner for Orient Analytics.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--synthetic", action="store_true", help="Generate and load synthetic data.")
    group.add_argument("--local", action="store_true", help="Load from local Excel files.")
    
    args = parser.parse_args()
    
    source = "synthetic" if args.synthetic else "local"
    run_pipeline(source)
