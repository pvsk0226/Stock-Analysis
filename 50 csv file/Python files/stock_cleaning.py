import pandas as  pd 
df = pd.read_csv(r"C:\Pavithra\Data driven stock analysis project 2\Outputfiles\Cumulativereturn.csv")

print(df.info())
print(df.head())

df = df.fillna(0)

df.to_csv("Cumulativereturn_clean.csv", index=False)

print("NaN values replaced with 0 and file saved as cleaned_file.csv")