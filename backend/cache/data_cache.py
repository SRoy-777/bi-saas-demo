DEV_MODE = False

from download_from_r2 import *
import pandas as pd
import os


# ---------------------------------------------------
# Load Snapshot
# ---------------------------------------------------

print("Loading parquet snapshots...")


# ---------------------------------------------------
# merged_sales
# ---------------------------------------------------

if DEV_MODE:

    print("DEV MODE ENABLED -> Loading limited rows...")

    merged_sales_df = pd.read_parquet(

        os.path.join(SNAPSHOT_DIR, "merged_sales.parquet")

    ).tail(1000)

else:

    print("PRODUCTION MODE -> Loading full merged_sales...")

    merged_sales_df = pd.read_parquet(

        os.path.join(SNAPSHOT_DIR, "merged_sales.parquet")

    )

# ---------------------------------------------------
# rm_zm
# ---------------------------------------------------

rm_zm_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "rm_zm.parquet")

)


# ---------------------------------------------------
# targets
# ---------------------------------------------------

targets_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "targets.parquet")

)


# ---------------------------------------------------
# merged_scheme
# ---------------------------------------------------

scheme_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "merged_scheme.parquet")

)


# ---------------------------------------------------
# tag_list
# ---------------------------------------------------

tag_list_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "tag_list.parquet")

)


# ---------------------------------------------------
# customer_list
# ---------------------------------------------------

customer_list_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "customer_list.parquet")

)

# ---------------------------------------------------
# user_access
# ---------------------------------------------------

user_access_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "user_access.parquet")

)

# ---------------------------------------------------
# Basket Analysis
# ---------------------------------------------------

tag_sold_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "tag_sold.parquet")

)


tag_received_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "tag_received.parquet")

)

# ---------------------------------------------------
# Branch Health
# ---------------------------------------------------

branch_daily_aggregate_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "branch_daily_aggregate.parquet")

)

daily_targets_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "daily_targets.parquet")

)

# ---------------------------------------------------
# Period Comparison Dashboard
# ---------------------------------------------------

# Uses:
# - branch_daily_aggregate_df
# - rm_zm_df
#
# No additional parquet required currently.

# ---------------------------------------------------
# Old Gold
# ---------------------------------------------------

old_gold_df = pd.read_parquet(

    os.path.join(SNAPSHOT_DIR, "old_gold_list.parquet")

)

# ---------------------------------------------------
# Date Conversion
# ---------------------------------------------------

branch_daily_aggregate_df['Date'] = pd.to_datetime(

    branch_daily_aggregate_df['Date']

)

daily_targets_df['Date'] = pd.to_datetime(

    daily_targets_df['Date']

)

old_gold_df['posting_date'] = pd.to_datetime(

    old_gold_df['posting_date']

)


# ---------------------------------------------------
# Standardize Text Columns
# ---------------------------------------------------

branch_daily_aggregate_df['Location'] = (

    branch_daily_aggregate_df['Location']

    .astype(str)

    .str.strip()

    .str.upper()

)

daily_targets_df['Location'] = (

    daily_targets_df['Location']

    .astype(str)

    .str.strip()

    .str.upper()

)

old_gold_df['location_name'] = (

    old_gold_df['location_name']

    .astype(str)

    .str.strip()

    .str.upper()

)

old_gold_df['item_type'] = (

    old_gold_df['item_type']

    .astype(str)

    .str.strip()

    .str.upper()

)

old_gold_df['transaction_type'] = (

    old_gold_df['transaction_type']

    .astype(str)

    .str.strip()

    .str.upper()

)

# ---------------------------------------------------
# Date Conversions
# ---------------------------------------------------

merged_sales_df['Invoice Date'] = pd.to_datetime(

    merged_sales_df['Invoice Date']

)


targets_df['month'] = pd.to_datetime(

    targets_df['month']

)


scheme_df['SCHEMEOPENINGDATE'] = pd.to_datetime(

    scheme_df['SCHEMEOPENINGDATE']

)


tag_list_df['tag_generated_date'] = pd.to_datetime(

    tag_list_df['tag_generated_date']

)


tag_list_df['tag_received_date'] = pd.to_datetime(

    tag_list_df['tag_received_date']

)

customer_list_df['birth_date'] = pd.to_datetime(

    customer_list_df['birth_date'],

    errors='coerce'

)

customer_list_df['anniversary_date'] = pd.to_datetime(

    customer_list_df['anniversary_date'],

    errors='coerce'

)


# ---------------------------------------------------
# Standardize Text Columns
# ---------------------------------------------------

merged_sales_df['Location Name'] = (

    merged_sales_df['Location Name']

    .astype(str)

    .str.strip()

    .str.upper()

)


rm_zm_df['location'] = (

    rm_zm_df['location']

    .astype(str)

    .str.strip()

    .str.upper()

)


rm_zm_df['rm'] = (

    rm_zm_df['rm']

    .astype(str)

    .str.strip()

    .str.upper()

)


rm_zm_df['zm'] = (

    rm_zm_df['zm']

    .astype(str)

    .str.strip()

    .str.upper()

)


tag_list_df['location_name'] = (

    tag_list_df['location_name']

    .astype(str)

    .str.strip()

    .str.upper()

)


tag_list_df['counter_code'] = (

    tag_list_df['counter_code']

    .astype(str)

    .str.strip()

    .str.upper()

)

tag_sold_df['location_name'] = (

    tag_sold_df['location_name']

    .astype(str)

    .str.strip()

    .str.upper()

)


tag_sold_df['counter'] = (

    tag_sold_df['counter']

    .astype(str)

    .str.strip()

    .str.upper()

)


tag_received_df['location_name'] = (

    tag_received_df['location_name']

    .astype(str)

    .str.strip()

    .str.upper()

)


tag_received_df['counter_code'] = (

    tag_received_df['counter_code']

    .astype(str)

    .str.strip()

    .str.upper()

)

customer_list_df['location_name'] = (

    customer_list_df['location_name']

    .astype(str)

    .str.strip()

    .str.upper()

)

print("Parquet snapshots loaded successfully.")