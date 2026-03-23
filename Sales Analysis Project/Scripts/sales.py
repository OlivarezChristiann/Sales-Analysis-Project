# TOTAL SALES PER DAY
daily_sales = """
SELECT DATE(sale_date) AS sale_date, SUM(unit_price * quantity) AS total_sales
FROM sales
GROUP BY sale_date
ORDER BY sale_date
"""

df_daily_sales = pd.read_sql(daily_sales, engine)
df_daily_sales['sale_date'] = pd.to_datetime(df_daily_sales['sale_date'])

plt.figure(figsize=(12, 6))
plt.plot(df_daily_sales['sale_date'], df_daily_sales['total_sales'], marker='o', color='blue')
plt.xlabel('Sale Date', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.title('Total Sales Per Day', fontsize=14)
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
plt.clf()


# TOTAL SALES PER PRODUCT
product_sales = """
SELECT p.product_name, SUM(unit_price * quantity) AS total_sales
FROM sales AS s
JOIN products AS p
ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC
"""

df_product_sales = pd.read_sql(product_sales, engine)

plt.figure(figsize=(12, 6))
plt.bar(df_product_sales['product_name'], df_product_sales['total_sales'], color='blue')
plt.xlabel('Product Name', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.title('Total Sales Per Product', fontsize=14)
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
plt.clf()


# TOTAL UNITS SOLD PER PRODUCT
product_units = """
SELECT p.product_name, SUM(quantity) AS total_units_sold
FROM sales AS s
JOIN products AS p
ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_units_sold DESC
"""

df_product_units = pd.read_sql(product_units, engine)

plt.figure(figsize=(12, 6))
plt.bar(df_product_units['product_name'], df_product_units['total_units_sold'], color='blue')
plt.xlabel('Product Name', fontsize=12)
plt.ylabel('Units Sold', fontsize=12)
plt.title('Total Units Sold Per Product', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
plt.clf()


# REVENUE CONTRIBUTION (PERCENTAGE)
percentage_revenue = """
WITH total_revenue AS (
    SELECT SUM(quantity * unit_price) AS grand_total
    FROM sales
)
SELECT 
    p.product_name,
    SUM(s.quantity * s.unit_price) AS product_revenue,
    ROUND((SUM(s.quantity * s.unit_price) / t.grand_total) * 100, 2) AS revenue_percentage
FROM sales AS s
JOIN products AS p ON s.product_id = p.product_id
CROSS JOIN total_revenue t
GROUP BY p.product_name, t.grand_total
ORDER BY revenue_percentage DESC
"""

df_percentage_revenue = pd.read_sql(percentage_revenue, engine)

plt.pie(
    df_percentage_revenue['revenue_percentage'],
    labels=df_percentage_revenue['product_name'],
    autopct='%1.1f%%'
)
plt.title('Revenue Contribution by Product', fontsize=14)
plt.show()
plt.clf()