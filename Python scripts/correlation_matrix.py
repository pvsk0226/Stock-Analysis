import pandas as pd

    # Load your CSV
df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\Outputfiles\fulldailyreturnstocks.csv")

    # Pivot so that each stock's close is a column
close_df = df.pivot(index="date", columns="Ticker", values="close")
correlation_matrix = close_df.corr()


correlation_matrix.to_csv("correlation_matrix.csv", index=False)

print("Saved as correlation_matrix.csv")

    # Check the reshaped dataframe
print(correlation_matrix.head())
