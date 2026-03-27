import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

print("Performing K-Means clustering on customer level...")

df = pd.read_csv("data_preprocessed.csv")

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Dynamic snapshot date
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Create RFM features

customer_df = df.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'Invoice': 'nunique',
    'TotalAmount': 'sum'
}).reset_index()

customer_df.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Scale features

scaler = StandardScaler()
X = scaler.fit_transform(customer_df[['Recency', 'Frequency', 'Monetary']])

# Apply K-Means

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
customer_df['Cluster'] = kmeans.fit_predict(X)

# Calculate summary

cluster_counts = customer_df['Cluster'].value_counts().sort_index()
cluster_summary = customer_df.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean().round(2)

# Clear cluster labels
cluster_labels = {
    0: "Regular Customers",
    1: "Occasional / Low-Value Customers",
    2: "Frequent High-Spenders",
    3: "VIP / Top-Tier Customers",
    4: "Churned / Inactive Customers"
}

# Save to clusters.txt (without special characters)
with open("clusters.txt", "w", encoding="utf-8") as f:
    f.write("CUSTOMER SEGMENTATION USING K-MEANS CLUSTERING (RFM Analysis)\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Number of clusters used: 5\n")
    f.write(f"Total customers analyzed: {len(customer_df)}\n\n")
    
    f.write("CLUSTER SUMMARY:\n")
    f.write("-" * 50 + "\n")
    
    for cluster_id in range(5):
        count = cluster_counts.get(cluster_id, 0)
        rec = cluster_summary.loc[cluster_id, 'Recency']
        freq = cluster_summary.loc[cluster_id, 'Frequency']
        mon = cluster_summary.loc[cluster_id, 'Monetary']
        label = cluster_labels[cluster_id]
        
        f.write(f"Cluster {cluster_id}: {label}\n")
        f.write(f"   Number of Customers : {count}\n")
        f.write(f"   Avg Recency         : {rec} days\n")
        f.write(f"   Avg Frequency       : {freq} orders\n")
        f.write(f"   Avg Monetary Value  : ${mon:,.2f}\n")
        f.write("-" * 50 + "\n")
    
    f.write("\nBusiness Interpretation:\n")
    f.write("- Cluster 3 (VIP)         : Highest spending customers - Priority for loyalty programs\n")
    f.write("- Cluster 2 (Frequent)    : Very active buyers\n")
    f.write("- Cluster 0 (Regular)     : Stable and reliable customer base\n")
    f.write("- Cluster 1 (Occasional)  : Low engagement - Potential for upselling\n")
    f.write("- Cluster 4 (Churned)     : Inactive customers - Win-back campaigns needed\n")

print("\nClustering completed successfully!")
print("Number of customers per cluster:")
print(cluster_counts)
print("\nResults saved in clusters.txt")