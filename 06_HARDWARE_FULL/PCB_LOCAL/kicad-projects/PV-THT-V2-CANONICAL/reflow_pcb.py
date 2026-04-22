#!/usr/bin/env python3
"""
Reflow PowerVerify THT PCB:
  - Resize board to 88 x 32 mm (62.5,86.5 -> 150.5,118.5)
  - Reposition all footprints to a conflict-free layout
  - Strip all traces and copper zones
  - Preserve nets, pads, schematic connectivity
"""
import re, sys, shutil, os, datetime

PCB = 'PV-THT-V2-CANONICAL.kicad_pcb'

# ============================================================
# TARGET POSITIONS: (x, y, rot)
# ============================================================
# Board: (62.5, 86.5) -> (150.5, 118.5) = 88 x 32mm
#
# Rows:
#  y=89.5   mounting holes H1, H2 (corners, tucked top)
#  y=93.5   LED row, 6mm pitch centered
#  y=93.5+  WH1-6 left column, WH7-12 right column (avoid LED x-range)
#  y=101.5  LED current-limit resistors vertical under each LED
#  y=108.5  power chain D3, FB1, D1 horizontal (y=108.5 gives pads at y=108.5)
#  y=108.5  U1 SOIC (pads y=106.6 to 110.4)
#  y=108.5  R3, R4 CC resistors vertical right of U1
#  y=113.5  R5, R6, R7 CFG resistors horizontal (pads y=113.5)
#  y=116.5  test points TP1-6 (2x2 pad, center y=116.5, edges 115.5-117.5)
#  y=115.5  mounting holes H3, H4

LAYOUT = {
    # ref:    (x,     y,     rot)
    'H1':    ( 65.5,  89.5,   0),
    'H2':    (147.5,  89.5,   0),
    'H3':    ( 65.5, 115.5,   0),
    'H4':    (147.5, 115.5,   0),

    # Wire holes: left (source) at x=68.5, right (device) at x=144.5
    # 2.54mm pitch, 6 holes spanning y=93.5 to 106.2
    'WH1':   ( 68.5,  93.50,  0),  'WH7':  (144.5,  93.50, 0),
    'WH2':   ( 68.5,  96.04,  0),  'WH8':  (144.5,  96.04, 0),
    'WH3':   ( 68.5,  98.58,  0),  'WH9':  (144.5,  98.58, 0),
    'WH4':   ( 68.5, 101.12,  0),  'WH10': (144.5, 101.12, 0),
    'WH5':   ( 68.5, 103.66,  0),  'WH11': (144.5, 103.66, 0),
    'WH6':   ( 68.5, 106.20,  0),  'WH12': (144.5, 106.20, 0),

    # LED row at y=93.5, 6mm pitch. Board center x = 106.5.
    # Order on board (L->R): LED1(PWR) LED2(DATA) LED7(PG) LED3(5V) LED4(9V) LED5(12V) LED6(20V)
    'LED1':  ( 88.5,  93.5,  0),
    'LED2':  ( 94.5,  93.5,  0),
    'LED7':  (100.5,  93.5,  0),
    'LED3':  (106.5,  93.5,  0),
    'LED4':  (112.5,  93.5,  0),
    'LED5':  (118.5,  93.5,  0),
    'LED6':  (124.5,  93.5,  0),

    # LED current-limit resistors at y=101.5 vertical (rot=90)
    # R pads at y=97.69 and y=105.31, x centered under each LED
    'R1':    ( 88.5, 101.5,  90),  # LED1 (VBUS -> LED1_A -> GND via LED1)
    'R2':    ( 94.5, 101.5,  90),  # LED2 (VBUS -> LED2_A -> GND via LED2)
    'R12':   (100.5, 101.5,  90),  # LED7 PG indicator (PG -> LED7_A -> GND via LED7)
    'R8':    (106.5, 101.5,  90),  # LED3 FLAG_5V
    'R9':    (112.5, 101.5,  90),  # LED4 FLAG_9V
    'R10':   (118.5, 101.5,  90),  # LED5 FLAG_12V
    'R11':   (124.5, 101.5,  90),  # LED6 FLAG_20V

    # Power chain at y=108.5 horizontal (rot=0), left portion of board
    # D3 (DO-15, 12.7mm pitch): pads at x = center +/- 6.35
    # FB1 (axial, 7.62mm pitch): pads at center +/- 3.81
    # D1 (DO-41, 7.62mm pitch): pads at center +/- 3.81
    'D3':    ( 77.5, 108.5,   0),  # pads x=71.15 (VBUS_IN, connects WH1), 83.85 (to FB1)
    'FB1':   ( 91.5, 108.5,   0),  # pads x=87.69 (VBUS_IN from D3), 95.31 (VBUS)
    'D1':    (101.5, 108.5,   0),  # pads x=97.69 (VBUS_IN... wait, D1 net is VBUS_IN->VBUS)

    # U1 SOIC-8 at center-right at y=108.5
    # Pads x=110, x=115; y=106.595 to 110.405 (SOIC pitch 1.27mm)
    'U1':    (112.5, 108.5,   0),

    # CC resistors vertical between U1 and right WH column
    'R3':    (122.5, 108.5,  90),  # CC1_SRC (pads y=104.69, 112.31)
    'R4':    (128.5, 108.5,  90),  # CC2_SRC

    # CFG resistors horizontal at y=113.5, left of U1 area
    # 7.62mm pitch, fit three in x = 72.5, 82.5, 92.5 (pads span 68.69-76.31, 78.69-86.31, 88.69-96.31)
    'R5':    ( 72.5, 113.5,   0),  # CFG3 (U1 pin 1)
    'R6':    ( 82.5, 113.5,   0),  # CFG2 (U1 pin 2)
    'R7':    ( 92.5, 113.5,   0),  # CFG1 (U1 pin 3)

    # Test points at y=116.5 (2x2 pads, 1mm edge margin from bottom 118.5)
    # Spread across board x=75 to 140
    'TP1':   ( 75.0, 116.5,   0),  # VBUS_IN
    'TP2':   ( 88.0, 116.5,   0),  # VBUS
    'TP3':   (101.0, 116.5,   0),  # GND
    'TP4':   (114.0, 116.5,   0),  # DP_SRC (NC in our design but TP retained)
    'TP5':   (127.0, 116.5,   0),  # DM_SRC (NC)
    'TP6':   (140.0, 116.5,   0),  # PG
}

def main():
    # Safety: ensure KiCad not holding the file
    for lck in ['~PV-THT-V2-CANONICAL.kicad_pcb.lck', '~PV-THT-V2-CANONICAL.kicad_pro.lck']:
        if os.path.exists(lck):
            print(f"ERROR: {lck} exists - close KiCad before running this script")
            sys.exit(1)

    if not os.path.exists(PCB):
        print(f"ERROR: {PCB} not found in {os.getcwd()}")
        sys.exit(1)

    # Backup
    backup = f"{PCB}.pre-reflow-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy2(PCB, backup)
    print(f"Backup saved: {backup}")

    with open(PCB) as f:
        text = f.read()

    # ---------- 1. Update Edge.Cuts rectangle ----------
    # Current: (gr_rect (start 62.5 86.5) (end 122.5 116.5) ...)
    # Target:  (gr_rect (start 62.5 86.5) (end 150.5 118.5) ...)
    old_edge = re.compile(
        r'(\(gr_rect\s+\(start\s+62\.5\s+86\.5\)\s+\(end\s+)122\.5\s+116\.5(\)\s*[^)]*\(layer\s+"Edge\.Cuts"\))',
        re.DOTALL
    )
    text, n = old_edge.subn(r'\g<1>150.5 118.5\g<2>', text)
    print(f"Edge.Cuts rectangle updated: {n} replacement(s)")

    # ---------- 2. Reposition footprints ----------
    # Each footprint block starts with (footprint "LIB:NAME"\n\t\t(layer ...)\n\t\t(uuid ...)\n\t\t(at X Y [ROT])
    # We find each footprint, read its Reference property, look up LAYOUT[ref], and rewrite the (at ...) line.
    moves = 0
    skipped = []
    def rewrite_footprint(match):
        nonlocal moves
        block = match.group(0)
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        if not ref_m:
            return block
        ref = ref_m.group(1)
        if ref not in LAYOUT:
            skipped.append(ref)
            return block
        nx, ny, nrot = LAYOUT[ref]
        # Replace only the FIRST (at ...) in this footprint block (footprint position, not pad positions)
        # The first (at ...) appears immediately after (uuid ...) at footprint-header level
        # We anchor on the footprint header pattern
        new_at = f'(at {nx} {ny} {nrot})' if nrot else f'(at {nx} {ny})'
        # Replace the footprint's own (at ...) - it's at indentation level \t\t (2 tabs)
        # Match only the first occurrence inside this block
        pattern = re.compile(r'(\t\t)\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\s*\)')
        new_block, sub_n = pattern.subn(r'\1' + new_at, block, count=1)
        if sub_n:
            moves += 1
            return new_block
        return block

    # Find footprint blocks. They're at indent level \t (1 tab) and balanced-paren.
    # We'll do a manual balanced-paren scan.
    out = []
    i = 0
    while i < len(text):
        j = text.find('\n\t(footprint ', i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j+1])  # include the newline before footprint
        # Find matching close paren
        depth = 0
        k = j + 1  # start at the (
        while k < len(text):
            if text[k] == '(':
                depth += 1
            elif text[k] == ')':
                depth -= 1
                if depth == 0:
                    k += 1
                    break
            k += 1
        block = text[j+1:k]  # the footprint ... ) block
        new_block = rewrite_footprint(re.match(r'.*', block, re.DOTALL))
        out.append(new_block)
        i = k

    text = ''.join(out)
    print(f"Footprints repositioned: {moves}")
    if skipped:
        print(f"WARNING: no layout entry for: {skipped}")

    # ---------- 3. Strip all traces (segments) and vias ----------
    # (segment (start ...) (end ...) ... (layer ...) ... (net N))
    before_len = len(text)
    text = re.sub(r'\n\t\(segment\b(?:[^()]*|\([^()]*\))*\)', '', text)
    text = re.sub(r'\n\t\(via\b(?:[^()]*|\([^()]*\))*\)', '', text)
    # Arc traces too
    text = re.sub(r'\n\t\(arc\b(?:[^()]*|\([^()]*\))*\)', '', text)
    print(f"Traces/vias/arcs stripped: removed {before_len - len(text)} bytes")

    # ---------- 4. Strip copper zones ----------
    # (zone ... ) blocks at top-level indent. Use balanced scanner.
    out = []
    i = 0
    zones_removed = 0
    while i < len(text):
        j = text.find('\n\t(zone', i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        # find end of this zone block
        depth = 0
        k = j + 1
        while k < len(text):
            if text[k] == '(':
                depth += 1
            elif text[k] == ')':
                depth -= 1
                if depth == 0:
                    k += 1
                    break
            k += 1
        zones_removed += 1
        i = k
    text = ''.join(out)
    print(f"Copper zones stripped: {zones_removed}")

    # ---------- Write ----------
    with open(PCB, 'w') as f:
        f.write(text)
    print(f"\nWrote {PCB}")
    print(f"Backup at:  {backup}")
    print("\nOpen in KiCad: the board will be 88x32mm with clean rows.")
    print("Expected state: no traces, no zones, all parts placed, ratsnest showing connections.")

if __name__ == '__main__':
    main()
