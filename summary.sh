#!/bin/bash

CONTAINER_NAME="analytics-container"
IMAGE_NAME="customer-analytics"

echo "====================================="
echo "Data Analytics Pipeline"
echo "====================================="

# Step 1: Build the image
echo "Step 1: Building Docker image..."
docker build -t $IMAGE_NAME .

# Step 2: Remove any existing container with the same name
echo "Step 2: Cleaning up old container if exists..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# Step 3: Run the container and execute the full pipeline automatically
echo "Step 3: Running pipeline inside container..."
docker run --name $CONTAINER_NAME $IMAGE_NAME python ingest.py

# Step 4: Create results directory on host
echo "Step 4: Creating results directory..."
mkdir -p results

# Step 5: Copy results from container to host
echo "Step 5: Copying results to host..."
docker cp $CONTAINER_NAME:/app/pipeline/data_raw.csv results/ 2>/dev/null || true
docker cp $CONTAINER_NAME:/app/pipeline/data_preprocessed.csv results/ 2>/dev/null || true
docker cp $CONTAINER_NAME:/app/pipeline/insight1.txt results/ 2>/dev/null || true
docker cp $CONTAINER_NAME:/app/pipeline/insight2.txt results/ 2>/dev/null || true
docker cp $CONTAINER_NAME:/app/pipeline/insight3.txt results/ 2>/dev/null || true
docker cp $CONTAINER_NAME:/app/pipeline/summary_plot.png results/ 2>/dev/null || true
docker cp $CONTAINER_NAME:/app/pipeline/clusters.txt results/ 2>/dev/null || true

echo "====================================="
echo "Results copied to ./results/"
echo "====================================="
ls results/

# Step 6: Stop and remove container
echo "Step 6: Cleaning up container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME

echo ""
echo "Done! All results are in the 'results/' directory."
