"""Section 5 — Sales forecasting (Holt-Winters exponential smoothing)."""
from __future__ import annotations

import json
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from config import FIGURES, TABLES
from kpis import completed_invoices, load_cleaned

plt.rcParams["font.family"] = "Tahoma"
plt.rcParams["axes.unicode_minus"] = False
warnings.filterwarnings("ignore")


def run_forecast(horizon: int = 6) -> dict:
    FIGURES.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    inv = completed_invoices(load_cleaned()["Invoice"])
    monthly = (
        inv.groupby("YearMonth")["TotalAmount"]
        .sum()
        .sort_index()
        .astype(float)
    )
    # Need enough points; seasonal period 12 if possible
    y = monthly.values
    idx = monthly.index.tolist()

    seasonal_periods = 12 if len(y) >= 24 else None
    if seasonal_periods:
        model = ExponentialSmoothing(
            y,
            trend="add",
            seasonal="add",
            seasonal_periods=seasonal_periods,
            initialization_method="estimated",
        )
        model_name = "Holt-Winters (additive trend + seasonality)"
        reason = (
            "سری فروش ماهانه دارای روند رشد و الگوی فصلی سالانه است؛ "
            "Holt-Winters برای داده‌های خرده‌فروشی با فصلی‌بودن ۱۲ماهه مناسب و قابل تفسیر است."
        )
    else:
        model = ExponentialSmoothing(y, trend="add", seasonal=None, initialization_method="estimated")
        model_name = "Holt linear trend (no seasonality)"
        reason = "تعداد ماه‌ها برای فصلی‌سازی ۱۲ماهه کافی نبود؛ مدل روند خطی هموارسازی نمایی استفاده شد."

    fitted = model.fit(optimized=True)
    fitted_vals = fitted.fittedvalues
    forecast = fitted.forecast(horizon)

    # Build future YearMonth labels
    last = idx[-1]
    ly, lm = map(int, last.split("-"))
    future_labels = []
    y0, m0 = ly, lm
    for _ in range(horizon):
        m0 += 1
        if m0 > 12:
            m0 = 1
            y0 += 1
        future_labels.append(f"{y0:04d}-{m0:02d}")

    # Simple holdout MAPE on last 6 months in-sample rolling isn't perfect;
    # report in-sample MAPE on fitted
    mape = float(np.mean(np.abs((y - fitted_vals) / np.clip(y, 1, None))) * 100)

    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.plot(idx, y, label="فروش واقعی", color="#0B6E4F", linewidth=2)
    ax.plot(idx, fitted_vals, label="برازش مدل", color="#1B4965", linestyle="--", linewidth=1.5)
    ax.plot(future_labels, forecast, label="پیش‌بینی", color="#E09F3E", linewidth=2, marker="o")
    ax.set_title("مقایسه فروش واقعی و پیش‌بینی‌شده")
    ax.set_xlabel("ماه")
    ax.set_ylabel("مبلغ فروش")
    ax.legend()
    # sparse ticks
    all_x = idx + future_labels
    tick_pos = list(range(0, len(all_x), max(1, len(all_x) // 12)))
    ax.set_xticks([all_x[i] for i in tick_pos])
    ax.tick_params(axis="x", rotation=60)
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / "06_forecast.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fc_df = pd.DataFrame({"YearMonth": future_labels, "ForecastSales": forecast})
    fc_df.to_csv(TABLES / "forecast_next_months.csv", index=False, encoding="utf-8-sig")

    result = {
        "model": model_name,
        "reason": reason,
        "horizon_months": horizon,
        "in_sample_mape_pct": round(mape, 2),
        "forecast": fc_df.to_dict(orient="records"),
        "last_actual_month": idx[-1],
        "last_actual_sales": float(y[-1]),
        "forecast_sum": float(np.sum(forecast)),
    }
    with open(TABLES / "forecast_summary.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Forecast done ->", FIGURES / "06_forecast.png")
    return result


if __name__ == "__main__":
    run_forecast()
