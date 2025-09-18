import pandas as pd
import os
input_folder = r"C:\Pavithra\Data driven stock analysis project 2\split_tickers"
 
# 📂 Create a new folder for updated files
output_folder = os.path.join(input_folder, "updated_files")
os.makedirs(output_folder, exist_ok=True)

# ⚡ Loop through all files
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):  # only CSV files
        file_path = os.path.join(input_folder, filename)

        # 📖 Read CSV
        df = pd.read_csv(file_path)

        # ➕ Add daily return column
        df["Daily Return"] = df["close"].pct_change()

        # ➕ Add red/green column based on open vs close
        df["Status"] = df.apply(
            lambda row: "Green" if row["close"] > row["open"] else "Red",
            axis=1
        )

        # 💾 Save updated CSV with same name inside updated_files folder
        output_path = os.path.join(output_folder, filename)
        df.to_csv(output_path, index=False)

        print("Updated:", filename)

print("All updated files saved inside:", output_folder)

