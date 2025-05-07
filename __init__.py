"""
StockPeek – minimal Yahoo‑Finance scraper.

>>> from stockpeek import scrape_quote
>>> scrape_quote("AAPL")
      Company   Price
0       Apple  184.11
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:      # running from source tree
    __version__ = "0.0.0-dev"

from .scraper import scrape_quote   # re‑export for convenience

__all__ = ["scrape_quote", "__version__"]
