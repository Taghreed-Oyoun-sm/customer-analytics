import sys
import pandas as pd
import subprocess

if len(sys.argv) < 2:
    input_path = "data_preprocessed.csv"
else:
    input_path = sys.argv[1]

df = pd.read_csv(input_path)

print("Generating textual insights...")

# Insight 1: Total revenue and unique customers

total_revenue = df['TotalAmount'].sum()
unique_customers = df['Customer ID'].nunique()

with open("insight1.txt", "w") as f:
    f.write(f"Total Revenue: ${total_revenue:,.2f}\n")
    f.write(f"Total Unique Customers: {unique_customers}\n")

print("Insight 1 saved (Revenue & Customers)")



# Insight 2: Top 5 countries by revenue

country_revenue = df.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False).head(5)

with open("insight2.txt", "w") as f:
    f.write("Top 5 Countries by Revenue:\n")
    f.write(country_revenue.to_string())

print("Insight 2 saved (Top Countries)")



# Insight 3: Average order value and most frequent purchase day

avg_order = df.groupby('Invoice')['TotalAmount'].sum().mean()
most_common_day = df['DayOfWeek'].value_counts().idxmax()  # 0=Monday ... 6=Sunday
day_name = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][most_common_day]

with open("insight3.txt", "w") as f:
    f.write(f"Average Order Value: ${avg_order:.2f}\n")
    f.write(f"Most Frequent Purchase Day: {day_name}\n")

print("Insight 3 saved (Avg Order Value & Day)")

print("All 3 insights generated successfully!")


# Call the next script
print("Calling visualize.py...")
subprocess.call([sys.executable, 'visualize.py'])