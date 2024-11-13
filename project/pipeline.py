import os
import pandas as pd
import requests
import sqlite3



# Define the URLs and output file names
datasets = {
    "air_quality": "https://data.cityofnewyork.us/api/views/c3uy-2p5r/rows.csv?accessType=DOWNLOAD",
    "chronic_disease": "https://data.cdc.gov/api/views/g4ie-h725/rows.csv?accessType=DOWNLOAD"
}

# Directory to save CSV files
save_path = './data'

os.makedirs(save_path, exist_ok=True)

def download_and_save_data(url, filename):
    # Download CSV from URL
    response = requests.get(url)
    if response.status_code == 200:
        # Define the CSV file path
        csv_file_path = os.path.join(save_path, filename)
        
        # Write the CSV content to a file
        with open(csv_file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded and saved CSV as '{csv_file_path}'.")

        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Define the SQLite database file path
        sqlite_file_path = os.path.join(save_path, filename.replace('.csv', '.db'))

        # Save the DataFrame to an SQLite database
        with sqlite3.connect(sqlite_file_path) as conn:
            df.to_sql(name=filename.replace('.csv', ''), con=conn, if_exists='replace', index=False)
        print(f"Saved data to SQLite database as '{sqlite_file_path}'.")
    else:
        print(f"Failed to download '{filename}'. Status code: {response.status_code}")

# Download each dataset and save as both CSV and SQLite
for name, url in datasets.items():
    csv_filename = f"{name}.csv"
    download_and_save_data(url, csv_filename)

print("All datasets have been downloaded and saved as both CSV and SQLite files.")
