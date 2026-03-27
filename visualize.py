import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

df = pd.read_csv("data_preprocessed.csv")

print("Generating 3 plots...")

# Create figure with better layout
fig = plt.figure(figsize=(16, 11))

# ==================== Plot 1: Histogram - Fixed Scale ====================
plt.subplot(2, 2, 1)
# Better filtering for visibility
amount_data = df[(df['TotalAmount'] > 0) & (df['TotalAmount'] < df['TotalAmount'].quantile(0.95))]

sns.histplot(data=amount_data, x='TotalAmount', bins=50, kde=True, color='skyblue')
plt.title('Distribution of Transaction Amount\n(Excluding Top 5% Outliers)')
plt.xlabel('Total Amount ($)')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)

# ==================== Plot 2: Top 10 Countries - Fixed Bar Chart ====================
plt.subplot(2, 2, 2)
top_countries = df['Country'].value_counts().head(10)

# Use horizontal bar with better scaling
sns.barplot(x=top_countries.values, y=top_countries.index, palette='Blues_d')
plt.title('Top 10 Countries by Number of Transactions')
plt.xlabel('Number of Transactions')
plt.ylabel('Country')
plt.grid(axis='x', alpha=0.3)

# Add value labels on the bars
for i, v in enumerate(top_countries.values):
    plt.text(v + 1000, i, f'{v:,}', va='center', fontsize=10)

# ==================== Plot 3: Correlation Heatmap ====================
plt.subplot(2, 2, 3)
numeric_cols = ['Quantity', 'Price', 'TotalAmount', 'Year', 'Month', 'DayOfWeek']
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, 
            cbar_kws={'shrink': 0.8})
plt.title('Correlation Heatmap of Numeric Features')

# Empty subplot with project info
plt.subplot(2, 2, 4)
plt.axis('off')
plt.text(0.5, 0.5, 'Customer Analytics Pipeline\nOnline Retail II Dataset\nSpring 2026', 
         ha='center', va='center', fontsize=12, alpha=0.7)

plt.tight_layout()
plt.savefig('summary_plot.png', dpi=300, bbox_inches='tight')
plt.close()


print("All 3 plots successfully saved in 'summary_plot.png'")


# Call the next script
print("Calling cluster.py...")
subprocess.call([sys.executable, 'cluster.py'])