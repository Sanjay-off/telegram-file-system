#!/bin/bash

echo "=========================================="
echo "  Telegram File System - Startup Script"
echo "=========================================="

# ----------------------------
# PATH CONFIGURATION
# ----------------------------
PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"

ADM_BOT="bot_admin/admin_main.py"
USR_BOT="bot_user/user_main.py"
REDIRECT="redirect_server/redirect_main.py"

LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"

# ----------------------------
# CREATE VENV IF NOT EXISTS
# ----------------------------
if [ ! -d "$VENV_DIR" ]; then
    echo "[+] Creating virtual environment..."
    python3 -m venv venv
fi

# ----------------------------
# ACTIVATE VENV
# ----------------------------
echo "[+] Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# ----------------------------
# INSTALL REQUIREMENTS
# ----------------------------
echo "[+] Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "-------------------------------------------"
echo " Starting Admin Bot (Bot A)"
echo "-------------------------------------------"

nohup python3 "$ADM_BOT" > "$LOG_DIR/admin_bot.log" 2>&1 &
echo "[+] Admin Bot running in background."

echo ""
echo "-------------------------------------------"
echo " Starting User Bot (Bot B)"
echo "-------------------------------------------"

nohup python3 "$USR_BOT" > "$LOG_DIR/user_bot.log" 2>&1 &
echo "[+] User Bot running in background."

echo ""
echo "-------------------------------------------"
echo " Starting Redirect Server (Port 5000)"
echo "-------------------------------------------"

nohup python3 "$REDIRECT" > "$LOG_DIR/redirect_server.log" 2>&1 &
echo "[+] Redirect Server running in background."

echo ""
echo "=========================================="
echo " All services started successfully! 🔥"
echo " Logs available in: $LOG_DIR"
echo "=========================================="
