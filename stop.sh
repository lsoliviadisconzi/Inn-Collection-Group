#!/usr/bin/env bash
# Stop the Inn Collection Group menu review server

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Try to stop using saved PID first
if [[ -f .server.pid ]]; then
    PID=$(cat .server.pid)
    if kill -0 $PID 2>/dev/null; then
        echo "Stopping server (PID: $PID)..."
        kill $PID
        # Wait for graceful shutdown
        for i in {1..10}; do
            if ! kill -0 $PID 2>/dev/null; then
                echo "Server stopped successfully"
                rm -f .server.pid
                exit 0
            fi
            sleep 0.5
        done
        # Force kill if still running
        echo "Server didn't stop gracefully, forcing..."
        kill -9 $PID 2>/dev/null || true
        echo "Server force-stopped"
        rm -f .server.pid
        exit 0
    else
        echo "PID file exists but process not running"
        rm -f .server.pid
    fi
fi

# Fallback: find and kill any process on port 8000
if lsof -ti:8000 >/dev/null 2>&1; then
    echo "Found server on port 8000, stopping..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    echo "Server stopped"
else
    echo "No server running on port 8000"
fi