#!/usr/bin/env bash
# CoachForge AI — unattended job runner. Invoked by launchd (see automation/launchd/).
# Usage: run-job.sh <analyst|publisher|creative|reporting>
set -uo pipefail

JOB="${1:-}"
case "$JOB" in
  analyst|publisher|creative|reporting) ;;
  *) echo "usage: run-job.sh <analyst|publisher|creative|reporting>" >&2; exit 2 ;;
esac

DIR="/Users/aaronhopkins/coachforge-marketing-team"
AUTO="$DIR/automation"
PROMPT_FILE="$AUTO/prompts/$JOB.txt"
SETTINGS_FILE="$AUTO/settings/$JOB.settings.json"
LOG_DIR="$AUTO/logs"

# launchd hands us a minimal environment; make sure claude + node are findable.
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/aaronhopkins/.local/bin:${PATH:-}"

[ -f "$PROMPT_FILE" ]   || { echo "missing prompt:   $PROMPT_FILE" >&2;   exit 1; }
[ -f "$SETTINGS_FILE" ] || { echo "missing settings: $SETTINGS_FILE" >&2; exit 1; }

mkdir -p "$LOG_DIR"
TS="$(date +%Y%m%d-%H%M%S)"
LOG="$LOG_DIR/$JOB-$TS.log"

cd "$DIR" || { echo "cannot cd $DIR" >&2; exit 1; }

# Keep the Mac awake until this job's process finishes (no-op if already awake).
caffeinate -i -w "$$" &

{
  echo "=== CoachForge job: $JOB ==="
  echo "started:  $(date)"
  echo "settings: $SETTINGS_FILE"
  echo "----------------------------------------"
} >>"$LOG" 2>&1

claude -p "$(cat "$PROMPT_FILE")" \
  --settings "$SETTINGS_FILE" \
  --output-format text >>"$LOG" 2>&1
STATUS=$?

{
  echo "----------------------------------------"
  echo "finished: $(date)  (exit $STATUS)"
} >>"$LOG" 2>&1

# Stable "latest" pointer for quick tailing.
ln -sf "$LOG" "$LOG_DIR/$JOB-latest.log"

if [ "$STATUS" -eq 0 ]; then
  "$AUTO/notify.sh" "CoachForge: $JOB finished" "Log: automation/logs/$JOB-$TS.log"
else
  "$AUTO/notify.sh" "CoachForge: $JOB FAILED (exit $STATUS)" "Check automation/logs/$JOB-$TS.log"
fi

exit "$STATUS"
