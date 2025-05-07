# stockpeek/cli.py
import argparse, sys
import pandas as pd
from .scraper import scrape_quote

def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Yahoo Finance quotes")
    parser.add_argument("tickers", nargs="+", help="e.g. AAPL MSFT TSLA")
    parser.add_argument("--csv", help="Save to CSV file")

    args = parser.parse_args()
    frames = [scrape_quote(t) for t in args.tickers]
    df = pd.concat(frames, ignore_index=True)

    if args.csv:
        df.to_csv(args.csv, index=False)
        print(f"Saved → {args.csv}")
    else:
        print(df.to_string(index=False))

    return 0

if __name__ == "__main__":
    sys.exit(main())
