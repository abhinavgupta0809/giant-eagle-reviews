from pathlib import Path

# Shown on the site; the site reads these from summary.meta, never from typed text.
PRODUCT_NAME = "Giant Eagle"
PRODUCT_COMPANY = "Giant Eagle"
PLAY_APP_ID = "com.gianteagle.apps.grocery"
APPSTORE_ID = "1465897036"
# Giant Eagle is a US-only grocer. Confirmed on the live stores 2026-10-20.
PLAY_LANGS = ("en",)  # "es" returned zero reviews on 2026-10-20
PLAY_COUNTRY = "us"
# US storefront only: the app is not sold elsewhere.
APPSTORE_COUNTRIES = ("us",)
# Last 12 months: widened from 6 at Abhinav's request on 2026-10-20 (6 months held only 164 reviews).
WINDOW_DAYS = 365
MAX_ROWS = 200_000
SEED = 42
PAGE_SIZE = 200
PAGE_DELAY = 0.5
RETRIES = 3
HTTP_TIMEOUT = (10, 45)
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
COLUMNS = (
    "review_id", "platform", "country", "store_lang", "timestamp", "date_utc", "rating",
    "title", "review_text", "app_version", "thumbs_up", "has_dev_reply",
)

ANNOTATION_MODEL = "claude-haiku-5-5"
ANNOTATION_BATCH_SIZE = 25
ANNOTATION_OUTPUT_TOKENS_PER_REVIEW = 180
ANNOTATION_PRICE_READ_DATE = "2026-10-09"
ANNOTATION_PRICING_URL = "https://platform.claude.com/docs/en/about-claude/pricing"
# USD per million tokens, used by dry runs and explicit --offline-prices runs.
ANNOTATION_ESTIMATE_PRICES = {
    "short": {"input": 0.10, "output": 0.50, "cache_write": 0.125, "cache_read": 0.01},
    "long": {"input": 0.50, "output": 2.50, "cache_write": 0.625, "cache_read": 0.05},
}
ANNOTATION_LONG_PROMPT_THRESHOLD = 100_000
