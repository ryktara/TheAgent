---
id: "0002"
title: "Auth and sessions"
status: accepted
decision_refs: ["D:branches"]
date: "2026-09-24"
---

# ADR 0002: Auth and sessions

## Context

Two actor classes: devices (tills, handheld stock scanners, print and label bridge) and staff (PIN, roles). Price overrides and returns need a supervisor override. Personas: cashier, store-manager, owner, stock-keeper, accountant, customer [D:branches].

## Decision

Device auth: each terminal enrolled once with a long-lived device token bound to a branch; rotated on re-enrol. Staff auth: 4–6 digit PIN hashed with Argon2id per branch, 3-strike 60 s lockout, verified offline against the local hash. Manager override: PIN of a staff whose role carries the permission, recorded as approver on the audit event. Owner and back-office web: email + password with optional TOTP. Sessions: device token (30 d absolute) plus staff session (shift-bound); server tokens are httpOnly cookies for web and bearer for devices.

## Alternatives

| Alternative | Rejected because |
|-------------|------------------|
| Per-staff passwords on the POS | too slow at the till; PINs are the industry norm |
| Shared terminal login without staff identity | no per-actor audit trail; fails the audit control |

## Consequences

- Every mutating request carries device id and staff id
- Offline PIN verification works from the local hash cache
- Role matrix lives in the people context and syncs to devices

## Revisit when

SSO for back-office users is requested, or a regulator requires biometric staff sign-in.
