import pandas as pd
from datetime import datetime


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df["month_name"] = df["date"].dt.strftime("%B")
    df["month_num"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    return df


def sheet_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("product")
        .agg(
            total_revenue=("revenue", "sum"),
            total_units=("units", "sum"),
            avg_revenue=("revenue", "mean"),
            num_sales=("revenue", "count"),
            rev_per_unit=(
                "revenue",
                lambda x: round(x.sum() / df.loc[x.index, "units"].sum(), 2),
            ),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )
    summary["avg_revenue"] = summary["avg_revenue"].round(2)
    return summary


def sheet_by_month(df: pd.DataFrame) -> pd.DataFrame:
    by_month = (
        df.groupby(["month_num", "month_name"])
        .agg(
            total_revenue=("revenue", "sum"),
            total_units=("units", "sum"),
            num_sales=("revenue", "count"),
        )
        .reset_index()
        .sort_values("month_num")
        .drop(columns="month_num")
    )
    by_month = by_month.rename(columns={"month_name": "month"})
    return by_month


def sheet_pivot(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.pivot_table(
        values="revenue",
        index="product",
        columns="region",
        aggfunc="sum",
        fill_value=0,
        margins=True,
        margins_name="Total",
    ).reset_index()
    return pivot


def sheet_top_sales(df: pd.DataFrame) -> pd.DataFrame:
    df["rev_per_unit"] = (df["revenue"] / df["units"]).round(2)
    top = df.sort_values("revenue", ascending=False).head(10).reset_index(drop=True)
    top.index += 1
    return top[
        ["date", "product", "category", "region", "revenue", "units", "rev_per_unit"]
    ]


def export_report(df: pd.DataFrame, output_path: str):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        sheet_summary(df).to_excel(writer, sheet_name="Summary", index=False)
        sheet_by_month(df).to_excel(writer, sheet_name="By Month", index=False)
        sheet_pivot(df).to_excel(writer, sheet_name="Revenue by Region", index=False)
        sheet_top_sales(df).to_excel(writer, sheet_name="Top Sales", index=False)
    print(f"Report exported to {output_path}")


if __name__ == "__main__":
    df = load_data("sales.csv")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"sales_report_{timestamp}.xlsx"
    export_report(df, output_path)
