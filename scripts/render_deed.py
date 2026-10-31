"""Render the master quitclaim deed template for each property block in an intake record.

Prototype for test-rendering only (no .docx yet). Usage:
    python scripts/render_deed.py samples/sample-intake-02.json [--month March --year 2027]

Any value the template needs but the record lacks prints as [[MISSING: name]].
"""
import argparse
import datetime as dt
import json
import pathlib
import re

import jinja2

ROOT = pathlib.Path(__file__).resolve().parent.parent


class Missing(jinja2.Undefined):
    def __str__(self):
        return f"[[MISSING: {self._undefined_name}]]"

    def upper(self):  # lets `| upper` keep the marker
        return str(self)


def long_date(iso):
    d = dt.date.fromisoformat(iso)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


def entity_form(name):
    n = (name or "").upper()
    if re.search(r"\bL\.?L\.?C\.?$", n):
        return "Limited Liability Company"
    if re.search(r"\b(INC|CORP|CORPORATION)\.?$", n):
        return "corporation"
    return None  # left undefined -> MISSING


def prepare(deed):
    for g in deed.get("grantors", []):
        if g.get("grantor_trust_date"):
            g["grantor_trust_date_long"] = long_date(g["grantor_trust_date"])
        if g.get("grantor_type") == "company" and entity_form(g.get("grantor_name")):
            g["grantor_entity_form"] = entity_form(g["grantor_name"])
        if g.get("spouse_same_address"):
            g.pop("spouse_address", None)
    for e in deed.get("grantees", []):
        if e.get("grantee_trust_date"):
            e["grantee_trust_date_long"] = long_date(e["grantee_trust_date"])
        if e.get("grantee_type") == "company" and entity_form(e.get("grantee_name")):
            e["grantee_entity_form"] = entity_form(e["grantee_name"])
    return deed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("record")
    ap.add_argument("--month", default=dt.date.today().strftime("%B"))
    ap.add_argument("--year", default=str(dt.date.today().year))
    a = ap.parse_args()

    firm = json.loads((ROOT / "config/firm.json").read_text())
    record = json.loads(pathlib.Path(a.record).read_text())
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(ROOT / "templates/deeds"),
        undefined=Missing,
        trim_blocks=False,
        extensions=["jinja2.ext.do"],
    )
    tpl = env.get_template("quitclaim-deed.md.j2")
    labels = firm["parcel_id_label"]
    for i, deed in enumerate(record["property_blocks"], 1):
        deed = prepare(deed)
        print(f"===== Property {i} =====")
        print(tpl.render(
            firm=firm,
            deed=deed,
            execution={"month": a.month, "year": a.year},
            parcel_label=labels.get(deed.get("property_county"), labels["_default"]),
        ))


if __name__ == "__main__":
    main()
