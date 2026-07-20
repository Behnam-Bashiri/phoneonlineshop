"""Section 3 & 4 helpers — visualizations, clustering, occasion analysis."""
from __future__ import annotations

import json

import jdatetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from config import FIGURES, IMPORTANT_OCCASIONS, TABLES
from kpis import completed_invoices, load_cleaned

# Windows-friendly Persian font
plt.rcParams["font.family"] = "Tahoma"
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", font="Tahoma")


def _save(fig, name: str):
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved", path)
    return path


def plot_sales_trend(inv: pd.DataFrame):
    monthly = inv.groupby("YearMonth")["TotalAmount"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.plot(monthly.index, monthly.values, color="#0B6E4F", linewidth=2)
    ax.set_title("روند فروش ماهانه")
    ax.set_xlabel("ماه")
    ax.set_ylabel("مبلغ فروش (ریال)")
    ax.tick_params(axis="x", rotation=60)
    # Show every 3rd tick
    ticks = list(range(0, len(monthly), 3))
    ax.set_xticks([monthly.index[i] for i in ticks])
    return _save(fig, "01_sales_trend.png"), monthly


def plot_branch_sales(inv: pd.DataFrame, branches: pd.DataFrame):
    g = (
        inv.groupby("BranchID")["TotalAmount"]
        .sum()
        .reset_index()
        .merge(branches[["BranchID", "BranchName"]], on="BranchID")
        .sort_values("TotalAmount", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(g["BranchName"], g["TotalAmount"], color="#1B4965")
    ax.set_title("مقایسه فروش شعب")
    ax.set_xlabel("مجموع فروش")
    return _save(fig, "02_branch_sales.png"), g


def plot_channel_donut(inv: pd.DataFrame):
    ch = inv.groupby("Channel")["TotalAmount"].sum()
    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ["#0B6E4F", "#1B4965", "#E09F3E"]
    wedges, texts, autotexts = ax.pie(
        ch.values,
        labels=ch.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[: len(ch)],
        pctdistance=0.75,
        wedgeprops=dict(width=0.45),
    )
    ax.set_title("سهم کانال‌های فروش")
    return _save(fig, "03_channel_donut.png"), ch


def build_customer_features(inv: pd.DataFrame) -> pd.DataFrame:
    inv = inv.dropna(subset=["InvoiceDate"]).copy()
    inv = inv.loc[inv["InvoiceDate"].astype(str).str.strip().str.lower() != "nan"]

    def to_ord(s):
        parts = str(s).replace("/", "-").split("-")
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
        return jdatetime.date(y, m, d).togregorian().toordinal()

    inv["_ord"] = inv["InvoiceDate"].map(to_ord)
    ref = int(inv["_ord"].max())
    feat = (
        inv.groupby("CustomerID")
        .agg(
            Recency=("_ord", lambda s: ref - s.max()),
            Frequency=("InvoiceID", "count"),
            Monetary=("TotalAmount", "sum"),
        )
        .reset_index()
    )
    return feat


def plot_customer_scatter(feat: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(feat["Frequency"], feat["Monetary"], alpha=0.35, c="#1B4965", s=18)
    ax.set_title("رفتار مشتریان (تعداد خرید vs مبلغ)")
    ax.set_xlabel("تعداد خرید (Frequency)")
    ax.set_ylabel("مجموع مبلغ (Monetary)")
    return _save(fig, "04_customer_behavior.png")


def cluster_customers(feat: pd.DataFrame, n_clusters: int = 4):
    X = feat[["Recency", "Frequency", "Monetary"]].copy()
    # Cap monetary outliers for stable clusters
    X["Monetary"] = np.clip(X["Monetary"], None, X["Monetary"].quantile(0.99))
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(Xs)
    out = feat.copy()
    out["Cluster"] = labels

    # Name clusters by monetary/frequency profile
    profiles = out.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean()
    names = {}
    for c, row in profiles.iterrows():
        if row["Monetary"] >= profiles["Monetary"].quantile(0.75) and row["Frequency"] >= profiles["Frequency"].median():
            names[c] = "مشتریان وفادار پرارزش"
        elif row["Frequency"] >= profiles["Frequency"].quantile(0.75):
            names[c] = "مشتریان پرتراکنش"
        elif row["Recency"] >= profiles["Recency"].quantile(0.75):
            names[c] = "مشتریان در خطر ریزش"
        else:
            names[c] = "مشتریان عادی / کم‌تراکنش"
    # Ensure unique names
    used = {}
    for c, n in names.items():
        if n in used:
            names[c] = f"{n} (گروه {c})"
        used[n] = True
    out["ClusterName"] = out["Cluster"].map(names)
    return out, profiles, names


def plot_clusters(clustered: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 6))
    for name, g in clustered.groupby("ClusterName"):
        ax.scatter(g["Frequency"], g["Monetary"], alpha=0.45, s=22, label=name)
    ax.set_title("خوشه‌بندی مشتریان")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Monetary")
    ax.legend(fontsize=8, loc="best")
    return _save(fig, "05_customer_clusters.png")


def analyze_discount(inv: pd.DataFrame) -> dict:
    df = inv.copy()
    df["HasDiscount"] = df["DiscountAmount"] > 0
    df["DiscountRate"] = np.where(df["TotalAmount"] + df["DiscountAmount"] > 0, df["DiscountAmount"] / (df["TotalAmount"] + df["DiscountAmount"]), 0)
    corr = float(df[["DiscountAmount", "TotalAmount"]].corr().iloc[0, 1])
    summary = (
        df.groupby("HasDiscount")
        .agg(AvgSales=("TotalAmount", "mean"), Count=("InvoiceID", "count"))
        .to_dict()
    )
    # Binned discount rate vs avg sales
    df["DiscBin"] = pd.cut(df["DiscountRate"], bins=[-0.01, 0, 0.05, 0.1, 0.2, 1], labels=["0%", "0-5%", "5-10%", "10-20%", ">20%"])
    by_bin = df.groupby("DiscBin", observed=False)["TotalAmount"].mean()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    by_bin.plot(kind="bar", ax=ax, color="#E09F3E")
    ax.set_title("میانگین مبلغ فاکتور بر اساس نرخ تخفیف")
    ax.set_xlabel("نرخ تخفیف")
    ax.set_ylabel("میانگین مبلغ")
    _save(fig, "07_discount_effect.png")

    return {
        "correlation_discount_sales": corr,
        "avg_with_discount": float(df.loc[df["HasDiscount"], "TotalAmount"].mean()),
        "avg_without_discount": float(df.loc[~df["HasDiscount"], "TotalAmount"].mean()),
        "by_bin": {str(k): float(v) for k, v in by_bin.items()},
    }


def analyze_occasions(inv: pd.DataFrame) -> dict:
    inv = inv.copy()
    inv["Day"] = inv["InvoiceDate"].map(lambda s: int(str(s).split("-")[2]))
    inv["Month"] = inv["Month"] if "Month" in inv.columns else inv["InvoiceDate"].map(lambda s: int(str(s).split("-")[1]))

    daily = inv.groupby(["Year", "Month", "Day"])["TotalAmount"].sum().reset_index()
    daily_mean = float(daily["TotalAmount"].mean())

    results = {}
    for name, days in IMPORTANT_OCCASIONS.items():
        mask = False
        for m, d in days:
            mask = mask | ((daily["Month"] == m) & (daily["Day"] == d))
        subset = daily.loc[mask]
        if len(subset) == 0:
            results[name] = {"avg_sales": None, "lift_vs_daily_mean": None, "n_days": 0}
        else:
            avg = float(subset["TotalAmount"].mean())
            results[name] = {
                "avg_sales": avg,
                "lift_vs_daily_mean": avg / daily_mean if daily_mean else None,
                "n_days": int(len(subset)),
            }
    return {"daily_mean": daily_mean, "occasions": results}


def sales_trend_insights(monthly: pd.Series) -> dict:
    s = monthly.astype(float)
    growth = s.pct_change()
    top_up = growth.nlargest(3)
    top_down = growth.nsmallest(3)
    return {
        "best_growth_months": {str(k): float(v) for k, v in top_up.items()},
        "worst_drop_months": {str(k): float(v) for k, v in top_down.items()},
        "overall_start": float(s.iloc[0]),
        "overall_end": float(s.iloc[-1]),
        "overall_change_pct": float((s.iloc[-1] / s.iloc[0]) - 1) if s.iloc[0] else None,
    }


def run_analysis_and_plots():
    FIGURES.mkdir(parents=True, exist_ok=True)
    data = load_cleaned()
    inv = completed_invoices(data["Invoice"])

    _, monthly = plot_sales_trend(inv)
    _, branch_g = plot_branch_sales(inv, data["Branch"])
    _, channels = plot_channel_donut(inv)

    feat = build_customer_features(inv)
    plot_customer_scatter(feat)
    clustered, profiles, names = cluster_customers(feat)
    plot_clusters(clustered)
    clustered.to_csv(TABLES / "customer_clusters.csv", index=False, encoding="utf-8-sig")

    discount = analyze_discount(inv)
    occasions = analyze_occasions(inv)
    trend = sales_trend_insights(monthly)

    # High vs low frequency customer traits
    q75 = feat["Frequency"].quantile(0.75)
    q25 = feat["Frequency"].quantile(0.25)
    high = feat.loc[feat["Frequency"] >= q75]
    low = feat.loc[feat["Frequency"] <= q25]

    summary = {
        "trend": trend,
        "discount": discount,
        "occasions": occasions,
        "channels": {str(k): float(v) for k, v in channels.items()},
        "cluster_names": {str(k): v for k, v in names.items()},
        "cluster_profiles": profiles.reset_index().to_dict(orient="records"),
        "high_freq_avg_monetary": float(high["Monetary"].mean()),
        "low_freq_avg_monetary": float(low["Monetary"].mean()),
        "high_freq_avg_recency": float(high["Recency"].mean()),
        "low_freq_avg_recency": float(low["Recency"].mean()),
        "top_branch": branch_g.iloc[-1].to_dict(),
        "bottom_branch": branch_g.iloc[0].to_dict(),
    }
    with open(TABLES / "analysis_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
    print("Analysis & plots done")
    return summary


if __name__ == "__main__":
    run_analysis_and_plots()
