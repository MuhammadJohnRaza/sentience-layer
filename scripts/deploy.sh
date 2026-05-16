#!/bin/bash
# Deployment script for the Sentience Layer.

ENV=${1:-staging}

echo "Deploying Sentience Layer to $ENV environment..."

echo "Pulling latest changes..."
sleep 1

echo "Building containers..."
docker-compose -f docker-compose.yml build

echo "Starting services..."
docker-compose -f docker-compose.yml up -d

echo "Deployment to $ENV complete!"
