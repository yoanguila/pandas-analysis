import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"])

print("=== RAW DATA ===")
print(df.head())
print(f"\nShape: {df.shape}")
print(f"Dtypes:\n{df.dtypes}")

print("\n=== GROUPBY: revenue by product ===")
by_product = df.groupby("product")["revenue"].sum().sort_values(ascending=True)
print(by_product)

print("\n=== GROUPBY: multiple aggregations ===")
summary = df.groupby("product").agg(
    total_revenue=("revenue", "sum"),
    total_units=("units", "sum"),
    avg_revenue=("revenue", "mean"),
    num_sales=("revenue", "count")
).sort_values("total_revenue", ascending=False)
print(summary)

print("\n=== GROUPBY: revenue by category and region ===")
by_cat_region = df.groupby(["category", "region"])["revenue"].sum().reset_index()
print(by_cat_region)

print("\n=== MERGE ===")
# Simulate a second dataframe with product metadata
products_meta = pd.DataFrame({
    "product": ["Web Scraper", "PDF Extractor", "Telegram Bot", "API Integration"],
    "hourly_rate": [45, 65, 40, 80],
    "complexity": ["medium", "high", "low", "high"]
})

merged = df.merge(products_meta, on="product", how="left")
print(merged[["date", "product", "revenue", "hourly_rate", "complexity"]].head(8))

print("\n=== MERGE: estimated hours per sale ===")
merged["estimated_hours"] = (merged["revenue"] / merged["hourly_rate"]).round(1)
print(merged.groupby("product")["estimated_hours"].sum().sort_values(ascending=False))

print("\n=== PIVOT TABLE ===")
pivot = df.pivot_table(
    values="revenue",
    index="product",
    columns="region",
    aggfunc="sum",
    fill_value=0
)
print(pivot)

print("\n=== PIVOT TABLE: units with margins ===")
pivot_units = df.pivot_table(
    values="units",
    index="category",
    columns="region",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="Total"
)
print(pivot_units)

print("\n=== APPLY ===")
def revenue_tier(revenue: int) -> str:
    if revenue >= 2000:
        return "high"
    elif revenue >= 1000:
        return "medium"
    return "low"

df["tier"] = df["revenue"].apply(revenue_tier)
print(df[["date", "product", "revenue", "tier"]].head(8))

print("\n=== APPLY: low-wise ===")
def revenue_per_unit(row):
    return round(row["revenue"] / row["units"], 2)

df["rev_per_unit"] = df.apply(revenue_per_unit, axis=1)
print(df[["product", "revenue", "units", "rev_per_unit"]].head(8))

print("\n=== APPLY: tier distribution ===")
print(df["tier"].value_counts())

print("\n=== DATES ===")
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%B")
df["quarter"] = df["date"].dt.quarter
df["week"] = df["date"].dt.isocalendar().week

print(df[["date", "month_name", "quarter", "week"]].head(8))

print("\n=== DATES: revenue by month ===")
by_month = df.groupby("month_name")["revenue"].sum()
print(by_month)

print("\n=== DATES: filter by date range ===")
q1 = df[(df["date"] >= "2024-01-01") & (df["date"] <= "2024-03-31")]
print(f"Q1 records: {len(q1)}")
print(f"Q1 revenue: ${q1['revenue'].sum():,}")

print("\n=== DATES: revenue by quarter ===")
by_quarter = df.groupby("quarter")["revenue"].sum()
print(by_quarter)


