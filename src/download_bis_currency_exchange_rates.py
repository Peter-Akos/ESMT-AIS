import pandas as pd

# Base API URL
base = "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_XRU/1.0"
# Time range and format
params = "&startPeriod=1984-01-01&format=csv"

# Constructing the specific URLs for each pair
# Structure: Frequency(D).Area.Currency.Type(A)
urls = [
    f"{base}/D.AU.AUD.A?{params}", # AUD/USD
    f"{base}/D.CA.CAD.A?{params}", # CAD/USD
    f"{base}/D.XM.EUR.A?{params}", # EUR/USD (XM = Euro Area)
    f"{base}/D.JP.JPY.A?{params}", # JPY/USD
    f"{base}/D.GB.GBP.A?{params}"  # GBP/USD
]

# Fetch and concatenate
# We use a simple list comprehension to read each URL into a dataframe
df = pd.concat([pd.read_csv(url) for url in urls])

print(df.head())
df.to_csv("data/bis_exchange_rates_1984_present.csv")

# Optional: Clean up for a nice table
# BIS CSVs provide 'TIME_PERIOD', 'CUR_CURRENCY', and 'OBS_VALUE'
df_clean = df[['TIME_PERIOD', 'CUR_CURRENCY', 'OBS_VALUE']].pivot(
    index='TIME_PERIOD', 
    columns='CUR_CURRENCY', 
    values='OBS_VALUE'
)

print(df_clean.head())