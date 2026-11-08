use projects;

select *
from ecommerce_dataset;

-- ==============================================================================
-- 1: OVERALL BUSINESS HEALTH & EXECUTIVE KPIS
-- ============================================================================== 

-- Query 1: Core Business Metrics
-- Business Context: Calculate gross transaction volume, unit demand, and overall customer reach.
-- Logic: Aggregate metrics across the entire dataset without exclusions.
select
	round(sum(`Total Amount`)) as Total_Revenue,
    sum(Quantity) as Total_Sold_QTY,
    count(distinct `Order ID`) as Distinct_Order,
    count(distinct `Customer ID`) as Total_Customer
from ecommerce_dataset;

-- Query 2: Order Fulfillment & Operational Funnel
-- Business Context: Measure order fulfillment efficiency and evaluate revenue leakage from cancellations and returns.
-- Logic: Compute order distribution percentages dynamically using a scalar subquery.
select
	`Order Status`,
    count(`Order Status`) as Order_Count,
    round(count(`Order Status`)/
    (select count(`Order Status`) from ecommerce_dataset)*100,1)
    as Order_Status_Distribution
from ecommerce_dataset
group by `Order Status`
order by Order_Count desc ;

-- ==============================================================================
-- SECTION 2: PRODUCT & CATEGORY PERFORMANCE
-- ==============================================================================


-- Query 3: Top 5 Revenue-Generating Products
-- Business Context: Identify top catalog drivers.
-- Logic: Filter out 'Cancelled' and 'Returned' orders so revenue figures reflect actual realized sales.
select
	`Product Name`,
    `Product Category`,
	round(sum(`Total Amount`)) as Total_Revenue,
    sum(Quantity) as Total_Sold_QTY
from ecommerce_dataset
where `Order Status` not in ("Canceled", "Returned")
group by `Product Name`, `Product Category`
order by Total_Revenue desc limit 5;

-- Query 4: Category Performance & Average Discount Analysis
-- Business Context: Compare categories by net volume, realized revenue, average discount depth, and average ticket size (AOV).
-- Logic: Group by category; multiply discount proportion by 100 for display percentage.
select
	`Product Category`,
    round(sum(`Total Amount`)) as Category_Revenue,
    sum(Quantity) as Sold_QTY,
    round(avg(`Discount Percent`)*100,2) as AVG_Discount_percent,
    round(avg(`Total Amount`)) as AOV
from ecommerce_dataset
group by `Product Category`
order by Category_Revenue desc;

-- Query 5: Category Quality & Customer Satisfaction (Rating vs Return Rate)
-- Business Context: Evaluate whether lower customer review ratings correlate with higher return rates.
-- Logic: Calculate category-level average rating and return rate using conditional aggregation (CASE WHEN).
select
	`Product Category`,
    round(avg(`Customer Rating`),2) as AVG_Rating,
    count(`Order ID`) as Total_Orders,
    sum(case when `Order Status`="Returned" then 1 else 0 end) as Returned_Orders,
    sum(case when `Order Status`="Returned" then 1 else 0 end)/count(`Order ID`)*100 as "Return_Rate_Pr%"
from ecommerce_dataset
group by `Product Category`
order by AVG_Rating;

-- Query 6: Category Risk Audit (Cancellation & Return Rates)
-- Business Context: Pinpoint problematic product lines that lead to operational losses and reverse-logistics costs.
-- Logic: Compute both cancellation rate and return rate side-by-side using conditional aggregation.
select
	`Product Category`,
    count(`Order ID`) as Total_Orders,
    sum(case when `Order Status`="Cancelled" then 1 else 0 end) as Cancelled_Orders,
	round(sum(case when `Order Status`="Cancelled" then 1 else 0 end)/count(`Order ID`)*100,2) as Cancellation_Rate,
    sum(case when `Order Status`="Returned" then 1 else 0 end) as Returned_Orders,
	round(sum(case when `Order Status`="Returned" then 1 else 0 end)/count(`Order ID`)*100,2) as Return_Rate
from ecommerce_dataset
group by `Product Category`
order by Return_Rate desc;

-- ==============================================================================
-- SECTION 3: GEOGRAPHICAL & MARKET EXPANSION
-- ============================================================================== */

-- Query 7: Top 3 Markets and Their Top 3 Shipping Hubs
-- Business Context: Identify top-performing country markets and find their primary urban delivery hubs.
-- Logic: 
--   1. country_revenue CTE identifies top 3 countries by realized net revenue.
--   2. city_revenue CTE ranks shipping cities within those top countries using
with country_revenue as(
select
	Country,
	round(sum(`Total Amount`)) as Total_Revenue
from ecommerce_dataset
where `Order Status` not in ("Cancelled", "Returned")
group by Country
order by Total_Revenue desc limit 3
),
city_revenue as(
select
	c.Country,
	e.`Shipping City`,
    round(sum(`Total Amount`)) as Revenue,
    count(distinct `Order ID`) as Total_Orders,
    dense_rank() over(
		partition by e.Country
        order by sum(e.`Total Amount`) desc) as rn
	from ecommerce_dataset e
    join country_revenue c
    on c.Country=e.country
where `Order Status` not in ("Cancelled","Returned")
group by c.Country, `Shipping City`)

select
cr.Country,
c.`Shipping City`,
c.Revenue,
c.Total_Orders,
c.rn
	from city_revenue c
    join country_revenue cr
    on c.Country=cr.Country
    where rn<=3
    order by cr.Country, c.rn;
	
-- Query 8: Best-Selling Product Category Per Country
-- Business Context: Identify product-market fit to optimize localized regional inventory and marketing campaigns.
-- Logic: Partition by country and rank product categories using DENSE_RANK(); filter for rank = 1.
with category_rank as(
select
	Country,
    `Product Category`,
    count(`Order ID`) as Total_Orders,
    sum(Quantity) as Units_Sold,
    round(sum(`Total Amount`)) as Total_Revenue,
	dense_rank() over(
			partition by Country
            order by sum(`Total Amount`) desc ) as rn
from ecommerce_dataset
where `Order Status` not in ("Cancelled", "Returned")
group by Country, `Product Category`)
select *
	from category_rank
    where rn=1
    order by Total_Revenue desc;
    
-- ==============================================================================
-- SECTION 4: PAYMENT PREFERENCE & PRICING ELASTICITY
-- ==============================================================================

-- Query 9: Payment Gateway Share & Average Basket Value
-- Business Context: Analyze checkout preferences and compare AOV across payment gateways.
-- Logic: CTE aggregates gateway usage; window function SUM() OVER() calculates transaction market share.
with payment as(
select
	`Payment Method`,
    count(`Order ID`) as usage_count,
    round(sum(`Total Amount`)) as total_revenue,
    round(avg(`Total Amount`)) as AOV
from ecommerce_dataset
where `Order Status` not in ("Cancelled","Returned")
group by `Payment Method`
)
select
	`Payment Method`,
    usage_count,
	round(usage_count*100/sum(usage_count) over(),2) as "usage_share_pr%",
    total_revenue,
    AOV
from payment
order by usage_count desc;

-- Query 10: Discount Sensitivity & Basket Size Elasticity
-- Business Context: Evaluate whether deeper discount promotions increase basket sizes or dilute margins.
-- Logic: Segment transactions into discount tiers using CASE WHEN; measure average units ordered.
select
	case
		when `Discount Percent` = 0 then "No Discount(0%)"
        when `Discount Percent`>0 and `Discount Percent` <= 0.05 then "Low Discount(1%-5%)"
        when `Discount Percent`>0.05 and `Discount Percent` <=0.15 then "Midium Discount(6%-15%)"
        else "High Discount(>15%)"
	end as Discount_Tier,
    count(`Order ID`) as Order_Counts,
    sum(Quantity) as Total_Units,
    round(avg(Quantity),2) as avg_units_per_order,
    round(avg(`Total Amount`),2) as AOV
from ecommerce_dataset
where `Order Status` not in ("Cancelled", "Returned")
group by Discount_Tier
order by avg_units_per_order;

-- ==============================================================================
-- SECTION 5: CUSTOMER LIFETIME VALUE & TIME-SERIES ANALYSIS
-- ==============================================================================
   
  -- Query 11: Repeat Customers & Customer Lifetime Value (CLV)
-- Business Context: Identify repeat buyers and measure customer retention value.
-- Logic: Filter grouped customer cohorts using HAVING COUNT(DISTINCT Order ID) > 1.
 select
	`Customer ID`,
    count(distinct `Order ID`) as Total_Orders,
    sum(Quantity) as Items_Purchased,
    round(sum(`Total Amount`),2) as Total_Spend,
    round(avg(`Total Amount`),2) as AOV
from ecommerce_dataset
where `Order Status` not in ("Cancelled", "Returned")
group by `Customer ID`
having Total_Orders>1
order by Total_Orders;

-- Query 12: Monthly Revenue Trend & Month-over-Month (MoM) Growth
-- Business Context: Track monthly sales trajectory and evaluate revenue growth momentum over time.
-- Logic: 
--   1. monthly_sales CTE groups net revenue by calendar Year and Month.
--   2. prev_month_sales CTE retrieves previous month's revenue using LAG().
--   3. Final SELECT computes growth percentage: ((current - previous) / previous) * 100.
with monthly_sales as(
select
	Year,
    Month,
    round(sum(`Total Amount`),2) as monthly_revenue
from ecommerce_dataset
where `Order Status` not in ("Cancelled", "Returned")
group by Year, Month),
prev_month_sales as(
select
	Year,
    Month,
    monthly_revenue,
    lag(monthly_revenue,1) over(order by Year, Month) as prev_month_revenue
from monthly_sales)
select
	Year,
    Month,
    monthly_revenue,
    prev_month_revenue,
    round((monthly_revenue-prev_month_revenue)/prev_month_revenue*100,2) as "MOM_growth%"
from prev_month_sales
order by Year, Month;


