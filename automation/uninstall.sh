#!/usr/bin/env bash
# Remove all CoachForge AI launchd jobs (and the daily wake, if set).
set -uo pipefail

LA="$HOME/Library/LaunchAgents"

for job in analyst publisher creative reporting; do
  plist="com.coachforge.$job.plist"
  if [ -f "$LA/$plist" ]; then
    launchctl unload "$LA/$plist" 2>/dev/null || true
    rm -f "$LA/$plist"
    echo "removed $plist"
  fi
done

echo
echo "To also clear the wake schedule:  sudo pmset repeat cancel"
echo "Remaining CoachForge jobs:"
launchctl list | grep coachforge || echo "  (none — all removed)"
