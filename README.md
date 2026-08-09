[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-1.5%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-38BDF8?style=for-the-badge)](https://seaborn.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5%2B-111726?style=for-the-badge)](https://matplotlib.org/)

An end-to-end Data Analytics project analyzing over *12,000 retail transaction records* ($1.39M total gross revenue)[span_0](start_span)[span_0](end_span). This project covers complete data pipeline operations—from data cleaning, missing value imputations, and normalization to exploratory data analysis (EDA), statistical correlation, and executive storytelling through a presentation deck[span_1](start_span)[span_1](end_span).

---

## 📌 Executive Summary & Key Performance Indicators (KPIs)

* *Total Gross Revenue:* $1,390,000 ($1.39M)[span_2](start_span)[span_2](end_span)
* *Total Orders Processed:* 12,000 (12.00K)[span_3](start_span)[span_3](end_span)
* *Average Order Value (AOV):* $115.04[span_4](start_span)[span_4](end_span)
* *Repeat Customer Rate:* 88.47% (Reflects strong customer brand equity)[span_5](start_span)[span_5](end_span)
* *Order Delivery Success Rate:* 54.82% (Operational bottleneck for fulfillment improvement)[span_6](start_span)[span_6](end_span)

---

## 🛠️ Data Pipeline & Engineering Methodology

1. *Missing Data Imputation:*
   * Imputed missing values in Discount Percent with 0 (assuming full-price purchase)[span_7](start_span)[span_7](end_span).
   * Imputed Shipping City with "Unknown" for incomplete location entries[span_8](start_span)[span_8](end_span).
   * Filled missing Customer Rating using median strategy[span_9](start_span)[span_9](end_span).
2. *Data Normalization & Standardization:*
   * Cleaned country names (e.g., mapped U.K., United Kingdom → UK)[span_10](start_span)[span_10](end_span).
   * Deduplicated transactional logs using Order ID[span_11](start_span)[span_11](end_span).
3. *Feature Engineering:*
   * Calculated Total Sales (gross line-item value post-discount)[span_12](start_span)[span_12](end_span).
   * Derived date features: Year, Month, Quarter, and Day of Week for seasonal trend evaluation[span_13](start_span)[span_13](end_span).

---

## 📊 Key Analytics Insights & Visual Storytelling

### 1. Monthly & Yearly Sales Performance
* *Trend Analysis:* Baseline revenue remains stable across years, with sharp seasonal spikes occurring during *Q4 (November & December)*[span_14](start_span)[span_14](end_span).
* *Partial Data Flag:* Observed a temporary sales dip in August 2026 due to partial month data capture[span_15](start_span)[span_15](end_span).

### 2. Category Revenue Engines
* *Top Drivers:* *Electronics* ($376K+) and *Home & Kitchen* ($275K+) drive over *45%* of gross retail sales[span_16](start_span)[span_16](end_span).
* *Low Performers:* Grocery and Books demonstrate low revenue contributions despite steady order volumes[span_17](start_span)[span_17](end_span).

### 3. Geographical Reach & City Hubs
* *Country Revenue:* Balanced distribution across major international markets (~$175K–$200K per country across UAE, UK, Germany, India, USA, Canada, and Australia)[span_18](start_span)[span_18](end_span).
* *City High-Performers:* Middle East hubs lead city metrics—*Abu Dhabi ($106K+)* and *Dubai ($92K+)* generate the highest individual city revenues[span_19](start_span)[span_19](end_span).

### 4. Pricing Behavior & Revenue Dynamics (Scatter Analysis)
* *Linear Scaling:* Revenue expands linearly with Unit Price ($0–$250), validating high-unit-value catalog items as core revenue drivers[span_20](start_span)[span_20](end_span).
* *Return Anomalies:* Identified negative total amounts ($0 to -$200) reflecting order refunds and returned goods[span_21](start_span)[span_21](end_span).

### 5. Fulfillment & Operations
* *Delivery Status:* *54.82%* of total orders successfully delivered[span_22](start_span)[span_22](end_span). High volumes in Shipped, Pending, Cancelled, and Returned indicate courier SLA bottlenecks[span_23](start_span)[span_23](end_span).
* *Payment Gateways:* Uniform adoption (~15%–17% split) across Cash on Delivery, Netbanking, Credit/Debit Cards, Paypal, and UPI[span_24](start_span)[span_24](end_span).

---

## 🎯 Strategic Action Plan & Business Recommendations

| Area | Recommended Action | Expected Business Impact |
| :--- | :--- | :--- |
| *Demand Growth* | Increase Q4 inventory levels and marketing ad-spend by *40%* starting late September[span_25](start_span)[span_25](end_span). | Capture Q4 holiday demand and prevent stockouts[span_26](start_span)[span_26](end_span). |
| *Pricing & Bundling* | Shift away from blanket discounts (weak correlation of -0.07)[span_27](start_span)[span_27](end_span). Bundle low-performing items (Books/Grocery) with Electronics[span_28](start_span)[span_28](end_span). | Maximize Basket Size and Average Order Value (AOV)[span_29](start_span)[span_29](end_span). |
| *Supply Chain* | Audit courier SLAs and establish local micro-fulfillment centers in top hubs (*Abu Dhabi & Dubai)[span_30](start_span)[span_30](end_span). | Improve delivery fulfillment rates above **75%* and lower transit times[span_31](start_span)[span_31](end_span). |

---

## 📂 Project Repository Structure

```text
ecommerce-sales-customer-analysis/
│
├── Clean Data/                   # Cleaned and processed dataset
├── Images/                       # High-resolution saved charts & visualizations
├── Notebook/                     # Jupyter Notebook with complete Python code & EDA
├── Persentation/                 # 10-Slide Executive PDF Presentation Deck
├── Raw Data/                     # Raw transactional dataset
└── README.md                     # Project documentation & summary

## 👤 Author & Contact Details

*Created by:* Mohammad Shadab  
Data Analyst

* 📄 *Resume:* [View Resume (PDF)](./Mohammad_Shadab_Resume.pdf)
* 💼 *LinkedIn:* [Mohammad Shadab](https://linkedin.com)
* 🐙 *GitHub:* [Mohammadshadab1](https://github.com/Mohammadshadab1)
* 🌐 *Portfolio:* [Mohammad Shadab Portfolio](https://your-portfolio-link.com)
* 📊 *Presentation Deck:* Included in the [/Persentation](./Persentation) folder[span_0](start_span)[span_0](end_span)
