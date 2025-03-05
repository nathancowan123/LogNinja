#!/bin/bash
# 🚀 What This Script Does

# ✅ Downloads the setup script (setup_temp_monitor.sh) from Pastebin
# ✅ Checks if the download was successful
# ✅ Makes the script executable (chmod +x)
# ✅ Runs the setup script automatically


# Define the Pastebin URL (Replace XXXXX with actual Pastebin ID)
PASTEBIN_URL="https://pastebin.com/raw/XXXXX"

echo "🚀 Downloading setup_temp_monitor.sh..."
wget -O setup_temp_monitor.sh "$PASTEBIN_URL"

# Check if download was successful
if [ $? -eq 0 ]; then
    echo "✅ Download complete. Making script executable..."
    chmod +x setup_temp_monitor.sh

    echo "🔧 Running setup_temp_monitor.sh..."
    ./setup_temp_monitor.sh
else
    echo "❌ Download failed! Check the Pastebin URL or your internet connection."
    exit 1
fi
