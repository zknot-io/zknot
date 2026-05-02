#!/usr/bin/env python3





"""
journal.py — Interactive JSON journaling script

Purpose:
  • Capture daily study logs, thoughts, pentest notes, and reflections.
  • Each entry gets a timestamp and optional tags for later search/filtering.
  • Designed to be simple enough to understand and expand.

Core Concepts:
  • File I/O (reading and writing to files)
  • JSON data structures
  • Loops and input handling
  • String manipulation
  • Error handling and script flow
"""

import json
from datetime import datetime
from pathlib import Path

# -----------------------------
# CONFIGURATION
# -----------------------------
# Define where the journal will be stored.
JOURNAL_FILE = Path.home() / "journal.json"

# Create the journal file if it doesn’t exist.
if not JOURNAL_FILE.exists():
    with open(JOURNAL_FILE, "w") as f:
        json.dump([], f, indent=2)

# -----------------------------
# INPUT SECTION
# -----------------------------
print("🧠 Study Journal")
print("Type your entry below. You can write multiple lines.")
print("When you’re done, type a single '.' on a new line and press Enter.\n")

lines = []
while True:
    line = input()
    if line.strip() == ".":  # stop reading input when a single dot is entered
        break
    lines.append(line)

# Join all lines into one string, separated by line breaks.
note = "\n".join(lines).strip()

# Ask for tags to make later filtering easy.
tags_input = input("\n🏷️  Enter tags (comma-separated): ").strip()
tags = [t.strip() for t in tags_input.split(",") if t.strip()]

# -----------------------------
# CREATE ENTRY OBJECT
# -----------------------------
entry = {
    "timestamp": datetime.now().isoformat(timespec="seconds"),
    "note": note,
    "tags": tags
}

# -----------------------------
# SAVE ENTRY
# -----------------------------
try:
    with open(JOURNAL_FILE, "r") as f:
        data = json.load(f)
except json.JSONDecodeError:
    print("⚠️  Warning: journal file was corrupted, starting fresh.")
    data = []

data.append(entry)

with open(JOURNAL_FILE, "w") as f:
    json.dump(data, f, indent=2)

# -----------------------------
# OUTPUT
# -----------------------------
print(f"\n✅ Entry saved to {JOURNAL_FILE}")
print(json.dumps(entry, indent=2))
