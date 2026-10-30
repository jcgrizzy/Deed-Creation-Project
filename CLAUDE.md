# CLAUDE.md — Deed Creation Project

Project brief for Claude (and any developer) working in this repo. Read this first.

## What this is

A deed intake and workflow system for Kelley, Grant & Tanis, P.A. (KGT), a Florida law firm. It collects structured intake data from clients, validates it against Florida execution and recording requirements, moves each file through defined stages, and later feeds a **drafting agent** that fills deed templates.

The agent **fills and flags**. It does not compose deeds from scratch and it does not give legal advice. Every draft goes through attorney review before execution.

## Source of truth

| File | Purpose |
|---|---|
| `spec/intake-fields.md` | Every intake field: ID, type, required/optional, validation rule |
| `spec/routing-rules.md` | STOP (attorney review) and FLAG conditions |
| `spec/workflow-stages.md` | File stages, owners, entry/exit criteria |
| `spec/florida-requirements.md` | Statutory execution/recording checklist (each item has a verification status) |
| `spec/cognito-build.md` | Cognito Forms build instructions for the client intake form (current task) |
| `design/` | Approved intake form mockup (PNG + static HTML) |
| `config/firm.json` | Fees, payment link, firm info — never hard-code these elsewhere |
| `templates/` | Client intake emails (EN/ES); deed templates go here as they are added |
| `samples/` | **Fictitious** test records only |

If code and spec disagree, the spec wins. Change the spec first (in a PR), then the code.

## Hard rules

- **No real client data in this repo.** Names, addresses, parcel IDs, legal descriptions, IDs, and payment details in `samples/` must be fictitious. Live data lives in the firm's Microsoft 365 environment.
- **No secrets.** API keys, tokens, and credentials go in environment variables or a secrets manager, never in a commit.
- **English/Spanish parity.** Any change to `templates/intake-email-en.md` needs the matching change in `intake-email-es.md` in the same PR.
- **Statutory items marked `VERIFY`** in `spec/florida-requirements.md` must not be hard-coded as validation logic until an attorney marks them `CONFIRMED`.
- **Field IDs are stable.** Deed templates reference intake field IDs as merge fields (`{{grantor_name}}`). Renaming a field means updating every template that uses it.

## Writing conventions (firm style)

- Legal documents: dates fully spelled out (e.g., "the twenty-ninth day of October, 2026").
- No absolute statements about outcomes; use hedged language.
- Client-facing text: open with the recipient's name or "Team" — never "Hi," "Hello," or "Dear." Use "Thank you." Never use "kindly."
- Keep prose tight; bullet actions and next steps.

## Workflow for contributors

- Branch from `main`, open a pull request, Conrad reviews and merges.
- Small, focused PRs. Describe what changed and why.
- Sample data changes go with the spec or code change that needs them.
