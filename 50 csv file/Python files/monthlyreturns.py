import pandas as pd

# Load data
df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\Outputfiles\fulldailyreturnstocks.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Pivot: each stock as a column, close price as values
close_df = df.pivot(index="date", columns="Ticker", values="close")

# Resample monthly, take last close of the month
monthly_close = close_df.resample("M").last()

# Calculate monthly returns (% change)
monthly_returns = monthly_close.pct_change()

# 🔹 Data cleaning: replace NaN with 0
monthly_returns = monthly_returns.fillna(0)

print(monthly_returns.head())

# Save cleaned data
monthly_returns.to_csv("monthly_returns.csv")
print("Monthly returns saved to monthly_returns.csv (NaN replaced with 0)")
