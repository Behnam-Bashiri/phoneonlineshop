"""Section 2 — KPI calculations."""
from __future__ import annotations

import json

import pandas as pd

from config import DATA_CLEANED, TABLES


def load_cleaned():
    return {
        "Product": pd.read_csv(DATA_CLEANED / "Product.csv"),
        "Branch": pd.read_csv(DATA_CLEANED / "Branch.csv"),
        "Customer": pd.read_csv(DATA_CLEANED / "Customer.csv"),
        "Invoice": pd.read_csv(DATA_CLEANED / "Invoice.csv"),
        "InvoiceItem": pd.read_csv(DATA_CLEANED / "InvoiceItem.csv"),
    }


def completed_invoices(inv: pd.DataFrame) -> pd.DataFrame:
    return inv.loc[inv["Status"].isin(["Completed"])].copy()


def compute_kpis() -> dict:
    TABLES.mkdir(parents=True, exist_ok=True)
    data = load_cleaned()
    inv = completed_invoices(data["Invoice"])
    items = data["InvoiceItem"]
    items = items.loc[items["InvoiceID"].isin(inv["InvoiceID"])]

    # --- Sales KPIs ---
    sales_kpis = {
        "total_sales": float(inv["TotalAmount"].sum()),
        "invoice_count": int(len(inv)),
        "avg_invoice_amount": float(inv["TotalAmount"].mean()),
        "avg_items_per_invoice": float(inv["ItemsCount"].mean()) if "ItemsCount" in inv else float(
            items.groupby("InvoiceID").size().mean()
        ),
        "total_discount": float(inv["DiscountAmount"].sum()),
    }

    # --- Time KPIs ---
    monthly = (
        inv.groupby("YearMonth", as_index=False)["TotalAmount"]
        .sum()
        .rename(columns={"TotalAmount": "Sales"})
        .sort_values("YearMonth")
    )
    yearly = (
        inv.groupby("Year", as_index=False)["TotalAmount"]
        .sum()
        .rename(columns={"TotalAmount": "Sales"})
        .sort_values("Year")
    )
    yearly["YoY_Growth"] = yearly["Sales"].pct_change()

    # --- Branch KPIs ---
    branch = (
        inv.groupby("BranchID")
        .agg(
            Sales=("TotalAmount", "sum"),
            InvoiceCount=("InvoiceID", "count"),
            AvgInvoice=("TotalAmount", "mean"),
        )
        .reset_index()
        .merge(data["Branch"][["BranchID", "BranchName", "City"]], on="BranchID", how="left")
        .sort_values("Sales", ascending=False)
    )

    # --- Customer KPIs ---
    cust = (
        inv.groupby("CustomerID")
        .agg(
            Purchases=("InvoiceID", "count"),
            TotalSpend=("TotalAmount", "sum"),
            AvgOrder=("TotalAmount", "mean"),
            FirstPurchase=("InvoiceDate", "min"),
            LastPurchase=("InvoiceDate", "max"),
        )
        .reset_index()
    )
    active_customers = int(cust["CustomerID"].nunique())
    # Simple CLV ≈ average order value × purchase frequency × expected lifespan years
    # Here: TotalSpend as historical CLV proxy + predictive CLV = AvgOrder * Purchases * 1.5
    cust["CLV"] = cust["AvgOrder"] * cust["Purchases"] * 1.5

    customer_kpis = {
        "active_customers": active_customers,
        "avg_spend_per_customer": float(cust["TotalSpend"].mean()),
        "avg_purchases_per_customer": float(cust["Purchases"].mean()),
        "avg_clv": float(cust["CLV"].mean()),
        "median_clv": float(cust["CLV"].median()),
    }

    # Persist tables
    monthly.to_csv(TABLES / "kpi_monthly_sales.csv", index=False, encoding="utf-8-sig")
    yearly.to_csv(TABLES / "kpi_yearly_sales.csv", index=False, encoding="utf-8-sig")
    branch.to_csv(TABLES / "kpi_branch.csv", index=False, encoding="utf-8-sig")
    cust.to_csv(TABLES / "kpi_customer.csv", index=False, encoding="utf-8-sig")

    result = {
        "sales": sales_kpis,
        "customer": customer_kpis,
        "yearly": yearly.to_dict(orient="records"),
        "top_branches": branch.head(5).to_dict(orient="records"),
        "bottom_branches": branch.tail(3).to_dict(orient="records"),
    }
    with open(TABLES / "kpis_summary.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)

    print("KPIs computed ->", TABLES)
    return result


if __name__ == "__main__":
    compute_kpis()
