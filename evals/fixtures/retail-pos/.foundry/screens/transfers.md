---
id: "transfers"
jobs: ["stock-transfer"]
personas: ["stock-keeper"]
route: "/transfers"
routes: [{path: "/transfers"}]
layout: "action-bar / high density"
components: ["button", "empty-state", "skeleton", "toast", "virtual-list"]
data:
  reads: ["transfer_get", "transfer_list"]
  writes: ["transfer_create", "transfer_stock_transfer", "transfer_update"]
  events: []
offline: true
print: false
---

# transfers

## Purpose

Move stock between stores or warehouse

Role access: stock-keeper.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Transfers   [ Draft | In transit | Discrepancy ]  [ Create ] |
+--------------------------------------------------------------+
| TR-221 Olaya > Malqa  | TR-221  In transit                   |
| TR-219 WH > Olaya     | SKU           Sent  Received         |
| TR-214 Malqa > WH !   | TSH-01 M Navy  10    10              |
|                       | ABY-07 52 Blk   5     4  !          |
+--------------------------------------------------------------+
| Scan [__________]  [ Dispatch ] [ Receive ] [ Discrepancy ]  |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Transfers   In transit v  [ + ]  |
+----------------------------------+
| TR-221 Olaya > Malqa  In transit |
| TR-214 Malqa > WH   Discrepancy  |
+----------------------------------+
| Scan [__________________]        |
| ABY-07 52 Blk  sent 5  recv 4 !  |
| [ Receive ]  [ Discrepancy ]     |
+----------------------------------+
```

Components from screens.md: TransferList, ScanField

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Create transfer | primary | `button` |
| Open transfer | secondary | `virtual-list` |
| Dispatch | primary | `button` |
| Receive by scanning | primary | `button` |
| Report discrepancy | secondary | `button` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No transfers yet. Create one to move stock between stores. | لا توجد تحويلات بعد. أنشئ تحويلًا لنقل المخزون بين الفروع. | copy.csv |
| loading | Loading transfers… | جارٍ تحميل التحويلات… | copy.csv |
| error | The transfer could not be saved. Try again. | تعذّر حفظ التحويل. أعد المحاولة. | copy.csv |
| offline | Offline. Scans are saved on this device and sync when the connection returns. | لا يوجد اتصال. تُحفظ عمليات المسح على هذا الجهاز وتُزامن عند عودة الاتصال. | copy.csv |
| locked | This transfer is in transit and cannot be edited. | هذا التحويل قيد النقل ولا يمكن تعديله. | copy.csv |
| success | Transfer received. Stock updated at this store. | تم استلام التحويل وتحديث مخزون هذا الفرع. | copy.csv |

## Validation and error copy

- `FRM-02` Error copy says what happened and how to fix it in one sentence.
- `FRM-01` Validate on blur; re-validate on change after the first error; summarise on submit.
- `FRM-03` Submit stays enabled; errors listed on attempt.

## Keyboard and shortcuts

| Key | Action |
|-----|--------|
| Tab / Shift+Tab | move focus |
| Enter | activate |
| Escape | close dialog or sheet |

## Accessibility checklist

- `A11Y-01`
- `A11Y-02`
- `A11Y-03`
- `A11Y-08`
- `A11Y-12`
- `A11Y-14`
- `A11Y-16`
- `A11Y-18`
- Screen note: Status text

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.transfers.viewed` (persona, branch)
- `screen.transfers.action` (action id, duration_ms)
- `screen.transfers.error` (code)

## Open questions

- Who resolves a discrepancy (sender, receiver or store manager), and does stock stay in transit until then?
