#!/bin/bash
# capture_puf.sh — capture a single PUF image, name by unit serial
#
# Usage: capture_puf.sh <unit_serial>
# Example: capture_puf.sh PV-2026-00042

SERIAL="$1"
if [ -z "$SERIAL" ]; then
    echo "usage: $0 <unit_serial>"
    echo "example: $0 PV-2026-00042"
    exit 1
fi

OUTDIR="$HOME/ZKNOT/6_SIG/puf_images"
mkdir -p "$OUTDIR"

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUTFILE="$OUTDIR/PV_${SERIAL}_${TIMESTAMP}.jpg"

# Capture single 1920x1080 frame from microscope
# -update 1 silences the "no image sequence pattern" warning
ffmpeg -y -hide_banner -loglevel warning \
       -f v4l2 -input_format mjpeg -video_size 1920x1080 \
       -i /dev/video0 \
       -update 1 -frames:v 1 \
       "$OUTFILE"

if [ -f "$OUTFILE" ]; then
    SIZE=$(stat -c%s "$OUTFILE")
    echo "Captured: $OUTFILE ($SIZE bytes)"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),$SERIAL,$OUTFILE,$SIZE" \
        >> "$OUTDIR/captures.log"
else
    echo "ERROR: capture failed"
    exit 1
fi
