# stockpeek/scraper.py
from __future__ import annotations
from typing import List
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

YAHOO_QUOTE_URL = "https://ca.finance.yahoo.com/quote/{ticker}"

def scrape_quote(ticker: str) -> pd.DataFrame:
    """Return a 1‑row DataFrame with company name & last price."""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(YAHOO_QUOTE_URL.format(ticker=ticker))

    time.sleep(1)                      # simple wait
    name = driver.find_element(By.XPATH, "//h1").text.split(" (")[0]
    price = driver.find_element(By.XPATH, "//fin-streamer[@data-field='regularMarketPrice']").text
    driver.quit()

    return pd.DataFrame([{"Company": name, "Price": float(price.replace(',', ''))}])
