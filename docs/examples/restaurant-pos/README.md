# Example: restaurant-pos T-008 (send to kitchen)

Produced by the P7b build loop in the scratch project (Sharjah brief, phases 0–10 unattended, T-000…T-008 built).

- `order-entry-{light,dark}-{ltr,rtl}.png`: `/order-entry` captured by the DoD screenshot step (1280×800, en/ar).
- `order-entry.e2e.spec.ts`: the Playwright acceptance test verbatim (table map → order entry → two items, one modifier →
  send to kitchen → state Sent, AED 34.00 → synced through the outbox → kds ticket → bump/recall; Arabic mirror + axe).
