# Pandas Sales Analysis

Data analysis and automated Excel report generation using pandas.

Reads a CSV of sales transactions, runs groupby, merge, pivot table, and date-based analysis, then exports a structured multi-sheet Excel report.

## Features
- Revenue and unit analysis grouped by product, category, and region
- Multi-table aggregations with custom metrics in a single operation
- Merge sales data with external product metadata
- Pivot tables with automatic subtotals
- Row-wise calculations with apply
- Date parsing: filter by range, extract month, quarter, and week
- Automated Excel export with one sheet per analysis section

## Output

Running `report.py` generates a timestamped Excel file with four sheets:

| Sheet | Content |
|-------|---------|
| Summary | Total revenue, units, avg revenue, and rev/unit by product |
| By Month | Monthly revenue and units in chronological order |
| Revenue by Region | Pivot table: product vs region with totals |
| Top Sales | Top 10 individual sales sorted by revenue |

## How to use
1. Clone this repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the analysis scripts:
```
python main.py
```
4. Generate the Excel report:
```
python report.py
```
5. Report will be saved as `sales_report_YYYYMMDD_HHMMSS.xlsx`

## Project structure
```
pandas-analysis/
├── main.py       # Exploratory analysis: groupby, merge, pivot, apply, dates
├── report.py     # Excel report generator with four sheets
└── sales.csv     # Sample sales data: 16 transactions across 4 months
```

## Tech stack
- Python 3
- pandas
- openpyxl

## Notes
- **groupby + agg**: Multiple aggregations in a single pass — sum, mean, count, and custom lambdas — instead of chaining separate operations.
- **merge**: Left join between sales data and product metadata to enrich records without modifying the source CSV.
- **pivot_table with margins**: Automatic subtotals per row and column with a single parameter — no manual summing needed.
- **apply with axis=1**: Row-wise calculations that access multiple columns simultaneously, useful for derived metrics like revenue per unit.
- **parse_dates**: Dates loaded as `datetime64` instead of strings, enabling direct filtering by range and extraction of month, quarter, and week with `.dt` accessor.
- **ExcelWriter context manager**: All sheets written in a single file open/close operation — cleaner and safer than opening the writer multiple times.