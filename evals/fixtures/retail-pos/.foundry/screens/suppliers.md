---
id: "suppliers"
jobs: ["manage-suppliers"]
personas: ["store-manager"]
route: "/suppliers"
routes: [{path: "/suppliers"}]
layout: "action-bar / high density"
components: ["button", "data-table", "empty-state", "input", "skeleton", "tabs", "toast", "virtual-list"]
data:
  reads: ["supplier_get", "supplier_list"]
  writes: ["supplier_create", "supplier_manage_suppliers", "supplier_update"]
  events: []
offline: true
print: false
---

# suppliers

## Purpose

Supplier master: contact, TRN, terms, lead time, return-to-vendor rules

Role access: store-manager.

## Layout zones

Desktop / tablet:

```
+--------------------------------------------------------------+
| Suppliers   Search [__________]                  [ Create ]  |
+--------------------------------------------------------------+
| Name            TRN        | [ Contact | Terms | POs | RTV ] |
| Al Noor Textile 3001234... | Name  [ Al Noor Textile     ]   |
| Riyadh Abayas   3009876... | TRN   [ 300123456700003     ]   |
| Gulf Denim  (blocked)      | Lead time [ 14 ] days          |
+--------------------------------------------------------------+
|                                     [ Block ]  [ Save ]      |
+--------------------------------------------------------------+
```

Phone:

```
+----------------------------------+
| Suppliers              [ + ]     |
+----------------------------------+
| Search [__________________]      |
| Al Noor Textile                  |
| Gulf Denim (blocked)             |
+----------------------------------+
| [ Contact | Terms | POs | RTV ]  |
| TRN [ 300123456700003 ]          |
| [ Block ]            [ Save ]    |
+----------------------------------+
```

Components from screens.md: SupplierTable, SupplierForm

## Actions

| Action | Kind | Component |
|--------|------|-----------|
| Create supplier | primary | `button` |
| Edit details | primary | `input` |
| Switch tab | secondary | `tabs` |
| Block supplier | destructive | `button` |
| View POs and RTVs | secondary | `data-table` |

## States

| State | Copy (en) | Copy (ar) | Notes |
|-------|-----------|-----------|-------|
| empty | No suppliers yet. Add your first supplier. | لا يوجد موردون بعد. أضف أول مورد. | copy.csv |
| loading | Loading suppliers… | جارٍ تحميل الموردين… | copy.csv |
| error | The supplier could not be saved. Check the TRN is 15 digits and try again. | تعذّر حفظ المورد. تأكّد أن الرقم الضريبي من 15 رقمًا ثم أعد المحاولة. | copy.csv |
| offline | Offline. Edits are saved on this device and sync when the connection returns. | لا يوجد اتصال. تُحفظ التعديلات على هذا الجهاز وتُزامن عند عودة الاتصال. | copy.csv |
| locked | This supplier is blocked. New purchase orders are not allowed. | هذا المورد موقوف. لا يمكن إنشاء أوامر شراء جديدة. | copy.csv |
| success | Supplier saved. | تم حفظ المورد. | copy.csv |

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
- `A11Y-10`
- `A11Y-11`
- `A11Y-12`
- `A11Y-14`
- Screen note: Form labels

## RTL notes

- `RTL-01`
- `RTL-03`
- `RTL-05`
- `RTL-07`
- Screen note: Mirrors

## Telemetry

- `screen.suppliers.viewed` (persona, branch)
- `screen.suppliers.action` (action id, duration_ms)
- `screen.suppliers.error` (code)

## Open questions

- none
