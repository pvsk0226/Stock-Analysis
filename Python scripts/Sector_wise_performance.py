import pandas as pd

# Read your main stock data
df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\Outputfiles\fulldailyreturnstocks.csv")

# Create a dictionary mapping Ticker -> Sector
stock_to_sector = {
    "ADANIENT": "MISCELLANEOUS",
    "ADANIPORTS": "MISCELLANEOUS",
    "APOLLOHOSP": "MISCELLANEOUS",
    "ASIANPAINT": "PAINTS",
    "AXISBANK": "BANKING",
    "BAJAJ-AUTO": "AUTOMOBILES",
    "BAJAJFINSV": "FINANCE",
    "BAJFINANCE": "FINANCE",
    "BEL": "DEFENCE",
    "BHARTIARTL": "TELECOM",
    "BPCL": "ENERGY",
    "BRITANNIA": "FOOD & TOBACCO",
    "CIPLA": "PHARMACEUTICALS",
    "COALINDIA": "MINING",
    "DRREDDY": "PHARMACEUTICALS",
    "EICHERMOT": "AUTOMOBILES",
    "GRASIM": "TEXTILES",
    "HCLTECH": "SOFTWARE",
    "HDFCBANK": "BANKING",
    "HDFCLIFE": "INSURANCE",
    "HEROMOTOCO": "AUTOMOBILES",
    "HINDALCO": "ALUMINIUM",
    "HINDUNILVR": "FMCG",
    "ICICIBANK": "BANKING",
    "INDUSINDBK": "BANKING",
    "INFY": "SOFTWARE",
    "ITC": "FOOD & TOBACCO",
    "JSWSTEEL": "STEEL",
    "KOTAKBANK": "BANKING",
    "LT": "ENGINEERING",
    "M&M": "AUTOMOBILES",
    "MARUTI": "AUTOMOBILES",
    "NESTLEIND": "FOOD & TOBACCO",
    "NTPC": "POWER",
    "ONGC": "ENERGY",
    "POWERGRID": "POWER",
    "RELIANCE": "ENERGY",
    "SBILIFE": "BANKING",
    "SBIN": "INSURANCE",
    "SHRIRAMFIN": "FINANCE",
    "SUNPHARMA": "PHARMACEUTICALS",
    "TATACONSUM": "FMCG",
    "TATAMOTORS": "AUTOMOBILES",
    "TATASTEEL": "STEEL",
    "TCS": "SOFTWARE",
    "TECHM": "SOFTWARE",
    "TITAN": "RETAILING",
    "TRENT": "RETAILING",
    "ULTRACEMCO": "CEMENT",
    "WIPRO": "SOFTWARE",
}

# Add new 'Sector' column by mapping Ticker
df["Sector"] = df["Ticker"].map(stock_to_sector)

# Save updated file
df.to_csv("stocks_with_sector.csv", index=False)

print("Sector column added and file saved as stocks_with_sector.csv")

