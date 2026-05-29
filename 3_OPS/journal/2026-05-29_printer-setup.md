# 2026-05-29 — Network Printer Setup (Debian Trixie)

## Outcome
Working network printing from the Debian box (mt@mt) to the HP Color LaserJet
Pro M478f over IPP Everywhere (driverless). Test print confirmed.

## What happened
- Goal was originally a Brother network printer, but `avahi-browse -rt _ipp._tcp`
  found no Brother — only the HP M478f at 10.0.0.58 (HP3024A9018598.local).
  Brother was off / unreachable / not on same network. Proceeded with the HP.
- HP advertises driverless support (txt: URF=..., rp=ipp/print), no vendor driver.
- CUPS auto-discovered and auto-created the queue before any manual lpadmin ran:
  queue `HP_Color_LaserJet_Pro_M478f_9f_018598`, device implicitclass://...
  Set as default, test print succeeded.

## Gotchas / lessons
- lpadmin and lpinfo live in /usr/sbin, which zsh does NOT put on PATH for a
  non-root user -> "command not found". Use sudo (adds sbin) or full path.
  lp and lpstat are in /usr/bin and work without sudo.
- Printer advertised Duplex=F. Auto two-sided may not be exposed over IPP even
  if hardware supports it. Untested. Revisit: lp -o sides=two-sided-long-edge.
- Used dnssd:// URI (tracks by UUID) as robust handle vs hardcoded IP.

## Daily-driver commands
- lp file.pdf                       # print to default (the HP)
- lp -n 3 file.pdf                  # copies
- lp -o ColorModel=Gray file.pdf    # grayscale
- lp -P 2-5 file.pdf                # page range
- lpstat -o                         # jobs in queue
- cancel -a                         # clear stuck jobs

## Open threads
- Brother never came online; if intended, wake it and re-run avahi-browse.
- Duplex unconfirmed on the HP.
