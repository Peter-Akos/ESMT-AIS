# ETF Backtesting Data Requirements (2013–Present)

## 1. Overview
This document outlines the required data fields, sources, and exact tickers needed to backtest a global macro strategy using ETFs instead of direct futures, bonds, or spot FX. The backtest window begins on **January 1, 2013**.

## 2. Where to Find the Data
For daily ETF data, you do not need expensive institutional data feeds. The following sources are reliable for the 2013-present timeframe:

* **Primary Free Source:** `yfinance` (Yahoo Finance API). It provides global market coverage and handles international ticker suffixes (e.g., `.DE`, `.TO`).
* **Alternative Free/Freemium Sources:** Tiingo (excellent for US ETFs), Alpha Vantage, or MarketData.app. 
* **Institutional/Paid Alternatives:** Interactive Brokers API, FirstRate Data, or Norgate Data (highly recommended for survivorship-bias-free ETF data, though less critical since none of these specific major ETFs have been delisted since 2013).

## 3. Data Fields Required
For every ETF, you must download the following daily fields:
* `Date`: The trading day.
* `Open`, `High`, `Low`, `Close`: Standard price action.
* `Volume`: Critical for checking liquidity and simulating slippage.
* **`Adj Close` (Crucial):** You *must* use the Adjusted Close for calculating your strategy's returns. ETFs pay out dividends, interest (especially the bond ETFs), and capital gains. The `Adj Close` factors these in, preventing fake "price drops" on ex-dividend dates from ruining your backtest.

---

## 4. Required ETF Tickers by Category

### Commodities
These are all US-listed and trade in USD. 

| Asset | Ticker | Exchange | Fund Name |
| :--- | :--- | :--- | :--- |
| Crude Oil | `USO` | NYSE Arca | United States Oil Fund |
| Natural Gas | `UNG` | NYSE Arca | United States Natural Gas Fund |
| Gold | `GLD` | NYSE Arca | SPDR Gold Shares |
| Corn | `CORN` | NYSE Arca | Teucrium Corn Fund |
| Wheat | `WEAT` | NYSE Arca | Teucrium Wheat Fund |

### 10-Year Government Bonds
*Warning: Because these trade on different global exchanges, their trading holidays and market hours will not align perfectly. You will need to forward-fill (`ffill`) missing data when aligning them to a single master calendar.*

| Country | Yahoo Ticker | Exchange | Denomination | Fund Name |
| :--- | :--- | :--- | :--- | :--- |
| United States | `IEF` | NASDAQ | USD | iShares 7-10 Year Treasury Bond ETF |
| Germany | `IS04.DE` | XETRA | EUR | iShares eb.rexx Govt Germany 5.5-10.5yr |
| United Kingdom | `IGLT.L` | LSE | GBP | iShares Core UK Gilts UCITS ETF |
| Canada | `XGB.TO` | TSX | CAD | iShares Core Canadian Gov Bond ETF |
| Japan | `XJSE.DE` | XETRA | EUR | Xtrackers II Japan Government Bond ETF |
| Australia | `IGB.AX` | ASX | AUD | iShares Treasury ETF |

### Currency Equivalents (Optional)
If your strategy executes FX trades via ETFs rather than spot FX, use these US-listed trusts (all trade in USD on NYSE Arca).

| Pair | Ticker | Fund Name |
| :--- | :--- | :--- |
| EUR/USD | `FXE` | Invesco CurrencyShares Euro Trust |
| JPY/USD | `FXY` | Invesco CurrencyShares Japanese Yen Trust |
| GBP/USD | `FXB` | Invesco CurrencyShares British Pound Sterling Trust |
| AUD/USD | `FXA` | Invesco CurrencyShares Australian Dollar Trust |
| CAD/USD | `FXC` | Invesco CurrencyShares Canadian Dollar Trust |

---

## 5. Important Data Processing Notes for Backtesting
1.  **Currency Alignment:** The international bond ETFs are priced in their local currencies (or EUR, in the case of the Japan proxy on Xetra). You will need to use your existing BIS exchange rate data to convert their daily `Adj Close` values back into your base currency (e.g., USD) to calculate true portfolio returns.
2.  **Calendar Synchronization:** Create a master trading calendar (usually the NYSE calendar) and align all international data to it. If the ASX (Australia) was open but the NYSE was closed, you generally drop that day or roll it forward depending on your execution logic.