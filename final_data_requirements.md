# Final ETF Backtesting Data Requirements (2013–Present)

## 1. Overview
This document outlines the required data fields, sources, and exact tickers needed to backtest a global macro strategy exclusively using US-listed, USD-denominated ETFs. The data window begins on **January 1, 2013**. 

By strictly using US-listed ETFs, this universe naturally aligns to the NYSE business-day calendar, eliminating time-zone mismatch and the need for spot currency conversions.

## 2. Where to Find the Data
The following sources are reliable for the 2013-present timeframe:

* **Primary Free Source:** `yfinance` (Yahoo Finance API). 
* **Alternative Sources:** Tiingo, Alpha Vantage, MarketData.app, or Interactive Brokers API.

## 3. Data Fields Required
For every ETF, you must download the following daily fields:
* **Date**: The trading day.
* **Open, High, Low, Close**: Standard price action.
* **Volume**: Critical for checking liquidity and simulating slippage.
* **Adj Close (Crucial)**: You must use the Adjusted Close for calculating your strategy's returns. ETFs pay out dividends and interest; the Adj Close factors these in, preventing fake price drops on ex-dividend dates from ruining the backtest.

---

## 4. The Expanded Strategy Universe

### Commodities
*Expanded to include precious metals, industrial metals, and broad agriculture to provide more diverse momentum signals.*

| Asset | Ticker | Exchange | Fund Name |
| :--- | :--- | :--- | :--- |
| Crude Oil | `USO` | NYSE Arca | United States Oil Fund |
| Natural Gas | `UNG` | NYSE Arca | United States Natural Gas Fund |
| Gold | `GLD` | NYSE Arca | SPDR Gold Shares |
| Silver | `SLV` | NYSE Arca | iShares Silver Trust |
| Copper | `CPER` | NYSE Arca | United States Copper Index Fund |
| Broad Agriculture | `DBA` | NYSE Arca | Invesco DB Agriculture Fund |
| Corn | `CORN` | NYSE Arca | Teucrium Corn Fund |
| Wheat | `WEAT` | NYSE Arca | Teucrium Wheat Fund |

### Fixed Income (Government & Corporate)
*Replaced foreign-listed bonds with US-listed global equivalents. Added duration and credit-risk variations to capture different interest rate cycles.*

| Category | Ticker | Exchange | Fund Name |
| :--- | :--- | :--- | :--- |
| US 7-10 Year Treasury | `IEF` | NASDAQ | iShares 7-10 Year Treasury Bond ETF |
| US 20+ Year Treasury | `TLT` | NASDAQ | iShares 20+ Year Treasury Bond ETF |
| US 1-3 Year Treasury | `SHY` | NASDAQ | iShares 1-3 Year Treasury Bond ETF |
| US Investment Grade | `LQD` | NYSE Arca | iShares iBoxx $ Inv Grade Corporate Bond ETF |
| US High Yield | `HYG` | NYSE Arca | iShares iBoxx $ High Yield Corporate Bond ETF |
| Intl Treasury (Dev Markets) | `BWX` | NYSE Arca | SPDR Bloomberg International Treasury Bond ETF |
| Emerging Market Bonds | `EMB` | NASDAQ | iShares J.P. Morgan USD Emerging Markets Bond ETF |

### Currency Equivalents
*Added the Swiss Franc as a traditional safe-haven currency proxy.*

| Pair | Ticker | Fund Name |
| :--- | :--- | :--- |
| EUR/USD | `FXE` | Invesco CurrencyShares Euro Trust |
| JPY/USD | `FXY` | Invesco CurrencyShares Japanese Yen Trust |
| GBP/USD | `FXB` | Invesco CurrencyShares British Pound Sterling Trust |
| AUD/USD | `FXA` | Invesco CurrencyShares Australian Dollar Trust |
| CAD/USD | `FXC` | Invesco CurrencyShares Canadian Dollar Trust |
| CHF/USD | `FXF` | Invesco CurrencyShares Swiss Franc Trust |

---

## 5. Important Data Processing Notes for Backtesting
1. **Unified Calendar:** Because all 21 ETFs trade on major US exchanges, simply align the daily data to the standard NYSE trading calendar. 
2. **First Year Warm-up:** The backtest data begins on January 1, 2013. Because the strategy requires a 12-month lookback window, the first actual portfolio weights and trades will not be generated until January 2014.
