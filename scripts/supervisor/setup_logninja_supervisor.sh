# Now, whenever you need to reconfigure Supervisor for LogNinja, just run:
# #!/bin/bash

echo "🚀 Setting up LogNinja with Supervisor..."

# Define paths
SUPERVISOR_CONF="/etc/supervisor/conf.d/logninja.conf"
LOGNINJA_DIR="/home/bruce/Projects/LogNinja-Core"
PYTHON_ENV="$LOGNINJA_DIR/venv/bin/python"
MAIN_SCRIPT="main.py"
LOG_DIR="$LOGNINJA_DIR/logs"

# Ensure logs directory exists
mkdir -p "$LOG_DIR"

# Create Supervisor config file for LogNinja
echo "🔧 Creating Supervisor config at $SUPERVISOR_CONF..."
sudo bash -c "cat > $SUPERVISOR_CONF" <<EOL
[program:logninja]
command=$PYTHON_ENV $MAIN_SCRIPT
directory=$LOGNINJA_DIR
autostart=true
autorestart=true
stderr_logfile=$LOG_DIR/supervisor_err.log
stdout_logfile=$LOG_DIR/supervisor_out.log
EOL

# Reload Supervisor and start LogNinja
echo "🔄 Reloading Supervisor..."
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start logninja

echo "✅ LogNinja has been added to Supervisor and started!"
