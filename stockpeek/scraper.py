# stockpeek/scraper.py
"""
Selenium‑based fallback scraper for Yahoo Finance.
Use only when the lighter requests‑based API is unavailable.

Requires:
    selenium>=4.20
    webdriver‑manager>=4.0
"""

from __future__ import annotations

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

YAHOO_QUOTE_URL = "https://ca.finance.yahoo.com/quote/{ticker}"


def _make_driver() -> webdriver.Chrome:
    """Create a headless Chrome driver that ignores TLS errors."""
    opts = Options()
    opts.add_argument("--headless=new")              # run invisibly
    opts.add_argument("--ignore-certificate-errors") # suppress local TLS issues
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def scrape_quote(ticker: str) -> pd.DataFrame:
    """
    Fetch the live price for *ticker* by rendering the Yahoo Finance page.

    Returns
    -------
    pandas.DataFrame
        One row with columns ``Company`` and ``Price``.
    """
    driver = _make_driver()
    driver.get(YAHOO_QUOTE_URL.format(ticker=ticker))

    wait = WebDriverWait(driver, 10)

    # Wait for company name <h1>
    name_el = wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
    # Wait for the price <fin-streamer> matching this ticker
    price_xpath = (
        f"//fin-streamer[@data-field='regularMarketPrice' "
        f"and @data-symbol='{ticker.upper()}']"
    )
    price_el = wait.until(EC.presence_of_element_located((By.XPATH, price_xpath)))

    # Extract text/attribute values
    company = name_el.text.split(" (")[0]
    price_str = price_el.get_attribute("value") or price_el.text

    driver.quit()

    if not price_str:
        raise RuntimeError(
            f"Yahoo returned empty price for {ticker!r}. "
            "The page layout may have changed."
        )

    return pd.DataFrame(
        [
            {
                "Company": company,
                "Price": float(price_str.replace(",", "")),
            }
        ]
    )
