# 4️⃣ restart_services.sh (Restart LogNinja & Supervisor)
#!/bin/bash
echo "🔄 Restarting LogNinja Service..."
sudo systemctl restart logninja
echo "✅ LogNinja Restarted!"

echo "🔄 Restarting Supervisor Service..."
sudo systemctl restart supervisor
echo "✅ Supervisor Restarted!"
