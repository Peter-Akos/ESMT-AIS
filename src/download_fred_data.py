import pandas as pd
from fredapi import Fred

# 1. Initialize with your API key
API_KEY = '67c03036b54b98aaae13cbfb05297032'
fred = Fred(api_key=API_KEY)

# 2. Define the Series IDs and their human-readable labels
series_dict = {
    'IRLTLT01USM156N': 'US_10Y_Yield',
    'IRLTLT01DEM156N': 'Germany_10Y_Yield',
    'IRLTLT01JPM156N': 'Japan_10Y_Yield',
    'IRLTLT01GBM156N': 'UK_10Y_Yield',
    'IRLTLT01CAM156N': 'Canada_10Y_Yield',
    'IRLTLT01AUM156N': 'Australia_10Y_Yield'
}

def download_fred_data(series_map):
    data_frames = []
    
    print("Starting data download...")
    
    for series_id, name in series_map.items():
        try:
            # Fetch series and name it
            series_data = fred.get_series(series_id)
            df = series_data.to_frame(name=name)
            data_frames.append(df)
            print(f"Successfully retrieved: {name}")
        except Exception as e:
            print(f"Error retrieving {series_id}: {e}")

    # 3. Merge all dataframes on the Date index
    if data_frames:
        final_df = pd.concat(data_frames, axis=1)
        
        # 4. Save to CSV
        filename = "data/global_10y_yields.csv"
        final_df.to_csv(filename)
        print(f"\nSuccess! Data saved to {filename}")
        return final_df
    else:
        print("No data was collected.")
        return None

if __name__ == "__main__":
    df = download_fred_data(series_dict)
    # Display the last few rows of the data
    if df is not None:
        print("\nPreview of recent data:")
        print(df.tail())