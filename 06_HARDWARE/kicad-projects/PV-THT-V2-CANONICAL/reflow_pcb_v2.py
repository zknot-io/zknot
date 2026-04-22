#!/usr/bin/env python3
"""
Reflow PowerVerify THT PCB (v2 - fixes rotation + multi-line Edge.Cuts):
  - Resize board to 88 x 32 mm (62.5,86.5 -> 150.5,118.5)
  - Reposition all footprints to a conflict-free layout
  - Strip all traces and copper zones
  - Preserve nets, pads, schematic connectivity

Rotation semantics for R_Axial_DIN0207_*_Horizontal footprint in this file:
  The local pad coordinates are along Y: pad1 (0, -3.81), pad2 (0, 3.81)
  So rot=0 -> pads aligned along Y (vertical body)
     rot=90 -> pads aligned along X (horizontal body)
"""
import re, sys, shutil, os, datetime

PCB = 'PV-THT-V2-CANONICAL.kicad_pcb'

# ============================================================
# TARGET POSITIONS: (x, y, rot)
# ============================================================
# Board: (62.5, 86.5) -> (150.5, 118.5) = 88 x 32mm
#
# Rows:
#  y=89.5   mounting holes H1, H2
#  y=93.5   LED row, 6mm pitch centered
#           WH1-6 left column (x=68.5), WH7-12 right column (x=144.5)
#  y=101.5  LED current-limit resistors VERTICAL (rot=0) under each LED
#           Pads at y=97.69 and y=105.31
#  y=108.5  Power chain D3, FB1, D1 HORIZONTAL (rot=0 intrinsic is X)
#           U1 SOIC-8 at center-right
#           R3, R4 CC resistors VERTICAL (rot=0) right of U1
#  y=112.5  R5, R6, R7 CFG resistors HORIZONTAL (rot=90) left of U1
#  y=116.5  Test points TP1-6 (2x2 pad, 1mm edge margin)
#  y=115.5  mounting holes H3, H4

LAYOUT = {
    # Mounting
    'H1':    ( 65.5,  89.5,   0),
    'H2':    (147.5,  89.5,   0),
    'H3':    ( 65.5, 115.5,   0),
    'H4':    (147.5, 115.5,   0),

    # Wire holes
    'WH1':   ( 68.5,  93.50,  0),  'WH7':  (144.5,  93.50, 0),
    'WH2':   ( 68.5,  96.04,  0),  'WH8':  (144.5,  96.04, 0),
    'WH3':   ( 68.5,  98.58,  0),  'WH9':  (144.5,  98.58, 0),
    'WH4':   ( 68.5, 101.12,  0),  'WH10': (144.5, 101.12, 0),
    'WH5':   ( 68.5, 103.66,  0),  'WH11': (144.5, 103.66, 0),
    'WH6':   ( 68.5, 106.20,  0),  'WH12': (144.5, 106.20, 0),

    # LED row - 6mm pitch centered at board-center x=106.5
    'LED1':  ( 88.5,  93.5,  0),
    'LED2':  ( 94.5,  93.5,  0),
    'LED7':  (100.5,  93.5,  0),
    'LED3':  (106.5,  93.5,  0),
    'LED4':  (112.5,  93.5,  0),
    'LED5':  (118.5,  93.5,  0),
    'LED6':  (124.5,  93.5,  0),

    # LED current-limit resistors - VERTICAL under each LED (rot=0)
    # Pads at y=97.69 (top, connects to LED cathode-side) and y=105.31 (bottom, to VBUS/rail)
    'R1':    ( 88.5, 101.5,   0),  # VBUS->LED1_A
    'R2':    ( 94.5, 101.5,   0),  # VBUS->LED2_A
    'R12':   (100.5, 101.5,   0),  # PG->LED7_A
    'R8':    (106.5, 101.5,   0),  # FLAG_5V
    'R9':    (112.5, 101.5,   0),  # FLAG_9V
    'R10':   (118.5, 101.5,   0),  # FLAG_12V
    'R11':   (124.5, 101.5,   0),  # FLAG_20V

    # Power chain (D3, FB1, D1 are horizontal footprints with local pads along X)
    # rot=0 gives horizontal body - good
    'D3':    ( 77.5, 108.5,   0),  # DO-15 12.7mm pitch: pads (71.15, 108.5) / (83.85, 108.5)
    'FB1':   ( 91.5, 108.5,   0),  # 7.62mm pitch:       pads (87.69, 108.5) / (95.31, 108.5)
    'D1':    (101.5, 108.5,   0),  # 7.62mm pitch:       pads (97.69, 108.5) / (105.31, 108.5)

    # U1 SOIC-8 at (112.5, 108.5)
    'U1':    (112.5, 108.5,   0),

    # CC resistors VERTICAL right of U1
    'R3':    (122.5, 108.5,   0),  # pads y=104.69, y=112.31
    'R4':    (128.5, 108.5,   0),

    # CFG resistors HORIZONTAL (rot=90), spread across bottom-left
    # Pads along X at ±3.81 from center, all at y=112.5
    'R5':    ( 70.0, 112.5,  90),  # pads (66.19, 112.5) / (73.81, 112.5)
    'R6':    ( 85.0, 112.5,  90),  # pads (81.19, 112.5) / (88.81, 112.5)
    'R7':    (100.0, 112.5,  90),  # pads (96.19, 112.5) / (103.81, 112.5)

    # Test points at y=116.5 - 2x2 SMD pads, 1mm from bottom edge at y=118.5
    'TP1':   ( 75.0, 116.5,   0),
    'TP2':   ( 88.0, 116.5,   0),
    'TP3':   (101.0, 116.5,   0),
    'TP4':   (114.0, 116.5,   0),
    'TP5':   (127.0, 116.5,   0),
    'TP6':   (140.0, 116.5,   0),
}

def main():
    for lck in ['~PV-THT-V2-CANONICAL.kicad_pcb.lck', '~PV-THT-V2-CANONICAL.kicad_pro.lck']:
        if os.path.exists(lck):
            print(f"ERROR: {lck} exists - close KiCad before running this script")
            sys.exit(1)

    if not os.path.exists(PCB):
        print(f"ERROR: {PCB} not found in {os.getcwd()}")
        sys.exit(1)

    backup = f"{PCB}.pre-reflow-v2-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy2(PCB, backup)
    print(f"Backup saved: {backup}")

    with open(PCB) as f:
        text = f.read()

    # ---------- 1. Update Edge.Cuts rectangle (multi-line aware) ----------
    # Match: (gr_rect\n\t\t(start 62.5 86.5)\n\t\t(end X Y)\n ... (layer "Edge.Cuts") ...)
    # Replace only the (end ...) line inside the Edge.Cuts rect block
    # Strategy: find the gr_rect block whose (layer ...) is "Edge.Cuts", replace its (end ...) line

    def replace_edge_cuts(text):
        # Walk gr_rect blocks
        new_parts = []
        i = 0
        replacements = 0
        while True:
            j = text.find('(gr_rect', i)
            if j < 0:
                new_parts.append(text[i:])
                break
            # Find end of this gr_rect block (balanced parens)
            depth = 0
            k = j
            while k < len(text):
                if text[k] == '(':
                    depth += 1
                elif text[k] == ')':
                    depth -= 1
                    if depth == 0:
                        k += 1
                        break
                k += 1
            block = text[j:k]
            if '"Edge.Cuts"' in block:
                # Replace the (end X Y) line
                new_block = re.sub(
                    r'\(end\s+[-\d.]+\s+[-\d.]+\s*\)',
                    '(end 150.5 118.5)',
                    block, count=1
                )
                if new_block != block:
                    replacements += 1
                new_parts.append(text[i:j])
                new_parts.append(new_block)
            else:
                new_parts.append(text[i:k])
            i = k
        return ''.join(new_parts), replacements

    text, n = replace_edge_cuts(text)
    print(f"Edge.Cuts rectangle updated: {n} replacement(s)")

    # ---------- 2. Reposition footprints ----------
    moves = 0
    skipped = []
    out = []
    i = 0
    while i < len(text):
        j = text.find('\n\t(footprint ', i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j+1])
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
        block = text[j+1:k]

        # Extract reference
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        if ref_m and ref_m.group(1) in LAYOUT:
            ref = ref_m.group(1)
            nx, ny, nrot = LAYOUT[ref]
            new_at = f'(at {nx} {ny} {nrot})' if nrot else f'(at {nx} {ny})'
            new_block, sub_n = re.subn(
                r'(\t\t)\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\s*\)',
                r'\1' + new_at,
                block, count=1
            )
            if sub_n:
                moves += 1
                out.append(new_block)
            else:
                out.append(block)
        else:
            if ref_m:
                skipped.append(ref_m.group(1))
            out.append(block)
        i = k

    text = ''.join(out)
    print(f"Footprints repositioned: {moves}")
    if skipped:
        print(f"WARNING: no layout entry for: {skipped}")

    # ---------- 3. Strip traces (segments), vias, arcs ----------
    before = len(text)
    # Balanced-paren strip for each type
    for token in ['segment', 'via', 'arc']:
        out = []
        i = 0
        removed = 0
        while i < len(text):
            j = text.find(f'\n\t({token} ', i)
            if j < 0:
                out.append(text[i:])
                break
            out.append(text[i:j])
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
            removed += 1
            i = k
        text = ''.join(out)
        if removed:
            print(f"  {token}s removed: {removed}")
    print(f"Total trace/via/arc bytes removed: {before - len(text)}")

    # ---------- 4. Strip copper zones ----------
    out = []
    i = 0
    zones_removed = 0
    while i < len(text):
        j = text.find('\n\t(zone', i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
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

    with open(PCB, 'w') as f:
        f.write(text)
    print(f"\nWrote {PCB}")
    print(f"Backup at:  {backup}")

if __name__ == '__main__':
    main()
