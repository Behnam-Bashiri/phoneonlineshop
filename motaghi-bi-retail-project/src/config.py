"""Project paths and shared constants."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_CLEANED = ROOT / "data" / "cleaned"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
TABLES = OUTPUTS / "tables"
REPORTS = ROOT / "reports"
DOCS = ROOT / "docs"

# Jalali date range: start of 1400 → mid 1405 (Shahrivar)
START_JALALI = (1400, 1, 1)
END_JALALI = (1405, 6, 31)

RANDOM_SEED = 42

# Persian holidays / peak seasons used in analysis (month, day) — approximate
IMPORTANT_OCCASIONS = {
    "نوروز": [(1, 1), (1, 2), (1, 3), (1, 4), (1, 13)],
    "یلدا": [(10, 30)],
    "دهه فجر": [(11, 12), (11, 22)],
    "شب‌های قدر / رمضان": [(9, 19), (9, 21), (9, 23)],
    "بازگشایی مدارس": [(7, 1)],
}

CHANNEL_MAP = {"Online": "آنلاین", "Store": "حضوری", "App": "اپلیکیشن"}
