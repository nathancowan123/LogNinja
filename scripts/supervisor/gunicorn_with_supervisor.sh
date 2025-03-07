#!/bin/bash

echo "🔄 Switching LogNinja to use Gunicorn with Supervisor..."

# Define Supervisor config file
SUPERVISOR_CONF="/etc/supervisor/conf.d/logninja.conf"

# Backup existing Supervisor config
if [ -f "$SUPERVISOR_CONF" ]; then
    sudo cp "$SUPERVISOR_CONF" "$SUPERVISOR_CONF.bak"
    echo "✅ Backup of existing Supervisor config created: $SUPERVISOR_CONF.bak"
fi

# Write new Supervisor configuration for Gunicorn
sudo tee "$SUPERVISOR_CONF" > /dev/null <<EOL
[program:logninja]
command=/home/bruce/Projects/LogNinja-Core/venv/bin/gunicorn -w 4 -b 0.0.0.0:8100 "app:create_app()"
directory=/home/bruce/Projects/LogNinja-Core
autostart=true
autorestart=true
stderr_logfile=/home/bruce/Projects/LogNinja-Core/logs/supervisor_err.log
stdout_logfile=/home/bruce/Projects/LogNinja-Core/logs/supervisor_out.log
EOL

echo "✅ Updated Supervisor configuration for LogNinja with Gunicorn."

# Restart Supervisor to apply changes
echo "🔄 Restarting Supervisor..."
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart logninja

echo "✅ LogNinja is now running with Gunicorn under Supervisor!"
