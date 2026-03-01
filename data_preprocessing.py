import pandas as pd
import os

def process_files(folder_path):
    all_df = []
    all_files = os.listdir(folder_path)
    print(f"{len(all_files)} files found.")
    csv_files = []
    for filename in all_files:
        if filename.endswith(".csv"):
            csv_files.append(filename)
            print(f"Processing {filename} ...")
            path = os.path.join(folder_path, filename)
            df = pd.read_csv(path)
            df["sales"] = df["quantity"] * df["price"].replace('[\$,]', '', regex=True).astype(float)
            df = df[["sales", "date", "region"]]
            all_df.append(df)
    print(f"{len(csv_files)} csv files processed")
    
    final_df = pd.concat(all_df, ignore_index=True)
    return final_df


result = process_files("data")
result.to_csv("preprocessed_data.csv", index = False)
    

