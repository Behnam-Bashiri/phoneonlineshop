# پروژه هوش تجاری — تحلیل فروش فروشگاه زنجیره‌ای

پروژه درس هوش تجاری (استاد: دکتر نشاطی) مطابق فایل تمرین.

## اجرای سریع

```bash
cd motaghi-bi-retail-project
python -m pip install -r requirements.txt
python src/run_all.py
```

پس از اجرا:

| مسیر | محتوا |
|---|---|
| `data/raw/` | داده خام با Null و نویز |
| `data/cleaned/` | داده پاک‌شده |
| `outputs/figures/` | ۶+ نمودار خواسته‌شده |
| `outputs/tables/` | KPIها و خروجی تحلیل |
| `docs/01_data_cleaning.md` | مستند پاکسازی |
| `reports/Final_Report.md` | گزارش جامع فارسی |

## بخش‌های پیاده‌سازی‌شده

1. **آماده‌سازی داده** — کیفیت‌سنجی، شناسایی ناقص/نویزی، پاکسازی، مستندسازی  
2. **KPI** — فروش، زمانی، شعب، مشتری + CLV  
3. **مصورسازی** — Line / Bar / Donut / Scatter / Cluster / Forecast  
4. **تحلیل** — روند، تخفیف، شعب، رفتار مشتری، K-Means، مناسبت‌ها  
5. **پیش‌بینی** — Holt-Winters (یا روند خطی در صورت کمبود فصل)

## ساختار کد

```
src/
  generate_data.py   # تولید دیتاست
  clean_data.py      # پاکسازی
  kpis.py            # شاخص‌ها
  analyze.py         # نمودار + تحلیل + خوشه
  forecast.py        # پیش‌بینی
  run_all.py         # اجرای کامل + گزارش
  config.py          # مسیرها و ثابت‌ها
```

## تحویل ZIP

طبق صورت‌مسئله نام فایل باید به شکل زیر باشد:

`stuNumber-lastname-firstname-FP.zip`

محتوای همین پوشه را فشرده کنید (ترجیحاً بدون `__pycache__`).

## وابستگی‌ها

Python 3.10+ و پکیج‌های `requirements.txt` (pandas, numpy, matplotlib, seaborn, scikit-learn, statsmodels, jdatetime).
