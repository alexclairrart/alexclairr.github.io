#!/bin/bash
# Test GitHub Actions workflows locally using act
# This runs the exact same workflows that will execute on GitHub

set -e

echo "🧪 Testing GitHub Actions workflows locally with act..."
echo

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "❌ act is not installed. Install it with: brew install act"
    echo "   See: https://github.com/nektos/act"
    exit 1
fi

echo "📋 Available workflows to test:"
echo "  1. EXIF Guard (checks for sensitive metadata)"
echo "  2. Watermark Check (verifies invisible watermarks)"
echo "  3. Both workflows"
echo

# Parse command line argument or prompt user
if [ $# -eq 1 ]; then
    choice="$1"
else
    echo -n "Enter your choice (1/2/3): "
    read choice
fi

case $choice in
    1)
        echo "🔍 Testing EXIF Guard workflow..."
        act -W .github/workflows/exif-guard.yml
        ;;
    2)
        echo "🖼️  Testing Watermark Check workflow..."
        act -W .github/workflows/check-watermark.yml
        ;;
    3)
        echo "🔍 Testing EXIF Guard workflow..."
        act -W .github/workflows/exif-guard.yml
        echo
        echo "🖼️  Testing Watermark Check workflow..."
        act -W .github/workflows/check-watermark.yml
        ;;
    *)
        echo "❌ Invalid choice. Please select 1, 2, or 3."
        exit 1
        ;;
esac

echo
echo "✅ Workflow testing complete!"
echo
echo "💡 Usage examples:"
echo "   ./test-github-workflows.sh     # Interactive mode"
echo "   ./test-github-workflows.sh 1   # Test EXIF only"
echo "   ./test-github-workflows.sh 2   # Test watermark only" 
echo "   ./test-github-workflows.sh 3   # Test both workflows"