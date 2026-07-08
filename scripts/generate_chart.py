"""
generate_chart.py

Reads the logged gold and BTC price history and renders a dashboard PNG
(dual-axis chart) to /assets/dashboard.png. This gets committed alongside
the data so the README always shows an up-to-date chart.
"""

import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
GOLD_CSV = DATA_DIR / "gold_prices.csv"
BTC_CSV = DATA_DIR / "btc_prices.csv"
OUTPUT_PNG = ASSETS_DIR / "dashboard.png"


def load_series(csv_path: Path):
    timestamps, prices = [], []
    if not csv_path.exists():
        return timestamps, prices
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(datetime.strptime(row["timestamp_utc"], "%Y-%m-%d %H:%M:%S"))
            prices.append(float(row["price_usd"]))
    return timestamps, prices


def main():
    ASSETS_DIR.mkdir(exist_ok=True)

    gold_t, gold_p = load_series(GOLD_CSV)
    btc_t, btc_p = load_series(BTC_CSV)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0d1117")
    ax1.set_facecolor("#0d1117")

    color_gold = "#d4af37"
    color_btc = "#f7931a"

    if gold_t:
        ax1.plot(gold_t, gold_p, color=color_gold, linewidth=2, label="Gold (XAU/USD)")
    ax1.set_ylabel("Gold price (USD)", color=color_gold)
    ax1.tick_params(axis="y", labelcolor=color_gold)
    ax1.tick_params(axis="x", colors="white")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))

    ax2 = ax1.twinx()
    if btc_t:
        ax2.plot(btc_t, btc_p, color=color_btc, linewidth=2, label="Bitcoin (BTC/USD)")
    ax2.set_ylabel("BTC price (USD)", color=color_btc)
    ax2.tick_params(axis="y", labelcolor=color_btc)

    for spine in ax1.spines.values():
        spine.set_color("#30363d")
    for spine in ax2.spines.values():
        spine.set_color("#30363d")

    ax1.set_title("Gold & Bitcoin — Live Price Dashboard", color="white", fontsize=14, pad=15)
    fig.autofmt_xdate()

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", facecolor="#161b22", labelcolor="white")

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150, facecolor=fig.get_facecolor())
    print(f"Saved chart to {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
