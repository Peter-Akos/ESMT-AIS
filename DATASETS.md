## Available datasets

- **Corn_historical_data.csv**  
  - **Source**: `yfinance` generic futures ticker `ZC=F`  
  - **Content**: Daily historical price data for Corn futures (Open, High, Low, Close, Adj Close, Volume) from 1980-01-01 to latest available date.

- **Crude_Oil_historical_data.csv**  
  - **Source**: `yfinance` generic futures ticker `CL=F`  
  - **Content**: Daily historical price data for Crude Oil futures from 1980-01-01 to latest available date.

- **Gold_historical_data.csv**  
  - **Source**: `yfinance` generic futures ticker `GC=F`  
  - **Content**: Daily historical price data for Gold futures from 1980-01-01 to latest available date.

- **Natural_Gas_historical_data.csv**  
  - **Source**: `yfinance` generic futures ticker `NG=F`  
  - **Content**: Daily historical price data for Natural Gas futures from 1980-01-01 to latest available date.

- **Wheat_historical_data.csv**  
  - **Source**: `yfinance` generic futures ticker `ZW=F`  
  - **Content**: Daily historical price data for Wheat futures from 1980-01-01 to latest available date.

- **global_10y_yields.csv**  
  - **Source**: FRED API via `fredapi`, using long-term government bond yield series.  
  - **Content**: Daily or monthly yields (depending on series frequency) for 10-year government bonds of:  
    - United States (`US_10Y_Yield`)  
    - Germany (`Germany_10Y_Yield`)  
    - Japan (`Japan_10Y_Yield`)  
    - United Kingdom (`UK_10Y_Yield`)  
    - Canada (`Canada_10Y_Yield`)  
    - Australia (`Australia_10Y_Yield`)

- **bis_exchange_rates_1984_present.csv**  
  - **Source**: BIS Web Statistics API (`WS_XRU`) via direct CSV download.  
  - **Content**: Exchange rate observations from 1984-01-01 onward for:  
    - AUD/USD  
    - CAD/USD  
    - EUR/USD  
    - JPY/USD  
    - GBP/USD  
  - Includes BIS fields like `TIME_PERIOD`, `CUR_CURRENCY`, `OBS_VALUE`; a cleaned pivoted version can be built from this.

