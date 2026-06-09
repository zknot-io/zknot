#!/usr/bin/env bash
# =============================================================================
# ZKNOT — Incremental Production Tasks (evening of 2026-05-07)
# =============================================================================
#
# These are ONLY the tasks NOT already covered by tasks 72-79 you added
# earlier today for the v5 mold workflow. Skipping all the:
#   - Slice and print mold (already task 72)
#   - Print cable shims (already task 73)
#   - Dry-fit (already task 74)
#   - Water test (already task 75)
#   - First pour (already task 76)
#   - Plug release method (already task 77)
#   - PCB orientation decision (already task 78)
#   - Source sacrificial USB-C cables (already task 79, zknot.ops)
#
# What's NEW: supplies, recipient decisions, post-pour processing for
# units 2-5, packaging, ship, Shopify updates.
# =============================================================================

set -e

echo "=== ZKNOT Incremental Production Tasks ==="
echo ""

# -----------------------------------------------------------------------------
# IMMEDIATE SUPPLIES RUN
# -----------------------------------------------------------------------------

task add "Buy more zip ties for pigtail strain relief" \
    project:zknot.ops workstream:ops priority:H \
    due:2026-05-08 cost:15 \
    +supplies +hardware

task add "Buy padded mailers ~110x50x20mm interior, qty 10" \
    project:zknot.ops workstream:ops priority:H \
    due:2026-05-08 cost:25 \
    +supplies +shipping

task add "Buy anti-static bags or kraft paper sleeves, qty 10" \
    project:zknot.ops workstream:ops priority:M \
    due:2026-05-08 cost:15 \
    +supplies +shipping

task add "Buy tamper-evident packaging seals (Brady VOID or equiv)" \
    project:zknot.ops workstream:ops priority:M \
    due:2026-05-08 cost:20 \
    +supplies +shipping

# -----------------------------------------------------------------------------
# PER-UNIT POURS FOR PV1-00002 THROUGH PV1-00005
# (PV1-00001 first pour already covered by task 76)
# -----------------------------------------------------------------------------

for sn in PV1-00002 PV1-00003 PV1-00004 PV1-00005; do
    task add "Pour ${sn} in v5 mold" \
        project:zknot.hw workstream:hw priority:H \
        +pour +rev1 +${sn}
    task add "Demold + trim sacrificial plug for ${sn}" \
        project:zknot.hw workstream:hw priority:H \
        +demold +rev1 +${sn}
    task add "PUF photograph + enroll ${sn} via API" \
        project:zknot.sw workstream:sw priority:H \
        +puf +rev1 +${sn}
done

# -----------------------------------------------------------------------------
# RECIPIENT DECISIONS (must be made before shipping)
# -----------------------------------------------------------------------------

task add "Decide recipients for PV1-00001..00005 (5 names + addresses)" \
    project:zknot.biz workstream:biz priority:H \
    due:2026-05-09 \
    +recipients +rev1

task add "Capture pilot recipient list in ~/ZKNOT/3_OPS/journal/2026-05-07_pilot_recipients.md" \
    project:zknot.biz workstream:biz priority:H \
    due:2026-05-09 \
    +recipients +rev1

task add "Draft 'Rev 1 pilot - please send feedback' email template for recipients" \
    project:zknot.biz workstream:biz priority:H \
    due:2026-05-10 \
    +recipients +rev1

# -----------------------------------------------------------------------------
# QC + SHIPPING
# -----------------------------------------------------------------------------

task add "QC scan QR codes PV1-00001..00005, verify CHAIN INTACT for each" \
    project:zknot.sw workstream:sw priority:H \
    +qc +rev1

task add "Continuity test PV1-00001..00005: charge phone, no data enumeration" \
    project:zknot.hw workstream:hw priority:H \
    +qc +rev1

task add "Package PV1-00001..00005 with insert cards + tamper seals" \
    project:zknot.ops workstream:ops priority:H \
    +packaging +rev1

task add "Ship PV1-00001..00005 — first PowerVerify units OUT THE DOOR" \
    project:zknot.ops workstream:ops priority:H \
    +ship +rev1 +milestone

# -----------------------------------------------------------------------------
# POST-SHIP IMMEDIATE FOLLOWUPS
# -----------------------------------------------------------------------------

task add "Update Shopify: remove 'ships June 30' pre-order language" \
    project:zknot.biz workstream:biz priority:H \
    +shopify +marketing

task add "Update Shopify: change 100W max to 60W max (GCT 3A rating)" \
    project:zknot.biz workstream:biz priority:H \
    +shopify +marketing

task add "Update Shopify copy to reflect potted Rev 1 with PUF tamper-evidence" \
    project:zknot.biz workstream:biz priority:M \
    +shopify +marketing

task add "Reddit followup post with attribution to community contributors" \
    project:zknot.biz workstream:biz priority:M \
    +reddit +marketing

# -----------------------------------------------------------------------------
# DEPENDENCY CHAIN — link new tasks to existing 72-79
# -----------------------------------------------------------------------------

echo ""
echo "=== After running, set up dependency chain ==="
echo "Get the new task IDs:"
echo "  task project:zknot.hw entry.after:today list"
echo "  task project:zknot.ops entry.after:today list"
echo ""
echo "Then chain them. Example pattern (substitute actual IDs):"
echo "  # Pour 00002 depends on first pour (task 76) being done"
echo "  task <pour-00002-id> modify depends:76"
echo "  task <pour-00003-id> modify depends:<pour-00002-id>"
echo "  ..."
echo "  # QC + package + ship chain"
echo "  task <qc-id> modify depends:<all-pour-ids>"
echo "  task <package-id> modify depends:<qc-id>"
echo "  task <ship-id> modify depends:<package-id>"
echo ""
echo "=== Quick views ==="
echo "  task project:zknot.hw +pour       # all pour tasks"
echo "  task project:zknot.ops +supplies  # shopping list"
echo "  task project:zknot.biz +shopify   # post-ship Shopify updates"
echo "  task ready                        # whatever's unblocked NOW"
