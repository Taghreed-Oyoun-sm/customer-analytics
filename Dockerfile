FROM python:3.11-slim

# Install required packages
RUN pip install --no-cache-dir pandas numpy matplotlib seaborn scikit-learn scipy requests openpyxl

# Create working directory
RUN mkdir -p /app/pipeline
WORKDIR /app/pipeline

# Copy the scripts 
COPY ingest.py preprocess.py analytics.py visualize.py cluster.py summary.sh README.md /app/pipeline/

# CMD to start interactive bash 
CMD ["/bin/bash"]