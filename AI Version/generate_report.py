import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from datetime import datetime
import re, os
from collections import Counter

# Style
plt.rcParams['font.family'] = 'DejaVu Sans'
COLORS = ['#2563eb','#0ea5e9','#10b981','#f59e0b','#ef4444','#8b5cf6','#ec4899','#14b8a6','#f97316','#6366f1']
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.25

INPUT = "/home/user/uploads/ecommerce_retail_transactions_raw.csv"
OUT_DIR = "/home/user/report_assets"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT)

# Basic info
total_rows = len(df)

# Clean Quantity: convert to numeric, handle negatives/zeros
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Unit_Price_USD'] = pd.to_numeric(df['Unit_Price_USD'], errors='coerce')
df['Discount_Percent'] = pd.to_numeric(df['Discount_Percent'], errors='coerce').fillna(0)
df['Customer_Rating'] = pd.to_numeric(df['Customer_Rating'], errors='coerce')

# Clean text fields
for col in ['Product_Category','Product_Name','Payment_Method','Country','Order_Status','Shipping_City']:
    df[col] = df[col].astype(str).str.strip()

# Normalize Payment Method
def norm_pay(x):
    x = x.lower().replace('_',' ').replace('.','').strip()
    x = re.sub(r'\s+', ' ', x)
    mapping = {
        'net banking': 'Net Banking',
        'netbanking': 'Net Banking',
        'credit card': 'Credit Card',
        'creditcard': 'Credit Card',
        'debit card': 'Debit Card',
        'cash on delivery': 'Cash on Delivery',
        'cod': 'Cash on Delivery',
        'paypal': 'PayPal',
        'pay pal': 'PayPal',
        'upi': 'UPI',
        'u p i': 'UPI',
    }
    return mapping.get(x, x.title())
df['Payment_Method_Clean'] = df['Payment_Method'].apply(norm_pay)

# Normalize Country
def norm_country(x):
    xl = x.strip().lower().replace('.','').replace(' ','')
    mp = {
        'usa': 'USA', 'us': 'USA', 'unitedstates': 'USA',
        'uk': 'UK', 'uk': 'UK', 'unitedkingdom': 'UK',
        'uae': 'UAE', 'uae': 'UAE',
        'india': 'India', 'in': 'India',
        'canada': 'Canada', 'ca': 'Canada',
        'australia': 'Australia', 'au': 'Australia',
        'germany': 'Germany', 'de': 'Germany', 'germany': 'Germany',
    }
    # handle variants
    x_clean = x.strip().lower()
    x_nopunct = re.sub(r'[^a-z]', '', x_clean)
    if x_nopunct in ['usa','us','unitedstates','unitedstatesofamerica']:
        return 'USA'
    if x_nopunct in ['uk','unitedkingdom','u k','england']:
        return 'UK'
    if x_nopunct in ['uae','unitedarabemirates']:
        return 'UAE'
    if x_nopunct in ['india','in','ind']:
        return 'India'
    if x_nopunct in ['canada','ca']:
        return 'Canada'
    if x_nopunct in ['australia','au']:
        return 'Australia'
    if x_nopunct in ['germany','de','deutschland']:
        return 'Germany'
    # fallback title
    if x.strip()=='' or x.strip().lower()=='nan':
        return 'Unknown'
    return x.strip().title()

df['Country_Clean'] = df['Country'].apply(lambda x: norm_country(str(x)))

# Normalize Order_Status
df['Order_Status_Clean'] = df['Order_Status'].str.strip().str.title()
df['Order_Status_Clean'] = df['Order_Status_Clean'].replace({'Nan':'Unknown'})

# Parse dates - multiple formats
def parse_date(s):
    s=str(s).strip()
    fmts = ["%Y-%m-%d","%Y/%m/%d","%m-%d-%Y","%d/%m/%Y","%d %b %Y","%d %B %Y","%b %d %Y","%B %d %Y","%Y-%m-%d","%d-%m-%Y"]
    # try pandas parser
    try:
        return pd.to_datetime(s, dayfirst=False, errors='coerce', infer_datetime_format=True)
    except:
        return pd.NaT

df['Order_Date_Parsed'] = pd.to_datetime(df['Order_Date'], errors='coerce', infer_datetime_format=True, dayfirst=False)
# fallback for others like 17 Jun 2024 already handled? but check NaT
mask = df['Order_Date_Parsed'].isna()
# try dayfirst
df.loc[mask, 'Order_Date_Parsed'] = pd.to_datetime(df.loc[mask, 'Order_Date'], errors='coerce', dayfirst=True)

df['Order_Month'] = df['Order_Date_Parsed'].dt.to_period('M').astype(str)
df['Order_YearMonth'] = df['Order_Date_Parsed'].dt.strftime('%Y-%m')

# Revenue calculation: Quantity * Unit_Price * (1 - discount/100)
# Flag invalid quantities <=0
df['Is_Valid_Qty'] = df['Quantity'] > 0
df['Revenue'] = df['Quantity'] * df['Unit_Price_USD'] * (1 - df['Discount_Percent']/100)
# For invalid qty, revenue is 0 or negative? set to 0 for analysis but keep count
df['Revenue_Clean'] = np.where(df['Is_Valid_Qty'], df['Revenue'], 0)
# Also gross before discount
df['Gross'] = df['Quantity'] * df['Unit_Price_USD']
df['Gross_Clean'] = np.where(df['Is_Valid_Qty'], df['Gross'], 0)

# Metrics
total_orders = len(df)
valid_orders = int(df['Is_Valid_Qty'].sum())
invalid_qty = total_orders - valid_orders
total_revenue = df['Revenue_Clean'].sum()
avg_order_value = total_revenue / valid_orders if valid_orders else 0
delivered = df[df['Order_Status_Clean']=='Delivered']
delivered_revenue = delivered['Revenue_Clean'].sum()
cancelled = df[df['Order_Status_Clean']=='Cancelled']
returned = df[df['Order_Status_Clean']=='Returned']

# Category
cat_rev = df.groupby('Product_Category')['Revenue_Clean'].sum().sort_values(ascending=False)
cat_orders = df.groupby('Product_Category').size().sort_values(ascending=False)

# Product
prod_rev = df.groupby('Product_Name')['Revenue_Clean'].sum().sort_values(ascending=False).head(10)
prod_qty = df.groupby('Product_Name')['Quantity'].apply(lambda x: x[x>0].sum()).sort_values(ascending=False).head(10)

# Country
country_rev = df.groupby('Country_Clean')['Revenue_Clean'].sum().sort_values(ascending=False)
country_orders = df.groupby('Country_Clean').size().sort_values(ascending=False)

# Payment
pay_rev = df.groupby('Payment_Method_Clean')['Revenue_Clean'].sum().sort_values(ascending=False)
pay_counts = df.groupby('Payment_Method_Clean').size().sort_values(ascending=False)

# Status
status_counts = df['Order_Status_Clean'].value_counts()
status_rev = df.groupby('Order_Status_Clean')['Revenue_Clean'].sum()

# Rating
rating_counts = df['Customer_Rating'].value_counts(dropna=False).sort_index()
avg_rating = df['Customer_Rating'].mean()

# Monthly trend
monthly = df[df['Is_Valid_Qty'] & df['Order_Date_Parsed'].notna()].groupby(df['Order_Date_Parsed'].dt.to_period('M'))['Revenue_Clean'].sum()
monthly.index = monthly.index.astype(str)
monthly = monthly.sort_index()

# Discount analysis
df['Discount_Bucket'] = pd.cut(df['Discount_Percent'], bins=[-1,0,5,10,15,20,25,100], labels=['0%','1-5%','6-10%','11-15%','16-20%','21-25%','>25%'])
discount_rev = df.groupby('Discount_Bucket')['Revenue_Clean'].mean()

# Helper to save charts
def save_fig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches='tight')
    plt.close()

# 1 Revenue by Category bar
plt.figure(figsize=(8,4.5))
ax = cat_rev.plot(kind='bar', color=COLORS[:len(cat_rev)], edgecolor='white')
plt.title('Revenue by Product Category (USD)', fontsize=11, weight='bold')
plt.ylabel('Revenue (USD)')
plt.xticks(rotation=25, ha='right')
for i,v in enumerate(cat_rev.values):
    ax.text(i, v+500, f"${v:,.0f}", ha='center', va='bottom', fontsize=7)
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"${x/1000:.0f}k"))
plt.grid(axis='y')
save_fig(os.path.join(OUT_DIR,'cat_rev.png'))

# 2 Orders by Category
plt.figure(figsize=(8,4.5))
ax = cat_orders.plot(kind='bar', color=COLORS[::-1][:len(cat_orders)])
plt.title('Order Count by Category', fontsize=11, weight='bold')
plt.ylabel('Orders')
plt.xticks(rotation=25, ha='right')
for i,v in enumerate(cat_orders.values):
    ax.text(i, v+5, str(v), ha='center', va='bottom', fontsize=7)
save_fig(os.path.join(OUT_DIR,'cat_orders.png'))

# 3 Status donut
plt.figure(figsize=(6,4.5))
vals = status_counts.values
labels = status_counts.index
colors = ['#10b981','#2563eb','#f59e0b','#ef4444','#8b5cf6','#6366f1','#14b8a6'][:len(vals)]
wedges, texts, autotexts = plt.pie(vals, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, wedgeprops=dict(width=0.45, edgecolor='white'))
plt.title('Order Status Distribution', fontsize=11, weight='bold')
save_fig(os.path.join(OUT_DIR,'status_pie.png'))

# 4 Monthly revenue trend
plt.figure(figsize=(9,4.5))
plt.plot(monthly.index, monthly.values, marker='o', color='#2563eb', linewidth=2)
plt.fill_between(monthly.index, monthly.values, alpha=0.12, color='#2563eb')
plt.title('Monthly Revenue Trend (Valid Quantities Only)', fontsize=11, weight='bold')
plt.ylabel('Revenue (USD)')
plt.xticks(rotation=45, ha='right', fontsize=7)
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"${x/1000:.0f}k"))
plt.grid(True)
save_fig(os.path.join(OUT_DIR,'monthly.png'))

# 5 Top 10 products revenue
plt.figure(figsize=(8,4.5))
prod_rev_sorted = prod_rev.sort_values(ascending=True)
plt.barh(prod_rev_sorted.index, prod_rev_sorted.values, color='#0ea5e9')
plt.title('Top 10 Products by Revenue', fontsize=11, weight='bold')
plt.xlabel('Revenue (USD)')
plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"${x/1000:.0f}k"))
for i,v in enumerate(prod_rev_sorted.values):
    plt.text(v+200, i, f"${v:,.0f}", va='center', fontsize=7)
save_fig(os.path.join(OUT_DIR,'top_products.png'))

# 6 Country revenue
plt.figure(figsize=(8,4.5))
cr = country_rev.head(8).sort_values(ascending=True)
plt.barh(cr.index, cr.values, color='#8b5cf6')
plt.title('Revenue by Country (Top 8)', fontsize=11, weight='bold')
plt.xlabel('Revenue (USD)')
plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"${x/1000:.0f}k"))
for i,v in enumerate(cr.values):
    plt.text(v+300, i, f"${v:,.0f}", va='center', fontsize=7)
save_fig(os.path.join(OUT_DIR,'country_rev.png'))

# 7 Payment method count vs revenue (dual)
fig, ax1 = plt.subplots(figsize=(8,4.5))
x = pay_counts.index
ax1.bar(x, pay_counts.values, color='#f59e0b', alpha=0.85, label='Orders')
ax1.set_ylabel('Order Count', color='#f59e0b')
ax1.tick_params(axis='x', rotation=25)
ax2 = ax1.twinx()
ax2.plot(x, pay_rev.reindex(pay_counts.index).values, color='#2563eb', marker='o', linewidth=2, label='Revenue')
ax2.set_ylabel('Revenue (USD)', color='#2563eb')
ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"${x/1000:.0f}k"))
plt.title('Payment Method: Orders vs Revenue', fontsize=11, weight='bold')
fig.tight_layout()
plt.savefig(os.path.join(OUT_DIR,'payment.png'), dpi=180, bbox_inches='tight')
plt.close()

# 8 Rating distribution
plt.figure(figsize=(6,4.5))
rating_valid = df['Customer_Rating'].dropna()
counts = rating_valid.value_counts().sort_index()
plt.bar(counts.index.astype(int).astype(str), counts.values, color='#10b981', edgecolor='white')
plt.title(f'Customer Rating Distribution (Avg: {avg_rating:.2f})', fontsize=11, weight='bold')
plt.xlabel('Rating (1-5)')
plt.ylabel('Count')
for i,v in enumerate(counts.values):
    plt.text(i, v+5, str(v), ha='center', fontsize=8)
save_fig(os.path.join(OUT_DIR,'rating.png'))

# 9 Discount bucket average revenue
plt.figure(figsize=(7,4.5))
db = discount_rev
plt.bar(db.index.astype(str), db.values, color='#ec4899')
plt.title('Avg Net Revenue per Order by Discount Bucket', fontsize=11, weight='bold')
plt.ylabel('Avg Revenue (USD)')
for i,v in enumerate(db.values):
    plt.text(i, v+2, f"${v:.0f}", ha='center', fontsize=7)
save_fig(os.path.join(OUT_DIR,'discount.png'))

# 10 Quantity anomaly
plt.figure(figsize=(6,3.5))
qvals = df['Quantity'].value_counts().sort_index()
# limit to -2 to 6
qvals = qvals[(qvals.index>=-1) & (qvals.index<=6)]
plt.bar(qvals.index.astype(str), qvals.values, color=['#ef4444' if x<=0 else '#2563eb' for x in qvals.index])
plt.title('Quantity Distribution (Highlighting Anomalies)', fontsize=11, weight='bold')
plt.xlabel('Quantity')
plt.ylabel('Orders')
for i,(k,v) in enumerate(qvals.items()):
    plt.text(i, v+15, str(v), ha='center', fontsize=7)
save_fig(os.path.join(OUT_DIR,'quantity.png'))

# Save summary stats for report
import json
summary = {
 'total_rows': int(total_rows),
 'valid_orders': int(valid_orders),
 'invalid_qty': int(invalid_qty),
 'total_revenue': float(total_revenue),
 'avg_order_value': float(avg_order_value),
 'delivered_revenue': float(delivered_revenue),
 'avg_rating': float(avg_rating),
 'cat_rev': cat_rev.to_dict(),
 'cat_orders': cat_orders.to_dict(),
 'status_counts': status_counts.to_dict(),
 'country_rev': country_rev.head(10).to_dict(),
 'pay_counts': pay_counts.to_dict(),
 'pay_rev': pay_rev.to_dict(),
 'top_products': prod_rev.to_dict(),
 'monthly': monthly.to_dict(),
 'missing_rating': int(df['Customer_Rating'].isna().sum()),
 'missing_discount': int((df['Discount_Percent']==0).sum()),
 'date_min': str(df['Order_Date_Parsed'].min()),
 'date_max': str(df['Order_Date_Parsed'].max()),
}
with open(os.path.join(OUT_DIR,'summary.json'),'w') as f:
    json.dump(summary,f,indent=2)
print("Done")
print(json.dumps(summary,indent=2))
