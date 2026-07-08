"""
fetch_prices.py

Fetches the latest gold (XAU/USD) and Bitcoin (BTC/USD) prices and appends
them to their respective CSV logs in /data. Designed to be run on a schedule
by GitHub Actions, but works fine run manually too.

Data sources:
- Gold: Alpha Vantage CURRENCY_EXCHANGE_RATE endpoint (requires free API key)
- Bitcoin: CoinGecko public API (no key required)
"""

import os
import csv
import requests
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
GOLD_CSV = DATA_DIR / "gold_prices.csv"
BTC_CSV = DATA_DIR / "btc_prices.csv"

ALPHAVANTAGE_KEY = os.environ["ALPHAVANTAGE_KEY"]


def fetch_gold_price() -> float:
    resp = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": "XAU",
            "to_currency": "USD",
            "apikey": ALPHAVANTAGE_KEY,
        },
        timeout=15,
    )
    resp.raise_for_status()
    payload = resp.json()["Realtime Currency Exchange Rate"]
    return float(payload["5. Exchange Rate"])


def fetch_btc_price() -> float:
    resp = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "bitcoin", "vs_currencies": "usd"},
        timeout=15,
    )
    resp.raise_for_status()
    return float(resp.json()["bitcoin"]["usd"])


def append_row(csv_path: Path, price: float) -> None:
    is_new_file = not csv_path.exists()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(["timestamp_utc", "price_usd"])
        writer.writerow([timestamp, f"{price:.2f}"])

    print(f"Logged {csv_path.name}: {timestamp} -> ${price:.2f}")


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    try:
        gold_price = fetch_gold_price()
        append_row(GOLD_CSV, gold_price)
    except Exception as e:
        print(f"Failed to fetch gold price: {e}")

    try:
        btc_price = fetch_btc_price()
        append_row(BTC_CSV, btc_price)
    except Exception as e:
        print(f"Failed to fetch BTC price: {e}")


if __name__ == "__main__":
    main()
