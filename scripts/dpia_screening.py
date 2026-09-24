#!/usr/bin/env python3
"""
DPIA Screening Engine
Applies the ICO/EDPB "nine criteria" (WP248) DPIA trigger logic to each
processing activity: under UK/EU guidance, meeting 2 or more criteria is a
strong indicator a DPIA is required under GDPR Article 35(3), and certain
single criteria (special category data at scale, automated decisions with
legal effect) can trigger a DPIA on their own.
"""

import json
from datetime import datetime, timezone

CRITERIA_LABELS = {
    "involves_special_category_data": "Processing of special category or highly sensitive data",
    "involves_criminal_offence_data": "Processing of criminal offence data",
    "involves_large_scale_processing": "Large-scale processing",
    "involves_systematic_monitoring": "Systematic monitoring of individuals",
    "involves_automated_decision_making_with_legal_effect": "Automated decision-making with legal or similarly significant effect",
    "involves_vulnerable_data_subjects": "Processing affecting vulnerable data subjects",
    "involves_new_technology": "Innovative use of new technology",
    "involves_data_matching_or_combining": "Data matching or combining datasets",
    "prevents_data_subjects_exercising_rights": "Processing that prevents data subjects exercising a right or using a service",
}

# Criteria that can independently trigger a DPIA even as a single hit,
# per ICO guidance on Article 35(3) - both are explicitly named in GDPR
# Article 35(3)(a) and (b).
SINGLE_TRIGGER_CRITERIA = {
    "involves_automated_decision_making_with_legal_effect",
    "involves_systematic_monitoring",
}

TWO_CRITERIA_THRESHOLD = 2


def load_activities():
    with open("activities/processing_activities.json") as f:
        return json.load(f)


def screen_activity(activity):
    screening = activity["dpia_screening"]
    matched_criteria = [k for k, v in screening.items() if v is True]

    single_trigger_hits = [c for c in matched_criteria if c in SINGLE_TRIGGER_CRITERIA]

    # Article 35(3)(b): large-scale processing of special category (Art 9) or
    # criminal offence (Art 10) data is an explicit, standalone DPIA trigger -
    # distinct from the general "2+ criteria" rule of thumb, and dependent on
    # BOTH conditions together, not either alone. Initially missing from this
    # tool's logic - added after cross-checking against ICO/EDPB source
    # guidance (see debugging-notes.md).
    large_scale_special_category_trigger = (
        screening.get("involves_large_scale_processing")
        and (screening.get("involves_special_category_data") or screening.get("involves_criminal_offence_data"))
    )

    meets_two_or_more = len(matched_criteria) >= TWO_CRITERIA_THRESHOLD

    dpia_required = bool(single_trigger_hits) or large_scale_special_category_trigger or meets_two_or_more

    if large_scale_special_category_trigger:
        reason = (
            "Triggers DPIA independently under Article 35(3)(b): large-scale "
            "processing of special category or criminal offence data"
        )
    elif single_trigger_hits:
        reason = (
            f"Triggers DPIA independently under Article 35(3): "
            f"{', '.join(CRITERIA_LABELS[c] for c in single_trigger_hits)}"
        )
    elif meets_two_or_more:
        reason = (
            f"Meets {len(matched_criteria)} of the ICO/EDPB nine criteria "
            f"(2+ is treated as a strong indicator a DPIA is required): "
            f"{', '.join(CRITERIA_LABELS[c] for c in matched_criteria)}"
        )
    else:
        reason = (
            f"Meets {len(matched_criteria)} of the nine criteria - below the "
            f"threshold for a mandatory DPIA. Recommend periodic re-screening "
            f"if the activity's scope changes."
        )

    return {
        "activity_id": activity["activity_id"],
        "activity_name": activity["activity_name"],
        "department": activity["department"],
        "criteria_matched_count": len(matched_criteria),
        "criteria_matched": [CRITERIA_LABELS[c] for c in matched_criteria],
        "dpia_required": dpia_required,
        "reason": reason,
    }


def main():
    activities = load_activities()
    results = [screen_activity(a) for a in activities]
    results.sort(key=lambda r: r["criteria_matched_count"], reverse=True)

    dpia_required_count = sum(1 for r in results if r["dpia_required"])

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "methodology": "ICO/EDPB nine-criteria screening (WP248), per GDPR Article 35(3)",
        "activities_screened": len(results),
        "dpia_required_count": dpia_required_count,
        "results": results,
    }

    output_path = f"reports/dpia-screening-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Screened {len(results)} activities. {dpia_required_count} require a DPIA.")
    print(f"Report written to {output_path}")
    for r in results:
        flag = "DPIA REQUIRED" if r["dpia_required"] else "No DPIA required"
        print(f"  [{flag}] {r['activity_id']} - {r['activity_name']} ({r['criteria_matched_count']} criteria)")


if __name__ == "__main__":
    main()
