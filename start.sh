#!/usr/bin/env bash
# Start the Inn Collection Group menu review server

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Check if server is already running
if lsof -ti:8000 >/dev/null 2>&1; then
    echo "Server is already running on port 8000"
    echo "Use ./stop.sh to stop it first, or check http://localhost:8000/"
    exit 1
fi

# Verify required directories exist
if [[ ! -d "pages" || ! -d "inncollectiongroup.com_root/menus_md" || ! -d "inncollectiongroup.com_root/documents/extracted-to-md" ]]; then
    echo "Error: Required directories not found. Make sure you're in the project root."
    exit 1
fi

# Initialize database if needed
if [[ ! -f "menu_review_state.sqlite3" ]]; then
    echo "Initializing database..."
    python3 -c "from db.database import init_db; init_db('menu_review_state.sqlite3', backup_dir='db/backups')"
fi

echo "Starting menu review server on http://localhost:8000/"
echo "Press Ctrl+C to stop"

# Start the server in the background
python3 menu_review_server.py &
SERVER_PID=$!

# Save PID for stop script
echo $SERVER_PID > .server.pid

# Wait a moment and verify it started
sleep 2
if kill -0 $SERVER_PID 2>/dev/null; then
    echo "Server started successfully (PID: $SERVER_PID)"
    echo "Open http://localhost:8000/ in your browser"
else
    echo "Server failed to start. Check the output above for errors."
    rm -f .server.pid
    exit 1
fi