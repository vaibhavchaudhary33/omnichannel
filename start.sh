#!/bin/bash

echo "🚀 Starting Omnichannel Data Ingestion Engine..."

# Start Shopify mock server in background
echo "▶ Starting Shopify mock server on port 5001..."
python mock_servers/shopify_mock.py > logs/shopify.log 2>&1 &
SHOPIFY_PID=$!

# Start Loyalty mock server in background
echo "▶ Starting Loyalty mock server on port 5002..."
python mock_servers/loyalty_mock.py > logs/loyalty.log 2>&1 &
LOYALTY_PID=$!

# Wait for servers to start
sleep 2

# Verify both servers are running
echo ""
echo "🔍 Verifying servers..."
curl -s http://localhost:5001/health && echo ""
curl -s http://localhost:5002/health && echo ""

echo ""
echo "✅ Both servers running!"
echo "   Shopify PID : $SHOPIFY_PID"
echo "   Loyalty PID : $LOYALTY_PID"
echo ""
echo "▶ Running pipeline..."
python pipeline.py

