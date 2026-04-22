# ZKNOT Session Journal Format

**Purpose:** Paste this into any future conversation with Claude at the end of a working session to generate a consistent journal document. The format mirrors the 2026-04-19 to 2026-04-22 journal that worked well.

---

## Paste-in prompt for future Claude

```
Generate a ZKNOT session journal in .docx format following the ZKNOT standard 
journal format. Use the structure below, fill in content from this conversation, 
and produce a downloadable Word document.

Session metadata:
- Date range: [START_DATE] to [END_DATE]
- Session focus: [ONE_LINE_SUMMARY]
- Runway status at end: [E.G. "25 days" OR "post-revenue"]

Required sections:
1. Title block — "ZKNOT INC." / "Session Journal" / date range / 
   tagline "Physics enforces. Math proves. You verify."
2. Executive Summary — 2-3 paragraphs plus a Headlines bullet list of 
   concrete deliverables shipped
3. Day-by-Day Narrative — one H2 per calendar day, H3 subsections for 
   major workstreams within the day
4. Deliverables Produced — grouped by type (Documents, KiCad files, 
   Code, Infrastructure, etc.)
5. Key Decisions Made — table format with Decision / Rationale columns
6. Technical Reference — key schematics, tables, paths, git state at 
   end of session
7. Lessons Learned — split into Technical / Process / Strategic 
   subsections
8. Closing — short paragraph reaffirming progress and the tagline

Formatting requirements:
- Calibri font, headings in navy (#1F3864) for H1, blue (#2E75B6) for H2, 
  dark gray (#333333) for H3
- "Page X of Y" footer per ZKNOT standing preference, with document title 
  and session dates
- US Letter page size (12240 x 15840 DXA) with 1" margins
- Tables use #2E75B6 header row, #BBBBBB cell borders, DXA widths
- Use docx-js, validate with the docx skill's validator before delivering
- Include the "Physics enforces. Math proves. You verify." tagline in 
  the title block and closing

Output file naming: ZKNOT_Session_Journal_[START_DATE]_[END_DATE].docx 
using YYYYMMDD format.

File target location for my notes: ~/ZKNOT/11_KM/session-notes/
```

---

## Section-by-section content guide

This guide tells future Claude WHAT to include in each section based on the 
information available in the conversation.

### 1. Title block
- "ZKNOT INC." centered, 32pt bold
- "Session Journal" centered, 28pt bold
- Date range centered, 22pt italic, gray
- Tagline centered, 20pt italic, blue (#2E75B6): 
  "Physics enforces. Math proves. You verify."

### 2. Executive Summary
- First paragraph: what state ZKNOT was in at the start of the session 
  and what state it's in at the end. Include runway status if relevant.
- Second paragraph: who this document serves (future-Shane reconstructing 
  context, or an acquirer asking "how did you get here?")
- Headlines bullet list: 5-10 concrete, verifiable facts about what 
  shipped or changed. NOT adjectives. Examples:
  - "Shopify storefront live at shop.zknot.io with payments enabled"
  - "PAT-002 companion document delivered, 32KB, 466 paragraphs"
  - "Git HEAD at commit [hash], pushed to origin/main"

### 3. Day-by-Day Narrative
- One H2 per calendar day ("Day 1 — April 19, 2026" or just the date)
- Opening paragraph: one-line theme of the day
- H3 subsections for major workstreams. Each should have:
  - What was done (bullets with specifics)
  - Key decisions made that day
  - Anything that went wrong and how it was resolved
- Keep narrative flow — this reads like a ship's log, not a task list

### 4. Deliverables Produced
Grouped by type. Each deliverable gets one bullet with:
- File name or URL
- One-line description
- Location on disk if applicable

Groups to consider:
- Documents (.docx, .pdf, .md files)
- KiCad files (symbols, footprints, projects)
- Code (scripts, firmware, backend changes)
- Social/Marketing (posts, listings, emails sent)
- Infrastructure (git commits, deployments, config changes)

### 5. Key Decisions Made
Table with two columns: Decision / Rationale

Include every decision that:
- Closes a previously-open question
- Commits to a path that's expensive to reverse
- Could be second-guessed by future-Shane without context

Examples of what qualifies:
- "Ship Rev 1 as direct-solder pigtail despite better alternatives"
- "Linux as primary workstation, Windows as fallback"
- "Keep 12_JOURNAL at top level rather than nesting in 11_KM/"

Examples of what does NOT qualify (too minor):
- "Used vim instead of nano to edit the file"
- "Picked a specific wording for a Reddit reply"

### 6. Technical Reference
Include only items future-Shane will need to recall quickly:
- Key schematic relationships (e.g., the CH224K CC topology diagram)
- Voltage/configuration tables
- Full paths to critical files on disk
- Git state at end of session (branch, HEAD hash, remote, last 3 commits)
- Environment details (KiCad version, Python version, Flatpak IDs, etc.)

Use monospace (Consolas) font for paths, commands, and diagrams.

### 7. Lessons Learned
Three subsections:

**Technical lessons** — things that would go into REV2_LESSONS.md or 
similar product-specific lesson files. Always include attribution if a 
Reddit commenter, engineer, or colleague contributed the insight. 
Examples:
- "CC1 and CC2 need independent 5.1kΩ pulldowns. (Attribution: u/quuxoo)"
- "OneDrive + KiCad = broken file locking. Use Linux."

**Process lessons** — things about how work got done (tools, workflows, 
mistakes to avoid). Examples:
- "Case-sensitive filesystems require vigilance on cross-platform work"
- "Shell function + alias with same name causes silent .zshrc failures"

**Strategic lessons** — things about decision-making, prioritization, 
market, business. Examples:
- "Rev 1 is a learning vehicle, not the end state"
- "Attribution converts critics into advocates"

### 8. Closing
- One paragraph reaffirming what was accomplished
- One paragraph on what comes next (if applicable)
- Closing tagline on its own line: "Physics enforces. Math proves. You verify."

---

## What makes this format work

Three design principles embedded in the structure:

**Chronological narrative + structured reference.** The day-by-day section 
captures the story ("why did we do X?"). The technical reference captures 
the facts ("what IS X?"). Future-Shane needs both — narrative for 
understanding, reference for execution.

**Attribution everywhere.** When someone else's insight changed your 
work, their name goes in the document. This compounds three ways: 
builds community, strengthens patent prosecution stories 
("improvement suggested by skilled artisan"), and gives future-you 
a map of who helped when you need help again.

**Concrete over abstract.** Every bullet should be checkable. 
"Shopify live" is checkable. "Made progress on sales" is not. 
This matters for KM because future-Shane can't verify vague claims 
months later.

---

## Quick-start version

If you're in a rush and want a minimum-viable journal:

```
Generate a ZKNOT session journal .docx covering [DATE_RANGE]. 
Use the standard ZKNOT journal format (title block, executive summary 
with headlines, day-by-day narrative, deliverables, decisions table, 
technical reference, lessons learned, closing). Page X of Y footer. 
Calibri font. Tagline "Physics enforces. Math proves. You verify." 
Save to ~/ZKNOT/11_KM/session-notes/ naming convention.
```

Then after Claude produces a draft, review and ask for specific sections 
to be expanded.

---

## File this at

`~/ZKNOT/11_KM/ZKNOT_Journal_Format_Template.md`

So future-Shane can find it by looking in the knowledge management folder 
alongside the other reference docs.
