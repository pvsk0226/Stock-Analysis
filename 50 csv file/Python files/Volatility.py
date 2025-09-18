
import pandas as pd

df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\Outputfiles\daily_with_volatility.csv")

selected = df[["Ticker", "date", "Daily Return", "Daily Return_std"]]

selected.to_csv("Volatility.csv", index=False)

print("Saved as Volatility.csv")