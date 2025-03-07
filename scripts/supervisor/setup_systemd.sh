# 2️⃣ setup_systemd.sh (Creates & Configures Systemd Service)
#!/bin/bash
SERVICE_FILE="/etc/systemd/system/logninja.service"
LOG_DIR="/home/bruce/Projects/LogNinja-Core/logs"

echo "🚀 Setting up LogNinja Systemd Service..."

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Write the systemd service file
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=LogNinja Monitoring Service
After=network.target

[Service]
User=bruce
WorkingDirectory=/home/bruce/Projects/LogNinja-Core
ExecStart=/home/bruce/Projects/LogNinja-Core/venv/bin/python main.py
Restart=always
StandardOutput=append:/home/bruce/Projects/LogNinja-Core/logs/systemd_out.log
StandardError=append:/home/bruce/Projects/LogNinja-Core/logs/systemd_err.log

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Systemd service created at $SERVICE_FILE"

# Reload systemd, enable, and start the service
sudo systemctl daemon-reload
sudo systemctl enable logninja
sudo systemctl start logninja

echo "✅ LogNinja Service Started Successfully!"
