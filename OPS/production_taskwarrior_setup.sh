#!/usr/bin/env bash
# =============================================================================
# ZKNOT — Production Cycle Tasks (2026-05-07 onward)
# =============================================================================
#
# Adds Taskwarrior tasks for the immediate production push:
#   - Resin mix and pour cycle for first 5 units
#   - Supplies acquisition (zip ties, shipping materials)
#   - First-batch ship-out tasks
#   - Recipient assignment + Shopify updates
#
# Usage:
#   bash this_script.sh
# =============================================================================

set -e

echo "=== ZKNOT Production Cycle Tasks ==="
echo "Adding tasks to Taskwarrior..."
echo ""

# -----------------------------------------------------------------------------
# IMMEDIATE: This week's production cycle
# -----------------------------------------------------------------------------

# Resin pour for first 5 units
task add "Mix resin pot 1 (EpoxAcast 690, 100A:30B + glitter)" \
    project:zknot.production \
    workstream:hw \
    priority:H \
    due:2026-05-08 \
    +pour +rev1

task add "Pour PV1-00001 in mold (chain pos 5, ZK-HFZZ-PKZ)" \
    project:zknot.production \
    workstream:hw \
    priority:H \
    due:2026-05-08 \
    +pour +rev1 +PV1-00001

task add "Demold + trim PV1-00001 after 24h cure" \
    project:zknot.production \
    workstream:hw \
    priority:H \
    due:2026-05-09 \
    +demold +rev1 +PV1-00001

task add "PUF photograph + enroll PV1-00001" \
    project:zknot.production \
    workstream:sw \
    priority:H \
    due:2026-05-09 \
    +puf +rev1 +PV1-00001

# Repeat block for PV1-00002 through PV1-00005
for sn in PV1-00002 PV1-00003 PV1-00004 PV1-00005; do
    task add "Pour ${sn} in mold" \
        project:zknot.production \
        workstream:hw \
        priority:H \
        due:2026-05-10 \
        +pour +rev1 +${sn}
    task add "Demold + trim ${sn} after 24h cure" \
        project:zknot.production \
        workstream:hw \
        priority:H \
        due:2026-05-11 \
        +demold +rev1 +${sn}
    task add "PUF photograph + enroll ${sn}" \
        project:zknot.production \
        workstream:sw \
        priority:H \
        due:2026-05-11 \
        +puf +rev1 +${sn}
done

# -----------------------------------------------------------------------------
# SUPPLIES RUN
# -----------------------------------------------------------------------------

task add "Buy more zip ties for pigtail strain relief (small, ~3-4 inch)" \
    project:zknot.production \
    workstream:ops \
    priority:H \
    due:2026-05-08 \
    cost:15 \
    +supplies +hardware

task add "Buy padded mailers or small boxes (~110x50x20mm interior, qty 25)" \
    project:zknot.production \
    workstream:ops \
    priority:H \
    due:2026-05-08 \
    cost:25 \
    +supplies +shipping

task add "Buy anti-static bags or kraft paper sleeves (qty 25)" \
    project:zknot.production \
    workstream:ops \
    priority:M \
    due:2026-05-08 \
    cost:15 \
    +supplies +shipping

task add "Buy tamper-evident packaging seals (Brady VOID labels or equiv)" \
    project:zknot.production \
    workstream:ops \
    priority:M \
    due:2026-05-08 \
    cost:20 \
    +supplies +shipping

task add "Print/buy USPS Priority shipping labels for first 5 units" \
    project:zknot.production \
    workstream:ops \
    priority:M \
    due:2026-05-12 \
    +supplies +shipping

# -----------------------------------------------------------------------------
# RECIPIENT DECISIONS (must be made before shipping)
# -----------------------------------------------------------------------------

task add "Decide recipients for PV1-00001 through PV1-00005 (5 names + addresses)" \
    project:zknot.production \
    workstream:biz \
    priority:H \
    due:2026-05-09 \
    +recipients +rev1

task add "Draft 'this is Rev 1 - please send feedback' email template for pilot recipients" \
    project:zknot.production \
    workstream:biz \
    priority:H \
    due:2026-05-09 \
    +recipients +rev1

# -----------------------------------------------------------------------------
# QC + SHIPPING
# -----------------------------------------------------------------------------

task add "QC scan QR codes for PV1-00001..00005, verify all show CHAIN INTACT" \
    project:zknot.production \
    workstream:sw \
    priority:H \
    due:2026-05-12 \
    +qc +rev1

task add "Continuity test PV1-00001..00005 (charge phone, no data enumeration)" \
    project:zknot.production \
    workstream:hw \
    priority:H \
    due:2026-05-12 \
    +qc +rev1

task add "Package PV1-00001..00005 with insert cards + tamper seals" \
    project:zknot.production \
    workstream:ops \
    priority:H \
    due:2026-05-12 \
    +packaging +rev1

task add "Ship PV1-00001..00005 — first PowerVerify units OUT THE DOOR" \
    project:zknot.production \
    workstream:ops \
    priority:H \
    due:2026-05-13 \
    +ship +rev1 +milestone

# -----------------------------------------------------------------------------
# POST-SHIP IMMEDIATE FOLLOWUPS
# -----------------------------------------------------------------------------

task add "Update Shopify listing: remove 'ships June 30' pre-order language" \
    project:zknot.production \
    workstream:biz \
    priority:H \
    due:2026-05-14 \
    +shopify +marketing

task add "Update Shopify product description: 60W max (NOT 100W)" \
    project:zknot.production \
    workstream:biz \
    priority:H \
    due:2026-05-14 \
    +shopify +marketing

task add "Update Shopify copy to reflect potted Rev 1 with PUF tamper-evidence" \
    project:zknot.production \
    workstream:biz \
    priority:M \
    due:2026-05-14 \
    +shopify +marketing

task add "Reddit followup post with attribution to community contributors" \
    project:zknot.production \
    workstream:biz \
    priority:M \
    due:2026-05-15 \
    +reddit +marketing

# -----------------------------------------------------------------------------
# WEEK 2: Capacity scaling
# -----------------------------------------------------------------------------

task add "Build/buy vacuum chamber for bubble removal (Day 5 commitment)" \
    project:zknot.production \
    workstream:hw \
    priority:H \
    due:2026-05-09 \
    cost:80 \
    +tools +supplies

task add "Print 2-4 additional molds for parallel pour throughput" \
    project:zknot.production \
    workstream:hw \
    priority:M \
    due:2026-05-15 \
    +tools +mold

task add "Pour PV1-00006..00010 (next batch of 5)" \
    project:zknot.production \
    workstream:hw \
    priority:M \
    due:2026-05-16 \
    +pour +rev1 +batch2

task add "Provision PV1-00006..00010 to chain (positions 10-14)" \
    project:zknot.production \
    workstream:sw \
    priority:M \
    due:2026-05-13 \
    +provisioning +rev1 +batch2

# -----------------------------------------------------------------------------
# REV 1 RETROSPECTIVE (after first 10 units shipped)
# -----------------------------------------------------------------------------

task add "Rev 1 retrospective: yield, defects, time-per-unit, recipient feedback" \
    project:zknot.production \
    workstream:ops \
    priority:M \
    due:2026-05-25 \
    +retrospective +rev1

task add "Capture Rev 2 wishlist (silkscreen +20%, charge arrow, ATECC608B, etc)" \
    project:zknot.production \
    workstream:hw \
    priority:M \
    due:2026-05-25 \
    +rev2 +planning

# -----------------------------------------------------------------------------
echo ""
echo "=== Tasks added ==="
echo "Run 'task project:zknot.production' to see them all"
echo "Run 'task project:zknot.production +pour' for pour cycle"
echo "Run 'task project:zknot.production +supplies' for shopping list"
echo "Run 'task project:zknot.production +rev1' for all rev 1 work"
echo "Run 'task ready' for what to work on next"
echo ""
echo "=== Quick views ==="
echo "  Today:     task due:today"
echo "  This week: task due.before:2026-05-15"
echo "  By cost:   task project:zknot.production cost.over:0"
