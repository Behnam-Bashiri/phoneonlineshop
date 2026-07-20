"""
Generate synthetic retail chain sales data (1400–mid 1405) with intentional
nulls and noisy values so the cleaning section of the assignment is meaningful.

Output CSV files in data/raw/:
  Product.csv, Branch.csv, Customer.csv, Invoice.csv, InvoiceItem.csv
"""
from __future__ import annotations

import random
from pathlib import Path

import jdatetime
import numpy as np
import pandas as pd

from config import DATA_RAW, END_JALALI, RANDOM_SEED, START_JALALI

rng = np.random.default_rng(RANDOM_SEED)
random.seed(RANDOM_SEED)


CATEGORIES = {
    "لبنیات": ["شیر", "ماست", "پنیر", "کره", "دوغ"],
    "نوشیدنی": ["آب‌معدنی", "نوشابه", "آبمیوه", "چای", "قهوه"],
    "خشکبار": ["پسته", "بادام", "کشمش", "گردو", "فندق"],
    "شوینده": ["مایع ظرفشویی", "پودر لباسشویی", "شامپو", "صابون", "سفیدکننده"],
    "خوراکی": ["برنج", "روغن", "ماکارونی", "کنسرو", "رب"],
    "تنقلات": ["چیپس", "شکلات", "بیسکویت", "آبنبات", "پفک"],
}

CITIES = [
    ("تهران", "مرکز"),
    ("اصفهان", "مرکز"),
    ("شیراز", "جنوب"),
    ("مشهد", "شرق"),
    ("تبریز", "شمال‌غرب"),
    ("اهواز", "جنوب"),
    ("کرج", "مرکز"),
    ("قم", "مرکز"),
]


def _jalali_range(start, end):
    y, m, d = start
    ey, em, ed = end
    cur = jdatetime.date(y, m, d)
    last = jdatetime.date(ey, em, min(ed, jdatetime.j_days_in_month[em - 1]))
    days = []
    while cur <= last:
        days.append(cur)
        cur += jdatetime.timedelta(days=1)
    return days


def generate_products(n: int = 90) -> pd.DataFrame:
    rows = []
    pid = 1
    for cat, items in CATEGORIES.items():
        for name in items:
            for variant in range(1, 4):
                base = float(rng.integers(20_000, 450_000))
                rows.append(
                    {
                        "ProductID": f"P{pid:04d}",
                        "ProductName": f"{name} {variant}",
                        "Category": cat,
                        "Brand": rng.choice(["برندآ", "برندب", "برندج", "برندد", "برنده"]),
                        "UnitPrice": base,
                        "UnitCost": round(base * float(rng.uniform(0.55, 0.8)), 0),
                        "IsActive": rng.choice([1, 1, 1, 0]),
                    }
                )
                pid += 1
                if pid > n:
                    break
            if pid > n:
                break
        if pid > n:
            break
    df = pd.DataFrame(rows)

    # Inject nulls / noise
    null_idx = rng.choice(df.index, size=max(3, len(df) // 25), replace=False)
    df.loc[null_idx, "Category"] = None
    noise_idx = rng.choice(df.index, size=max(2, len(df) // 30), replace=False)
    df.loc[noise_idx, "UnitPrice"] = -abs(df.loc[noise_idx, "UnitPrice"])
    zero_idx = rng.choice(df.index, size=2, replace=False)
    df.loc[zero_idx, "UnitPrice"] = 0
    return df


def generate_branches() -> pd.DataFrame:
    rows = []
    for i, (city, region) in enumerate(CITIES, start=1):
        rows.append(
            {
                "BranchID": f"B{i:02d}",
                "BranchName": f"شعبه {city}",
                "City": city,
                "Region": region,
                "ChannelType": rng.choice(["Hybrid", "Store", "Store"]),
                "OpenDate": str(jdatetime.date(1395 + (i % 5), (i % 12) + 1, 1)),
                "Area_sqm": int(rng.integers(180, 1200)),
            }
        )
    # Extra online hub
    rows.append(
        {
            "BranchID": "B99",
            "BranchName": "انبار مرکزی آنلاین",
            "City": "تهران",
            "Region": "مرکز",
            "ChannelType": "Online",
            "OpenDate": "1398-01-01",
            "Area_sqm": 2500,
        }
    )
    df = pd.DataFrame(rows)
    df.loc[df.sample(2, random_state=RANDOM_SEED).index, "Region"] = None
    df.loc[0, "Area_sqm"] = -50  # noisy
    return df


def generate_customers(n: int = 2200) -> pd.DataFrame:
    first = ["علی", "زهرا", "محمد", "فاطمه", "حسین", "مریم", "رضا", "سارا", "امیر", "نرگس"]
    last = ["رضایی", "محمدی", "حسینی", "کریمی", "احمدی", "موسوی", "جعفری", "نوری"]
    rows = []
    for i in range(1, n + 1):
        city, _ = CITIES[i % len(CITIES)]
        join = jdatetime.date(
            int(rng.integers(1398, 1405)),
            int(rng.integers(1, 13)),
            int(rng.integers(1, 29)),
        )
        rows.append(
            {
                "CustomerID": f"C{i:05d}",
                "FullName": f"{rng.choice(first)} {rng.choice(last)}",
                "Gender": rng.choice(["M", "F", "M", "F", "Unknown"]),
                "Age": int(rng.integers(18, 72)),
                "City": city,
                "JoinDate": str(join),
                "Phone": f"09{rng.integers(10, 99)}{rng.integers(1000000, 9999999)}",
            }
        )
    df = pd.DataFrame(rows)
    # Nulls and noise
    df.loc[rng.choice(df.index, 40, replace=False), "Age"] = None
    df.loc[rng.choice(df.index, 15, replace=False), "Age"] = int(rng.integers(120, 180))
    df.loc[rng.choice(df.index, 25, replace=False), "Gender"] = None
    df.loc[rng.choice(df.index, 20, replace=False), "City"] = ""
    df.loc[rng.choice(df.index, 10, replace=False), "FullName"] = None
    # Duplicate customer ids (noise)
    dup = df.iloc[5].copy()
    dup["FullName"] = "نام تکراری"
    df = pd.concat([df, pd.DataFrame([dup])], ignore_index=True)
    return df


def _seasonal_multiplier(jd: jdatetime.date) -> float:
    """Boost sales around Nowruz, Yalda, school start, etc."""
    m, d = jd.month, jd.day
    if m == 1 and d <= 15:
        return 1.55
    if m == 10 and d >= 28:
        return 1.35
    if m == 7 and d <= 10:
        return 1.25
    if m == 12:
        return 1.2
    if m in (4, 5):  # summer soft
        return 0.9
    return 1.0


def generate_invoices_and_items(
    products: pd.DataFrame,
    branches: pd.DataFrame,
    customers: pd.DataFrame,
    n_invoices: int = 16000,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    days = _jalali_range(START_JALALI, END_JALALI)
    # Weight later years slightly higher (growth)
    year_w = {d.year: 0.7 + 0.12 * (d.year - 1400) for d in days}
    weights = np.array([year_w[d.year] * _seasonal_multiplier(d) for d in days], dtype=float)
    weights /= weights.sum()

    cust_ids = customers["CustomerID"].unique().tolist()
    branch_ids = branches["BranchID"].tolist()
    # Prefer physical branches; B99 for online
    branch_probs = np.array([0.08 if b != "B99" else 0.12 for b in branch_ids], dtype=float)
    branch_probs /= branch_probs.sum()

    product_ids = products["ProductID"].tolist()
    price_map = dict(zip(products["ProductID"], products["UnitPrice"].clip(lower=1)))

    inv_rows = []
    item_rows = []
    item_id = 1

    chosen_days = rng.choice(days, size=n_invoices, p=weights)

    for i in range(1, n_invoices + 1):
        jd = chosen_days[i - 1]
        channel = rng.choice(["Store", "Online", "App"], p=[0.62, 0.25, 0.13])
        if channel == "Online":
            branch = "B99"
        else:
            branch = rng.choice(branch_ids, p=branch_probs)

        cust = rng.choice(cust_ids)
        n_lines = int(rng.integers(1, 7))
        discount_pct = float(rng.choice([0, 0, 0, 5, 10, 15, 20], p=[0.45, 0.15, 0.1, 0.12, 0.1, 0.05, 0.03]))

        line_sum = 0.0
        inv_disc = 0.0
        for _ in range(n_lines):
            pid = rng.choice(product_ids)
            qty = int(rng.integers(1, 6))
            unit = abs(float(price_map.get(pid, 50_000)))
            line_disc = unit * qty * (discount_pct / 100.0) * float(rng.uniform(0.3, 1.0))
            line_total = unit * qty - line_disc
            line_sum += line_total
            inv_disc += line_disc
            item_rows.append(
                {
                    "InvoiceItemID": f"II{item_id:07d}",
                    "InvoiceID": f"INV{i:06d}",
                    "ProductID": pid,
                    "Quantity": qty,
                    "UnitPrice": unit,
                    "LineDiscount": round(line_disc, 0),
                    "LineTotal": round(line_total, 0),
                }
            )
            item_id += 1

        inv_rows.append(
            {
                "InvoiceID": f"INV{i:06d}",
                "CustomerID": cust,
                "BranchID": branch,
                "InvoiceDate": str(jd),
                "Channel": channel,
                "PaymentMethod": rng.choice(["Cash", "Card", "OnlinePay", "Wallet"], p=[0.2, 0.45, 0.25, 0.1]),
                "DiscountAmount": round(inv_disc, 0),
                "TotalAmount": round(line_sum, 0),
                "Status": rng.choice(["Completed", "Completed", "Completed", "Cancelled", "Returned"], p=[0.9, 0.03, 0.03, 0.02, 0.02]),
            }
        )

    invoices = pd.DataFrame(inv_rows)
    items = pd.DataFrame(item_rows)

    # --- Inject data-quality issues ---
    # Null dates / amounts
    invoices.loc[rng.choice(invoices.index, 35, replace=False), "InvoiceDate"] = None
    invoices.loc[rng.choice(invoices.index, 20, replace=False), "TotalAmount"] = None
    invoices.loc[rng.choice(invoices.index, 15, replace=False), "Channel"] = None
    invoices.loc[rng.choice(invoices.index, 10, replace=False), "BranchID"] = "BXX"  # invalid FK
    invoices.loc[rng.choice(invoices.index, 8, replace=False), "CustomerID"] = "CXXXXX"

    # Negative / extreme totals
    invoices.loc[rng.choice(invoices.index, 12, replace=False), "TotalAmount"] = -rng.integers(10_000, 500_000)
    invoices.loc[rng.choice(invoices.index, 5, replace=False), "TotalAmount"] = rng.integers(50_000_000, 90_000_000)

    # Duplicate invoice rows
    invoices = pd.concat([invoices, invoices.iloc[[3, 7, 11]]], ignore_index=True)

    # Item issues
    items.loc[rng.choice(items.index, 40, replace=False), "Quantity"] = None
    items.loc[rng.choice(items.index, 25, replace=False), "Quantity"] = -int(rng.integers(1, 5))
    items.loc[rng.choice(items.index, 15, replace=False), "ProductID"] = "PXXXX"
    items.loc[rng.choice(items.index, 20, replace=False), "LineTotal"] = None

    return invoices, items


def main() -> None:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    products = generate_products()
    branches = generate_branches()
    customers = generate_customers()
    invoices, items = generate_invoices_and_items(products, branches, customers)

    products.to_csv(DATA_RAW / "Product.csv", index=False, encoding="utf-8-sig")
    branches.to_csv(DATA_RAW / "Branch.csv", index=False, encoding="utf-8-sig")
    customers.to_csv(DATA_RAW / "Customer.csv", index=False, encoding="utf-8-sig")
    invoices.to_csv(DATA_RAW / "Invoice.csv", index=False, encoding="utf-8-sig")
    items.to_csv(DATA_RAW / "InvoiceItem.csv", index=False, encoding="utf-8-sig")

    print("Raw datasets written to", DATA_RAW)
    for name, df in [
        ("Product", products),
        ("Branch", branches),
        ("Customer", customers),
        ("Invoice", invoices),
        ("InvoiceItem", items),
    ]:
        print(f"  {name}: {len(df):,} rows")


if __name__ == "__main__":
    main()
