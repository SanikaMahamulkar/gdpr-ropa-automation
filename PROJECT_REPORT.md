# GDPR Data Mapping & ROPA Automation - Project Report

Author: Sanika Mahamulkar, MSc Cybersecurity, University of Bristol
Repository: https://github.com/SanikaMahamulkar/gdpr-ropa-automation
Date: September 2026

## Executive Summary

This project builds GDPR privacy compliance tooling: a structured data model for processing activities, an automated DPIA screening engine implementing real ICO/EDPB trigger logic under Article 35, and a Record of Processing Activities generator satisfying Article 30(1)'s controller record-keeping obligation. It extends the earlier project series into privacy-specific compliance, a discipline increasingly bundled into GRC Analyst roles but rarely demonstrated by entry-level candidates with working tooling behind it.

Five sample processing activities were screened, correctly identifying two requiring a DPIA. During development, the screening logic was checked against real ICO/EDPB source guidance rather than accepted on the strength of a plausible-looking result, which surfaced a genuine gap: the tool initially implemented only two of the three explicit statutory DPIA triggers under Article 35(3), missing the large-scale special-category-data trigger entirely. This was found and fixed before it produced an incorrect result on the available sample data - the check was prompted by wanting to understand *why* a borderline case (sensitive HR data) was correctly screened as not requiring a DPIA, not by an existing wrong answer.

## Objectives

1. Build a structured data model capturing everything GDPR Article 30(1) requires a controller to record.
2. Build an automated DPIA screening engine implementing real Article 35(3) and EDPB WP248 guidance, not an approximation.
3. Generate an audit-ready ROPA document combining processing activity data with DPIA screening outcomes.
4. Test the screening logic against a genuinely varied set of processing activities, not a single easy case.
5. Verify the tool's legal logic against primary/authoritative guidance rather than assuming a reasonable-looking implementation is correct.

## Methodology

Five processing activities were constructed with deliberately different risk profiles: routine transactional processing, sensitive employee health data at small scale, ad-tech behavioural tracking with international transfers, an automated credit-scoring system with legal effect, and a low-risk internal IT process. This spread was designed to exercise the screening logic's edge cases - particularly the question of whether sensitive data alone, without scale, should trigger a DPIA.

## A Genuine Gap, Found Through Verification Rather Than a Wrong Answer

The DPIA screening engine's first version implemented two of GDPR's three explicit Article 35(3) DPIA triggers - automated decision-making with legal effect, and systematic monitoring - alongside the general EDPB "two or more of nine criteria" rule of thumb. When the sensitive HR health-data activity (PA-002) was correctly screened as not requiring a DPIA, this result was checked against primary ICO/EDPB guidance rather than accepted because it looked reasonable, given how consequential getting special-category-data screening wrong could be in a real deployment.

That check surfaced Article 35(3)(b): large-scale processing of special category or criminal offence data is itself an explicit, standalone DPIA trigger - a combined condition requiring both "large-scale" and "special category/criminal offence data" together, entirely separate from the general nine-criteria threshold. The tool's original logic had no path to this trigger at all. PA-002's own screening result did not change once the trigger was added (the activity is genuinely not large-scale, so the new trigger correctly does not apply to it either) - but the fix closed a real gap that the existing sample data happened not to expose, which is precisely why the verification step mattered rather than being redundant.

Full detail, including a note on the actual (non-absolute) legal status of the "two or more criteria" rule of thumb, is in debugging-notes.md.

## Control Mapping

Full detail in control-mapping.md. In summary: every ROPA field maps to a specific Article 30(1) sub-clause (purpose, legal basis, data subject/data categories, recipients, transfers, retention, security measures), and the screening engine implements all three Article 35(3) explicit triggers plus the EDPB nine-criteria general screen. The tool's scope and limitations are stated explicitly, including that it performs DPIA *screening* only (not the DPIA itself), that the two-criteria threshold is a practitioner rule of thumb rather than strict law, and that it does not implement the Article 30(5) small-organisation exemption.

## Conclusion

This project delivers working GDPR privacy compliance tooling validated against real regulatory guidance, including a genuine gap in its own legal logic found through deliberate verification rather than in response to an obviously wrong result. It demonstrates a specific, distinctive GRC skill - privacy/data protection tooling grounded in actual Article 30 and Article 35 requirements - that most entry-level GRC candidates have not built working software to demonstrate.

## Skills Demonstrated

- GDPR Article 30 and Article 35 practical application: record-keeping requirements, DPIA trigger criteria
- ICO/EDPB (WP248) guidance research and application to real screening logic
- Verifying a tool's legal/business logic against primary source guidance rather than assuming a plausible implementation is correct
- Distinguishing a rule-of-thumb heuristic from a strict legal requirement, and documenting that distinction for the tool's users
- Python scripting for structured data processing and audit-ready report generation
- Privacy programme documentation: ROPA production, DPIA screening records
- Deliberate edge-case test data design to surface gaps a simple test set would miss
