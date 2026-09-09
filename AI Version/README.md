![Project Banner](https://raw.githubusercontent.com/Mohammadshadab1/ecommerce-sales-customer-analysis/main/Images/banner.svg)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-1.5%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5%2B-111726?style=for-the-badge)](https://matplotlib.org/)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Generation-FF6F00?style=for-the-badge)](https://www.reportlab.com/)

# 🤖 AI-Powered E-Commerce Report Automation Pipeline

An **end-to-end automated analytics pipeline** that transforms raw e-commerce transaction data into a complete, boardroom-ready business intelligence report — with a single command.

This project demonstrates the power of **programmatic report generation**: from raw CSV ingestion and data cleaning to automated visualization, JSON KPI extraction, PDF compilation, and PowerPoint deck creation.

---

## 📌 Executive Summary

* *Total Transactions Processed:* 12,180 rows
* *Valid Orders After Cleaning:* 11,988
* *Total Gross Revenue:* $1.42M
* *Average Order Value (AOV):* $118.37
* *Delivery Success Rate:* 54.8%
* *Average Customer Rating:* 3.90
* *Automation Time:* Under 60 seconds

---

## 🚀 What This Pipeline Does

Run one script, get six deliverables:

```
Raw CSV In
    │
    ▼
┌─────────────────────────────┐
│  1. Data Cleaning Engine    │  → Fixes invalid quantities, formats dates,
│     (generate_report.py)    │    standardizes text fields
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  2. KPI Summary Generator   │  → Exports key metrics as structured JSON
│     (summary.json)          │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  3. Auto-Visualization      │  → Generates 11 publication-ready charts
│     (report_assets/*.png)   │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  4. PDF Report Builder      │  → Compiles executive PDF with ReportLab
│     (build_pdf.py)          │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  5. PowerPoint Deck         │  → Auto-builds presentation slides
│     (.pptx output)          │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  6. Cleaned Dataset Export  │  → Analysis-ready Excel file
│     (.xlsx output)          │
└─────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core automation engine |
| **Pandas** | Data ingestion, cleaning, transformation |
| **NumPy** | Numerical computations |
| **Matplotlib** | Automated chart generation (11 visualizations) |
| **ReportLab** | Professional PDF report compilation |
| **JSON** | Structured KPI extraction and storage |
| **OpenPyXL / XlsxWriter** | Excel export |
| **python-pptx** | PowerPoint deck automation |

---

## 📊 Auto-Generated Visualizations

The pipeline produces **11 chart assets** automatically:

| Chart | File | Insight |
|-------|------|---------|
| Category Orders | `cat_orders.png` | Order volume by product category |
| Category Revenue | `cat_rev.png` | Revenue distribution across categories |
| Country Revenue | `country_rev.png` | Geographic revenue breakdown |
| Discount Analysis | `discount.png` | Discount percentage impact |
| Monthly Trends | `monthly.png` | Time-series revenue trends |
| Payment Methods | `payment.png` | Payment gateway distribution |
| Quantity Distribution | `quantity.png` | Order quantity patterns |
| Customer Ratings | `rating.png` | Rating distribution analysis |
| Order Status | `status_pie.png` | Fulfillment status breakdown |
| Top Products | `top_products.png` | Best-selling items by volume |
| Summary Dashboard | `summary.png` | Executive KPI snapshot |

---

## 📂 Project Structure

```
Ecommerce-Work-with-AI/
│
├── uploads/
│   └── ecommerce_retail_transactions_raw.csv    # Raw input data
│
├── report_assets/                               # Auto-generated charts
│   ├── cat_orders.png
│   ├── cat_rev.png
│   ├── country_rev.png
│   ├── discount.png
│   ├── monthly.png
│   ├── payment.png
│   ├── quantity.png
│   ├── rating.png
│   ├── status_pie.png
│   ├── summary.png
│   └── top_products.png
│
├── build_pdf.py                                 # PDF report generator
├── generate_report.py                           # Main automation script
├── summary.json                                 # Extracted KPIs
│
├── Ecommerce_Retail_Transactions_CLEANED.xlsx   # Cleaned dataset
├── Ecommerce_Retail_Transactions_Full_Report.pdf # Executive PDF
├── Ecommerce_Retail_Transactions_Report.pptx    # PowerPoint deck
│
└── README.md                                    # This file
```

---

## ⚡ How to Run

### Prerequisites

```bash
pip install pandas numpy matplotlib reportlab openpyxl python-pptx
```

### Step 1: Generate Charts & Summary

```bash
python generate_report.py
```

**Output:**
- `report_assets/` folder with 11 charts
- `summary.json` with structured KPIs

### Step 2: Build PDF Report

```bash
python build_pdf.py
```

**Output:**
- `Ecommerce_Retail_Transactions_Full_Report.pdf`

### Step 3: Open PowerPoint Deck

The `.pptx` file is auto-generated with all charts embedded and ready for presentation.

---

## 📈 Sample KPI Output (summary.json)

```json
{
  "total_rows": 12180,
  "valid_orders": 11988,
  "invalid_qty": 192,
  "total_revenue": 1419076.146,
  "avg_order_value": 118.37472022021,
  "delivered_revenue": 781808.084,
  "avg_rating": 3.896185737976783,
  "cat_rev": {
    "Electronics": 384734.249,
    "Home & Kitchen": 280336.7655,
    "Sports": 223669.1095,
    "Fashion": 184665.247,
    "Toys": 142462.863,
    "Beauty": 90465.0105,
    "Books": 65407.6995,
    "Grocery": 47335.202
  },
  "cat_orders": {
    "Home & Kitchen": 1568,
    "Toys": 1557,
    "Books": 1552,
    "Fashion": 1539,
    "Beauty": 1510,
    "Electronics": 1507,
    "Grocery": 1491,
    "Sports": 1456
  }
}
```

---

## 🎯 Why This Matters

| Manual Process | Automated Pipeline |
|---------------|-------------------|
| 4-6 hours of cleaning + viz + report writing | **< 60 seconds** |
| Risk of human error in calculations | **100% reproducible** |
| Static, one-time report | **Re-run on new data instantly** |
| Designer needed for PDF/PPT | **Programmatic, brand-consistent output** |

This isn't just analytics — it's **analytics infrastructure**.

---

## 🔄 Comparison: Manual vs. AI-Assisted

This repository is the **automated companion** to my original manual analysis project:

| | [Manual Version](https://github.com/Mohammadshadab1/ecommerce-sales-customer-analysis) | **This AI Pipeline** |
|---|---|---|
| Approach | Hands-on EDA + Power BI | Programmatic automation |
| Time to Report | Days | Seconds |
| Reproducibility | Medium | High |
| Best For | Deep-dive exploration | Scheduled/operational reporting |

> 💡 **Pro Tip:** Use the manual version for exploratory analysis. Use this pipeline for recurring reports.

---

## 📬 Let's Connect

*Created by:* Mohammad Shadab
Data Analyst | Automation Enthusiast

* 📧 *Email:* [jrshadab921@gmail.com](mailto:jrshadab921@gmail.com)
* 💼 *LinkedIn:* [Mohammad Shadab](https://www.linkedin.com/in/mohammad-shadab-550aab24b)
* 🐙 *GitHub:* [Mohammadshadab1](https://github.com/Mohammadshadab1)
* 🌐 *Portfolio:* [Mohammad Shadab Portfolio](https://myportfoliowebsite-lyart.vercel.app/)

---

Created with 🤖 + 💡 by Mohammad Shadab
