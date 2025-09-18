import pandas as pd
import os

# folder where all your CSV files are stored
folder_path = r"C:\Pavithra\Data driven stock analysis project 2\split_tickers"

performance = []

for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Ensure sorted by date
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')
        
        # First & last closing price
        first_close = df['close'].iloc[0]
        last_close = df['close'].iloc[-1]
        
        # Calculate yearly return
        yearly_return = ((last_close - first_close) / first_close) * 100
        
        # Stock name (remove .csv extension)
        stock_name = file.replace(".csv", "")
        
        performance.append([stock_name, yearly_return])

# Convert to DataFrame
performance_df = pd.DataFrame(performance, columns=["Stock", "Return (%)"])

# Rank best & worst
top_10_green = performance_df.sort_values(by="Return (%)", ascending=False).head(10)
top_10_red = performance_df.sort_values(by="Return (%)", ascending=True).head(10)

print("Top 10 Green Stocks (Best Performers):")
print(top_10_green)

print("\nTop 10 Red Stocks (Worst Performers):")
print(top_10_red)

# Optionally save results
performance_df.to_csv("Stock_Performance_Ranking.csv", index=False)
