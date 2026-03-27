import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
import subprocess

if len(sys.argv) < 2:
    print("Usage: python preprocess.py <input_csv>")
    sys.exit(1)

input_path = sys.argv[1]
df = pd.read_csv(input_path)

print("Original shape:", df.shape)
print("Columns:", df.columns.tolist())

# 1. Data Cleaning

df = df.drop_duplicates()                                        

df = df[~df['Invoice'].astype(str).str.startswith('C')]           

df = df.dropna(subset=['Customer ID'])                              
df['Description'] = df['Description'].fillna('Unknown')

df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]                  

print("After cleaning shape:", df.shape)


# 2. Feature Transformation 

df['TotalAmount'] = df['Quantity'] * df['Price']

le_country = LabelEncoder()
df['Country_encoded'] = le_country.fit_transform(df['Country'])

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek

scaler = StandardScaler()
df[['Quantity_scaled', 'Price_scaled', 'TotalAmount_scaled']] = scaler.fit_transform(df[['Quantity', 'Price', 'TotalAmount']])

print("Feature transformation done.")


# 3. Dimensionality Reduction

numeric_for_pca = ['Quantity', 'Price', 'TotalAmount']
pca = PCA(n_components=2)
df[['PCA1', 'PCA2']] = pca.fit_transform(df[numeric_for_pca])

print("PCA applied.")


# 4. Discretization

df['Amount_bin'] = pd.cut(df['TotalAmount'], bins=[0, 10, 50, 100, 500, np.inf], labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])

df['Quantity_bin'] = pd.cut(df['Quantity'], bins=[0, 5, 20, 50, np.inf], labels=['Small', 'Medium', 'Large', 'Very Large'])

print("Discretization applied.")


# Save
df.to_csv('data_preprocessed.csv', index=False)
print("Preprocessing finished → data_preprocessed.csv")


# Call next script
print("Calling analytics.py...")
subprocess.call([sys.executable, 'analytics.py', 'data_preprocessed.csv'])