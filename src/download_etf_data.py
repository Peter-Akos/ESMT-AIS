import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path


START_DATE = "2013-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")
DATA_DIR = Path("data")


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _download_and_save(ticker: str, label: str) -> None:
    print(f"Downloading data for {label} ({ticker})...")

    data = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=False)

    if data.empty:
        print(f"  -> No data returned for {ticker} from {START_DATE}.")
        return

    # Newer yfinance versions sometimes return a MultiIndex on columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    filename = DATA_DIR / f"{label}_etf_data.csv"
    data.to_csv(filename)
    print(f"  -> Saved {len(data)} rows to {filename}")


def download_commodity_etfs() -> None:
    """US-listed commodity ETFs (priced in USD)."""
    tickers = {
        "USO": "USO",   # United States Oil Fund
        "UNG": "UNG",   # United States Natural Gas Fund
        "GLD": "GLD",   # SPDR Gold Shares
        "CORN": "CORN", # Teucrium Corn Fund
        "WEAT": "WEAT", # Teucrium Wheat Fund
    }

    for label, ticker in tickers.items():
        _download_and_save(ticker, label)


def download_10y_govt_bond_etfs() -> None:
    """10-year government bond proxies via ETFs."""
    tickers = {
        "IEF": "IEF",       # US 7-10Y Treasuries, USD
        "IS04_DE": "IS04.DE",  # Germany 5.5-10.5Y, EUR (XETRA)
        "IGLT_L": "IGLT.L", # UK Gilts, GBP (LSE)
        "XGB_TO": "XGB.TO", # Canada Gov Bonds, CAD (TSX)
        "XJSE_DE": "XJSE.DE", # Japan Gov Bonds, EUR (XETRA)
        "IGB_AX": "IGB.AX", # Australia Treasuries, AUD (ASX)
    }

    for label, ticker in tickers.items():
        _download_and_save(ticker, label)


def download_fx_etfs() -> None:
    """Currency ETF proxies for major FX pairs (optional)."""
    tickers = {
        "FXE": "FXE",  # EUR/USD
        "FXY": "FXY",  # JPY/USD
        "FXB": "FXB",  # GBP/USD
        "FXA": "FXA",  # AUD/USD
        "FXC": "FXC",  # CAD/USD
    }

    for label, ticker in tickers.items():
        _download_and_save(ticker, label)


def download_all_etf_data() -> None:
    """Download all required ETF datasets for 2013-present."""
    _ensure_data_dir()
    print(f"Downloading ETF data from {START_DATE} to {END_DATE}...")

    print("\n== Commodity ETFs ==")
    download_commodity_etfs()

    print("\n== 10Y Government Bond ETFs ==")
    download_10y_govt_bond_etfs()

    print("\n== FX ETFs (optional) ==")
    download_fx_etfs()


if __name__ == "__main__":
    download_all_etf_data()

