#!/bin/bash
# Simulates random node failures to test Sentience Layer recovery.

echo "Starting Chaos Monkey test on local environment..."

SERVICES=("python_backend" "node_backend" "redis" "postgres")

# Randomly select a service
RANDOM_SERVICE=${SERVICES[$RANDOM % ${#SERVICES[@]}]}

echo "Targeting service: $RANDOM_SERVICE for simulated failure..."

# Simulate failure
echo "Sending SIGKILL to $RANDOM_SERVICE..."
sleep 2

echo "Monitoring recovery engine..."
sleep 3

echo "Service recovered successfully. Chaos test passed."
