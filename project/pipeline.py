import os
import pandas as pd
import requests
import sqlite3


urls = {
    "sugar_sweetened_beverages": "https://data.chhs.ca.gov/dataset/bb703230-1f5f-44b5-8a90-55e45e08c452/resource/4a8dde27-c4e1-4ca3-860b-447d813b2ce6/download/sugar-sweetened-beverage-consumption-in-california-residents-20122013.csv",
    "adult_depression": "https://data.chhs.ca.gov/dataset/5a281abf-1730-43b0-b17b-ac6a35db5760/resource/724c6fd8-a645-4e52-b63f-32631a20db5d/download/adult-depression-lghc-indicator-24.csv"
}

save_path = '../data'
os.makedirs(save_path, exist_ok=True)

def download_and_clean_data(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        csv_path = os.path.join(save_path, filename)
        with open(csv_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded '{filename}' successfully.")
    else:
        print(f"Failed to download '{filename}'. Status code: {response.status_code}")
        return

    df = pd.read_csv(csv_path)


    df.dropna(inplace=True)  
    for col in df.select_dtypes(include=['object']):
        
        df[col] = df[col].str.strip()

 
    cleaned_path = os.path.join(save_path, f"cleaned_{filename}")
    df.to_csv(cleaned_path, index=False)
    print(f"Cleaned data saved to '{cleaned_path}'.")

download_and_clean_data(urls["sugar_sweetened_beverages"], "sugar_sweetened_beverages.csv")
download_and_clean_data(urls["adult_depression"], "adult_depression.csv")

print("Data processing complete.")
