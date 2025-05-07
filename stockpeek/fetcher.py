import pandas as pd, requests, datetime as dt
URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"

def fetch_quote_api(ticker: str) -> pd.DataFrame:
    r = requests.get(URL.format(ticker=ticker), timeout=8)
    r.raise_for_status()
    meta = r.json()["chart"]["result"][0]["meta"]
    return pd.DataFrame([{
        "Company": meta["symbol"],
        "Price":   meta["regularMarketPrice"],
        "Time":    dt.datetime.fromtimestamp(meta["regularMarketTime"])
    }])
