#!/usr/bin/env python3
"""
Generates a GDPR Article 30-compliant Record of Processing Activities (ROPA)
document, combining processing activity data with the latest DPIA screening
results into a single audit-ready record.
"""

import json
import glob
from datetime import datetime, timezone


def load_activities():
    with open("activities/processing_activities.json") as f:
        return json.load(f)


def latest_dpia_screening():
    files = sorted(glob.glob("reports/dpia-screening-*.json"))
    if not files:
        raise SystemExit("No DPIA screening results found. Run dpia_screening.py first.")
    with open(files[-1]) as f:
        return json.load(f), files[-1]


def main():
    activities = load_activities()
    dpia_data, dpia_path = latest_dpia_screening()
    dpia_by_id = {r["activity_id"]: r for r in dpia_data["results"]}

    lines = []
    lines.append("# Record of Processing Activities (ROPA)")
    lines.append("")
    lines.append("Maintained under GDPR Article 30(1) (controller record-keeping obligation).")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"**Activities recorded:** {len(activities)}")
    lines.append(f"**DPIA screening source:** `{dpia_path}`")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| ID | Activity | Department | Legal Basis | Special Category Data | Third Country Transfer | DPIA Required |")
    lines.append("|---|---|---|---|---|---|---|")
    for a in activities:
        dpia = dpia_by_id.get(a["activity_id"], {})
        special_cat = "Yes" if a["dpia_screening"]["involves_special_category_data"] else "No"
        transfer = "Yes" if a["third_country_transfers"] else "No"
        dpia_flag = "**YES**" if dpia.get("dpia_required") else "No"
        lines.append(
            f"| {a['activity_id']} | {a['activity_name']} | {a['department']} | "
            f"{a['legal_basis'].replace('_', ' ').title()} | {special_cat} | {transfer} | {dpia_flag} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Full Records (Article 30(1) Required Fields)")
    lines.append("")

    for a in activities:
        dpia = dpia_by_id.get(a["activity_id"], {})
        lines.append(f"### {a['activity_id']}: {a['activity_name']}")
        lines.append("")
        lines.append(f"- **Controller:** {a['controller_name']}")
        lines.append(f"- **Department:** {a['department']}")
        lines.append(f"- **Purpose of processing (Art. 30(1)(b)):** {a['purpose_of_processing']}")
        lines.append(f"- **Legal basis:** {a['legal_basis'].replace('_', ' ').title()}")
        lines.append(f"- **Categories of data subjects (Art. 30(1)(c)):** {', '.join(a['categories_of_data_subjects'])}")
        lines.append(f"- **Categories of personal data (Art. 30(1)(c)):** {', '.join(a['categories_of_personal_data'])}")
        lines.append(f"- **Categories of recipients (Art. 30(1)(d)):** {', '.join(a['categories_of_recipients'])}")

        if a["third_country_transfers"]:
            lines.append(f"- **Third country transfers (Art. 30(1)(e)):** Yes — {a['transfer_details']}")
        else:
            lines.append("- **Third country transfers (Art. 30(1)(e)):** None")

        lines.append(f"- **Retention period (Art. 30(1)(f)):** {a['retention_period']}")
        lines.append(f"- **Security measures (Art. 30(1)(g)):** {a['security_measures']}")
        lines.append("")

        if dpia:
            flag = "**DPIA REQUIRED**" if dpia["dpia_required"] else "DPIA not required"
            lines.append(f"- **DPIA screening outcome:** {flag}")
            lines.append(f"  - {dpia['reason']}")

        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("This ROPA should be reviewed and re-screened whenever a recorded activity's scope, "
                  "data categories, or recipients change, and at minimum annually. Activities flagged "
                  "as requiring a DPIA should not proceed (or continue, if already live) without a "
                  "completed DPIA on file.")

    output_path = f"reports/ropa-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.md"
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"ROPA written to {output_path}")


if __name__ == "__main__":
    main()
