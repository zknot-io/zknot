#!/usr/bin/env python3
"""
Targeted fix for remaining DRC shorting errors:
  - R1, R2: rotate 90 (their local pads are along X, need to be along Y)
  - R3, R4: move right to clear R11 diagonal
"""
import re, sys, shutil, os, datetime

PCB = 'PV-THT-V2-CANONICAL.kicad_pcb'

FIXES = {
    # ref:    (x, y, rot)
    'R1':   (88.5, 101.5, 90),   # was rot=0 -> horizontal pads; 90 -> vertical pads
    'R2':   (94.5, 101.5, 90),
    'R3':  (130.0, 108.5,  0),   # was x=122.5; move 7.5mm right
    'R4':  (136.0, 108.5,  0),   # was x=128.5; move 7.5mm right
}

def main():
    for lck in ['~PV-THT-V2-CANONICAL.kicad_pcb.lck', '~PV-THT-V2-CANONICAL.kicad_pro.lck']:
        if os.path.exists(lck):
            print(f"ERROR: {lck} exists - close KiCad"); sys.exit(1)
    if not os.path.exists(PCB):
        print(f"ERROR: {PCB} not found"); sys.exit(1)

    backup = f"{PCB}.fix-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy2(PCB, backup)
    print(f"Backup: {backup}")

    with open(PCB) as f:
        text = f.read()

    moves = 0
    out = []
    i = 0
    while i < len(text):
        j = text.find('\n\t(footprint ', i)
        if j < 0:
            out.append(text[i:]); break
        out.append(text[i:j+1])
        depth = 0; k = j + 1
        while k < len(text):
            if text[k] == '(': depth += 1
            elif text[k] == ')':
                depth -= 1
                if depth == 0: k += 1; break
            k += 1
        block = text[j+1:k]
        ref_m = re.search(r'"Reference"\s+"([^"]+)"', block)
        if ref_m and ref_m.group(1) in FIXES:
            ref = ref_m.group(1)
            nx, ny, nrot = FIXES[ref]
            new_at = f'(at {nx} {ny} {nrot})' if nrot else f'(at {nx} {ny})'
            new_block, n = re.subn(
                r'(\t\t)\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\s*\)',
                r'\1' + new_at,
                block, count=1
            )
            if n:
                moves += 1
                print(f"  {ref} -> ({nx}, {ny}, rot={nrot})")
            out.append(new_block)
        else:
            out.append(block)
        i = k

    text = ''.join(out)
    print(f"Moves applied: {moves}")

    with open(PCB, 'w') as f:
        f.write(text)
    print(f"Wrote {PCB}")
    print(f"Backup: {backup}")

if __name__ == '__main__':
    main()
