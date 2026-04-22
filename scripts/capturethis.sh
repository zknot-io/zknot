#!/bin/bash

TARGET_FILE="/home/marctremb/org_notes/capturethis"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo -n "Thought: "
read -r INPUT

if [[ -n "$INPUT" ]]; then
  echo -e "* $TIMESTAMP\n  $INPUT\n" >> "$TARGET_FILE"
  echo "Captured."
else
  echo "No input. Nothing saved."
fi
