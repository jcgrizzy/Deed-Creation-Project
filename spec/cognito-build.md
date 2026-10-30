# Deed Intake Form — Cognito Build Instructions

Mirror of the shared build doc (Claude Docs: "Deed Intake Form — Cognito Build Instructions"). If they differ, ask Conrad which is current.

## Scope

Build a one-page deed intake form in Cognito Forms for Kelley, Grant & Tanis, P.A. Clients use it to acknowledge the firm's disclaimers and submit the parties and property for a deed. The payment step (LawPay) is **out of scope for now**. Conrad will send those instructions separately.

## Mockup

Build the form to match this approved layout: [`design/intake-form-mockup.png`](../design/intake-form-mockup.png). A static HTML version is at [`design/intake-form-mockup.html`](../design/intake-form-mockup.html). It shows the default state: individual grantor, married, no mortgage.

## Form setup

Create one form named **Deed Request** with five sections and a submit button on a single page, in this order. Leave room for a Payment page at the end; do not build it yet.

1. Acknowledgement
2. Your Contact Information
3. Property Being Transferred (repeating)
4. Grantor(s): Current Owners (repeating)
5. Grantee(s): New Owners (repeating)
6. Submit button: label it **Continue to Payment** for now

**Form-level settings**

- Title: Deed Request. Subtitle: "Thank you for contacting the firm about your deed. All fields are required unless marked optional."
- Theme: navy accent (#1E3A5F), white sections on a light warm-gray background (#F4F2EE), to match the mockup.
- Mark every field below **Required** unless the table says otherwise.
- Keep internal field names exactly as listed. These map to the spec field IDs (see the mapping table at the end) and will feed the deed-drafting agent.
- **No fee amounts anywhere on the form.** Fees are handled in the email the firm sends the client.

## Fields

Copy help text and acknowledgement wording word for word; the firm's attorneys approved it.

### 1. Acknowledgement

Add a **Content** field with these two paragraphs, then the checkbox.

> I understand that the Firm does not collect documentary stamp taxes in connection with the deed. The State of Florida may later determine that documentary stamp taxes were due and may assess the tax and applicable penalties. Questions regarding documentary stamp taxes should be directed to the [Florida Department of Revenue](https://floridarevenue.com/taxes/taxesfees/Pages/doc_stamp.aspx).
>
> I also understand that the Firm does not advise whether changes to my deed may affect or reset my property taxes. Questions regarding property taxes should be directed to the Property Appraiser for the county where the property is located.

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| I acknowledge and understand the above. | Acknowledgement | Yes/No, displayed as a checkbox | Yes, must be checked | Validation rule V1 |
| Have questions first? We can set up a paid 30-minute consultation for $250. | ConsultationNote | Content | — | Add a "Book a consultation" link; Conrad will supply the URL |

### 2. Your Contact Information

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Full name | RequesterName | Name | Yes | Person filling out the form; may not be an owner |
| Email | RequesterEmail | Email | Yes | |
| Phone | RequesterPhone | Phone (US) | Yes | |

### 3. Property Being Transferred

**Repeating Section** named `Properties`. Help text: "Add each property separately." Button text: **+ Add another property**. Minimum 1.

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Property address | PropertyAddress | Address (US) | Yes | Default state to Florida |
| Does this property have a mortgage on it? | HasMortgage | Choice, radio buttons: "No mortgage" / "Yes, it has a mortgage" | Yes | Drives rule L1 |
| (warning) | MortgageWarning | Content | — | "A property with a mortgage needs attorney review before we can prepare the deed. You can still submit this form, and we will contact you about next steps." Amber callout |

### 4. Grantor(s): Current Owners

**Repeating Section** named `Grantors`. Help text: "The person or people transferring the property. List **all current owners** exactly as their names appear on the current deed." Button text: **+ Add another grantor**. Minimum 1.

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Grantor is | GrantorType | Choice, radio buttons: "An individual" / "A company or trust" | Yes | Default: An individual |
| Full legal name | GrantorName | Textbox | Yes | L2 |
| Company or trust name | GrantorEntityName | Textbox | Yes, when shown | L3 |
| Mailing address | GrantorAddress | Address (US) | Yes | |
| Name of person signing | GrantorSignatoryName | Textbox | Yes, when shown | L3 |
| Title (Manager, Trustee, etc.) | GrantorSignatoryTitle | Textbox | Yes, when shown | L3 |
| Marital status | GrantorMaritalStatus | Choice, radio buttons: Single / Married / Widowed / Divorced | Yes, when shown | L2 |
| Spouse's full name (to sign the deed) | GrantorSpouseName | Textbox | Yes, when shown | L4 |
| (spouse note) | SpouseNote | Content | — | L4. "If your spouse is **not** listed on the current deed, your spouse must also sign the new deed unless the property is not your homestead. We recommend your spouse sign regardless of homestead status to prevent issues with a sale later." |

### 5. Grantee(s): New Owners

**Repeating Section** named `Grantees`. Help text: "Everyone who will be on title after the transfer. If current owners will **stay on title**, list them here too, along with the person being added." Button text: **+ Add another grantee**. Minimum 1.

| Label | Internal name | Cognito type | Required | Notes |
|---|---|---|---|---|
| Full legal name | GranteeName | Textbox | Yes | |
| Mailing address | GranteeAddress | Address (US) | Yes | Florida recording requires the grantee's address |

## Conditional logic

Set with each field's **Show If** or custom-error rule. Rules inside a repeating section apply per row.

| Rule | Applies to | Condition | Expression (reference) |
|---|---|---|---|
| V1 | Acknowledgement | Custom error blocks submit unless checked. Error text: "Please check the acknowledgement to continue." | Error if `=Acknowledgement = false` |
| L1 | MortgageWarning | Show if the property has a mortgage | `=HasMortgage = "Yes, it has a mortgage"` |
| L2 | GrantorName, GrantorMaritalStatus | Show if the grantor is an individual | `=GrantorType = "An individual"` |
| L3 | GrantorEntityName, GrantorSignatoryName, GrantorSignatoryTitle | Show if the grantor is a company or trust | `=GrantorType = "A company or trust"` |
| L4 | GrantorSpouseName, SpouseNote | Show if individual **and** married | `=GrantorType = "An individual" and GrantorMaritalStatus = "Married"` |

A "Yes, it has a mortgage" answer does **not** stop submission. It only shows the warning; the firm reviews those files after submit (routing rule S1).

## Testing and handoff

Run each test with made-up data, then send Conrad the form's preview link.

- [ ] Submitting without the acknowledgement checked shows the V1 error and blocks submit
- [ ] "Yes, it has a mortgage" shows the amber warning; "No mortgage" hides it
- [ ] "A company or trust" shows entity name, signer, and title, and hides marital status
- [ ] "Married" shows spouse name and the spouse note; any other status hides them
- [ ] Two grantors with different answers each show their own fields
- [ ] Adding a second property, grantor, and grantee works; each new row starts blank
- [ ] Hidden required fields do not block submission
- [ ] Form displays correctly on a phone
- [ ] No fee amounts appear anywhere on the form

**Open items for Conrad**

- [ ] Payment page and LawPay link (instructions to follow)
- [ ] "Book a consultation" link URL
- [ ] Who receives submission notifications, and the confirmation message clients see after submitting
- [ ] Spanish version of the form

## Cognito name → spec field ID

| Cognito internal name | Spec field ID (`spec/intake-fields.md`) |
|---|---|
| Acknowledgement | `acknowledgement` (new — add to spec) |
| RequesterName / RequesterEmail / RequesterPhone | `requester_name` / `requester_email` / `requester_phone` |
| Properties.PropertyAddress | `property_address` |
| Properties.HasMortgage | `has_mortgage` |
| Grantors.GrantorType | `grantor_type` |
| Grantors.GrantorName / GrantorEntityName | `grantor_name` |
| Grantors.GrantorAddress | `grantor_address` |
| Grantors.GrantorMaritalStatus | `grantor_marital_status` |
| Grantors.GrantorSpouseName | `grantor_spouse_name` |
| Grantors.GrantorSignatoryName / GrantorSignatoryTitle | `grantor_signatory_name` / `grantor_signatory_title` |
| Grantees.GranteeName / GranteeAddress | `grantee_name` / `grantee_address` |
