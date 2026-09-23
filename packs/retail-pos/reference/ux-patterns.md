# Retail POS — UX patterns

Operational UI: scan-first, forgiving, readable from arm's length. Every pattern names its id so
screen specs can cite it. Baseline: touch 48 dp, text 16 px minimum, contrast 4.5:1, tabular
numerals everywhere an amount appears.

## Scan-first checkout

- **RET-SCAN-01 Global scan capture.** A keyboard-wedge scanner types fast digits ending in Enter;
  the app detects bursts (under 30 ms between keys) and routes them to the basket regardless of
  focus. Camera scan is a button on tablets; Bluetooth scanners in HID mode behave the same.
- **RET-SCAN-02 Feedback.** Every scan gives a beep plus the line flashing; unknown code gives a
  distinct low tone and red toast, never a modal that blocks the next scan.
- **RET-SCAN-03 Repeat scans.** Scanning the same code increments qty on the last line instead of
  adding a new line (configurable for serial-tracked items).
- **RET-SCAN-04 Newest on top.** The basket shows the latest line at the top, highlighted for 2 s.
- **RET-SRCH-01 Big search.** One field at the top, 56 px tall, accepts barcode, PLU, SKU or name
  in Arabic or English; results from a local index in under 200 ms.
- **RET-NUM-01 Numpad first.** Qty, weight, price and PIN use a fixed 3×4 numpad with 00 and
  backspace; a typed number followed by a scan sets qty ("3 ×" then scan).
- **RET-VAR-01 Variant matrix.** Size by colour grid with stock per cell; out-of-stock cells
  hatched; tapping a cell adds the variant.

## Weighed item entry

- **RET-WGT-01 PLU picture grid.** Produce shown as pictures with names and 4–5 digit PLUs;
  typing the PLU filters the grid.
- **RET-WGT-02 Live scale.** Weight shown in kg with 3 decimals; Accept enables only on a stable
  reading above zero; tare chips for common containers.
- **RET-WGT-03 Scale labels.** EAN-13 starting with 2: item code and embedded weight or price are
  decoded per the store's configured layout; the check digit and price check digit are validated.
- **RET-WGT-04 Manual weight.** Allowed only with a manager PIN and logged.

## Returns lookup

- **RET-RTN-01 Receipt barcode.** Every receipt prints a barcode/QR of its number; scanning it on
  returns opens the sale directly.
- **RET-RTN-02 Alternatives.** Lookup by phone, card last 4 + date, or date + amount.
- **RET-RTN-03 Returnable qty.** Each line shows sold, already returned and returnable; the
  stepper cannot exceed returnable.
- **RET-RTN-04 Policy banner.** Days since purchase and the policy window shown in colour and text;
  outside window requires manager PIN.
- **RET-RTN-05 Refund method.** Defaults to the original tender; store credit offered as a choice.

## Price override PIN

- **RET-OVR-01 Inline.** Tap the price on a line, type the new price, pick a reason chip (damaged,
  price match, shelf label wrong, manager discretion).
- **RET-OVR-02 Approval.** If the change exceeds the cashier's limit the manager-pin modal opens
  in place showing old → new and the percent; manager taps a badge or types a PIN.
- **RET-OVR-03 Trace.** The line shows a strike-through list price and a small lock icon; the
  receipt shows the original price and the saving.

## Promotions engine display

- **RET-PRM-01 Badges.** A promoted line shows a badge with the promotion name; a BOGO free item
  shows "Free" in green.
- **RET-PRM-02 Near-miss hint.** "Add 1 more to get 1 free" appears on the line when a customer is
  one item from a threshold (mix-and-match, BOGO, tiered).
- **RET-PRM-03 Savings total.** Totals panel shows "You saved" above the total; the receipt and
  customer display repeat it.
- **RET-PRM-04 Deterministic order.** Promotions re-evaluate after every line change; a line
  never flickers between promotions on repeated evaluation.

## Tender

- **RET-TND-01 Tender tiles.** Cash, card, wallet, gift card, store credit, points, khaata; tiles
  hidden when not enabled for the store.
- **RET-TND-02 Quick cash.** Exact and next notes (AED 10/50/100/200, SAR 50/100/500, PKR 500/1000/5000).
- **RET-TND-03 Remaining bar.** Turns green at zero; change due shown 40 px.

## Label printing

- **RET-LBL-01 Queues.** Labels queue from GRN, price change, promotion start and manual scans.
- **RET-LBL-02 Templates.** Shelf edge (name en/ar, VAT-inclusive price, unit price per kg or
  100 g, barcode), product sticker, jewellery tag; ZPL for Zebra, TSPL for TSC, Dymo via driver.
- **RET-LBL-03 Preview.** Rendered preview before print; missing Arabic name flagged.

## Customer display

- **RET-CDS-01 Mirror.** Last scanned line large; basket list; total 64 px; savings.
- **RET-CDS-02 Language.** Follows the customer language on the attached Customer, else store default.
- **RET-CDS-03 Idle.** Promotions slideshow; never shows staff UI.

## Stock operations

- **RET-STK-01 Count mode.** Scan increments count; numpad for bulk; variance shown only after
  submit for blind counts.
- **RET-STK-02 Reason codes.** Damage, expiry, theft, sample, correction; each maps to a report.

## Offline and sync

- **RET-OFF-01 Banner.** Offline banner amber, not blocking; count of queued sales.
- **RET-OFF-02 Card fallback.** When the terminal is standalone, cashier keys the approval code.

## RTL and bilingual

- **RET-RTL-01 Mirror.** Layout mirrors in ar/ur; numerals, SKUs, barcodes and prices stay LTR.
- **RET-RTL-02 Product names.** Show name in UI language with the other language under it.

## Accessibility

- Colour never the only signal (icons and text on badges).
- Every scan result announced via an aria-live region.
- Keyboard-only checkout possible (F-keys for Pay, Park, Customer).

## Keyboard shortcuts (desktop tills)

| Key | Action |
|-----|--------|
| F1 | Help and shortcut sheet |
| F2 | Focus big search |
| F3 | Attach customer |
| F4 | Quantity (then numpad) |
| F5 | Price override (opens manager-pin when over limit) |
| F6 | Park sale |
| F7 | Recall parked sale |
| F8 | Returns lookup |
| F9 | Gift card balance |
| F10 | Open drawer (no sale, audited) |
| F12 | Pay |
| Esc | Close overlay, never clears the basket |
| Del | Void selected line (reason required) |
