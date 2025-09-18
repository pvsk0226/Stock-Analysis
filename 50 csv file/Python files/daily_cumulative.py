import pandas as pd

# Read your daily returns file
df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\Outputfiles\fulldailyreturnstocks.csv")

# Sort data by Ticker and date so cumulative order is correct
df = df.sort_values(by=["Ticker", "date"])

# Calculate cumulative return per stock
df["cumulative_return"] = (
    df.groupby("Ticker")["Daily Return"]
      .transform(lambda x: (1 + x/100).cumprod() - 1) * 100
)

# Save to a new CSV
df.to_csv("daily_with_cumulative_return.csv", index=False)

print("Saved as daily_with_cumulative_return.csv")

