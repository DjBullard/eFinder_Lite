#!/usr/bin/env bash
set -Eeuo pipefail

# --- config ---
APP_HOME="/home/efinder"
VENV_PY="$APP_HOME/venv-efinder/bin/python"
APP="$APP_HOME/Solver/eFinder_Lite.py"
LOG="$APP_HOME/efinder.log"

# Minimal, known-good PATH for cron
export PATH="/home/efinder/venv-efinder/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Make sure we start from the same place you were using in cron
cd "$APP_HOME"

# Optional tiny log “rotation” to prevent a runaway log file (10 MB)
if [ -f "$LOG" ] && [ "$(stat -c%s "$LOG")" -gt 10485760 ]; then
  mv -f "$LOG" "${LOG}.$(date +%Y%m%d-%H%M%S)"
fi

# Launch detached so it survives cron's session cleanly
nohup "$VENV_PY" "$APP" >> "$LOG" 2>&1 &

