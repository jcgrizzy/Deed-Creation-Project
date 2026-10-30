# Intake Fields

Each field ID doubles as a merge field in deed templates (`{{field_id}}`).

**Source** column:
- `CURRENT` — already asked in the firm's intake email
- `PROPOSED` — recommended addition; needs Conrad's approval before it goes into the client email
- `DERIVED` — not asked of the client; pulled by staff or the agent (property appraiser, clerk records)

**Req**: `Y` required · `C` conditional (see rule) · `N` optional

## 1. Requester

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `requester_name` | Person contacting the firm | text | Y | PROPOSED | May differ from grantor |
| `requester_email` | Email | email | Y | PROPOSED | |
| `requester_phone` | Phone | phone | Y | PROPOSED | |
| `preferred_language` | Language | enum: `en`, `es` | Y | DERIVED | Selects email template |
| `payment_received` | Payment confirmed | bool | Y | DERIVED | From LawPay; one fee per property |
| `acknowledgement` | I acknowledge and understand the above (doc stamps / property tax disclaimer) | bool | Y | CURRENT | Must be `true` to submit; wording in `spec/cognito-build.md` |

## 2. Deed

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `deed_type` | Type of deed | enum: `quitclaim`, `warranty`, `special_warranty`, `enhanced_life_estate` | Y | PROPOSED | Attorney may override at review |
| `consideration_amount` | Consideration | currency | Y | PROPOSED | Default nominal ($10.00); any other amount → FLAG (doc stamps) |

## 3. Property (repeat block — one per property)

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `property_address` | Property address being transferred | address | Y | CURRENT | Must resolve to one parcel |
| `property_county` | County | enum (FL counties) | Y | DERIVED | From address |
| `parcel_id` | Parcel ID / folio | text | Y | DERIVED | From county property appraiser |
| `legal_description` | Legal description | long text | Y | DERIVED | Verbatim from vesting deed; mismatch with appraiser → FLAG |
| `vesting_deed_ref` | Prior deed book/page or instrument no. | text | Y | DERIVED | From clerk records |
| `vesting_deed_names` | Owners exactly as named on vesting deed | list | Y | DERIVED | Must match `grantors` |
| `has_mortgage` | Confirmation property has NO mortgage | bool | Y | CURRENT | `true` (has mortgage) → STOP |
| `is_homestead` | Is this the grantor's homestead? | bool | Y | PROPOSED | Drives spousal joinder |

## 4. Grantors (repeat block — ALL current owners)

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `grantor_name` | Name of grantor | text | Y | CURRENT | Must match `vesting_deed_names` |
| `grantor_address` | Address of grantor | address | Y | CURRENT | Post office address |
| `grantor_type` | Individual / LLC / corporation / trust / estate | enum | Y | PROPOSED | Non-individual → see routing rules |
| `grantor_marital_status` | Marital status | enum: `single`, `married`, `widowed`, `divorced` | C | CURRENT | Required if `grantor_type = individual` |
| `grantor_spouse_name` | Spouse name (joins in signing) | text | C | CURRENT | Required if married and spouse not on title |
| `grantor_signatory_name` | Authorized signer | text | C | PROPOSED | Required if entity/trust |
| `grantor_signatory_title` | Signer title (Manager, Trustee, etc.) | text | C | PROPOSED | Required if entity/trust |
| `grantor_deceased` | Is any owner on title deceased? | bool | Y | PROPOSED | `true` → STOP |

## 5. Grantees (repeat block — ALL new owners)

| Field ID | Label | Type | Req | Source | Validation / notes |
|---|---|---|---|---|---|
| `grantee_name` | Name of grantee | text | Y | CURRENT | Include current owners staying on title |
| `grantee_address` | Address of grantee | address | Y | CURRENT | Post office address — recording requirement |
| `grantee_type` | Individual / entity / trust | enum | Y | PROPOSED | |
| `vesting_type` | How multiple grantees take title | enum: `jtwros`, `tenants_in_common`, `tenancy_by_entirety` | C | PROPOSED | Required if >1 grantee; TBE only if grantees are married to each other |
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
