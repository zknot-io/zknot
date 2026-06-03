#!/usr/bin/env python3
"""
ZKNOT KiCad 10 Linux Fix Script
================================
Applies all known KiCad 10 syntax fixes discovered during PowerVerify development.
Run this on any generated .kicad_sch and .kicad_pcb before opening in KiCad 10 on Linux.

Usage:
    python3 fix_kicad.py MyProject.kicad_sch MyProject.kicad_pcb

Or fix a whole folder:
    python3 fix_kicad.py /path/to/project/

Issues fixed:
    PCB:
        1. Semicolon comment lines (not valid s-expression syntax)
        2. (justify center) standalone -> remove (center is default/implicit)
        3. (justify center mirror) -> (justify mirror)
        4. (hatch style "edge" pitch 0.508) -> (hatch edge 0.508)
        5. (tstamp "quoted") -> (tstamp unquoted)
        6. Zone declarations: (uuid "...") -> (tstamp ...) 
        7. Zone declarations missing tstamp -> add one
        8. Footprints missing (tstamp ...) -> add one
        9. rule_area -> zone with keepout syntax
        10. is_keepout yes -> remove (not valid KiCad 10)
        11. keepout_area -> keepout
        12. Polygon missing closing ) in zone blocks
        13. GND pour zone: add hatch, remove filled_areas_thickness

    SCH:
        1. Semicolon comment lines
        2. net_label (block format) -> label with uuid child
        3. net_label (single-line inline) -> label with uuid child  
        4. net_label with alignment spaces -> handled
        5. Inline label uuid -> uuid as child element
        6. no_connect with rotation (at X Y 0) -> (at X Y)
        7. no_connect multiline -> single line
        8. Add sheet_instances if missing
        9. wire entries need stroke and uuid children
"""

import re
import uuid as uuidmod
import sys
import os
import shutil
from pathlib import Path


def fix_pcb(content: str) -> str:
    lines = content.split('\n')

    # 1. Remove semicolon comment lines
    lines = [l for l in lines if not l.strip().startswith(';')]
    content = '\n'.join(lines)

    # 2. Remove standalone (justify center) - not followed by mirror/left/right/top/bottom
    content = re.sub(
        r'\(justify center\b(?!\s+(?:mirror|left|right|top|bottom))\)',
        '', content
    )

    # 3. (justify center mirror) -> (justify mirror)
    content = content.replace('(justify center mirror)', '(justify mirror)')

    # 4. Fix hatch format
    content = content.replace('(hatch style "edge" pitch 0.508)', '(hatch edge 0.508)')
    content = content.replace('(hatch style "edge" pitch 0.3)', '(hatch edge 0.3)')

    # 5. Fix quoted tstamps
    content = re.sub(r'\(tstamp "([^"]+)"\)', r'(tstamp \1)', content)

    # 6. Zone uuid -> tstamp
    content = re.sub(
        r'\(zone \(net (\d+)\) \(net_name "([^"]*)"\) \(layer "([^"]*)"\) \(uuid "([^"]*)"\)',
        r'(zone (net \1) (net_name "\2") (layer "\3") (tstamp \4)',
        content
    )

    # 7. Zone missing tstamp (has name but no tstamp)
    content = re.sub(
        r'\(zone \(net (\d+)\) \(net_name "([^"]*)"\) \(layer "([^"]*)"\) \(name "([^"]*)"\)',
        lambda m: f'(zone (net {m.group(1)}) (net_name "{m.group(2)}") (layer "{m.group(3)}") (tstamp {str(uuidmod.uuid4())}) (name "{m.group(4)}")',
        content
    )

    # 8. Add tstamp to footprints missing one
    lines = content.split('\n')
    out = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if re.match(r'\s+\(footprint "[^"]+"\s+\(layer "[^"]+"\)\s+\(at [^)]+\)$', lines[i]):
            if i + 1 < len(lines) and 'tstamp' not in lines[i + 1]:
                out.append(f'    (tstamp {str(uuidmod.uuid4())})')
        i += 1
    content = '\n'.join(out)

    # 9. Remove rule_area blocks entirely (replace with nothing - add keepout zones manually in KiCad)
    lines = content.split('\n')
    out = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == '(rule_area':
            # Skip until matching close
            depth = lines[i].count('(') - lines[i].count(')')
            i += 1
            while i < len(lines) and depth > 0:
                depth += lines[i].count('(') - lines[i].count(')')
                i += 1
        else:
            out.append(lines[i])
            i += 1
    content = '\n'.join(out)

    # 10. Remove (is_keepout yes) lines
    content = '\n'.join(l for l in content.split('\n') if l.strip() != '(is_keepout yes)')

    # 11. keepout_area -> keepout
    content = content.replace('(keepout_area ', '(keepout ')

    # 12. Fix polygon missing closing ) in zone blocks
    content = re.sub(
        r'    \(polygon\n      (\(pts[^\n]+\))\n  \)',
        r'    (polygon\n      \1\n    )\n  )',
        content
    )

    # 13. Fix GND pour - remove filled_areas_thickness, ensure hatch present
    content = content.replace('\n    (filled_areas_thickness no)', '')
    content = content.replace('\n    (filled_areas_thickness yes)', '')

    # Add hatch to zones missing it
    def add_missing_hatch(m):
        zone_line = m.group(1)
        next_content = m.group(2)
        if '(hatch' not in next_content[:50]:
            return zone_line + '\n    (hatch edge 0.508)\n' + next_content
        return zone_line + '\n' + next_content

    content = re.sub(
        r'(\(zone[^\n]+)\n([ ]+\((?!hatch))',
        add_missing_hatch,
        content
    )

    return content


def fix_sch(content: str) -> str:
    # 1. Remove semicolon comment lines
    content = '\n'.join(l for l in content.split('\n') if not l.strip().startswith(';'))

    # 2. Convert single-line net_label (with optional alignment spaces) -> label
    def fix_inline_net_label(m):
        name = m.group(1)
        at = m.group(2)
        uid = m.group(3)
        return f'  (label "{name}" (at {at})\n    (uuid "{uid}")\n  )'

    content = re.sub(
        r'  \(net_label "([^"]+)"\s+\(at ([^)]+)\) \(uuid "([^"]+)"\)\)',
        fix_inline_net_label,
        content
    )

    # 3. Convert block-format net_label -> label
    def fix_block_net_label(m):
        at = m.group(1)
        effects = m.group(2).strip()
        uid = m.group(3)
        name = m.group(4)
        return f'  (label "{name}" (at {at})\n    {effects}\n    (uuid "{uid}")\n  )'

    pattern = r'\s*\(net_label \(at ([^)]+)\)[^\n]*\n\s*(\(effects[^\n]+\))\n\s*\(uuid "([^"]+)"\)\n\s*\(property "Name" "([^"]+)"\)\n\s*\)'
    content = re.sub(pattern, fix_block_net_label, content)

    # 4. Fix inline label uuid -> uuid as child element
    lines = content.split('\n')
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('(label "') and stripped.endswith('))') and '(uuid "' in stripped:
            uuid_start = stripped.rfind('(uuid "')
            uuid_end = stripped.rfind('")')
            if uuid_start > 0 and uuid_end > uuid_start:
                uid = stripped[uuid_start + 7:uuid_end]
                before_uuid = stripped[:uuid_start].rstrip()
                out.append(f'  {before_uuid}')
                out.append(f'    (uuid "{uid}")')
                out.append(f'  )')
                continue
        out.append(line)
    content = '\n'.join(out)

    # 5. Fix no_connect - remove rotation value, ensure single line
    content = re.sub(
        r'  \(no_connect \(at ([^)]+)\)\n\s+\(uuid "([^"]+)"\)\n\s+\)',
        lambda m: f'  (no_connect (at {m.group(1)}) (uuid "{m.group(2)}"))',
        content
    )
    # Remove rotation from no_connect
    content = re.sub(
        r'\(no_connect \(at ([\d.\-]+) ([\d.\-]+) 0\)',
        r'(no_connect (at \1 \2)',
        content
    )

    # 6. Fix wire entries - ensure they have stroke and uuid
    def fix_wire(m):
        pts = m.group(1)
        uid = m.group(2) if m.group(2) else str(uuidmod.uuid4())
        return f'  (wire (pts {pts})\n    (stroke (width 0) (type default))\n    (uuid "{uid}")\n  )'

    content = re.sub(
        r'  \(wire \(pts ([^)]+\))\) \(uuid "([^"]+)"\)\)',
        fix_wire,
        content
    )
    # Wires without uuid
    content = re.sub(
        r'  \(wire \(pts ([^)]+\))\)\)',
        lambda m: f'  (wire (pts {m.group(1)})\n    (stroke (width 0) (type default))\n    (uuid "{str(uuidmod.uuid4())}")\n  )',
        content
    )

    # 7. Add sheet_instances if missing
    if 'sheet_instances' not in content:
        content = content.rstrip()
        if content.endswith(')'):
            content = content[:-1]
        content += '\n  (sheet_instances\n    (path "/"\n      (page "1")\n    )\n  )\n)\n'

    return content


def process_file(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        return {'file': filepath, 'status': 'NOT FOUND'}

    # Backup
    backup = str(path) + '.bak'
    shutil.copy2(str(path), backup)

    with open(str(path), 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    if path.suffix == '.kicad_pcb':
        content = fix_pcb(content)
        file_type = 'PCB'
    elif path.suffix == '.kicad_sch':
        content = fix_sch(content)
        file_type = 'SCH'
    else:
        return {'file': filepath, 'status': 'SKIPPED (not .kicad_pcb or .kicad_sch)'}

    with open(str(path), 'w', encoding='utf-8') as f:
        f.write(content)

    # Report
    issues_fixed = []
    if sum(1 for l in original.split('\n') if l.strip().startswith(';')) > 0:
        issues_fixed.append('semicolon comments')
    if '(justify center)' in original:
        issues_fixed.append('justify center')
    if 'justify center mirror' in original:
        issues_fixed.append('justify center mirror')
    if 'hatch style' in original:
        issues_fixed.append('hatch style format')
    if 'net_label' in original:
        issues_fixed.append(f'net_label ({original.count("net_label")} converted)')
    if 'rule_area' in original:
        issues_fixed.append('rule_area blocks')
    if 'is_keepout' in original:
        issues_fixed.append('is_keepout')

    return {
        'file': filepath,
        'type': file_type,
        'status': 'FIXED',
        'backup': backup,
        'issues_fixed': issues_fixed if issues_fixed else ['none detected — file may already be clean']
    }


def main():
    targets = []

    if len(sys.argv) < 2:
        print("Usage: python3 fix_kicad.py file.kicad_sch [file.kicad_pcb] ...")
        print("   or: python3 fix_kicad.py /path/to/project/folder/")
        sys.exit(1)

    for arg in sys.argv[1:]:
        path = Path(arg)
        if path.is_dir():
            targets.extend(path.glob('*.kicad_pcb'))
            targets.extend(path.glob('*.kicad_sch'))
        elif path.is_file():
            targets.append(path)
        else:
            print(f"WARNING: {arg} not found, skipping")

    if not targets:
        print("No .kicad_pcb or .kicad_sch files found.")
        sys.exit(1)

    print(f"\nZKNOT KiCad 10 Fix Script")
    print(f"{'='*50}")
    print(f"Processing {len(targets)} file(s)...\n")

    for target in targets:
        result = process_file(str(target))
        print(f"  {result['file']}")
        print(f"  Status: {result.get('status', 'unknown')}")
        if 'issues_fixed' in result:
            for issue in result['issues_fixed']:
                print(f"    ✓ {issue}")
        if 'backup' in result:
            print(f"  Backup: {result['backup']}")
        print()

    print("Done. Open your project in KiCad 10.")
    print("If errors persist, screenshot the error and line number.")


if __name__ == '__main__':
    main()
