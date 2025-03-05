#!/bin/bash
# Here’s a universal shell script (setup_temp_monitor.sh) that:

# ✅ Installs temperature monitoring tools for both Linux & Windows (WSL)
# ✅ Runs the sensors-detect tool on Linux to enable CPU temp monitoring
# ✅ Ensures coretemp module loads at boot on Linux
# ✅ Provides instructions for Windows users

# echo "🚀 Setting up CPU Temperature Monitoring..."

# Detect OS
OS_NAME=$(uname -s)

if [[ "$OS_NAME" == "Linux" ]]; then
    echo "🖥 Detected Linux. Installing required packages..."

    # Install lm-sensors and necessary tools
    if command -v apt &>/dev/null; then
        sudo apt update && sudo apt install -y lm-sensors hddtemp
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y lm_sensors hddtemp
    elif command -v pacman &>/dev/null; then
        sudo pacman -S lm_sensors hddtemp --noconfirm
    else
        echo "⚠️ Unsupported package manager! Install lm-sensors manually."
        exit 1
    fi

    echo "🔍 Running sensors-detect..."
    sudo sensors-detect --auto

    echo "🔧 Enabling coretemp module..."
    echo "coretemp" | sudo tee -a /etc/modules

    echo "✅ Setup complete! Run 'sensors' to check temperatures."
    echo "📢 If 'sensors' doesn't work after reboot, try: sudo modprobe coretemp"

elif [[ "$OS_NAME" == "MINGW64_NT"* || "$OS_NAME" == "CYGWIN_NT"* ]]; then
    echo "🖥 Detected Windows (via WSL)."

    echo "⚠️ Temperature monitoring is not natively supported in WSL."
    echo "💡 Use a tool like HWMonitor, OpenHardwareMonitor, or Core Temp."
    echo "👉 Download OpenHardwareMonitor: https://openhardwaremonitor.org/"
    echo "👉 Download Core Temp: https://www.alcpu.com/CoreTemp/"
    echo "👉 To view temp in PowerShell: Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace root/wmi"

else
    echo "⚠️ Unsupported OS: $OS_NAME"
    exit 1
fi
