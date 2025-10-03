#!/bin/bash

echo "🧹 CLEAN RESTART SCRIPT"
echo "======================================================================"
echo ""

# Step 1: Clean Python cache
echo "1️⃣  Cleaning Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name '*.pyc' -delete 2>/dev/null
echo "   ✅ Cache cleaned"
echo ""

# Step 2: Verify fixes are present
echo "2️⃣  Verifying fixes..."
python verify_and_fix.py
if [ $? -ne 0 ]; then
    echo "   ❌ Verification failed!"
    exit 1
fi
echo ""

# Step 3: Show available options
echo "======================================================================"
echo "🚀 SYSTEM READY!"
echo "======================================================================"
echo ""
echo "Choose what to run:"
echo ""
echo "  1. New automation run:"
echo "     python full_automation.py --auto-approve"
echo ""
echo "  2. Resume from checkpoint (if you have one):"
echo "     python full_automation.py --list-checkpoints"
echo "     python full_automation.py --resume SESSION_ID"
echo ""
echo "  3. Test Station 11 only:"
echo "     python test_station_11_fix.py"
echo ""
echo "  4. Test Stations 8-14:"
echo "     python test_stations_8_14_pdf.py"
echo ""
echo "======================================================================"
