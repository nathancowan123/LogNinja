# Description: This script stops the LogNinja and Supervisor services.
#!/bin/bash
echo "🛑 Stopping LogNinja Service..."
sudo systemctl stop logninja
echo "✅ LogNinja Stopped!"

echo "🛑 Stopping Supervisor Service..."
sudo systemctl stop supervisor
echo "✅ Supervisor Stopped!"
