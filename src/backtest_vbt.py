import pandas as pd
import numpy as np
import vectorbt as vbt
import bt

# ==========================================
# 1. LOAD DATA & INITIAL SETUP
# ==========================================
file_path = "data/etf_data_clean.csv"
try:
    prices = pd.read_csv(file_path, index_col=0, parse_dates=True)
except FileNotFoundError:
    print(f"Error: Could not find {file_path}.")
    exit()

# Parameters based on strategy definition
L = 252            # 12-month lookback 
skip = 21          # 1-month skip 
window = L - skip  # 231 days
tc_bps = 0.0010    # 10 bps transaction cost 

# ==========================================
# 2. SIGNAL CONSTRUCTION
# ==========================================
print("Calculating risk-adjusted momentum signals...")

log_rets = np.log(prices / prices.shift(1))

# Raw momentum: 11-month sum of log returns, shifted by 1 month 
raw_mom = log_rets.rolling(window=window).sum().shift(skip)

# 11-month annualized volatility, shifted by 1 month 
vol_11m = log_rets.rolling(window=window).std() * np.sqrt(252)
vol_11m = vol_11m.shift(skip)

# Risk-adjusted momentum score 
mom_score = raw_mom / vol_11m

# 1-month annualized volatility (for risk parity weighting) 
vol_1m = log_rets.rolling(window=21).std() * np.sqrt(252)

# ==========================================
# 3. PORTFOLIO CONSTRUCTION
# ==========================================
print("Generating target weights...")

# Find the first trading day of every month
rebal_dates = prices.groupby([prices.index.year, prices.index.month]).apply(lambda x: x.index[0]).values
rebal_dates = pd.DatetimeIndex(rebal_dates)

# Initialize a sparse DataFrame for weights (filled with NaNs)
target_weights = pd.DataFrame(np.nan, index=prices.index, columns=prices.columns)

for date in rebal_dates:
    if date not in mom_score.index:
        continue
        
    scores = mom_score.loc[date].dropna()
    vols = vol_1m.loc[date].dropna()
    
    valid_tickers = scores.index.intersection(vols.index)
    
    # If not enough data (e.g., year 1), stay in cash
    if valid_tickers.empty:
        target_weights.loc[date] = 0.0
        continue
        
    scores = scores[valid_tickers]
    vols = vols[valid_tickers]
    
    ranks = scores.rank(pct=True)
    
    longs = ranks[ranks >= 0.70].index
    shorts = ranks[ranks <= 0.30].index
    
    inv_vol = 1.0 / vols
    
    # Initialize all to 0.0. This ensures assets dropping out of the top/bottom 30% are sold.
    date_weights = pd.Series(0.0, index=prices.columns)
    
    # Assign and normalize Longs (+1.0)
    if not longs.empty:
        lw = inv_vol[longs]
        date_weights[longs] = lw / lw.sum()
        
    # Assign and normalize Shorts (-1.0)
    if not shorts.empty:
        sw = inv_vol[shorts]
        date_weights[shorts] = -(sw / sw.sum())
        
    target_weights.loc[date] = date_weights

clean_weights = target_weights.fillna(0)

# 2. DEFINE THE BT STRATEGY
# We chain together pre-implemented logical blocks
momentum_strategy = bt.Strategy('Global_Macro_L_S', [
    bt.algos.RunMonthly(),                # Trigger on the first day of the month
    bt.algos.SelectAll(),                 # Keep all assets available
    bt.algos.WeighTarget(clean_weights),  # Look up our custom weights for this date
    bt.algos.Rebalance()                  # Execute the trades to hit the targets
])

# 3. CONFIGURE THE BACKTEST ENGINE
# We pass the prices and set the 10 bps transaction cost you defined
def fee_model(quantity, price):
    # 10 bps (0.0010) fee applied to the total trade value
    return abs(quantity) * price * 0.0010

backtest = bt.Backtest(
    momentum_strategy, 
    prices, 
    commissions=fee_model
)

# 4. RUN AND EVALUATE
print("Running bt backtest engine...")
results = bt.run(backtest)

# Display institutional-grade metrics
results.display()

# Plot the equity curve
results.plot()