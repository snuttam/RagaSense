#!/bin/bash

# 🎵 RagaSense MLflow UI Starter Script

echo "🎵 Starting RagaSense MLflow UI..."
echo "=================================="

# Set up environment
export PATH="/Users/adhi/Library/Python/3.13/bin:$PATH"
export PATH="/Users/adhi/.local/bin:$PATH"

# Check if MLflow is available
if ! command -v mlflow &> /dev/null; then
    echo "❌ MLflow not found in PATH"
    echo "Available paths:"
    echo $PATH
    exit 1
fi

echo "✅ MLflow found: $(which mlflow)"
echo "✅ MLflow version: $(mlflow --version)"

# Start MLflow UI
echo "🚀 Starting MLflow UI on http://localhost:5000"
echo "📊 You can access the UI at:"
echo "   - http://localhost:5000"
echo "   - http://0.0.0.0:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

mlflow ui --host 0.0.0.0 --port 5000
