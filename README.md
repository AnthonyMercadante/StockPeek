# StockPeek 📈  
A **one‑file‑install** tool to fetch live quotes from Yahoo Finance — either by
hitting Yahoo’s JSON API (fast, no browser) or, when you’re being rate‑limited,
by spinning up headless Chrome through Selenium. It works as **both** a Python
library *and* a command‑line program.

---

## Why did I build this?
* **Real‑world utility** – quick look‑ups in a shell, notebooks, or scripts.
* **Interview‑ready sample** – shows packaging, CLI design, API calls,
  Selenium automation, retry logic, and graceful fall‑backs.
* **Zero setup pain** – `pip install stockpeek` is all you need; chromedriver
  is auto‑managed.

---

## Installation

```bash
# 1) Inside a virtual‑env (recommended)
python -m pip install --upgrade pip

# 2) Grab the latest commit directly from GitHub
pip install git+https://github.com/AnthonyMercadante/stockpeek.git
````

> **Dependencies**: `pandas`, `requests`, `selenium`, `webdriver‑manager`.
> They’re pulled in automatically by the install.

---

## Quick start (CLI)

```bash
# Fetch AAPL & MSFT with the default fast JSON API
$ stockpeek AAPL MSFT
 Company   Price                Time
   AAPL   184.30  2025‑05‑06 22:19:02
   MSFT   407.94  2025‑05‑06 22:19:02

# Force Selenium mode (browser render) and save to CSV
$ stockpeek TSLA --mode selenium --csv tesla.csv
Saved → tesla.csv
```

*(If the executable isn’t on your `PATH`, call it via
`.venv\Scripts\stockpeek.exe` on Windows or `python -m stockpeek …`.)*

---

## Quick start (Python)

```python
>>> from stockpeek import fetch_quote_api        # fast mode
>>> fetch_quote_api("NVDA")
  Company   Price                Time
0    NVDA  893.52 2025‑05‑06 22:20:11

>>> from stockpeek import scrape_quote          # Selenium fallback
>>> scrape_quote("NVDA")
  Company   Price
0  NVIDIA  893.55
```

---

## How it works

| Mode              | Backend                                            | When used                                                    |
| ----------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| **api** (default) | `requests` → `v7/finance/quote` JSON               | Fast, no browser; retries with back‑off                      |
| **selenium**      | Headless Chrome via Selenium‑4 + webdriver‑manager | When you pass `--mode selenium` *or* the API hits a hard 429 |

The `fetch_quote_api()` helper transparently falls back to Selenium if Yahoo
keeps returning *HTTP 429 Too Many Requests* after six exponential retries.

---

## Troubleshooting

| Issue                            | Fix                                                                 |
| -------------------------------- | ------------------------------------------------------------------- |
| `ModuleNotFoundError: stockpeek` | Re‑run `pip install -e .` and activate your venv                    |
| `HTTPError 429` (API)            | Wait a few seconds **or** let the auto Selenium fallback do its job |
| `selenium: handshake failed`     | Update Chrome & chromedriver, or use API mode                       |
| `stockpeek not recognized`       | Call the full path: `.\venv\Scripts\stockpeek.exe …`                |

---

## Contributing

Pull requests are welcome for:

* Non‑US exchanges support
* Price caching layer / batching
* Proper unit tests for the CLI

Run `pre‑commit run --all-files` before opening a PR.

---

## License

MIT © 2025 Anthony Mercadante

```
```
