#!/usr/bin/env bash
# Install the CoachForge AI launchd jobs.
#
#   ./install.sh                  # installs analyst + creative + reporting (no publishing)
#   ./install.sh --with-publisher # also installs the daily publisher (schedules Approved rows)
#   ./install.sh --wake           # also set a daily 06:25 wake-from-sleep (needs sudo)
#
# The publisher is opt-in on purpose: it schedules REAL posts for any Content
# Calendar row you've marked Approved. Only enable it once you've watched one
# scheduling run and trust it.
set -euo pipefail

AUTO="/Users/aaronhopkins/coachforge-marketing-team/automation"
LA="$HOME/Library/LaunchAgents"

WITH_PUBLISHER=0
SET_WAKE=0
for arg in "$@"; do
  case "$arg" in
    --with-publisher) WITH_PUBLISHER=1 ;;
    --wake) SET_WAKE=1 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

JOBS=(analyst creative reporting)
[ "$WITH_PUBLISHER" -eq 1 ] && JOBS+=(publisher)

chmod +x "$AUTO/run-job.sh" "$AUTO/notify.sh"
mkdir -p "$LA"

for job in "${JOBS[@]}"; do
  plist="com.coachforge.$job.plist"
  cp "$AUTO/launchd/$plist" "$LA/$plist"
  launchctl unload "$LA/$plist" 2>/dev/null || true
  launchctl load "$LA/$plist"
  echo "loaded  $plist"
done

if [ "$WITH_PUBLISHER" -eq 0 ]; then
  echo "skipped com.coachforge.publisher.plist  (run with --with-publisher to enable the draft-builder)"
fi

if [ "$SET_WAKE" -eq 1 ]; then
  echo
  echo "Setting a daily 06:25 wake so the morning jobs fire from sleep (sudo)..."
  sudo pmset repeat wakeorpoweron MTWRFSU 06:25:00 \
    && echo "wake scheduled (check: pmset -g sched)" \
    || echo "could not set wake; set it manually if you want wake-from-sleep."
  echo "Note: pmset repeat holds ONE schedule, so the Sun 18:00 roll-up is not covered by it."
fi

echo
echo "Installed jobs:"
launchctl list | grep coachforge || echo "  (none found — check for errors above)"
echo
echo "Schedule (Europe/London):"
echo "  analyst    daily 07:00"
echo "  publisher  daily 07:30   $([ "$WITH_PUBLISHER" -eq 1 ] && echo '(ENABLED)' || echo '(not installed)')"
echo "  creative   Mon   06:30"
echo "  reporting  Sun   18:00"
