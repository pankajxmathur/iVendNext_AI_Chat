#!/bin/bash
# Script to fix Frappe installation and install iVendNext AI Chat

echo "=== Fixing Frappe Installation ==="

# Navigate to bench directory
cd ~/frappe-bench

# Step 1: Check if frappe app exists
if [ ! -d "apps/frappe" ]; then
    echo "ERROR: Frappe app not found in apps directory!"
    echo "Your bench installation is incomplete."
    exit 1
fi

# Step 2: Uninstall PyPI frappe (if installed)
echo "Removing PyPI frappe package..."
pip uninstall frappe -y 2>/dev/null || true

# Step 3: Reinstall frappe from the apps directory
echo "Installing Frappe from apps directory..."
pip install -e apps/frappe

# Step 4: Verify installation
echo "Verifying Frappe installation..."
python -c "import frappe; print(f'Frappe version: {frappe.__version__}')"

if [ $? -ne 0 ]; then
    echo "ERROR: Frappe installation failed!"
    exit 1
fi

echo ""
echo "=== Installing iVendNext AI Chat ==="

# Step 5: Remove old installation if exists
rm -rf apps/ivendnext_ai_chat 2>/dev/null || true

# Step 6: Clone the app
echo "Cloning iVendNext AI Chat..."
cd apps
git clone https://github.com/pankajxmathur/iVendNext_AI_Chat ivendnext_ai_chat
cd ..

# Step 7: Install Python dependencies
echo "Installing Python dependencies..."
pip install -e apps/ivendnext_ai_chat

# Step 8: Install Python requirements
echo "Installing app requirements..."
pip install -r apps/ivendnext_ai_chat/requirements.txt

# Step 9: Install app on site
echo ""
echo "Please run the following command to install the app on your site:"
echo "bench --site acme.local install-app ivendnext_ai_chat"
echo ""
echo "Then build and restart:"
echo "bench build --app ivendnext_ai_chat"
echo "bench restart"
