# Intake Fields

Each field ID doubles as a merge field in deed templates (`{{field_id}}`).

**Source** column:
- `CURRENT` — already asked in the firm's intake email
- `PROPOSED` — recommended addition; needs Conrad's approval before it goes into the client email
- `DERIVED` — not asked of the client; pulled by staff or the agent (property appraiser, clerk records)
- `PHASE2` — added from the paralegal review of October 30, 2026; on the Phase 2 form (`spec/cognito-build.md`)

**Uploads** (`doc` type) are stored in Cognito / Microsoft 365 only. The record carries a reference, never the file, and never in this repo.

**Req**: `Y` required · `C` conditional (see rule) · `N` optional

## 1. Requester

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `requester_name` | Person contacting the firm | text | Y | PROPOSED | May differ from grantor |
| `requester_email` | Email | email | Y | PROPOSED | |
| `requester_phone` | Phone | phone | Y | PROPOSED | |
| `requester_role` | Your role | enum: `grantor`, `grantee`, `other` | Y | PHASE2 | |
| `requester_role_other` | Role description | text | C | PHASE2 | Required if `requester_role = other` |
| `grantor_authorization_doc` | Signed grantor authorization | doc | C | PHASE2 | Required if `requester_role ≠ grantor`; missing → S9 |
| `number_of_deeds` | Number of properties / deeds | int 1–10 | Y | PHASE2 | Must equal count of property blocks; one fee per deed |
| `preferred_language` | Language | enum: `en`, `es` | Y | DERIVED | Selects email template |
| `payment_received` | Payment confirmed | bool | Y | DERIVED | From LawPay; one fee per property |
| `acknowledgement` | I acknowledge and understand the above (doc stamps / property tax disclaimer) | bool | Y | CURRENT | Must be `true` to submit; wording in `spec/cognito-build.md` |

## 2. Deed

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `deed_type` | Type of deed | enum: `quitclaim`, `warranty`, `special_warranty`, `enhanced_life_estate` | Y | PROPOSED | Attorney may override at review |
| `consideration_amount` | Consideration | currency | Y | PROPOSED | Default nominal ($10.00); any other amount → FLAG (doc stamps) |

## 3. Property (repeat block — one per deed)

In Phase 2 each property block **contains** its own grantors (§4), signing answer, and grantees (§5). Fields in §4 and §5 are scoped to their property block.

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `property_address` | Property address being transferred | address | Y | CURRENT | Must resolve to one parcel |
| `property_county` | County | enum (67 FL counties) | Y | PHASE2 | Client selects; staff verifies against appraiser (was DERIVED) |
| `parcel_id` | Parcel ID / folio | text | Y | DERIVED | From county property appraiser |
| `legal_description` | Legal description | long text | Y | DERIVED | Verbatim from vesting deed; mismatch with appraiser → FLAG |
| `vesting_deed_ref` | Prior deed book/page or instrument no. | text | Y | DERIVED | From clerk records |
| `vesting_deed_names` | Owners exactly as named on vesting deed | list | Y | DERIVED | Must match `grantors` |
| `has_mortgage` | Confirmation property has NO mortgage | bool | Y | CURRENT | `true` (has mortgage) → STOP |
| `all_sign_together` | All signers sign at same time and place | bool | C | PHASE2 | Asked if >1 signer; `false` → separate signature/notary blocks per signer |

## 4. Grantors (repeat block — ALL current owners)

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `grantor_name` | Name of grantor | text | Y | CURRENT | Must match `vesting_deed_names` |
| `grantor_address` | Address of grantor | address | Y | CURRENT | Post office address |
| `grantor_type` | Individual / company / trust | enum: `individual`, `company`, `trust` | Y | PHASE2 | Was five values; estate no longer offered on the form (staff sets `estate` if needed → S4) |
| `grantor_marital_status` | Marital status | enum: `single`, `married`, `widowed`, `divorced` | C | CURRENT | Required if `grantor_type = individual` |
| `is_homestead` | Is this property the grantor's homestead? | bool | C | PHASE2 | Asked if married individual (moved here from §3) |
| `grantor_spouse_name` | Spouse name (joins in signing) | text | C | CURRENT | Required if married and `is_homestead = true`; optional otherwise |
| `spouse_same_address` | Spouse address same as grantor | bool | C | PHASE2 | Asked if spouse name given |
| `spouse_address` | Spouse mailing address | address | C | PHASE2 | Required if `spouse_same_address = false` |
| `spouse_photo_id` | Spouse photo ID | doc | C | PHASE2 | If spouse named — pending Conrad |
| `grantor_photo_id` | Grantor photo ID | doc | C | PHASE2 | Required if individual |
| `deceased_spouse_on_deed` | Late spouse on current deed | bool | C | PHASE2 | Asked if widowed; `true` → F8 |
| `death_certificate_doc` | Death certificate | doc | C | PHASE2 | Required if `deceased_spouse_on_deed = true` |
| `former_spouse_on_deed` | Former spouse on current deed | bool | C | PHASE2 | Asked if divorced; `true` → F9 |
| `divorce_docs` | Final judgment and/or settlement agreement | doc | C | PHASE2 | Required if `former_spouse_on_deed = true` |
| `grantor_entity_state` | State of organization | enum (US states) | C | PHASE2 | Required if company |
| `grantor_entity_status` | Active / inactive | enum: `active`, `inactive` | C | PHASE2 | Required if company; `inactive` → S7 |
| `grantor_trust_date` | Date of trust | date | C | PHASE2 | Required if trust |
| `grantor_trust_docs` | Trust agreement / certification | doc | C | PHASE2 | Required if trust |
| `grantor_signing_state` | State where grantor signs | enum (US states) | C | PHASE2 | Required if `all_sign_together = false`; fills notary venue |
| `spouse_signing_state` | State where spouse signs | enum (US states) | C | PHASE2 | As above, if spouse named |
| `grantor_signatory_name` | Authorized signer (trustee for trusts) | text | C | PROPOSED | Required if company/trust |
| `grantor_signatory_title` | Signer title (Manager, Trustee, etc.) | text | C | PROPOSED | Required if entity/trust |
| `grantor_deceased` | Is any owner on title deceased? | bool | Y | DERIVED | Set by staff from title review; `true` and not covered by F8 → S2. Not asked on the Phase 2 form |

## 5. Grantees (repeat block — ALL new owners)

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `grantee_name` | Name of grantee | text | Y | CURRENT | Include current owners staying on title |
| `grantee_address` | Address of grantee | address | Y | CURRENT | Post office address — recording requirement |
| `grantee_type` | Individual / company / trust | enum: `individual`, `company`, `trust` | Y | PHASE2 | |
| `grantee_photo_id` | Grantee photo ID | doc | C | PHASE2 | Required if individual |
| `grantee_entity_state` | State of organization | enum (US states) | C | PHASE2 | Required if company |
| `grantee_entity_status` | Active / inactive | enum | C | PHASE2 | Required if company; `inactive` → S8 |
| `grantee_trust_date` | Date of trust | date | C | PHASE2 | Required if trust |
| `grantee_trustee_names` | Trustee name(s) | text | C | PHASE2 | Required if trust |
| `grantee_trust_docs` | Trust agreement / certification | doc | C | PHASE2 | Required if trust |
| `vesting_type` | How multiple grantees take title | enum: `jtwros`, `tenants_in_common`, `tenancy_by_entirety` | C | PROPOSED | Per property block. Required if >1 grantee; TBE only if grantees are married to each other. Form question pending Conrad |
| `remainderman_names` | Remaindermen | list | C | PROPOSED | Required if `deed_type = enhanced_life_estate` |

## 6. Execution

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `execution_method` | How signing will happen | enum: `in_office`, `mail_out`, `remote_online_notary` | Y | PROPOSED | |
| `witnesses_provided_by` | Who supplies the two witnesses | enum: `firm`, `client` | Y | PROPOSED | |
| `witness_1_name` / `witness_1_address` | Witness 1 | text / address | Y | DERIVED | Captured at execution |
| `witness_2_name` / `witness_2_address` | Witness 2 | text / address | Y | DERIVED | Captured at execution |
| `notary_type` | Physical presence / online | enum | Y | DERIVED | Captured at execution |
| `execution_date` | Date signed | date | Y | DERIVED | Rendered fully spelled out on the deed |

## 7. Drafting (not asked of the client)

Used by the deed templates (`spec/deed-templates.md`). Set by staff or the agent.

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `grantor_descriptor` | Marital descriptor in the deed | text | C | DERIVED | Individuals only, e.g. "a married man", "an unmarried woman"; wording style pending Conrad |
| `spouse_pronoun` | "his" / "her" in "joined by [his/her] spouse" | text | C | DERIVED | Tied to C12 decision (gendered vs neutral) |
| `grantor_entity_form` / `grantee_entity_form` | "Limited Liability Company" / "corporation" | text | C | DERIVED | Inferred from the company name suffix; otherwise staff sets it |
| `grantee_descriptor` | Marital descriptor for grantee | text | N | DERIVED | Some templates include it; optional |
| `notary_county` | County for notary venue | text | N | DERIVED | Blank line if unknown |
| `tax_year` | "Subject to taxes for" year | int | Y | DERIVED | Year of execution |
| `preparer_*` | Preparing attorney name and address | config | Y | DERIVED | From `config/firm.json` → `deed_preparer` |
