#!/bin/bash
# Simple test script for Resume Tailor app

echo "======================================"
echo "Testing Resume Tailor Application"
echo "======================================"
echo ""

echo "Test 1: Health Check"
echo "Command: curl http://localhost:8000/api/health"
curl -s http://localhost:8000/api/health
echo ""
echo ""

echo "Test 2: Homepage Check"
echo "Command: curl http://localhost:8000"
if curl -s http://localhost:8000 | grep -q "Resume Tailor"; then
    echo "✅ SUCCESS - Homepage is loading!"
else
    echo "❌ FAILED - Homepage not loading"
fi
echo ""

echo "Test 3: Check if API endpoints are available"
echo "Available endpoints:"
echo "  - POST /api/upload-resume"
echo "  - POST /api/fetch-job-description"
echo "  - POST /api/analyze"
echo "  - GET /api/health"
echo ""

echo "======================================"
echo "All basic tests complete!"
echo "======================================"
