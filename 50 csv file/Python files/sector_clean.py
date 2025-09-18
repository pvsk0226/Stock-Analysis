import pandas as pd

# Read your sector file
sector_df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\Sector_data.csv")

# Extract the part after ':' and remove any extra spaces
sector_df["Ticker"] = sector_df["Symbol"].str.split(":").str[1].str.strip()

# Save cleaned file
sector_df.to_csv("sector_cleaned.csv", index=False)

print("Cleaned and saved as sector_cleaned.csv")
