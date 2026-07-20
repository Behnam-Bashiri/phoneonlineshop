"""
Master pipeline: generate → clean → KPIs → analyze/plots → forecast → final report.
Run from project root or from src/:

  python src/run_all.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure src is on path
SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from analyze import run_analysis_and_plots
from clean_data import run_cleaning
from config import DOCS, FIGURES, REPORTS, TABLES
from forecast import run_forecast
from generate_data import main as generate_data
from kpis import compute_kpis


def _fmt_money(x) -> str:
    try:
        return f"{float(x):,.0f}"
    except Exception:
        return str(x)


def _fmt_pct(x) -> str:
    try:
        if x is None or (isinstance(x, float) and (x != x)):
            return "—"
        return f"{float(x) * 100:.1f}%"
    except Exception:
        return str(x)


def build_final_report(kpis: dict, analysis: dict, forecast: dict) -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    sales = kpis["sales"]
    cust = kpis["customer"]
    trend = analysis["trend"]
    disc = analysis["discount"]
    occ = analysis["occasions"]

    yearly_rows = ""
    for r in kpis["yearly"]:
        yearly_rows += f"| {r['Year']} | {_fmt_money(r['Sales'])} | {_fmt_pct(r.get('YoY_Growth'))} |\n"

    cluster_rows = ""
    for p in analysis["cluster_profiles"]:
        c = p["Cluster"]
        name = analysis["cluster_names"].get(str(c), f"Cluster {c}")
        cluster_rows += (
            f"| {name} | {p['Recency']:.1f} | {p['Frequency']:.2f} | {_fmt_money(p['Monetary'])} |\n"
        )

    occ_rows = ""
    for name, info in occ["occasions"].items():
        lift = info.get("lift_vs_daily_mean")
        lift_s = f"{lift:.2f}x" if lift else "—"
        occ_rows += f"| {name} | {_fmt_money(info.get('avg_sales'))} | {lift_s} | {info.get('n_days', 0)} |\n"

    fc_rows = ""
    for r in forecast["forecast"]:
        fc_rows += f"| {r['YearMonth']} | {_fmt_money(r['ForecastSales'])} |\n"

    top_b = analysis["top_branch"]
    bot_b = analysis["bottom_branch"]

    md = f"""# گزارش جامع پروژه هوش تجاری
## تحلیل داده‌های فروش فروشگاه زنجیره‌ای

**استاد:** دکتر نشاطی  
**عنوان:** تحلیل داده‌های فروش یک فروشگاه زنجیره‌ای  
**بازه زمانی داده:** ابتدای سال ۱۴۰۰ تا اواسط سال ۱۴۰۵  

---

## فهرست مطالب
1. [مقدمه و هدف](#1-مقدمه-و-هدف)
2. [اطلاعات دیتاست](#2-اطلاعات-دیتاست)
3. [بخش اول: آماده‌سازی داده](#3-بخش-اول-آماده‌سازی-داده)
4. [بخش دوم: محاسبه KPIها](#4-بخش-دوم-محاسبه-kpiها)
5. [بخش سوم: مصورسازی](#5-بخش-سوم-مصورسازی)
6. [بخش چهارم: تحلیل داده‌ها](#6-بخش-چهارم-تحلیل-داده‌ها)
7. [بخش پنجم: پیش‌بینی فروش](#7-بخش-پنجم-پیش‌بینی-فروش)
8. [جمع‌بندی و پیشنهادات مدیریتی](#8-جمع‌بندی-و-پیشنهادات-مدیریتی)

---

## 1. مقدمه و هدف

این پروژه با هدف پاکسازی داده‌های فروش، استخراج شاخص‌های کلیدی عملکرد (KPI)، مصورسازی،
تحلیل رفتار مشتریان (شامل خوشه‌بندی) و پیش‌بینی روند فروش با پایتون انجام شده است.

مسیر اجرای کامل پروژه:

```bash
cd motaghi-bi-retail-project
python -m pip install -r requirements.txt
python src/run_all.py
```

خروجی‌ها در پوشه‌های `outputs/figures`، `outputs/tables`، `docs` و `reports` ذخیره می‌شوند.

---

## 2. اطلاعات دیتاست

پنج جدول اصلی:

| جدول | شرح |
|---|---|
| Product | اطلاعات محصولات |
| Branch | اطلاعات شعب |
| Customer | اطلاعات مشتریان |
| Invoice | اطلاعات فاکتورها |
| InvoiceItem | جزئیات اقلام فاکتور |

> **نکته:** در فایل تمرین، دیتاست جداگانه همراه PDF نبود؛ بنابراین دیتاست واقعی‌نما با همان ساختار
> و بازه زمانی (۱۴۰۰ تا میانه ۱۴۰۵)، همراه مقادیر Null و نویزی عمدی تولید و سپس پاکسازی شده است.
> کد تولید در `src/generate_data.py` و داده خام در `data/raw` قرار دارد.

---

## 3. بخش اول: آماده‌سازی داده

جزئیات کامل کیفیت داده و اقدامات در فایل `docs/01_data_cleaning.md` آمده است.

### خلاصه روش‌ها
- شناسایی Null، مقادیر خالی، تکراری‌ها، کلید خارجی نامعتبر، سن/قیمت/مقدار پرت و منفی
- پر کردن منطقی فیلدهای توصیفی (دسته، منطقه، جنسیت، شهر)
- حذف یا اصلاح رکوردهای نویزی عددی
- بازسازی مبلغ فاکتور از جمع اقلام برای یکپارچگی

### خروجی
جداول پاک‌شده در `data/cleaned/` ذخیره شده‌اند.

---

## 4. بخش دوم: محاسبه KPIها

### شاخص‌های فروش
| شاخص | مقدار |
|---|---|
| مجموع فروش | {_fmt_money(sales['total_sales'])} |
| تعداد فاکتورها | {sales['invoice_count']:,} |
| میانگین مبلغ هر فاکتور | {_fmt_money(sales['avg_invoice_amount'])} |
| میانگین تعداد اقلام هر فاکتور | {sales['avg_items_per_invoice']:.2f} |
| مجموع تخفیف | {_fmt_money(sales['total_discount'])} |

### شاخص‌های زمانی (فروش سالانه و رشد)
| سال | فروش | نرخ رشد سالانه |
|---|---|---|
{yearly_rows}

جداول ماهانه/سالانه/شعبه/مشتری در `outputs/tables/` ذخیره شده‌اند.

### شاخص‌های مشتری
| شاخص | مقدار |
|---|---|
| تعداد مشتریان فعال | {cust['active_customers']:,} |
| میانگین خرید هر مشتری | {_fmt_money(cust['avg_spend_per_customer'])} |
| میانگین تعداد خرید هر مشتری | {cust['avg_purchases_per_customer']:.2f} |
| میانگین CLV (تقریبی) | {_fmt_money(cust['avg_clv'])} |
| میانه CLV | {_fmt_money(cust['median_clv'])} |

**تعریف CLV استفاده‌شده:**  
`CLV ≈ میانگین مبلغ سفارش × تعداد خرید × ۱.۵`  
ضریب ۱.۵ به‌عنوان افق عمر مورد انتظار ساده‌شده برای مقایسه نسبی مشتریان به کار رفته است.

---

## 5. بخش سوم: مصورسازی

### 1) روند فروش در طول زمان
![روند فروش](../outputs/figures/01_sales_trend.png)

**تفسیر:** فروش ماهانه در طول بازه عموماً روند صعودی دارد و در ماه‌های نزدیک به مناسبت‌ها
(به‌ویژه نوروز) قله‌های مشخص دیده می‌شود. تغییر کلی از ابتدای سری تا انتها حدود
{_fmt_pct(trend.get('overall_change_pct'))} است.

### 2) مقایسه فروش شعب
![فروش شعب](../outputs/figures/02_branch_sales.png)

**تفسیر:** شعبه برتر از نظر فروش **{top_b.get('BranchName', top_b.get('BranchID'))}** و شعبه ضعیف‌تر
**{bot_b.get('BranchName', bot_b.get('BranchID'))}** است. تفاوت عملکرد می‌تواند ناشی از موقعیت،
ترافیک، یا سهم کانال آنلاین باشد.

### 3) سهم کانال‌های فروش
![کانال‌ها](../outputs/figures/03_channel_donut.png)

**تفسیر:** ترکیب کانال‌ها نشان می‌دهد فروش حضوری همچنان سهم اصلی را دارد و کانال‌های دیجیتال
(آنلاین/اپ) مکمل رشد هستند.

### 4) رفتار مشتریان
![رفتار مشتریان](../outputs/figures/04_customer_behavior.png)

**تفسیر:** پراکندگی Frequency–Monetary نشان می‌دهد گروه کوچکی از مشتریان سهم بالایی از مبلغ را دارند
(الگوی کلاسیک خرده‌فروشی).

### 5) خوشه‌بندی مشتریان
![خوشه‌ها](../outputs/figures/05_customer_clusters.png)

**تفسیر:** با K-Means روی ویژگی‌های RFM، چهار خوشه متمایز به‌دست آمد (جزئیات در بخش ۴).

### 6) فروش واقعی در برابر پیش‌بینی
![پیش‌بینی](../outputs/figures/06_forecast.png)

**تفسیر:** مدل هموارسازی نمایی روند و فصلی‌بودن را دنبال می‌کند؛ جزئیات مدل در بخش ۵ آمده است.

---

## 6. بخش چهارم: تحلیل داده‌ها

### 6.1 تحلیل روند فروش
- شروع سری: {_fmt_money(trend['overall_start'])}
- پایان سری: {_fmt_money(trend['overall_end'])}
- تغییر کلی: {_fmt_pct(trend.get('overall_change_pct'))}

**قوی‌ترین رشد ماهانه:**
{chr(10).join(f"- `{k}`: {_fmt_pct(v)}" for k, v in trend['best_growth_months'].items())}

**بیشترین افت ماهانه:**
{chr(10).join(f"- `{k}`: {_fmt_pct(v)}" for k, v in trend['worst_drop_months'].items())}

### 6.2 تحلیل اثر تخفیف
- همبستگی مبلغ تخفیف و مبلغ فروش: **{disc['correlation_discount_sales']:.3f}**
- میانگین فاکتور با تخفیف: {_fmt_money(disc['avg_with_discount'])}
- میانگین فاکتور بدون تخفیف: {_fmt_money(disc['avg_without_discount'])}

**تحلیل:** همبستگی مثبت/منفی باید با احتیاط تفسیر شود؛ تخفیف اغلب روی سبدهای بزرگ‌تر اعمال می‌شود
و لزوماً به‌معنای علیت «تخفیف → فروش بیشتر» نیست. نمودار `07_discount_effect.png` میانگین مبلغ
را بر اساس بازه نرخ تخفیف نشان می‌دهد.

![اثر تخفیف](../outputs/figures/07_discount_effect.png)

### 6.3 تحلیل عملکرد شعب
- **برتر:** {top_b.get('BranchName')} — فروش {_fmt_money(top_b.get('TotalAmount'))}
- **نیازمند بررسی:** {bot_b.get('BranchName')} — فروش {_fmt_money(bot_b.get('TotalAmount'))}

پیشنهاد: برای شعب ضعیف، بررسی ترکیب موجودی، ساعات شلوغی، و کمپین محلی؛ برای شعب قوی، الگوبرداری.

### 6.4 تحلیل رفتار مشتریان
- میانگین Monetary مشتریان پرتراکنش: {_fmt_money(analysis['high_freq_avg_monetary'])}
- میانگین Monetary مشتریان کم‌تراکنش: {_fmt_money(analysis['low_freq_avg_monetary'])}
- میانگین Recency پرتراکنش‌ها: {analysis['high_freq_avg_recency']:.1f} روز
- میانگین Recency کم‌تراکنش‌ها: {analysis['low_freq_avg_recency']:.1f} روز

مشتریان پرتراکنش معمولاً فاصله خرید کوتاه‌تر و ارزش تجمعی بالاتر دارند؛ مشتریان کم‌تراکنش
هدف مناسبی برای کمپین بازگشت (win-back) هستند.

### 6.5 خوشه‌بندی مشتریان (K-Means روی RFM)
| عنوان خوشه | میانگین Recency | میانگین Frequency | میانگین Monetary |
|---|---|---|---|
{cluster_rows}

### 6.6 تحلیل اثر مناسبت‌ها
میانگین فروش روزانه کل: {_fmt_money(occ['daily_mean'])}

| مناسبت | میانگین فروش روز مناسبت | نسبت به میانگین روزانه | تعداد روز مشاهده‌شده |
|---|---|---|---|
{occ_rows}

---

## 7. بخش پنجم: پیش‌بینی فروش

### مدل انتخاب‌شده
**{forecast['model']}**

### دلیل انتخاب
{forecast['reason']}

### دقت درون‌نمونه‌ای
MAPE ≈ **{forecast['in_sample_mape_pct']}%**

### نتیجه پیش‌بینی ({forecast['horizon_months']} ماه آینده)
آخرین ماه واقعی: `{forecast['last_actual_month']}` با فروش {_fmt_money(forecast['last_actual_sales'])}

| ماه | فروش پیش‌بینی‌شده |
|---|---|
{fc_rows}

جمع پیش‌بینی افق: {_fmt_money(forecast['forecast_sum'])}

### تحلیل نتایج
اگر روند فصلی حفظ شود، مدیریت باید موجودی و نیروی انسانی را حول قله‌های تاریخی
(نوروز و پایان سال) تقویت کند. خطای مدل برای برنامه‌ریزی سطح کلان مناسب است؛ برای SKU-level
به مدل‌های جزئی‌تر نیاز است.

---

## 8. جمع‌بندی و پیشنهادات مدیریتی

1. **پاکسازی داده را制度化 کنید** (قواعد FK، بازه مجاز سن/قیمت، حذف duplicate).
2. **روی خوشه وفادار پرارزش** برنامه وفاداری و پیشنهاد شخصی‌سازی اجرا کنید.
3. **شعب ضعیف** را با بنچمارک شعب برتر مقایسه و اقدام اصلاحی تعریف کنید.
4. **تخفیف** را هدفمند (روی سبد یا مشتریان در خطر ریزش) نگه دارید، نه همگانی.
5. **پیش‌بینی ماهانه** را ماه‌به‌ماه با داده واقعی به‌روز کنید (retrain).

---

## پیوست — ساختار پروژه

```
motaghi-bi-retail-project/
├── data/raw/              # داده خام (با Null و نویز)
├── data/cleaned/          # داده پاک‌شده
├── src/                   # کدهای پایتون
├── outputs/figures/       # نمودارها
├── outputs/tables/        # جداول KPI و خلاصه‌ها
├── docs/                  # مستندات فنی پاکسازی
├── reports/               # گزارش نهایی
├── requirements.txt
└── README.md
```

*این گزارش به‌صورت خودکار پس از اجرای `python src/run_all.py` تولید/به‌روزرسانی می‌شود.*
"""
    out = REPORTS / "Final_Report.md"
    out.write_text(md, encoding="utf-8")
    # Also copy a short index to docs
    (DOCS / "README_DOCS.md").write_text(
        "# مستندات\n\n- `01_data_cleaning.md` — جزئیات پاکسازی\n"
        "- `../reports/Final_Report.md` — گزارش جامع نهایی\n",
        encoding="utf-8",
    )
    print("Final report ->", out)
    return out


def main():
    print("=" * 60)
    print("1/5 Generating raw data...")
    generate_data()
    print("2/5 Cleaning...")
    run_cleaning()
    print("3/5 KPIs...")
    kpis = compute_kpis()
    print("4/5 Analysis & visualizations...")
    analysis = run_analysis_and_plots()
    print("5/5 Forecasting...")
    forecast = run_forecast()
    build_final_report(kpis, analysis, forecast)
    print("=" * 60)
    print("DONE")
    print("Figures:", FIGURES)
    print("Tables:", TABLES)
    print("Report:", REPORTS / "Final_Report.md")


if __name__ == "__main__":
    main()
