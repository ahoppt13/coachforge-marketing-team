#!/usr/bin/env bash
# Best-effort macOS notification. Title = $1, message = $2. Never fails the caller.
TITLE="${1:-CoachForge}"
MSG="${2:-}"
TITLE="${TITLE//\"/\\\"}"
MSG="${MSG//\"/\\\"}"
/usr/bin/osascript -e "display notification \"$MSG\" with title \"$TITLE\"" >/dev/null 2>&1 || true
