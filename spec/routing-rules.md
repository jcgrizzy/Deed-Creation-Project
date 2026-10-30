# Routing Rules

Evaluated after intake and again after document collection, **per property block**.

Rules marked `PHASE2 — PROPOSED` came from the Phase 2 form changes and need attorney approval before they go into validation logic.

- **STOP** — file moves to *Attorney Review* and drafting does not start until an attorney clears it.
- **FLAG** — drafting may proceed, but the flag is shown on the draft and must be cleared at attorney review.

## STOP

| ID | Condition | Why |
|---|---|---|
| S1 | `has_mortgage = true` | Doc stamp exposure on the mortgage balance; possible due-on-sale issue; firm intake assumes no mortgage |
| S2 | `grantor_deceased = true` and not a widowed grantor's late spouse with death certificate (F8) | Title may need probate or a PR deed — outside standard deed intake |
| S3 | Grantor names don't match `vesting_deed_names` | Wrong or missing grantor makes the deed defective |
| S4 | `grantor_type` is `trust` or `estate` | Need to confirm signing authority (trust documents now uploaded at intake; letters of administration for estates) |
| S5 | `is_homestead = true`, grantor married, and spouse not joining | Homestead conveyance generally requires spousal joinder (Fla. Const. art. X, § 4(c)) |
| S6 | Property address resolves to zero or multiple parcels | Can't produce a reliable legal description |
| S7 | `grantor_entity_status = inactive` | PHASE2 — PROPOSED. An inactive company may need reinstatement before it can convey |
| S8 | `grantee_entity_status = inactive` | PHASE2 — PROPOSED. Confirm the company can take title |
| S9 | `requester_role ≠ grantor` and no `grantor_authorization_doc` | PHASE2 — PROPOSED. No written authority from the grantor to proceed |
| S10 | Required upload missing or unreadable (photo ID, death certificate, divorce documents, trust documents) | PHASE2 — PROPOSED. Staff requests the document before drafting |

## FLAG

| ID | Condition | Why |
|---|---|---|
| F1 | `grantor_type = company` | Confirm signatory authority (Sunbiz record, operating agreement/resolution) |
| F2 | `consideration_amount` above nominal | Doc stamps may be due; firm does not collect them — confirm client was advised |
| F3 | Legal description on vesting deed differs from property appraiser | Use vesting deed; attorney confirms |
| F4 | Grantor married, spouse not on title, `is_homestead = false` | Firm recommends spouse sign anyway to avoid issues on a later sale |
| F5 | `vesting_type = tenancy_by_entirety` | Confirm grantees are married to each other |
| F6 | More than one grantee and `vesting_type` blank | Florida default is tenants in common unless survivorship is expressly stated — confirm intent |
| F7 | `deed_type = enhanced_life_estate` | Attorney confirms remaindermen and retained powers language |
| F8 | `deceased_spouse_on_deed = true` | PHASE2 — PROPOSED. Confirm the prior deed vested survivorship (TBE or JTWROS) and the death certificate matches; if not, escalate to S2 |
| F9 | `former_spouse_on_deed = true` | PHASE2 — PROPOSED. Confirm the judgment or settlement awards the property to the grantor; if not, the former spouse may need to join |
| F10 | `all_sign_together = false` | PHASE2 — PROPOSED. Separate signature and notary blocks; confirm each signer's state and witness arrangements |
| F11 | `requester_role ≠ grantor` | PHASE2 — PROPOSED. Confirm the authorization is signed by every grantor |
