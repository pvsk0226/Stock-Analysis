import pandas as pd

# Step 1 — Read your combined file
df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\dailyreturn n color\fulldailyreturnstocks.csv")


# Step 2 — Compute standard deviation of daily_return per stock
volatility = df.groupby("Ticker")["Daily Return"].std().reset_index()
volatility.rename(columns={"Daily Return": "Daily Return_std"}, inplace=True)

# Step 3 — Merge this std back to the original daily data
df = df.merge(volatility, on="Ticker", how="left")

# Now each row has:
# Ticker, date, open, close, daily_return, daily_return_std

# Step 4 — Save to a new CSV
df.to_csv("daily_with_volatility.csv", index=False)

print("Saved as daily_with_volatility.csv")
