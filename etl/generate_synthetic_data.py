import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ====================================================
# MASTER DATA CONSTANTS
# ====================================================

LOCATIONS = [
    {'rm': 'Anupam', 'zm': 'SSM Mohua', 'location': 'SILIGURI', 'code': '103'},
    {'rm': 'Anupam', 'zm': 'SSM Mohua', 'location': 'JALPAIGURI', 'code': '106'},
    {'rm': 'Anupam', 'zm': 'SSM Mohua', 'location': 'MALBAZAR', 'code': '113'},
    {'rm': 'Anupam', 'zm': 'Tridip', 'location': 'RAGHUNATHGANJ', 'code': '120'},
    {'rm': 'Anupam', 'zm': 'Tridip', 'location': 'BELDANGA', 'code': '121'},
    {'rm': 'Anupam', 'zm': 'Tridip', 'location': 'SAINTHIA', 'code': '124'},
    {'rm': 'Anupam', 'zm': 'Tridip', 'location': 'MOLLARPUR', 'code': '125'},
    {'rm': 'Anupam', 'zm': 'Rajib', 'location': 'BETHUADAHARI', 'code': '123'},
    {'rm': 'Anupam', 'zm': 'Rajib', 'location': 'CHAKDAHA', 'code': '126'},
    {'rm': 'Anupam', 'zm': 'Rajib', 'location': 'BALURGHAT', 'code': '104'},
    {'rm': 'Anupam', 'zm': 'Rajib', 'location': 'ISLAMPUR', 'code': '105'},
    {'rm': 'Arindam', 'zm': 'Rajib', 'location': 'RAIGANJ', 'code': '102'},
    {'rm': 'Arindam', 'zm': 'Rajib', 'location': 'KALIYAGANJ', 'code': '111'},
    {'rm': 'Arindam', 'zm': 'Rajib', 'location': 'RAIGANJ MEGA', 'code': '115'},
    {'rm': 'Arindam', 'zm': 'Preetam', 'location': 'ALIPURDUAR', 'code': '107'},
    {'rm': 'Arindam', 'zm': 'Preetam', 'location': 'FALAKATA', 'code': '112'},
    {'rm': 'Arindam', 'zm': 'Preetam', 'location': 'MATHABHANGA', 'code': '127'},
    {'rm': 'Arindam', 'zm': 'Preetam', 'location': 'DHUPGURI', 'code': 'FRN001'},
    {'rm': 'Arindam', 'zm': 'Sudhanshu', 'location': 'KALIACHAK', 'code': '116'},
    {'rm': 'Arindam', 'zm': 'Sudhanshu', 'location': 'GAZOLE', 'code': '117'},
    {'rm': 'Arindam', 'zm': 'Sudhanshu', 'location': 'DHULIYAN', 'code': '118'},
    {'rm': 'Arindam', 'zm': 'Sudhanshu', 'location': 'SUJAPUR', 'code': '119'}
]

FIRST_NAMES = [
    "SUPRIYA", "BABLU", "SAMPA", "SOHINI", "LAXMI", "SABARNI", "SHREYA",
    "MOUMITA", "BIDISHA", "SANJIT", "SENABUL", "AMIT", "PRIYA", "RAHUL",
    "POOJA", "VIKRAM", "ANKITA", "SUMAN", "RAJESH", "NEHA", "DIPANKAR",
    "MANISHA", "JHARNA", "TUMPA", "RIMA", "ARUP", "SHALINI", "SOUMYADIP"
]

LAST_NAMES = [
    "SARKAR", "SAHA", "BHATTACHARJEE", "TIWARI", "DEBNATH", "DAS",
    "PAUL", "ROY", "HAQUE", "MUKHERJEE", "LASKAR", "PASMAN", "HALDAR",
    "SEN", "CHAKRABORTY", "DEY", "GHOSH", "BANERJEE", "DUTTA", "KARMAKAR"
]

ORAMENTS = [
    {"cat": "GPB", "subcat": "GPB-CHUR", "counter": "G-BANGLE", "type": "GOLD"},
    {"cat": "GC", "subcat": "GC-BB", "counter": "G-CHAIN", "type": "GOLD"},
    {"cat": "GNB", "subcat": "GNB-CHN", "counter": "G-BANGLE", "type": "GOLD"},
    {"cat": "DIA", "subcat": "DIA-RING", "counter": "DIAMOND", "type": "DIAMOND"},
    {"cat": "SMRT", "subcat": "SMRT-GAN", "counter": "SILVER", "type": "SILVER"},
    {"cat": "GART", "subcat": "GART-GOD", "counter": "G-MISC", "type": "GOLD"},
    {"cat": "BBL", "subcat": "BBL-FNC", "counter": "G-BANGLE", "type": "GOLD"},
    {"cat": "BBT", "subcat": "BBT-FNC", "counter": "G-PR", "type": "GOLD"}
]

SALES_PERSONS = [
    {"code": "E00087", "name": "JHARNA DAS"},
    {"code": "E00110", "name": "MANISHA PASMAN"},
    {"code": "E00014", "name": "TUMPA SHARMA"},
    {"code": "E00232", "name": "MANIMESH HALDAR"},
    {"code": "E00289", "name": "RIMA DAS"}
]

ASTROLOGERS = [
    {"code": "A_00001", "name": "SANJAY LASKAR"},
    {"code": "A_00003", "name": "DIPANKAR MUKHOPADHYAY"},
    {"code": "A_00004", "name": "DIPANKAR DAS"}
]

VENDORS = [
    {"code": "V_00012", "name": "JAGDAMBA GOLD & DIAMONDS PRIVATE LIMITED"},
    {"code": "V_00014", "name": "KAANISK JEWELS PVT LTD"},
    {"code": "K_00002", "name": "KOLKATA ART"}
]

# Helper to generate random full names
def gen_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

# Helper to generate random date
def gen_date(start_year=2025, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 6, 1)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return (start + timedelta(seconds=random_second)).replace(hour=0, minute=0, second=0, microsecond=0)

# ====================================================
# GENERATORS
# ====================================================

def generate_rm_zm():
    df = pd.DataFrame(LOCATIONS)
    return df

def generate_user_access():
    ALL_LOCATIONS = 'RAIGANJ MEGA,BETHUADAHARI,BELDANGA,RAGHUNATHGANJ,DHULIYAN,KALIACHAK,SUJAPUR,GAZOLE,RAIGANJ,KALIYAGANJ,BALURGHAT,ISLAMPUR,SILIGURI,JALPAIGURI,FALAKATA,DHUPGURI,MALBAZAR,ALIPURDUAR,SAINTHIA,CHAKDAHA,MOLLARPUR,MATHABHANGA'
    ALL_DASHBOARDS = 'performance,comparison,aging-stock,daily-customer,mini-nsv,stock-movement,basket-analysis,branch-health,old-gold,period-comparison,company-snapshot'

    users = [
        # Public demo account — full admin access
        # Email   : demo@admin.com
        # Password: demo@1234
        {'email': 'demo@admin.com', 'password': 'demo@1234', 'dashboards': ALL_DASHBOARDS, 'locations': ALL_LOCATIONS},
    ]
    df = pd.DataFrame(users)
    return df

def generate_targets(num_months=24):
    records = []
    start_date = datetime(2025, 1, 1)
    
    for i in range(num_months):
        month_dt = start_date + timedelta(days=31 * i)
        # Normalize to 1st of month
        month_dt = month_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        for loc in LOCATIONS:
            records.append({
                'month': month_dt,
                'location': loc['location'],
                'nsv': float(random.randint(50, 250) * 100000),
                'gold_w': float(random.randint(200, 1000)),
                'diamond_cts': float(random.randint(1, 10) + round(random.random(), 2)),
                'silver_w': float(random.randint(200, 2000)),
                'gemstone_nsv': float(random.randint(1000, 100000)),
                'mohor_nsv': float(random.randint(10000, 200000))
            })
            
    df = pd.DataFrame(records)
    return df

def generate_daily_targets(num_days=600):
    records = []
    start_date = datetime(2025, 1, 1)
    
    for d in range(num_days):
        date_dt = start_date + timedelta(days=d)
        for loc in LOCATIONS:
            # Generate daily target (approx 1/30 of month)
            records.append({
                'Date': date_dt,
                'Location': loc['location'],
                'nsv_target': float(random.randint(5000, 50000)),
                'gold_target': float(random.randint(5, 50)),
                'diamond_cts_target': float(random.randint(0, 1) + round(random.random(), 2)),
                'silver_target': float(random.randint(5, 100)),
                'gemstone_target': float(random.randint(100, 5000)),
                'mohor_target': float(random.randint(500, 10000))
            })
            
    df = pd.DataFrame(records)
    return df

def generate_customer_list(num_customers=5000):
    records = []
    for i in range(num_customers):
        cus_id = f"CUS{str(i).zfill(8)}"
        phone = f"9{str(random.randint(0, 999999999)).zfill(9)}"
        loc = random.choice(LOCATIONS)
        
        # Birthday and anniversary
        birth = datetime(random.randint(1970, 2005), random.randint(1, 12), random.randint(1, 28))
        anniv = datetime(random.randint(1995, 2024), random.randint(1, 12), random.randint(1, 28)) if random.random() > 0.3 else None
        
        records.append({
            'phone_no.': phone,
            'customer_no.': cus_id,
            'name': gen_name(),
            'birth_date': birth,
            'anniversary_date': anniv,
            'location_code': loc['code'],
            'location_name': loc['location']
        })
        
    df = pd.DataFrame(records)
    return df

def generate_tag_list(num_tags=10000):
    records = []
    for i in range(num_tags):
        tag_no = f"TAG{str(i).zfill(8)}"
        orn = random.choice(ORAMENTS)
        loc = random.choice(LOCATIONS)
        
        gen_dt = gen_date(2024, 2025)
        # Received is after or equal to gen date
        rec_dt = gen_dt + timedelta(days=random.randint(0, 60)) if random.random() > 0.05 else None
        
        records.append({
            'tag_no.': tag_no,
            'counter_code': orn['counter'],
            'net_weight': float(round(random.uniform(1.0, 50.0), 3)),
            'location_code': loc['code'],
            'ornament_category_code': orn['cat'],
            'tag_generated_date': gen_dt,
            'tag_received_date': rec_dt,
            'ornament_sub_category_code': orn['subcat'],
            'weight_range_code': f"WR{str(random.randint(1, 5000)).zfill(7)}" if random.random() > 0.1 else None,
            'location_name': loc['location']
        })
        
    df = pd.DataFrame(records)
    return df

def generate_tag_received(num_records=5000):
    records = []
    for i in range(num_records):
        tag_no = f"REC{str(i).zfill(8)}"
        orn = random.choice(ORAMENTS)
        loc = random.choice(LOCATIONS)
        rec_dt = gen_date(2024, 2026)
        
        weight = float(round(random.uniform(0.5, 30.0), 3))
        # Baskets
        if weight <= 1.5:
            b = "0.000 - 1.500"
        elif weight <= 3.0:
            b = "0.000 - 3.000"
        elif weight <= 6.0:
            b = "3.001 - 6.000"
        else:
            b = "6.001 - 9.000"
            
        records.append({
            'tag_no.': tag_no,
            'counter_code': orn['counter'],
            'net_weight': weight,
            'location_code': loc['code'],
            'ornament_category_code': orn['cat'],
            'tag_received_date': rec_dt,
            'ornament_sub_category_code': orn['subcat'],
            'location_name': loc['location'],
            'basket': b,
            'subcat_basket': f"{orn['subcat']}_{b}"
        })
        
    df = pd.DataFrame(records)
    return df

def generate_tag_sold(num_records=5000):
    records = []
    for i in range(num_records):
        tag_no = f"SLD{str(i).zfill(8)}"
        orn = random.choice(ORAMENTS)
        loc = random.choice(LOCATIONS)
        inv_dt = gen_date(2024, 2026)
        
        qty = float(round(random.uniform(1.0, 30.0), 3))
        # Baskets
        if qty <= 1.5:
            b = "0.000 - 1.500"
        elif qty <= 3.0:
            b = "3.001 - 6.000"
        elif qty <= 9.0:
            b = "6.001 - 9.000"
        else:
            b = "9.001 - 12.000"
            
        records.append({
            'tag_no': tag_no,
            'location_name': loc['location'],
            'invoice_date': inv_dt,
            'counter': orn['counter'],
            'ornament_category_code': orn['cat'],
            'ornament_sub_category_code': orn['subcat'],
            'bom_qty': qty,
            'basket': b,
            'subcat_basket': f"{orn['subcat']}_{b}"
        })
        
    df = pd.DataFrame(records)
    return df

def generate_old_gold(num_records=1000):
    records = []
    for i in range(num_records):
        post_dt = gen_date(2025, 2026)
        loc = random.choice(LOCATIONS)
        phone = int(f"9{str(random.randint(0, 999999999)).zfill(9)}")
        
        records.append({
            'posting_date': post_dt,
            'customer_code': f"CUS{str(i).zfill(8)}",
            'customer_name': gen_name(),
            'location_code': loc['code'],
            'location_name': loc['location'],
            'item_type': random.choice(['Gold', 'Silver', 'Diamond', 'Platinum']),
            'net_weight': float(round(random.uniform(0.5, 100.0), 3)),
            'amount': float(random.randint(5000, 300000)),
            'own': random.choice([0, 1]),
            'sale_bill_amount': random.randint(0, 500000),
            'transaction_type': random.choice(['Exchange', 'Purchase']),
            'phone_number': phone
        })
        
    df = pd.DataFrame(records)
    return df

def generate_branch_daily_aggregate(num_records=5000):
    records = []
    start_dt = datetime(2025, 1, 1)
    
    for i in range(num_records):
        date_dt = start_dt + timedelta(days=random.randint(0, 500))
        loc = random.choice(LOCATIONS)
        
        nsv = float(random.randint(50, 1500) * 1000)
        gold = float(round(random.uniform(0.0, 150.0), 3))
        gold_nsv = float(gold * 7000 * random.uniform(0.9, 1.1)) if gold > 0 else 0.0
        
        records.append({
            'Date': date_dt,
            'Location': loc['location'],
            'nsv': nsv,
            'gold': gold,
            'gold_nsv': gold_nsv,
            'diamond_cts': float(round(random.uniform(0.0, 5.0), 2)),
            'diamond_nsv': float(random.randint(0, 200000)),
            'silver_gms': float(round(random.uniform(0.0, 500.0), 3)),
            'silver_nsv': float(random.randint(0, 35000)),
            'mohor_nsv': float(random.randint(0, 50000)),
            'gemstone_nsv': float(random.randint(0, 40000)),
            'invoices': random.randint(0, 30),
            'tags': random.randint(0, 50),
            'customers': random.randint(0, 30),
            'scheme_count': random.randint(0, 10),
            'scheme_payment': random.randint(0, 10) * 2000,
            'Footfall': random.randint(5, 100),
            'Cash': int(nsv * random.uniform(0.1, 0.4)),
            'Cheque': 0,
            'Card': int(nsv * random.uniform(0.1, 0.3)),
            'UPI': int(nsv * random.uniform(0.2, 0.5)),
            'NEFT/RTGS': int(nsv * random.uniform(0.0, 0.2))
        })
        
    df = pd.DataFrame(records)
    return df

def generate_merged_scheme(num_records=1000):
    records = []
    
    for i in range(num_records):
        loc = random.choice(LOCATIONS)
        sp = random.choice(SALES_PERSONS)
        cus_code = f"CUS{str(i).zfill(8)}"
        cus_name = gen_name()
        phone = float(f"9{str(random.randint(0, 999999999)).zfill(9)}")
        
        scheme_open = gen_date(2024, 2026)
        maturity = scheme_open + timedelta(days=365)
        
        emi = random.choice([1000, 2000, 5000, 10000])
        no_installments = random.choice([6, 10, 11, 12])
        
        records.append({
            'CompName': 'ABC JEWELLERS PVT. LTD',
            'ComAddress': 'ABC HUB, SILIGURI',
            'CompPostCode': 734001,
            'CompCity': 'SILIGURI',
            'ComGstin': '19AABCO1999E1Z6',
            'CompPAN': 'AABCO1999E',
            'SCHEMEOPENINGDATE': scheme_open,
            'INVENTLOCATIONID': loc['code'],
            'LocationName': loc['location'],
            'SALESPERSONCODE': sp['code'],
            'SalesPersonName': sp['name'],
            'CUSTOMERCODE': cus_code,
            'CUSTOMERNAME': cus_name,
            'custMobileNo': phone,
            'receiptNo': None,
            'SCHEMECODE': f"SCH-{emi}",
            'schemedes': f"Scheme EMI {emi}",
            'schemenature': 'Fix EMI',
            'NOOFINSTALLMENT': no_installments,
            'SCHEMEENTRYNO': f"SCH{str(i).zfill(8)}",
            'EMIAMOUNT': emi,
            'SCHEMECLOSINGVALUE': 0,
            'schemefirstpaydate': scheme_open,
            'SchemefirstPayamt': emi,
            'Goldrate': 0,
            'MATURITYDATE': maturity,
            'cash': random.randint(0, emi),
            'Noncash': emi,
            'SCHEMEENTRYSTATUS': 'Release'
        })
        
    df = pd.DataFrame(records)
    return df

def generate_merged_sales(num_records=5000):
    records = []
    
    for i in range(num_records):
        loc = random.choice(LOCATIONS)
        orn = random.choice(ORAMENTS)
        sp = random.choice(SALES_PERSONS)
        ast = random.choice(ASTROLOGERS)
        vendor = random.choice(VENDORS)
        
        inv_dt = gen_date(2025, 2026)
        cus_code = f"CUS{str(random.randint(1, 1000)).zfill(8)}"
        cus_name = gen_name()
        
        gross_w = float(round(random.uniform(2.0, 40.0), 3))
        net_w = float(round(gross_w * random.uniform(0.9, 0.98), 3))
        qty = random.choice([1, 1, 1, 1, 1, -1]) # returns are -1
        
        bom_qty = net_w
        bom_price = float(random.randint(6000, 7500))
        bom_amount = float(round(bom_qty * bom_price, 2))
        discount = float(round(bom_amount * random.uniform(0.0, 0.1), 2))
        bom_line_amt = float(round(bom_amount - discount, 2))
        
        gross_amt = bom_amount
        discount_amt = discount
        line_amt_str = str(bom_line_amt)
        
        tax_pct = 3.0
        tax_amt = float(round(bom_line_amt * 0.03, 2))
        charges = float(random.randint(100, 2000))
        payable = float(round(bom_line_amt + tax_amt + charges, 2))
        
        records.append({
            'Company': 'ABC JEWELLERS PVT. LTD',
            'Name': 'ABC JEWELLERS PVT. LTD',
            'Sales Type': 'Sales' if qty > 0 else 'Return',
            'Pre Document No': f"OG-P-SI-C{loc['code']}-{str(i).zfill(7)}" if random.random() > 0.8 else None,
            'Document No.': f"OG-SI-C{loc['code']}-{str(i).zfill(8)}",
            'External Document No': f"OG-SI-C{loc['code']}-{str(i).zfill(8)}",
            'Customer order No': f"CORD-C{loc['code']}-{str(random.randint(100, 10000))}" if random.random() > 0.5 else None,
            'Invoice Date': inv_dt,
            'Posting Date': inv_dt,
            'Customer Code': cus_code,
            'Customer Name': cus_name,
            'Cust Gst No': None,
            'State Code': 'WB',
            'Location Code': loc['code'],
            'Location Name': loc['location'],
            'Location GSTIN No.': '19AABCO1999E1Z6',
            'Tag No': f"TAG{str(random.randint(1, 10000)).zfill(8)}",
            'Item Type Group': orn['type'],
            'Sales Person Code': sp['code'],
            'Sales Person Name': sp['name'],
            'Astrologer Code': ast['code'] if random.random() > 0.8 else None,
            'Astrologer Name': ast['name'] if random.random() > 0.8 else None,
            'Item Id': f"FG-{orn['cat']}-ITEM-22K",
            'Item Name': f"{orn['type']} {orn['subcat']} (22K)",
            'HSN/SAC Code': 71131910.0,
            'Item Category Code': 'FG ITEM',
            'Ornament Category Code': orn['cat'],
            'Ornament Sub Category Code': orn['subcat'],
            'Counter': orn['counter'],
            'Purity': 91.66 if orn['type'] == 'GOLD' else 75.0,
            'Ornament Size': str(random.choice([2.4, 2.6, 18, 20])),
            'Design Code': f"DGR-D{str(random.randint(1, 10000)).zfill(8)}" if random.random() > 0.2 else None,
            'Collection': None,
            'Vendor Code': vendor['code'],
            'Vendor Name': vendor['name'],
            'Style Code': 'FS',
            'Theme Code': 'GE',
            'Brand Id': 'MOHOR' if random.random() > 0.5 else 'DITI',
            'Target Group': random.choice(['NONE', 'FEMALE', 'MALE']),
            'Gross Weight': gross_w,
            'Net Weight': net_w,
            'Quantity': qty,
            'UOM': 'PCS',
            'Gross Amount': gross_amt,
            'Discount Amount': discount_amt,
            'Offer Code': f"FY25-26-OD-{str(random.randint(1, 100)).zfill(6)}" if random.random() > 0.8 else None,
            'Line Amount': line_amt_str,
            'Tax Percentage': tax_pct,
            'Tax Amount': tax_amt,
            'Charges Amount': charges,
            'Payble Amount': payable,
            'Bom Item': f"MK-{orn['cat']}-T-22K",
            'Bom Line No': '10000',
            'Bom Type': 'SEVICE' if random.random() > 0.5 else 'MATERIAL',
            'Bom Item Type': orn['type'],
            'Bom Category': 'GRAW',
            'Bom Sub category': 'GRAW',
            'Bom Gross Weight': '0',
            'Bom Net Weight': net_w,
            'Bom Qty': bom_qty,
            'Bom UOM': 'GMS' if orn['type'] in ['GOLD', 'SILVER'] else 'CTS',
            'Bom Price': str(bom_price),
            'Bom Amount': bom_amount,
            'Bom Discount': discount,
            'Bom Line Amount': bom_line_amt,
            'Incentive/Commision': orn['type'].capitalize(),
            'Unnamed: 66': None
        })
        
    df = pd.DataFrame(records)
    return df

# ====================================================
# MASTER RUNNER
# ====================================================

def generate_all_dfs():
    print("Generating synthetic dataframes...")
    return {
        'rm_zm': generate_rm_zm(),
        'user_access': generate_user_access(),
        'targets': generate_targets(),
        'daily_targets': generate_daily_targets(),
        'customer_list': generate_customer_list(),
        'tag_list': generate_tag_list(),
        'tag_received': generate_tag_received(),
        'tag_sold': generate_tag_sold(),
        'old_gold_list': generate_old_gold(),
        'branch_daily_aggregate': generate_branch_daily_aggregate(),
        'merged_scheme': generate_merged_scheme(),
        'merged_sales': generate_merged_sales()
    }

if __name__ == "__main__":
    dfs = generate_all_dfs()
    # Save a sample to test
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Save raw equivalent files
    print("Saving mock raw spreadsheets to simulate input files...")
    dfs['rm_zm'].to_excel("data/raw/rm_zm.xlsx", index=False)
    dfs['targets'].to_excel("data/raw/targets.xlsx", index=False)
    dfs['daily_targets'].to_excel("data/processed/daily_targets.xlsx", index=False)
    dfs['branch_daily_aggregate'].to_excel("data/processed/branch_daily_aggregate.xlsx", index=False)
    dfs['customer_list'].to_excel("data/processed/processed_customer.xlsx", index=False)
    dfs['tag_list'].to_excel("data/processed/processed_tags.xlsx", index=False)
    dfs['tag_received'].to_excel("data/processed/tag_received.xlsx", index=False)
    dfs['tag_sold'].to_excel("data/processed/tag_sold.xlsx", index=False)
    dfs['old_gold_list'].to_excel("data/processed/processed_old_gold.xlsx", index=False)
    dfs['merged_scheme'].to_excel("data/processed/merged_scheme_joining_report.xlsx", index=False)
    dfs['merged_sales'].to_excel("data/processed/merged_sales.xlsx", index=False)
    dfs['user_access'].to_excel("data/processed/user_access.xlsx", index=False)
    
    print("All mock files successfully saved under data/raw and data/processed.")
