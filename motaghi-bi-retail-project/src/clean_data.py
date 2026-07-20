"""
Section 1 — Data quality assessment and cleaning.
Loads raw CSVs, documents issues, applies cleaning rules, saves cleaned tables.
"""
from __future__ import annotations

import json
from pathlib import Path

import jdatetime
import numpy as np
import pandas as pd

from config import DATA_CLEANED, DATA_RAW, DOCS, TABLES


def _parse_jalali(s):
    """Return normalized Jalali date string YYYY-MM-DD, or None if invalid."""
    if pd.isna(s) or str(s).strip() == "" or str(s).strip().lower() in {"nan", "nat", "none"}:
        return None
    try:
        parts = str(s).replace("/", "-").split("-")
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
        jd = jdatetime.date(y, m, d)
        return f"{jd.year:04d}-{jd.month:02d}-{jd.day:02d}"
    except Exception:
        return None


def _quality_report(name: str, df: pd.DataFrame) -> dict:
    return {
        "table": name,
        "rows": int(len(df)),
        "cols": int(df.shape[1]),
        "null_counts": {
            c: int(df[c].isna().sum()) + int((df[c].astype(str).str.strip() == "").sum())
            for c in df.columns
        },
        "duplicate_rows": int(df.duplicated().sum()),
    }


def clean_products(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    notes = []
    before = len(df)
    df = df.copy()
    pos = df.loc[df["UnitPrice"] > 0, "UnitPrice"]
    median_price = float(pos.median()) if len(pos) else 100_000
    bad_price = (df["UnitPrice"].isna()) | (df["UnitPrice"] <= 0)
    notes.append(f"Product: {bad_price.sum()} ردیف با قیمت نامعتبر -> جایگزینی با میانه ({median_price:,.0f})")
    df.loc[bad_price, "UnitPrice"] = median_price

    n_cat = df["Category"].isna().sum()
    df["Category"] = df["Category"].fillna("سایر")
    notes.append(f"Product: {n_cat} Category خالی -> 'سایر'")

    df.loc[
        (df["UnitCost"].isna()) | (df["UnitCost"] <= 0) | (df["UnitCost"] >= df["UnitPrice"]),
        "UnitCost",
    ] = df["UnitPrice"] * 0.7
    notes.append(f"Product: ردیف‌ها قبل={before} بعد={len(df)}")
    return df, notes


def clean_branches(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    notes = []
    df = df.copy()
    n_reg = df["Region"].isna().sum()
    df["Region"] = df["Region"].fillna(
        df["City"].map(lambda c: "مرکز" if c in ("تهران", "اصفهان", "کرج", "قم") else "سایر")
    )
    notes.append(f"Branch: {n_reg} Region خالی پر شد")
    bad_area = df["Area_sqm"] <= 0
    notes.append(f"Branch: {bad_area.sum()} Area نامعتبر -> میانه")
    med = df.loc[df["Area_sqm"] > 0, "Area_sqm"].median()
    df.loc[bad_area, "Area_sqm"] = med
    return df, notes


def clean_customers(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    notes = []
    before = len(df)
    df = df.copy()
    dup = df.duplicated(subset=["CustomerID"], keep="first").sum()
    df = df.drop_duplicates(subset=["CustomerID"], keep="first")
    notes.append(f"Customer: حذف {dup} رکورد تکراری بر اساس CustomerID")

    med_age = df["Age"].median()
    bad_age = df["Age"].isna() | (df["Age"] < 10) | (df["Age"] > 100)
    notes.append(f"Customer: {bad_age.sum()} Age نامعتبر -> میانه ({med_age})")
    df.loc[bad_age, "Age"] = med_age
    df["Age"] = df["Age"].astype(int)

    df["Gender"] = df["Gender"].fillna("Unknown")
    df["Gender"] = df["Gender"].replace({"": "Unknown"})
    empty_city = (df["City"].isna()) | (df["City"].astype(str).str.strip() == "")
    notes.append(f"Customer: {empty_city.sum()} City خالی -> 'نامشخص'")
    df.loc[empty_city, "City"] = "نامشخص"
    df["FullName"] = df["FullName"].fillna("بدون‌نام")
    notes.append(f"Customer: ردیف‌ها قبل={before} بعد={len(df)}")
    return df, notes


def clean_invoices(
    df: pd.DataFrame, valid_branches: set, valid_customers: set
) -> tuple[pd.DataFrame, list[str]]:
    notes = []
    before = len(df)
    df = df.copy()

    # Drop exact duplicates
    dups = df.duplicated().sum()
    df = df.drop_duplicates()
    notes.append(f"Invoice: حذف {dups} ردیف کاملاً تکراری")

    # Parse dates; drop null dates
    df["InvoiceDate"] = df["InvoiceDate"].map(_parse_jalali)
    null_dates = df["InvoiceDate"].isna().sum()
    df = df.dropna(subset=["InvoiceDate"]).copy()
    notes.append(f"Invoice: حذف {null_dates} فاکتور بدون تاریخ معتبر")

    # Invalid FK
    bad_b = ~df["BranchID"].isin(valid_branches)
    bad_c = ~df["CustomerID"].isin(valid_customers)
    notes.append(f"Invoice: حذف {bad_b.sum()} Branch نامعتبر و {bad_c.sum()} Customer نامعتبر")
    df = df.loc[~bad_b & ~bad_c].copy()

    # Channel
    df["Channel"] = df["Channel"].fillna("Store")
    df["Channel"] = df["Channel"].replace({"": "Store"})

    # Amounts: recompute later from items preferred; here fix extremes/negatives
    q99 = df["TotalAmount"].quantile(0.99)
    extreme = (df["TotalAmount"].isna()) | (df["TotalAmount"] < 0) | (df["TotalAmount"] > q99 * 3)
    notes.append(f"Invoice: {extreme.sum()} مبلغ نامعتبر/افراطی -> NaN (بازسازی از اقلام)")
    df.loc[extreme, "TotalAmount"] = np.nan

    df["DiscountAmount"] = df["DiscountAmount"].fillna(0).clip(lower=0)
    df["Year"] = df["InvoiceDate"].map(lambda x: int(str(x).split("-")[0]))
    df["Month"] = df["InvoiceDate"].map(lambda x: int(str(x).split("-")[1]))
    df["YearMonth"] = df.apply(lambda r: f"{r['Year']:04d}-{r['Month']:02d}", axis=1)

    notes.append(f"Invoice: ردیف‌ها قبل={before} بعد={len(df)}")
    return df, notes


def clean_items(
    df: pd.DataFrame, valid_products: set, valid_invoices: set
) -> tuple[pd.DataFrame, list[str]]:
    notes = []
    before = len(df)
    df = df.copy()

    bad_p = ~df["ProductID"].isin(valid_products)
    bad_i = ~df["InvoiceID"].isin(valid_invoices)
    notes.append(f"InvoiceItem: حذف {bad_p.sum()} محصول و {bad_i.sum()} فاکتور نامعتبر")
    df = df.loc[~bad_p & ~bad_i].copy()

    bad_qty = df["Quantity"].isna() | (df["Quantity"] <= 0)
    notes.append(f"InvoiceItem: {bad_qty.sum()} Quantity نامعتبر -> حذف ردیف")
    df = df.loc[~bad_qty].copy()
    df["Quantity"] = df["Quantity"].astype(int)

    # Rebuild LineTotal if missing or inconsistent
    df["UnitPrice"] = df["UnitPrice"].abs()
    df["LineDiscount"] = df["LineDiscount"].fillna(0).clip(lower=0)
    expected = df["UnitPrice"] * df["Quantity"] - df["LineDiscount"]
    miss = df["LineTotal"].isna() | (df["LineTotal"] < 0)
    notes.append(f"InvoiceItem: بازسازی LineTotal برای {miss.sum()} ردیف")
    df.loc[miss, "LineTotal"] = expected.loc[miss]
    df["LineTotal"] = df["LineTotal"].clip(lower=0)

    notes.append(f"InvoiceItem: ردیف‌ها قبل={before} بعد={len(df)}")
    return df, notes


def rebuild_invoice_totals(invoices: pd.DataFrame, items: pd.DataFrame) -> pd.DataFrame:
    agg = items.groupby("InvoiceID").agg(
        ItemsCount=("InvoiceItemID", "count"),
        ItemsQty=("Quantity", "sum"),
        RecalcTotal=("LineTotal", "sum"),
        RecalcDiscount=("LineDiscount", "sum"),
    )
    out = invoices.merge(agg, on="InvoiceID", how="inner")
    # Prefer item-based totals
    out["TotalAmount"] = out["RecalcTotal"]
    out["DiscountAmount"] = out["RecalcDiscount"]
    out = out.drop(columns=["RecalcTotal", "RecalcDiscount"])
    # Keep only completed for KPI core (status filter applied in KPI module)
    return out


def run_cleaning() -> dict:
    DATA_CLEANED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    raw = {
        "Product": pd.read_csv(DATA_RAW / "Product.csv"),
        "Branch": pd.read_csv(DATA_RAW / "Branch.csv"),
        "Customer": pd.read_csv(DATA_RAW / "Customer.csv"),
        "Invoice": pd.read_csv(DATA_RAW / "Invoice.csv"),
        "InvoiceItem": pd.read_csv(DATA_RAW / "InvoiceItem.csv"),
    }

    quality_before = [_quality_report(k, v) for k, v in raw.items()]
    all_notes: list[str] = []

    products, n = clean_products(raw["Product"])
    all_notes += n
    branches, n = clean_branches(raw["Branch"])
    all_notes += n
    customers, n = clean_customers(raw["Customer"])
    all_notes += n
    invoices, n = clean_invoices(raw["Invoice"], set(branches["BranchID"]), set(customers["CustomerID"]))
    all_notes += n
    items, n = clean_items(raw["InvoiceItem"], set(products["ProductID"]), set(invoices["InvoiceID"]))
    all_notes += n
    invoices = rebuild_invoice_totals(invoices, items)

    # Drop invoices that lost all items
    all_notes.append(f"Invoice پس از همگام‌سازی با اقلام: {len(invoices)} فاکتور")

    cleaned = {
        "Product": products,
        "Branch": branches,
        "Customer": customers,
        "Invoice": invoices,
        "InvoiceItem": items,
    }
    for name, df in cleaned.items():
        df.to_csv(DATA_CLEANED / f"{name}.csv", index=False, encoding="utf-8-sig")

    quality_after = [_quality_report(k, v) for k, v in cleaned.items()]

    doc = {
        "quality_before": quality_before,
        "quality_after": quality_after,
        "actions": all_notes,
    }
    with open(TABLES / "cleaning_summary.json", "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    # Markdown documentation
    lines = [
        "# مستندسازی پاکسازی داده",
        "",
        "## بررسی کیفیت داده (قبل از پاکسازی)",
        "",
    ]
    for q in quality_before:
        lines.append(f"### {q['table']}")
        lines.append(f"- تعداد ردیف: **{q['rows']:,}** | ستون: {q['cols']} | ردیف تکراری: {q['duplicate_rows']}")
        nulls = {k: v for k, v in q["null_counts"].items() if v > 0}
        if nulls:
            lines.append("- مقادیر ناقص: " + ", ".join(f"`{k}={v}`" for k, v in nulls.items()))
        else:
            lines.append("- مقادیر ناقص قابل توجه: ندارد")
        lines.append("")

    lines += ["## اقدامات پاکسازی", ""]
    for a in all_notes:
        lines.append(f"- {a}")
    lines += ["", "## کیفیت پس از پاکسازی", ""]
    for q in quality_after:
        lines.append(f"- **{q['table']}**: {q['rows']:,} ردیف، تکراری={q['duplicate_rows']}")

    lines += [
        "",
        "## روش‌های به‌کاررفته",
        "",
        "| نوع مشکل | روش |",
        "|---|---|",
        "| Null در دسته‌بندی/منطقه/جنسیت/شهر | پر کردن با مقدار منطقی یا برچسب «سایر/نامشخص» |",
        "| قیمت/مقدار منفی یا صفر | جایگزینی با میانه یا حذف ردیف اقلام |",
        "| سن پرت (>100) | جایگزینی با میانه |",
        "| کلید خارجی نامعتبر | حذف رکورد |",
        "| فاکتور تکراری | حذف duplicate |",
        "| مبلغ فاکتور افراطی/خالی | بازسازی از جمع اقلام فاکتور |",
        "",
    ]
    (DOCS / "01_data_cleaning.md").write_text("\n".join(lines), encoding="utf-8")
    print("Cleaning done. Docs ->", DOCS / "01_data_cleaning.md")
    return doc


if __name__ == "__main__":
    run_cleaning()
