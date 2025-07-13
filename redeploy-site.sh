#!/bin/bash

# Navigate to project directory
cd /root/mlh-portfolio-site

# Pull latest changes from GitHub
git fetch && git reset origin/main --hard

# Activate virtual env
source python3-virtualenv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Restart the systemd service
sudo systemctl restart myportfolio

echo "Site redeployed and service restarted."
