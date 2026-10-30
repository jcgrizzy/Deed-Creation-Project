# Deed Intake Form — Cognito Build Instructions (Phase 2)

Phase 2 revises the Phase 1 form using the paralegal review of October 30, 2026. Changes from Phase 1 are listed in **What changed** below so the builder can edit the existing form rather than start over.

Text marked **DRAFT** has not been approved by an attorney. Build it as written so the flow can be tested, but do not publish the form until Conrad approves the wording.

The Claude Docs mirror ("Deed Intake Form — Cognito Build Instructions") reflects Phase 1. This file is current until that doc is updated.

## Scope

Build the **Deed Request** form in Cognito Forms for Kelley, Grant & Tanis, P.A. Clients acknowledge the firm's disclaimers and submit the parties, property, and supporting documents for each deed. The payment step (LawPay) is still **out of scope**; Conrad is building it separately.

## What changed from Phase 1

- **Contact:** added "Your role" (Grantor / Grantee / Other) and a grantor authorization upload when the person submitting is not a grantor.
- **Structure:** new "How many deeds?" dropdown. Each deed is one **Property block** holding its own Property, Grantor(s), and Grantee(s), in that order. Property 2 starts only after Property 1's grantees.
- **Property:** added County.
- **Grantor:** three types (Individual / Company / Trust) instead of two. New homestead, spouse address, widowed, and divorced branches. Photo ID, death certificate, divorce documents, and trust document uploads. Company active/inactive.
- **Signing:** new "Will all signers sign at the same time?" question per property. "No" adds a signing-state field per grantor and switches the deed to separate signature and notary blocks.
- **Grantee:** three types (Individual / Company / Trust), with photo ID, active/inactive, and trust document fields.
- **Disclaimer:** the deed's NOTE paragraph stays on the deed (page 1 footer), not on the form. See **Deed disclaimer**.

## Form setup

One form named **Deed Request**, single page, in this order:

1. Acknowledgement (unchanged — stays at the top)
2. Your Contact Information
3. Number of Deeds
4. Property Blocks (repeating; one per deed)
   - 4a. Property
   - 4b. Grantor(s): Current Owners (nested repeating)
   - 4c. Signing
   - 4d. Grantee(s): New Owners (nested repeating)
5. Submit button: **Continue to Payment**

**Form-level settings** (unchanged)

- Title: Deed Request. Subtitle: "Thank you for contacting the firm about your deed. All fields are required unless marked optional."
- Theme: navy accent (#1E3A5F), white sections on a light warm-gray background (#F4F2EE).
- Every field is **Required** unless the table says otherwise. Required fields hidden by Show If do not block submission.
- Keep internal field names exactly as listed. They map to spec field IDs (table at the end) and feed the deed-drafting agent.
- **No fee amounts anywhere on the form.**
- **File uploads:** allow PDF, JPG, PNG, HEIC; up to 5 files per upload field; 10 MB per file. Set the entry retention policy before go-live (photo IDs and trust documents are sensitive). Uploaded files never go into the GitHub repo.

## Fields

Copy help text and acknowledgement wording word for word.

### 1. Acknowledgement (unchanged)

Content field with these two paragraphs, then the checkbox.

> I understand that the Firm does not collect documentary stamp taxes in connection with the deed. The State of Florida may later determine that documentary stamp taxes were due and may assess the tax and applicable penalties. Questions regarding documentary stamp taxes should be directed to the [Florida Department of Revenue](https://floridarevenue.com/taxes/taxesfees/Pages/doc_stamp.aspx).
>
> I also understand that the Firm does not advise whether changes to my deed may affect or reset my property taxes. Questions regarding property taxes should be directed to the Property Appraiser for the county where the property is located.

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| I acknowledge and understand the above. | Acknowledgement | Yes/No, checkbox | Must be checked | V1 |
| Have questions first? We can set up a paid 30-minute consultation for $250. | ConsultationNote | Content | — | "Book a consultation" link; Conrad supplies URL |

### 2. Your Contact Information

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Full name | RequesterName | Name | Yes | |
| Email | RequesterEmail | Email | Yes | |
| Phone | RequesterPhone | Phone (US) | Yes | |
| Your role in this transfer | RequesterRole | Choice, radio: Grantor (current owner) / Grantee (new owner) / Other | Yes | **New** |
| Please describe your role | RequesterRoleOther | Textbox | Yes, when shown | **New.** L10. Placeholder: "e.g., grantor's daughter, property manager, attorney" |
| (authorization note) | AuthorizationNote | Content | — | **New.** L11. **DRAFT:** "Because you are not a current owner, we need written authorization from the grantor before we can prepare the deed. Download the Grantor Authorization form, have each grantor sign it, and upload it below." Link to the authorization form (see `templates/grantor-authorization.md`) |
| Signed Grantor Authorization | GrantorAuthorization | File Upload | Yes, when shown | **New.** L11 |

### 3. Number of Deeds

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| How many properties (deeds) do you need prepared? | NumberOfDeeds | Choice, dropdown: 1–10 | Yes | **New.** Default 1. Help text: "Each property gets its own deed." |

### 4. Property Blocks

**Repeating Section** named `PropertyBlocks`. Item label: **Property {ItemNumber}**.

- Set **Minimum Items** and **Maximum Items** to `=NumberOfDeeds` so the right number of blocks appears and the client cannot add or remove them. Hide the add/remove buttons.
- **Verify in Cognito:** if your plan does not allow an expression for the item count, set Minimum 1, keep the **+ Add another property** button, and add validation V2 (block count must equal NumberOfDeeds).

Each Property Block contains 4a–4d in order.

#### 4a. Property

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Property address | PropertyAddress | Address (US) | Yes | Default state Florida |
| County | PropertyCounty | Choice, dropdown: the 67 Florida counties | Yes | **New.** Staff verifies against the property appraiser |
| Does this property have a mortgage on it? | HasMortgage | Choice, radio: No mortgage / Yes, it has a mortgage | Yes | L1 |
| (warning) | MortgageWarning | Content | — | L1. Amber callout (unchanged wording) |

#### 4b. Grantor(s): Current Owners

**Nested Repeating Section** named `Grantors` inside each Property Block. Help text (unchanged): "The person or people transferring the property. List **all current owners** exactly as their names appear on the current deed." Button: **+ Add another grantor**. Minimum 1.

Do not list a joining spouse as a separate grantor; the spouse fields below capture them.

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Grantor is | GrantorType | Choice, radio: An individual / A company / A trust | Yes | **Changed** (was two options). Default: An individual |
| **Individual** | | | | |
| Full legal name | GrantorName | Textbox | Yes, when shown | L2 |
| Mailing address | GrantorAddress | Address (US) | Yes | All types |
| Marital status | GrantorMaritalStatus | Choice, radio: Single / Married / Widowed / Divorced | Yes, when shown | L2 |
| Is this property your homestead (your primary residence)? | GrantorIsHomestead | Choice, radio: Yes / No | Yes, when shown | **New.** L4 |
| Spouse's full legal name | GrantorSpouseName | Textbox | Yes if homestead; optional if not | **Changed.** L4; required by L5 |
| (spouse must sign) | SpouseRequiredNote | Content | — | **New.** L5. **DRAFT:** "Because this property is your homestead, your spouse must also sign the new deed, even if your spouse is not listed on the current deed." |
| (spouse recommended) | SpouseRecommendedNote | Content | — | **New.** L6. **DRAFT:** "Because this property is not your homestead, your spouse is not required to sign. We recommend your spouse sign regardless to prevent issues with a sale later. If your spouse will sign, enter their name above." |
| Is your spouse's mailing address the same as yours? | SpouseSameAddress | Choice, radio: Yes / No | Yes, when shown | **New.** L7 |
| Spouse's mailing address | SpouseAddress | Address (US) | Yes, when shown | **New.** L8 |
| Spouse's photo ID | SpousePhotoID | File Upload | Yes, when shown | **New.** L7. Not in the paralegal list; added because the spouse is a signer. Remove if Conrad prefers |
| Is your late spouse listed on the current deed? | DeceasedSpouseOnDeed | Choice, radio: Yes / No | Yes, when shown | **New.** L12 |
| Death certificate | DeathCertificate | File Upload | Yes, when shown | **New.** L13. Help: "Upload a copy of the death certificate." |
| Is your former spouse listed on the current deed? | FormerSpouseOnDeed | Choice, radio: Yes / No | Yes, when shown | **New.** L14 |
| Final judgment of dissolution and/or settlement agreement | DivorceDocuments | File Upload | Yes, when shown | **New.** L15 |
| Photo ID | GrantorPhotoID | File Upload | Yes, when shown | **New.** L2. Help: "Upload a copy of a current government-issued photo ID (front)." |
| **Company** | | | | |
| Company name (exactly as registered) | GrantorEntityName | Textbox | Yes, when shown | L3 |
| State where the company was formed | GrantorEntityState | Choice, dropdown: US states | Yes, when shown | **New.** L3. Default Florida. Fills "a Florida limited liability company" |
| Is the company active or inactive? | GrantorEntityStatus | Choice, radio: Active / Inactive | Yes, when shown | **New.** L3 |
| (inactive warning) | GrantorInactiveWarning | Content | — | **New.** L16. Amber. **DRAFT:** "An inactive company may need to be reinstated before it can transfer property. You can still submit this form, and we will contact you about next steps." |
| Name of person signing for the company | GrantorSignatoryName | Textbox | Yes, when shown | L3 |
| Title (Manager, Member, President, etc.) | GrantorSignatoryTitle | Textbox | Yes, when shown | L3 |
| **Trust** | | | | |
| Trust name | GrantorTrustName | Textbox | Yes, when shown | **New.** L9. Placeholder: "The Jane Sample Revocable Trust" |
| Date of the trust | GrantorTrustDate | Date | Yes, when shown | **New.** L9 |
| Trustee name(s) | GrantorTrusteeNames | Textbox | Yes, when shown | **New.** L9. Replaces signatory fields for trusts |
| Trust documents | GrantorTrustDocuments | File Upload | Yes, when shown | **New.** L9. Help: "Upload the trust agreement, or a certification of trust, and any amendments." |
| **Signing (shown only when signers sign separately)** | | | | |
| State where this grantor will sign | GrantorSigningState | Choice, dropdown: US states | Yes, when shown | **New.** L18. Fills that signer's notary block |
| State where the spouse will sign | SpouseSigningState | Choice, dropdown: US states | Yes, when shown | **New.** L18 + spouse named |

#### 4c. Signing

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Will everyone signing this deed sign at the same time and place? | AllSignTogether | Choice, radio: Yes / No | Yes, when shown | **New.** L17. Help: "Includes any spouse who is signing." |
| (separate signing note) | SeparateSigningNote | Content | — | **New.** L18. "We will prepare a separate signature and notary section for each person." |

#### 4d. Grantee(s): New Owners

**Nested Repeating Section** named `Grantees` inside each Property Block. Help text (unchanged): "Everyone who will be on title after the transfer. If current owners will **stay on title**, list them here too, along with the person being added." Button: **+ Add another grantee**. Minimum 1.

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Grantee is | GranteeType | Choice, radio: An individual / A company / A trust | Yes | **New.** Default: An individual |
| Full legal name | GranteeName | Textbox | Yes, when shown | G1 |
| Mailing address | GranteeAddress | Address (US) | Yes | All types |
| Photo ID | GranteePhotoID | File Upload | Yes, when shown | **New.** G1 |
| Company name (exactly as registered) | GranteeEntityName | Textbox | Yes, when shown | **New.** G2 |
| State where the company was formed | GranteeEntityState | Choice, dropdown: US states | Yes, when shown | **New.** G2. Default Florida |
| Is the company active or inactive? | GranteeEntityStatus | Choice, radio: Active / Inactive | Yes, when shown | **New.** G2 |
| Trust name | GranteeTrustName | Textbox | Yes, when shown | **New.** G3 |
| Date of the trust | GranteeTrustDate | Date | Yes, when shown | **New.** G3 |
| Trustee name(s) | GranteeTrusteeNames | Textbox | Yes, when shown | **New.** G3 |
| Trust documents | GranteeTrustDocuments | File Upload | Yes, when shown | **New.** G3 |

**Optional — pending Conrad's decision (not in the paralegal list):** a "How will the new owners hold title?" question at the end of 4d, shown when there are two or more grantees: Joint tenants with right of survivorship / Tenants in common / Tenants by the entirety (married to each other) / Not sure, the attorney will advise. The survivorship template depends on this answer; without it, staff must ask. See `spec/deed-templates.md`.

## Conditional logic

Rules inside a repeating section apply per row. Expressions are a reference; confirm syntax in the Cognito editor.

| Rule | Applies to | Show if / condition | Expression (reference) |
|---|---|---|---|
| V1 | Acknowledgement | Error blocks submit unless checked: "Please check the acknowledgement to continue." | Error if `=Acknowledgement = false` |
| V2 | PropertyBlocks | Fallback only. Error: "Please add one property for each deed requested." | Error if `=PropertyBlocks.Count() <> NumberOfDeeds` |
| L1 | MortgageWarning | Property has a mortgage | `=HasMortgage = "Yes, it has a mortgage"` |
| L2 | GrantorName, GrantorMaritalStatus, GrantorPhotoID | Grantor is an individual | `=GrantorType = "An individual"` |
| L3 | GrantorEntityName, GrantorEntityState, GrantorEntityStatus, GrantorSignatoryName, GrantorSignatoryTitle | Grantor is a company | `=GrantorType = "A company"` |
| L4 | GrantorIsHomestead | Individual and married | `=GrantorType = "An individual" and GrantorMaritalStatus = "Married"` |
| L5 | SpouseRequiredNote; makes GrantorSpouseName required | Married and homestead | `=… and GrantorIsHomestead = "Yes"` |
| L6 | SpouseRecommendedNote | Married and not homestead | `=… and GrantorIsHomestead = "No"` |
| — | GrantorSpouseName | Shown once homestead is answered | `=… and GrantorIsHomestead <> null` |
| L7 | SpouseSameAddress, SpousePhotoID | Married and a spouse name is entered (either homestead answer) | `=… and GrantorSpouseName <> null` |
| L8 | SpouseAddress | L7 and address is not the same | `=… and SpouseSameAddress = "No"` |
| L9 | GrantorTrustName, GrantorTrustDate, GrantorTrusteeNames, GrantorTrustDocuments | Grantor is a trust | `=GrantorType = "A trust"` |
| L10 | RequesterRoleOther | Role is Other | `=RequesterRole = "Other"` |
| L11 | AuthorizationNote, GrantorAuthorization | Person submitting is not a grantor | `=RequesterRole <> "Grantor (current owner)"` |
| L12 | DeceasedSpouseOnDeed | Individual and widowed | `=GrantorType = "An individual" and GrantorMaritalStatus = "Widowed"` |
| L13 | DeathCertificate | Late spouse is on the deed | `=… and DeceasedSpouseOnDeed = "Yes"` |
| L14 | FormerSpouseOnDeed | Individual and divorced | `=GrantorType = "An individual" and GrantorMaritalStatus = "Divorced"` |
| L15 | DivorceDocuments | Former spouse is on the deed | `=… and FormerSpouseOnDeed = "Yes"` |
| L16 | GrantorInactiveWarning | Company is inactive | `=GrantorType = "A company" and GrantorEntityStatus = "Inactive"` |
| L17 | AllSignTogether | More than one signer on this property | `=Grantors.Count() > 1 or Grantors.Any(GrantorSpouseName <> null)` |
| L18 | SeparateSigningNote, GrantorSigningState, SpouseSigningState | Signers will not sign together | `=AllSignTogether = "No"` (SpouseSigningState also needs a spouse name) |
| G1 | GranteeName, GranteePhotoID | Grantee is an individual | `=GranteeType = "An individual"` |
| G2 | GranteeEntityName, GranteeEntityState, GranteeEntityStatus | Grantee is a company | `=GranteeType = "A company"` |
| G3 | GranteeTrustName, GranteeTrustDate, GranteeTrusteeNames, GranteeTrustDocuments | Grantee is a trust | `=GranteeType = "A trust"` |

None of the warnings (mortgage, inactive company) block submission. The firm reviews those files after submit (routing rules S1, S7, S8).

## Deed disclaimer

The paralegal asked whether the deed's NOTE paragraph ("This Quit Claim Deed has been prepared at the Grantor's request without examination or legal opinion of title…") belongs at the end of the form.

**Recommendation:** keep it on the deed, not the form. Put it as a footnote at the bottom of page 1, in a smaller font than the body, as she suggested. The templates currently place it in three different spots; the master template fixes the position (see `spec/deed-templates.md`).

The form's acknowledgement already covers doc stamps and property tax. It does not cover "no title search." **Open for Conrad:** add a third acknowledgement paragraph? **DRAFT** if yes:

> I understand that the Firm will prepare the deed at my request without a title search, lien search, or legal opinion of title, and that the deed provides no warranty of title.

## Testing and handoff

Use made-up data only. Send Conrad the preview link when done.

- [ ] Acknowledgement unchecked shows V1 and blocks submit
- [ ] NumberOfDeeds = 3 shows Property 1, 2, 3, each with its own grantor and grantee sections in order
- [ ] Role "Grantor" hides the authorization upload; "Grantee" and "Other" show it and make it required
- [ ] County dropdown lists all 67 Florida counties
- [ ] Married + homestead Yes: spouse name required, required note shows
- [ ] Married + homestead No: spouse name optional, recommended note shows; entering a name shows the same-address question
- [ ] Spouse address "No" shows and requires the spouse address
- [ ] Widowed + late spouse on deed shows and requires the death certificate; "No" hides it
- [ ] Divorced + former spouse on deed shows and requires divorce documents; "No" hides it
- [ ] Individual grantor and grantee require a photo ID upload
- [ ] Company shows name, state, active/inactive, signer, title; Inactive shows the amber warning and still submits
- [ ] Trust shows trust name, date, trustee, documents
- [ ] One grantor, no spouse: the signing question is hidden
- [ ] Two signers + "No" shows a signing-state field for each signer
- [ ] Hidden required fields do not block submission
- [ ] Form works on a phone, including uploads from the camera
- [ ] No fee amounts appear anywhere

**Open items for Conrad**

- [ ] Approve all **DRAFT** wording (spouse notes, inactive warning, authorization note, optional third acknowledgement)
- [ ] Approve the Grantor Authorization form (`templates/grantor-authorization.md`) — paralegal offered to build the printable version
- [ ] Add the vesting question to 4d? (see Optional above)
- [ ] Keep the spouse photo ID upload?
- [ ] Entry retention period for uploaded IDs and documents
- [ ] Carried over from Phase 1: LawPay page, consultation link URL, notification recipients and confirmation message, Spanish version

## Cognito name → spec field ID

| Cognito internal name | Spec field ID (`spec/intake-fields.md`) |
|---|---|
| Acknowledgement | `acknowledgement` |
| RequesterName / RequesterEmail / RequesterPhone | `requester_name` / `requester_email` / `requester_phone` |
| RequesterRole / RequesterRoleOther | `requester_role` / `requester_role_other` |
| GrantorAuthorization | `grantor_authorization_doc` |
| NumberOfDeeds | `number_of_deeds` |
| PropertyBlocks.PropertyAddress / PropertyCounty / HasMortgage | `property_address` / `property_county` / `has_mortgage` |
| PropertyBlocks.AllSignTogether | `all_sign_together` |
| Grantors.GrantorType | `grantor_type` |
| Grantors.GrantorName / GrantorEntityName / GrantorTrustName | `grantor_name` (by type) |
| Grantors.GrantorAddress | `grantor_address` |
| Grantors.GrantorMaritalStatus | `grantor_marital_status` |
| Grantors.GrantorIsHomestead | `is_homestead` |
| Grantors.GrantorSpouseName / SpouseSameAddress / SpouseAddress | `grantor_spouse_name` / `spouse_same_address` / `spouse_address` |
| Grantors.SpousePhotoID / GrantorPhotoID | `spouse_photo_id` / `grantor_photo_id` |
| Grantors.DeceasedSpouseOnDeed / DeathCertificate | `deceased_spouse_on_deed` / `death_certificate_doc` |
| Grantors.FormerSpouseOnDeed / DivorceDocuments | `former_spouse_on_deed` / `divorce_docs` |
| Grantors.GrantorEntityState / GrantorEntityStatus | `grantor_entity_state` / `grantor_entity_status` |
| Grantors.GrantorSignatoryName / GrantorSignatoryTitle | `grantor_signatory_name` / `grantor_signatory_title` |
| Grantors.GrantorTrustDate / GrantorTrusteeNames / GrantorTrustDocuments | `grantor_trust_date` / `grantor_signatory_name` (trustee) / `grantor_trust_docs` |
| Grantors.GrantorSigningState / SpouseSigningState | `grantor_signing_state` / `spouse_signing_state` |
| Grantees.GranteeType | `grantee_type` |
| Grantees.GranteeName / GranteeEntityName / GranteeTrustName | `grantee_name` (by type) |
| Grantees.GranteeAddress | `grantee_address` |
| Grantees.GranteePhotoID | `grantee_photo_id` |
| Grantees.GranteeEntityState / GranteeEntityStatus | `grantee_entity_state` / `grantee_entity_status` |
| Grantees.GranteeTrustDate / GranteeTrusteeNames / GranteeTrustDocuments | `grantee_trust_date` / `grantee_trustee_names` / `grantee_trust_docs` |
