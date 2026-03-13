import pandas as pd
import matplotlib.pyplot as plt
import math

# 1. Load the cleaned data
file_path = "data/etf_data_clean.csv"
print(f"Loading clean data from {file_path}...")

try:
    df_clean = pd.read_csv(file_path, index_col=0, parse_dates=True)
except FileNotFoundError:
    print(f"Error: Could not find {file_path}. Please run the cleaning script first.")
    exit()

# 2. Determine the grid layout
num_etfs = len(df_clean.columns)
cols = 3  # 3 charts per row is usually a good balance for readability
rows = math.ceil(num_etfs / cols)

# 3. Create the figure and subplots
# We dynamically size the figure based on how many rows we need
fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(16, 3 * rows))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# 4. Loop through each ETF and plot it
print(f"Plotting {num_etfs} instruments...")
for i, ticker in enumerate(df_clean.columns):
    ax = axes[i]
    # Plot the series
    df_clean[ticker].plot(ax=ax, color='tab:blue')
    
    # Formatting
    ax.set_title(f"{ticker} - Closing Price", fontweight='bold')
    ax.set_xlabel("") # Remove the 'Date' label to save space
    ax.set_ylabel("Price (USD)")
    ax.grid(True, linestyle='--', alpha=0.6)

# 5. Clean up empty subplots
# If your number of ETFs isn't perfectly divisible by 3, 
# this removes the blank charts at the bottom right.
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# 6. Adjust layout and display
plt.tight_layout()
plt.show()