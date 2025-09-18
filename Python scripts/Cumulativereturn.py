import pandas as pd

df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\daily_with_cumulative_return.csv")

selected = df[["Ticker", "date", "Daily Return", "cumulative_return"]]

selected.to_csv("Cumulativereturn.csv", index=False)

print("Saved as Cumulativereturn.csv")