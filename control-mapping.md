# Control Mapping

This document maps each capability in this project to the specific GDPR article or guidance it implements.

| Capability | Legal Basis / Guidance |
|---|---|
| Record of Processing Activities generation | GDPR Article 30(1) - controller record-keeping obligation |
| Purpose, legal basis, data subject/data category fields | GDPR Article 30(1)(b), (c) |
| Recipients tracking | GDPR Article 30(1)(d) |
| Third country transfer flagging | GDPR Article 30(1)(e) |
| Retention period recording | GDPR Article 30(1)(f) |
| Security measures recording | GDPR Article 30(1)(g) |
| Automated decision-making / systematic monitoring triggers | GDPR Article 35(3)(a), (c) |
| Large-scale special category/criminal offence data trigger | GDPR Article 35(3)(b) |
| Nine-criteria general screening (2+ criteria threshold) | EDPB Guidelines on DPIAs (WP248 rev.01), ICO DPIA guidance |

## Screening Tool Scope and Limitations

- This tool performs **DPIA screening** (should a DPIA be done) - it does not perform the DPIA itself. A flagged activity still requires a full DPIA to be completed separately, assessing necessity, proportionality, risk, and mitigations under Article 35(7).
- The "2 or more criteria" general threshold is applied as a practitioner rule of thumb, consistent with common guidance, but is not itself a strict legal test - screening output should be reviewed by a person with data protection expertise before being treated as final, particularly for borderline (single-criterion) cases.
- This tool covers UK GDPR / EU GDPR Article 35 criteria specifically. Some supervisory authorities (e.g. the ICO's own Article 35(4) list, CNIL's list in France) publish additional jurisdiction-specific "must-DPIA" categories not fully represented here; a real deployment operating in multiple jurisdictions would need to check the relevant local authority's published list as well.
- Article 30(5) provides a limited exemption from record-keeping for organisations with fewer than 250 employees, unless the processing is likely to result in a risk, is not occasional, or involves special category/criminal offence data. This tool assumes the record-keeping obligation applies and does not implement that exemption check.

## Review Cadence

Processing activity records and their DPIA screening status should be reviewed whenever an activity's scope, data categories, or recipients materially change, and at minimum annually as part of a standing data protection governance cycle.
