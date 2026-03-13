import yfinance as yf
import pandas as pd

# Define the 21 tickers from our final expanded universe
tickers = [
    # Commodities
    "USO", "UNG", "GLD", "SLV", "CPER", "DBA", "CORN", "WEAT",
    # Fixed Income
    "IEF", "TLT", "SHY", "LQD", "HYG", "BWX", "EMB",
    # Currencies
    "FXE", "FXY", "FXB", "FXA", "FXC", "FXF"
]

# Set the exact start date defined in the requirements
start_date = "2013-01-01"

print(f"Downloading daily 'Adj Close' for {len(tickers)} ETFs...")

# yf.download returns a multi-index DataFrame when pulling multiple tickers.
# We isolate just the "Adj Close" column right away to keep things clean.
# yfinance will automatically align everything to standard US market days.
raw_data = yf.download(tickers, start=start_date)

raw_data.to_csv("data/etf_data.csv")
