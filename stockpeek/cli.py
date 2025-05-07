# stockpeek/cli.py
"""
Command‑line interface for StockPeek.

Examples
--------
# Fast, no‑browser API mode (default)
$ stockpeek AAPL MSFT TSLA

# Force Selenium mode
$ stockpeek GOOGL --mode selenium --csv goog.csv
"""

from __future__ import annotations

import argparse
import sys
import pandas as pd


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="stockpeek",
        description="Fetch live quotes from Yahoo Finance.",
    )
    p.add_argument("tickers", nargs="+", help="e.g. AAPL MSFT TSLA")
    p.add_argument(
        "--mode",
        choices=["api", "selenium"],
        default="api",
        help="api = requests/JSON (fast, no browser) "
             "selenium = headless Chrome scrape (fallback)",
    )
    p.add_argument("--csv", metavar="PATH", help="Save results to CSV file")
    return p.parse_args()


def _resolve_fetch(mode: str):
    if mode == "api":
        from .fetcher import fetch_quote_api as fetch  # lightweight import
    else:  # selenium
        from .scraper import scrape_quote as fetch
    return fetch


def main() -> int:  # return code for sys.exit
    args = _parse_args()
    fetch = _resolve_fetch(args.mode)

    frames = []
    for tkr in args.tickers:
        try:
            frames.append(fetch(tkr))
        except Exception as exc:  # noqa: BLE001  (broad OK for CLI)
            print(f"[WARN] {tkr}: {exc}", file=sys.stderr)

    if not frames:
        print("No quotes retrieved; exiting with error.", file=sys.stderr)
        return 1

    df = pd.concat(frames, ignore_index=True)

    if args.csv:
        df.to_csv(args.csv, index=False)
        print(f"Saved → {args.csv}")
    else:
        print(df.to_string(index=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
