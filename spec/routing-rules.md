# Routing Rules

Evaluated after intake and again after document collection.

- **STOP** — file moves to *Attorney Review* and drafting does not start until an attorney clears it.
- **FLAG** — drafting may proceed, but the flag is shown on the draft and must be cleared at attorney review.

## STOP

| ID | Condition | Why |
|---|---|---|
| S1 | `has_mortgage = true` | Doc stamp exposure on the mortgage balance; possible due-on-sale issue; firm intake assumes no mortgage |
| S2 | `grantor_deceased = true` | Title may need probate, PR deed, or death certificate/affidavit — outside standard deed intake |
| S3 | Grantor names don't match `vesting_deed_names` | Wrong or missing grantor makes the deed defective |
| S4 | `grantor_type` is `trust` or `estate` | Need to confirm signing authority (trust certificate, letters of administration) |
| S5 | `is_homestead = true`, grantor married, and spouse not joining | Homestead conveyance generally requires spousal joinder (Fla. Const. art. X, § 4(c)) |
| S6 | Property address resolves to zero or multiple parcels | Can't produce a reliable legal description |

## FLAG

| ID | Condition | Why |
|---|---|---|
| F1 | `grantor_type` is `llc` or `corporation` | Confirm signatory authority (Sunbiz record, operating agreement/resolution) |
| F2 | `consideration_amount` above nominal | Doc stamps may be due; firm does not collect them — confirm client was advised |
| F3 | Legal description on vesting deed differs from property appraiser | Use vesting deed; attorney confirms |
| F4 | Grantor married, spouse not on title, `is_homestead = false` | Firm recommends spouse sign anyway to avoid issues on a later sale |
| F5 | `vesting_type = tenancy_by_entirety` | Confirm grantees are married to each other |
| F6 | More than one grantee and `vesting_type` blank | Florida default is tenants in common unless survivorship is expressly stated — confirm intent |
| F7 | `deed_type = enhanced_life_estate` | Attorney confirms remaindermen and retained powers language |
