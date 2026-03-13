import pandas as pd

# 1. Load the data
# Because your CSV has a multi-level header (Price Type, then Ticker), 
# we need to tell pandas to read the first two rows as the header.
file_path = "data/etf_data.csv"
print(f"Loading data from {file_path}...\n")

try:
    df = pd.read_csv(file_path, index_col=0, header=[0, 1], parse_dates=True)
except FileNotFoundError:
    print(f"Error: Could not find {file_path}. Please check the path.")
    exit()

# 2. Isolate the Close Prices
# The backtest strategy only requires daily closing prices to calculate returns.
# We slice the MultiIndex to grab only the "Close" columns.
df_close = df["Close"]

# 3. Analyze Missing Values (Before Treatment)
print("--- MISSING VALUES REPORT (BEFORE) ---")
total_rows = len(df_close)
missing_counts = df_close.isnull().sum()

cols_with_missing = missing_counts[missing_counts > 0]

if cols_with_missing.empty:
    print("Great news! No missing values detected in the dataset.")
else:
    for ticker, count in cols_with_missing.items():
        pct_missing = (count / total_rows) * 100
        print(f"{ticker}: {count} missing days ({pct_missing:.2f}%)")

# 4. Treat the Missing Values
print("\n--- TREATING MISSING VALUES ---")
# Forward-fill (ffill) is used to prevent look-ahead bias by carrying the 
# previous day's closing price forward if a day is missing.
df_clean = df_close.ffill()

# 5. Analyze Remaining Missing Values (After ffill)
remaining_missing = df_clean.isnull().sum()
remaining_cols = remaining_missing[remaining_missing > 0]

if not remaining_cols.empty:
    print("\nWarning: Some missing values remain at the very start of the dataset.")
    print("This usually means the ETF incepted after your start date.")
    for ticker, count in remaining_cols.items():
        print(f"  -> {ticker}: {count} leading missing days.")
else:
    print("All missing values successfully treated via forward-fill.")

# 6. Save the Cleaned Data
# We save this single-level DataFrame so the momentum script can read it easily.
output_path = "data/etf_data_clean.csv"
df_clean.to_csv(output_path)
print(f"\nSuccess! Cleaned data saved to: {output_path}")