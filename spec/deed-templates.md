# Deed Templates

How the drafting agent turns an intake record into a deed. Source: the seven quitclaim deeds the paralegal sent on October 30, 2026.

**The original source deeds are not in this repo.** They are completed client deeds with real names, addresses, parcel IDs, and legal descriptions, and they stay in the firm's Microsoft 365 environment.

`templates/deeds/source-scrubbed/` holds **scrubbed copies** of all seven: original Word formatting, with every name, address, parcel ID, legal description, and trust date replaced by fictitious values, and the author metadata and page thumbnail removed. The source deeds' drafting errors (C2, C3, C4, etc.) are kept on purpose so the copies match the originals. Use them for layout reference when building the .docx template. The scrub script is not committed because its find-list contains the real data.

The placeholder template is `templates/deeds/quitclaim-deed.md.j2`.

## Approach

The seven files share one body. They differ only in the grantor clause, grantee clause, one optional homestead clause, and the signature/notary blocks. So the repo carries **one master template** with conditional clauses, not seven copies. The agent picks clauses from intake fields; it never writes clause language itself.

Every clause in the master template is lifted from the firm's own deeds. Wording changes are limited to the cleanup items below, each marked for attorney review.

## Source variants → clause selection

| Source file | What makes it different | Selected when |
|---|---|---|
| Individ to Individ Deed | Base: individual grantor, individual grantees, joint signature block "as to both signatures" | `grantor_type = individual`, `all_sign_together` true or one signer |
| Individ to Individ Deed (right of survivorship) | Grantee clause adds "as joint tenants with right of survivorship" | `vesting_type = jtwros` |
| Individ to Individ Deed (signed separately) | One signature + witness + notary block **per signer**; witnesses labeled "as to [name]"; each notary block has its own state | `all_sign_together = false` |
| Individ to Individ Deed (NON HOMESTEAD LANGUAGE) | Adds grantor warranty that the property is not homestead or contiguous to homestead | Married individual grantor, `is_homestead = false`, spouse **not** signing |
| Individual to LLC QCD | Grantee clause: "[NAME], a [State] Limited Liability Company" | `grantee_type = company` |
| LLC to Individual QCD | Grantor clause names the company; signature block "BY: [signer] ITS: [title]"; notary names signer "as [title] of [company]" | `grantor_type = company` |
| Trust to Ind. Deed | Grantor clause "[TRUSTEE], AS TRUSTEE OF THE [TRUST] DATED [date], under Florida Statutes §689.073, with full power and authority…"; same text in signature and notary blocks | `grantor_type = trust` |

Clauses combine. An LLC grantor conveying to two individuals as JTWROS, signing separately, uses the company grantor clause, the survivorship grantee clause, and separate blocks.

### Joining spouse

When `grantor_spouse_name` is filled, the grantor clause reads "[GRANTOR], joined by [his/her] spouse, [SPOUSE]" (from the signed-separately deed), and the spouse gets a signature line and is named in the notary certificate. The base Individ to Individ deed had the spouse signing without the "joined by" language; the master template always includes it. **Attorney review.**

### Trust grantee

None of the seven deeds conveys **to** a trust. The master template uses the trust grantor wording pattern ("[TRUSTEE], as Trustee of the [TRUST] dated [date]") for a trust grantee. **Attorney review** before use.

## Deed disclaimer (NOTE)

The NOTE paragraph appears in all seven deeds but in three places: before "IN WITNESS WHEREOF" (five deeds), after the notary block (two deeds). The paralegal suggested a page-1 footnote in a smaller font.

The master template puts it in the **page 1 footer, 9 pt**, body stays 12 pt Courier. When the template is built as a .docx, use a first-page-only footer so it does not repeat. **Attorney review:** confirm a footer placement satisfies the firm's intent for the disclaimer to be read.

## Cleanup found in the source deeds

Described without client details. Each needs an attorney decision; none is applied silently to legal language.

| # | Deed | Issue | Master template |
|---|---|---|---|
| C1 | All seven | Notary certificate does not state "by means of [ ] physical presence or [ ] online notarization." Florida's statutory acknowledgment form appears to require it (§ 695.25 / § 117.05(13), Fla. Stat.; checklist item 7, **VERIFY**) | Adds the checkbox line. **Attorney confirm** |
| C2 | LLC to Individual | Company name in the body differs from the company in the signature block and notary certificate (carried over from another file); notary month differs from deed month | Single `grantor_name` field feeds all three places |
| C3 | LLC to Individual | Witness #2 has no "Address:" line | All witnesses get name and address lines (checklist item 2) |
| C4 | Signed separately | Second signer's witnesses are both labeled "Witness #1" | Numbered #1 / #2 per signer |
| C5 | Individ to Individ (base) | Two grantees with no vesting language; Florida defaults to tenants in common for non-spouses (§ 689.15, **VERIFY**) | States vesting from `vesting_type`; blank → F6 |
| C6 | Individ to Individ (base) | Grantees listed as "FIRST and FIRST LAST" rather than each full name | Each grantee's full legal name |
| C7 | All seven | Title alternates "QUIT CLAIM DEED" / "QUITCLAIM DEED", including inside one deed | "QUITCLAIM DEED" throughout. **Conrad pick** |
| C8 | Several | "by, [GRANTOR]" stray comma; "who are" / "addresses are" with a single person | Singular/plural by count |
| C9 | All seven | Header label "Property Control No." (Palm Beach term). Broward uses "Folio" | Label set per county from `config/firm.json`; default "Parcel Identification No." **Conrad pick** |
| C10 | All seven | 1-inch top margin on page 1. Confirm the 3" × 3" recording space at top right is clear (§ 695.26, checklist item 8, **VERIFY**) | Note for .docx build |
| C11 | Survivorship, LLC, Trust | Notary venue state/county left blank vs. filled in others | Fills `grantor_signing_state` / `notary_county` when known, else blank line |
| C12 | All seven | Marital descriptors are gendered ("a married man", "an unmarried woman") | Uses `grantor_descriptor`. **Conrad pick:** keep gendered (form must ask) or neutral ("a married person") |

## Merge rules for the agent

- Names in the deed body, signature blocks, and notary certificate are **ALL CAPS**; addresses are as entered.
- Deed date and notary date: "this ___ day of {{month}}, {{year}}" — day left blank for execution, month and year from the planned execution date. Dates otherwise fully spelled out (firm style).
- Consideration: "TEN DOLLARS ($10.00)" unless `consideration_amount` differs (→ F2).
- `tax_year` = execution year.
- Legal description is pasted verbatim from the vesting deed; never retyped or reformatted.
- Any unfilled field renders as `[[MISSING: field_id]]` and the draft cannot leave Stage 6.
- The agent lists every routing FLAG on a cover sheet, not in the deed.

## Next steps

- [ ] Attorney decisions on C1, C7, C9, C12, joining-spouse wording, trust grantee wording, and NOTE placement
- [ ] Build `quitclaim-deed.docx` from the master template (docxtpl / Jinja placeholders), 12 pt Courier, first-page footer for NOTE
- [ ] Test-render against `samples/` records and compare to the source deeds line by line
