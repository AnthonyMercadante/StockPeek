# stockpeek/fetcher.py
"""
Requests‑based quote fetcher with automatic fallback to Selenium
when Yahoo returns a persistent 429 Too Many Requests.
"""

from __future__ import annotations

import datetime as dt
import random
import time
from typing import Final, Dict, Any

import pandas as pd
import requests

_URL: Final[str] = (
    "https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
)
_UA: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)


def _api_get(url: str, max_retries: int = 6) -> Dict[str, Any]:
    """GET with back‑off on 429; raise on other 4xx/5xx."""
    for attempt in range(max_retries):
        resp = requests.get(url, headers={"User-Agent": _UA}, timeout=8)
        if resp.status_code != 429:
            resp.raise_for_status()
            return resp.json()

        # 429 → exponential back‑off (1, 2, 4, 8, 16, 32 s + jitter)
        sleep_for = 2 ** attempt + random.random()
        time.sleep(sleep_for)

    # last retry still 429 – let caller decide
    resp.raise_for_status()  # will raise HTTPError


def fetch_quote_api(ticker: str) -> pd.DataFrame:
    """
    Return latest quote for *ticker*.  
    Falls back to Selenium when Yahoo keeps returning 429 Too Many Requests.
    """
    try:
        data = _api_get(_URL.format(ticker=ticker))
        result = data["quoteResponse"]["result"][0]
        ts = result.get("regularMarketTime") or 0
        return pd.DataFrame(
            [
                {
                    "Company": result["symbol"],
                    "Price": result["regularMarketPrice"],
                    "Time": dt.datetime.fromtimestamp(ts),
                }
            ]
        )

    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 429:
            # Hard throttle → fallback
            from .scraper import scrape_quote   # late import to avoid Selenium deps unless needed

            return scrape_quote(ticker)

        raise  # re‑raise other HTTP errors unchanged
