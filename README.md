# Customer Analytics Pipeline — CSCI461 Assignment 1

## Team Members
| Name | Student ID |
|------|------------|
| Farah Awadalla | 231000006 |
| Taghreed Oyoun | 231002478 |

---

## Dataset
- **Name:** Online Retail II
- **Source:** UCI Machine Learning Repository
- **Link:** https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **Description:** Raw transactional data from a UK-based online retail company (2009–2011), containing invoices, products, quantities, prices, and customer IDs.

---

## What Farah Implemented
- **Dockerfile** — Base image `python:3.11-slim`, installs all required packages, sets up `/app/pipeline/` as working directory
- **ingest.py** — Downloads the Online Retail II dataset from UCI, extracts the Excel file from the zip, and saves it as `data_raw.csv`
- **preprocess.py** — Full preprocessing pipeline:
  - *Data Cleaning:* removes duplicates, drops cancelled invoices, drops rows with missing Customer ID, filters invalid quantities/prices
  - *Feature Transformation:* creates `TotalAmount`, encodes `Country`, extracts date features (Year, Month, DayOfWeek), scales numeric columns with StandardScaler
  - *Dimensionality Reduction:* applies PCA (2 components) on Quantity, Price, TotalAmount
  - *Discretization:* bins `TotalAmount` into 5 categories and `Quantity` into 4 categories

## What Taghreed Implemented
- **analytics.py** — Generates 3 textual insights from the preprocessed data:
  - `insight1.txt`: Total revenue and number of unique customers
  - `insight2.txt`: Top 5 countries by revenue
  - `insight3.txt`: Average order value and most frequent purchase day
- **visualize.py** — Generates 3 meaningful plots saved as `summary_plot.png`:
  - Histogram of transaction amounts (excluding top 5% outliers)
  - Horizontal bar chart of top 10 countries by number of transactions
  - Correlation heatmap of numeric features
- **cluster.py** — Applies K-Means clustering (k=5) using RFM (Recency, Frequency, Monetary) features, labels each cluster, and saves results to `clusters.txt`
- **summary.sh** — Copies all output files (`.csv`, `.txt`, `.png`) from the container to `results/` on the host, then stops and removes the container

---

## Project Structure
```
customer-analytics/
├── Dockerfile
├── ingest.py
├── preprocess.py
├── analytics.py
├── visualize.py
├── cluster.py
├── summary.sh
├── README.md
└── results/
    ├── data_raw.csv
    ├── data_preprocessed.csv
    ├── insight1.txt
    ├── insight2.txt
    ├── insight3.txt
    ├── summary_plot.png
    └── clusters.txt
```

---

## Execution Flow

```
ingest.py
   └──> preprocess.py
            └──> analytics.py
                     └──> visualize.py
                               └──> cluster.py
```

Each script automatically calls the next one using `subprocess.call()`.

---

## Docker Build & Run Commands

### 1. Build the Docker image
```bash
docker build -t customer-analytics .
```

### 2. Run the container (interactive)
```bash
docker run -it --name analytics-container customer-analytics
```

### 3. Inside the container — run the full pipeline
```bash
python ingest.py
```

### 4. Open a new terminal on the host — copy results and clean up
```bash
bash summary.sh analytics-container
```

> This copies all outputs to `results/` on your host machine, then stops and removes the container.

---

## Sample Outputs

### insight1.txt
```
Total Revenue: $xxxxxx.xx
Total Unique Customers: xxxx
```

### insight2.txt
```
Top 5 Countries by Revenue:
United Kingdom    xxxxxxxxx.xx
Netherlands        xxxxxxxxx.xx
...
```

### insight3.txt
```
Average Order Value: $xxx.xx
Most Frequent Purchase Day: Thursday
```

### clusters.txt (excerpt)
```
CUSTOMER SEGMENTATION USING K-MEANS CLUSTERING (RFM Analysis)
======================================================================
Cluster 0: Regular Customers
   Number of Customers : xxx
   Avg Recency         : xx days
   Avg Frequency       : x orders
   Avg Monetary Value  : $xxx.xx
...
```

### summary_plot.png
Three plots: transaction amount distribution, top 10 countries by transactions, and a correlation heatmap.
