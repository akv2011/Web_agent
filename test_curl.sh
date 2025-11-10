#!/bin/bash

# API Test Script for Grounding Agent

echo "═══════════════════════════════════════════════════════════"
echo "    GROUNDING AGENT API - CURL TESTS"
echo "═══════════════════════════════════════════════════════════"
echo ""

BASE_URL="http://localhost:3000"

# Test 1: Root endpoint
echo "[TEST 1] Root Endpoint"
echo "─────────────────────────────────────────────────────────"
curl -s $BASE_URL/ | python -m json.tool
echo ""
echo ""

# Test 2: Health check
echo "[TEST 2] Health Check"
echo "─────────────────────────────────────────────────────────"
curl -s $BASE_URL/health | python -m json.tool
echo ""
echo ""

# Test 3: API usage info
echo "[TEST 3] API Usage Info"
echo "─────────────────────────────────────────────────────────"
curl -s $BASE_URL/api/agent | python -m json.tool
echo ""
echo ""

# Test 4: Simple calculator
echo "[TEST 4] Simple Calculator"
echo "Query: Calculate sqrt(144)"
echo "─────────────────────────────────────────────────────────"
curl -s -X POST $BASE_URL/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query":"Calculate sqrt(144)"}' | python -m json.tool
echo ""
echo ""

# Test 5: Weather query
echo "[TEST 5] Weather Query"
echo "Query: What is the weather in London?"
echo "─────────────────────────────────────────────────────────"
curl -s -X POST $BASE_URL/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the weather in London?"}' | python -m json.tool
echo ""
echo ""

# Test 6: Multiple tools
echo "[TEST 6] Multiple Tools"
echo "Query: Weather in Tokyo and calculate 25% of 500"
echo "─────────────────────────────────────────────────────────"
curl -s -X POST $BASE_URL/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the weather in Tokyo and calculate 25% of 500?"}' | python -m json.tool
echo ""
echo ""

# Test 7: Math operations
echo "[TEST 7] Math Operations"
echo "Query: Calculate 15 * 23 + sqrt(169)"
echo "─────────────────────────────────────────────────────────"
curl -s -X POST $BASE_URL/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query":"Calculate 15 * 23 + sqrt(169)"}' | python -m json.tool
echo ""
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "    ALL TESTS COMPLETED!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "✅ Your API is working correctly!"
echo ""
echo "Next steps:"
echo "  1. Test more queries"
echo "  2. Deploy to Vercel: vercel --prod"
echo "  3. Update the form with your deployment URL"
echo ""
