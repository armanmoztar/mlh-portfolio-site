# Kill all existing tmux sessions
tmux kill-server 2>/dev/null || true

#  Navigate to project directory
cd ~/mlh-portfolio-site || {
  echo "Project directory not found!"
  exit 1
}

# Pull changes from GitHub main branch
git pull
git reset origin/main --hard

# Activate virtual environment, install dependencies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Start new detached tmux session that runs Flask
tmux new-session -d -s flask "cd ~/mlh-portfolio-site && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0 --port=5000"

echo "Flask app deployed successfully"

