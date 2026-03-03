import yfinance as yf
import pandas as pd
from datetime import datetime

def download_commodity_data():
    # Dictionary mapping the Name to the yfinance Ticker Symbol
    # We use the generic symbols (e.g., GC=F) to ensure we get data back to 1980
    tickers = {
        "Gold": "GC=F",
        "Crude_Oil": "CL=F",
        "Natural_Gas": "NG=F",
        "Corn": "ZC=F",
        "Wheat": "ZW=F"
    }

    start_date = "1980-01-01"
    end_date = datetime.now().strftime('%Y-%m-%d')

    for name, ticker in tickers.items():
        print(f"Downloading data for {name} ({ticker})...")
        
        # Fetch data
        data = yf.download(ticker, start=start_date, end=end_date)

        if not data.empty:
            # Clean up the multi-index columns if they exist (common in newer yfinance versions)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            # Save to CSV
            filename = f"data/{name}_historical_data.csv"
            data.to_csv(filename)
            print(f"Successfully saved {len(data)} rows to {filename}")
        else:
            print(f"No data found for {ticker} starting from {start_date}")

if __name__ == "__main__":
    # Ensure yfinance is installed: pip install yfinance
    download_commodity_data()