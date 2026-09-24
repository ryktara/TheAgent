# PRD model sections

`foundry.py prd-skeleton` writes the file; only these two blocks are authored by the model.
Everything else (frontmatter, sections 2–8, 10) stays as generated.

## 1. Product

Replace `<!-- model: write -->` and its comment with one paragraph:

> A <form factor> point of sale for <who> in <where> [D:region]. <Primary persona> <does the
> core job> [D:service-model]. <Payment and receipt facts> [D:payments]. It must never
> <the one failure the business cannot absorb> [D:offline].

Rules: 4–7 sentences; every sentence that rests on a decision ends with `[D:<id>]`; no feature
list (section 4 holds it).

## 9. Success metrics

Replace `<!-- model: write -->` and its comment with 3–5 numbered lines:

> 1. <metric> under/over <number> <unit> within <window>

Each metric maps to a must-have job in section 3. Example set for an operational POS pack:

1. Median order entry under 45 seconds per order within 30 days of go-live
2. 99% of submitted orders visible on the work queue within 1 second during opening hours, first 90 days
3. Zero lost orders during measured connectivity drops in the first 90 days
4. Shift close reconciled within 5 minutes on 95% of shifts from month two
