#!/bin/bash

# Navigate to project directory
cd /root/mlh-portfolio-site

# Pull latest changes from GitHub
git fetch && git reset origin/main --hard

# Stop Docker containers
docker compose -f docker-compose.prod.yml down

# Rebuild and start containers
docker compose -f docker-compose.prod.yml up -d --build

echo "Site redeployed using Docker Compose."
