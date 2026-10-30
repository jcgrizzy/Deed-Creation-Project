# Workflow Stages

Each file carries `stage`, `stage_owner`, and a timestamp for every transition.

| # | Stage | Owner | Enters when | Exits when |
|---|---|---|---|---|
| 1 | Inquiry | Staff | Client contacts firm | Intake email sent (EN or ES) |
| 2 | Awaiting Payment & Info | Client | Intake email sent | Payment confirmed **and** intake fields received |
| 3 | Document Collection | Staff / Agent | Stage 2 complete | Parcel ID, legal description, and vesting deed pulled |
| 4 | Validation | Agent | Stage 3 complete | Routing rules run; no STOP → Stage 6; any STOP → Stage 5 |
| 5 | Attorney Review (pre-draft) | Attorney | STOP triggered | Cleared → Stage 6; declined → Closed |
| 6 | Drafting | Agent | Validation passed or cleared | Draft generated with any FLAGs listed |
| 7 | Attorney Review (draft) | Attorney | Draft generated | Approved, all FLAGs cleared |
| 8 | Execution | Staff / Client | Draft approved | Signed, witnessed, notarized original received |
| 9 | Recording | Staff | Original received | Recorded; instrument number captured |
| 10 | Closed | Staff | Recorded copy sent to client | — |

## Open questions

- Where do files live: SharePoint List, Dataverse, or the existing intake system?
- Reminder cadence if a client stalls in Stage 2 or Stage 8.
- Who is the default attorney reviewer, and is there a backup?
