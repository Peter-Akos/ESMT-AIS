# Global ETF Momentum Strategy Definition

## 1. Strategy Overview

The goal is to backtest a **cross-asset, long–short momentum strategy** implemented exclusively via US-listed, USD-denominated ETFs (commodities, government bond ETFs, and currency trusts). The strategy:

- **Rebalances monthly** on the first NYSE business day of each month.
- **Ranks instruments by Risk-Adjusted Momentum** over a **12‑month lookback window**, skipping the most recent 1 month to avoid short‑term mean reversion.
- **Goes long the strongest (top 30% ranked) instruments** and **short the weakest (bottom 30% ranked) instruments**, subject to liquidity and risk constraints.
- Uses **inverse-volatility weighting** to ensure highly volatile assets (like commodities) do not dominate the risk profile of the portfolio.

---

## 2. Data and Transformations

### 2.1 Raw Inputs

For each US-listed ETF we have:

- Date (trading day)
- Open, High, Low, Close
- Adj Close (used for returns)
- Volume

The **primary price input for the strategy** is the **daily Adj Close** of each ETF from **2013-01-01 to 2026-03-10**.

### 2.2 Calendar and Missing Data Handling

1. **Master calendar**: construct a master **NYSE business-day calendar** over the backtest window.
2. **Align all ETF series** to this calendar using standard pandas methods. Because all assets are US-listed, trading days will natively align, requiring minimal forward-filling.
3. **Liquidity filter**:
  - Compute rolling average dollar volume over a chosen window (e.g. 20 days).
  - Optionally exclude instruments from trading when liquidity falls below a threshold.

### 2.3 Return Computation

For each instrument i:

1. Compute **daily log returns** from Adj Close:
   r(i,t) = ln( P(i,t) / P(i,t-1) )
   
2. Optionally also compute **simple returns** for reporting:
   R(i,t) = ( P(i,t) / P(i,t-1) ) - 1
   
3. Handle missing prices by ensuring no return is computed when either P(i,t) or P(i,t-1) is missing.

### 2.4 Momentum Signal Construction

For each monthly rebalancing date T:

1. Let L = 252 trading days (12 months) and skip = 21 trading days (1 month). The lookback window is [T-L, T-skip].
2. Calculate the **raw momentum** as the sum of log returns over that window:
   raw_mom(i,T) = sum( r(i,t) )
3. Calculate the **annualized volatility** of log returns over that exact same window:
   vol_11m(i,T) = stdev( r(i,t) ) * sqrt(252)
4. Define the final **risk-adjusted momentum score** to rank all assets fairly:
   mom_score(i,T) = raw_mom(i,T) / vol_11m(i,T)

---

## 3. Portfolio Construction and Rebalancing

### 3.1 Rebalancing Schedule

The strategy **rebalances monthly** on the **first NYSE business day** of each month.

### 3.2 Ranking and Selection

On each rebalancing date:

1. **Filter tradable universe**: Exclude instruments failing liquidity criteria or lacking sufficient lookback history.
2. **Rank instruments**: Sort descending by the risk-adjusted mom_score(i,T).
3. **Define long and short buckets**:
  - **Top 30%** of instruments go **long**.
  - **Bottom 30%** of instruments go **short**.
  - The middle 40% are not traded.

### 3.3 Inverse Volatility Weighting Scheme

Weights are volatility-adjusted to equalize risk contribution:

1. Estimate each instrument’s **30‑day rolling annualized volatility**, vol_1m(i,T), at each rebalance.
2. For instruments in the **long bucket**, allocate weights inversely proportional to recent volatility:
   w_long(i,T) = 1 / vol_1m(i,T)
   Normalize these weights so the long book sums to +1.0.
3. For instruments in the **short bucket**:
   w_short(i,T) = 1 / vol_1m(i,T)
   Normalize these weights so they sum to 1.0, then multiply by -1.0 so the short book sums to -1.0.

### 3.4 Transaction Costs and Constraints

For more realistic backtests:

- Apply **bid–ask spread and commission assumptions** per trade (e.g. bps per turnover).
- Limit **maximum weight per instrument** and **per asset class**.
- Optionally cap **portfolio-level leverage**.

---

## 4. Backtest Mechanics and Outputs

### 4.1 Position and PnL Computation

Between rebalancing dates:

1. **Hold weights fixed** in terms of capital allocation (or shares), adjusting only for price changes.
2. Daily portfolio return is the sum of the weighted daily simple returns of the selected assets.
3. Deduct **transaction costs** on rebalancing days based on changes in weights.
4. Accumulate daily returns into a **portfolio equity curve**.

### 4.2 Key Metrics

For each parameter configuration, the backtest should output:

- Cumulative return and **equity curve** over time.
- Annualized return, volatility, and **Sharpe ratio**.
- **Max drawdown** and Calmar ratio.
- Long and short **hit rates** (fraction of periods with positive returns).
- Turnover and transaction cost drag.