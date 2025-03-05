# 1️⃣ install_supervisor.sh (Install & Setup Supervisor)
# #!/bin/bash
echo "🚀 Installing Supervisor..."
sudo apt update && sudo apt install supervisor -y
echo "✅ Supervisor Installed!"

# Reload Supervisor to make sure it's running
sudo systemctl restart supervisor
sudo systemctl enable supervisor
echo "✅ Supervisor Started & Enabled!"
