# 3️⃣ check_services.sh (Check Status of LogNinja & Supervisor)
#!/bin/bash
echo "🔍 Checking LogNinja Service..."
sudo systemctl status logninja --no-pager

echo "🔍 Checking Supervisor Service..."
sudo systemctl status supervisor --no-pager
