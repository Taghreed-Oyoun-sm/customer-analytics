import sys
import pandas as pd
import requests
import zipfile
import io
import subprocess


url = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"

print(f"Downloading raw dataset from UCI: {url}")

# Download the zip file
response = requests.get(url)
response.raise_for_status() 


# Extract the Excel file from the zip
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    excel_files = [f for f in z.namelist() if f.lower().endswith('.xlsx')]
    if not excel_files:
        print("No .xlsx file found in the zip!")
        sys.exit(1)
    
    excel_name = excel_files[0]
    print(f"Extracting {excel_name} ...")
    
    with z.open(excel_name) as f:
        df = pd.read_excel(f)


# Save as data_raw.csv
df.to_csv('data_raw.csv', index=False)


print(f"Dataset downloaded and ingested successfully! Shape: {df.shape}")
print("Columns:", df.columns.tolist())


# Automatically call the next script
print("Calling preprocess.py...")
subprocess.call([sys.executable, 'preprocess.py', 'data_raw.csv'])