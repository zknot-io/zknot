---
title: Critical-Capabilities Lens — Scoping Without Over-Building
system: critical-capabilities-lens
status: active
created: 2026-06-05
owner: Shane
---

# Critical-Capabilities Lens — Scoping Without Over-Building

A reusable five-move method for defining what any system (product, service, internal tool) is *for*, what's critical, and where to stop — so layering stays clean and nothing gets over-built.

## The five moves

1. **One-sentence job.**
   Write it as: *"X exists so [who] can [do what] without [what cost or trust]."*
   If it needs two sentences, X is overloaded — split it or cut it.

2. **Critical = irreducible.**
   For each candidate capability, ask: *"Remove it — does the one-sentence job still hold?"*
   - Job still holds → not critical. It's *later*.
   - Job breaks → critical. Keep.

3. **Keep a "not" list.**
   Explicitly write what the system refuses to be, and maintain it. Scope discipline is a refusal list, not willpower.

4. **One boundary question.**
   Reduce scope decisions to a single yes/no router that sorts any proposed feature into core vs. elsewhere. (e.g. verifyknot's: *"Does this help a stranger check a claim without trusting us?"*)

5. **Layer test.**
   Layers are good when each has **one nameable job** and a **one-sentence handoff** to the next.
   "Too many layers" really means "layers whose responsibilities I can't tell apart."
   **Count responsibilities, not layers.**

## The trap to avoid

Running this lens on *everything at once* is the same over-build bug wearing a strategist's hat — over-*planning* instead of over-*coding*.

- Run it on the **live node** (the problem in front of you), not the whole business.
- Let **demand pull the definition** the same way it pulls the build.
- The north-star pipeline already orders the nodes; each one earns its full scoping when it becomes the active problem.

## Companion principle (from verifyknot / PUF work)

**Capture is cheap, build is expensive — let demand pull the build.**
Store signed data now (near-free, irreversible-after-the-fact); build heavy machinery (verifiers, matchers, management UIs) only when a real buyer or solicitation is reaching for it. Capturing buys the *option*; demand triggers the *build*.

## Quick application checklist

- [ ] Can I state its job in one sentence?
- [ ] Have I marked each capability critical (irreducible) vs. later?
- [ ] Do I have a written "not" list?
- [ ] Is there a single boundary question for new features?
- [ ] Does each layer have one nameable job + a one-sentence handoff?
- [ ] Am I scoping the live node only, not the whole business?
