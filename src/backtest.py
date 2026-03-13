import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD DATA & INITIAL SETUP
# ==========================================
file_path = "data/etf_data_clean.csv"
try:
    prices = pd.read_csv(file_path, index_col=0, parse_dates=True)
except FileNotFoundError:
    print(f"Error: Could not find {file_path}. Please run the cleaning script first.")
    exit()

# Parameters
L = 252            # 12-month lookback
skip = 21          # 1-month skip
window = L - skip  # 231 days
tc_bps = 0.0000    # 10 bps transaction cost per side

# Compute Returns
log_rets = np.log(prices / prices.shift(1))
simple_rets = prices.pct_change()

# ==========================================
# 2. SIGNAL CONSTRUCTION
# ==========================================
print("Calculating momentum signals and volatility...")

# Raw momentum: 11-month sum of log returns, shifted by 1 month
raw_mom = log_rets.rolling(window=window).sum().shift(skip)

# 11-month annualized volatility, shifted by 1 month
vol_11m = log_rets.rolling(window=window).std() * np.sqrt(252)
vol_11m = vol_11m.shift(skip)

# Risk-adjusted momentum score
mom_score = raw_mom / vol_11m

# 1-month annualized volatility (for risk parity weighting, NOT shifted)
# We calculate this right on the rebalance day to capture the most current risk regime
vol_1m = log_rets.rolling(window=21).std() * np.sqrt(252)

# ==========================================
# 3. PORTFOLIO CONSTRUCTION & REBALANCING
# ==========================================
print("Executing monthly rebalancing...")

# Find the first trading day of every month to act as our rebalance dates
rebal_dates = prices.groupby(prices.index.to_period('M')).apply(lambda x: x.index[0]).values

# Initialize target weights DataFrame
target_weights = pd.DataFrame(0.0, index=rebal_dates, columns=prices.columns)

# Container to store per-asset per-rebalance diagnostics
records = []

for date in rebal_dates:
    if date not in mom_score.index:
        continue
        
    scores = mom_score.loc[date].dropna()
    vols = vol_1m.loc[date].dropna()
    raw = raw_mom.loc[date].dropna()
    vol_11 = vol_11m.loc[date].dropna()
    
    # Need both score and vol to proceed
    valid_tickers = scores.index.intersection(vols.index)
    if valid_tickers.empty:
        continue
        
    scores = scores[valid_tickers]
    vols = vols[valid_tickers]
    raw = raw[valid_tickers.intersection(raw.index)]
    vol_11 = vol_11[valid_tickers.intersection(vol_11.index)]
    
    # Rank instruments
    ranks = scores.rank(pct=True)
    
    # Define buckets (Top 30%, Bottom 30%)
    longs = ranks[ranks >= 0.70].index
    shorts = ranks[ranks <= 0.30].index
    
    # Inverse volatility weighting
    inv_vol = 1.0 / vols
    
    # Assign and normalize Longs (+1.0)
    if not longs.empty:
        long_w = inv_vol[longs]
        target_weights.loc[date, longs] = long_w / long_w.sum()
        
    # Assign and normalize Shorts (-1.0)
    if not shorts.empty:
        short_w = inv_vol[shorts]
        target_weights.loc[date, shorts] = -(short_w / short_w.sum())

    # Store diagnostics for this rebalance
    for ticker in valid_tickers:
        records.append(
            {
                "date": date,
                "ticker": ticker,
                "raw_mom": raw.get(ticker, np.nan),
                "vol_11m": vol_11.get(ticker, np.nan),
                "mom_score": scores[ticker],
                "rank_pct": ranks[ticker],
                "vol_1m": vols[ticker],
                "weight": target_weights.loc[date, ticker],
            }
        )

# ==========================================
# 4. BACKTEST MECHANICS (VECTORIZED)
# ==========================================
print("Simulating daily portfolio PnL...")

# Align target weights to the daily calendar
# We shift(1) because weights calculated at the close of day T apply to returns on T+1
daily_weights = target_weights.reindex(prices.index).shift(1).ffill().fillna(0)

# Persist weights and diagnostics for external analysis / visualization
weights_output_path_daily = "data/daily_weights.csv"
weights_output_path_rebal = "data/target_weights_monthly.csv"
diagnostics_output_path = "data/rebalance_diagnostics.csv"

daily_weights.to_csv(weights_output_path_daily)
target_weights.to_csv(weights_output_path_rebal)

if records:
    diag_df = pd.DataFrame.from_records(records).set_index(["date", "ticker"]).sort_index()
    diag_df.to_csv(diagnostics_output_path)
    print(f"Saved rebalance diagnostics to {diagnostics_output_path}")

print(f"Saved daily weights to {weights_output_path_daily}")
print(f"Saved rebalance-date weights to {weights_output_path_rebal}")

# Calculate Daily PnL (Gross)
# We multiply yesterday's weights by today's simple returns
port_rets_gross = (daily_weights * simple_rets).sum(axis=1)

# Calculate Transaction Costs
# We estimate turnover as the absolute change in weights on rebalance days
weight_changes = daily_weights.diff().abs().sum(axis=1)
tc_drag = weight_changes * tc_bps

# Deduct TC to get Net Returns
port_rets_net = port_rets_gross - tc_drag

# Build Equity Curve
equity_curve = (1 + port_rets_net).cumprod()

# Track Long/Short Legs separately for hit rates
long_rets = (daily_weights[daily_weights > 0] * simple_rets).sum(axis=1)
short_rets = (daily_weights[daily_weights < 0] * simple_rets).sum(axis=1)

# ==========================================
# 5. KEY METRICS COMPUTATION
# ==========================================
print("\n--- BACKTEST RESULTS ---")

# Setup for metrics
total_days = len(equity_curve)
years = total_days / 252
cum_ret = equity_curve.iloc[-1] - 1

ann_ret = (1 + cum_ret) ** (1 / years) - 1
ann_vol = port_rets_net.std() * np.sqrt(252)
sharpe = ann_ret / ann_vol if ann_vol != 0 else 0

# Drawdown Calculation
cum_max = equity_curve.cummax()
drawdowns = (equity_curve - cum_max) / cum_max
max_dd = drawdowns.min()
calmar = ann_ret / abs(max_dd) if max_dd != 0 else 0

# Hit Rates (Monthly)
monthly_rets = port_rets_net.resample("ME").apply(lambda x: (1 + x).prod() - 1)
monthly_long_rets = long_rets.resample("ME").apply(lambda x: (1 + x).prod() - 1)
monthly_short_rets = short_rets.resample("ME").apply(lambda x: (1 + x).prod() - 1)

hit_rate_total = (monthly_rets > 0).mean()
hit_rate_long = (monthly_long_rets > 0).mean()
hit_rate_short = (monthly_short_rets > 0).mean()

avg_turnover_per_rebalance = weight_changes[weight_changes > 0].mean()

print(f"Cumulative Return:   {cum_ret * 100:.2f}%")
print(f"Annualized Return:   {ann_ret * 100:.2f}%")
print(f"Annualized Vol:      {ann_vol * 100:.2f}%")
print(f"Sharpe Ratio:        {sharpe:.2f}")
print(f"Max Drawdown:        {max_dd * 100:.2f}%")
print(f"Calmar Ratio:        {calmar:.2f}")
print(f"Avg Turnover/Rebal:  {avg_turnover_per_rebalance * 100:.2f}%")
print(f"Total TC Drag:       {tc_drag.sum() * 100:.2f}%")
print(f"Win Rate (Overall):  {hit_rate_total * 100:.1f}% of months")
print(f"Win Rate (Longs):    {hit_rate_long * 100:.1f}% of months")
print(f"Win Rate (Shorts):   {hit_rate_short * 100:.1f}% of months")

# ==========================================
# 6. PLOTTING
# ==========================================
plt.figure(figsize=(14, 6))
plt.plot(equity_curve, label='L/S Momentum Strategy (Net of Fees)', color='blue')
plt.title('Global ETF Momentum Strategy - Equity Curve', fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Cumulative Portfolio Value ($1 Growth)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.fill_between(drawdowns.index, drawdowns, 0, color='red', alpha=0.3, label='Drawdown')
plt.legend()
plt.tight_layout()
plt.show()