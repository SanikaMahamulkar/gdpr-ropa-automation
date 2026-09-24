# Debugging Notes

## Incomplete DPIA trigger logic: found via guidance cross-check, not a code error

**Context:** the DPIA screening engine's first version implemented two of the standalone DPIA triggers from GDPR Article 35(3) - automated decision-making with legal effect, and systematic monitoring - plus the general "2 or more of the nine EDPB criteria" rule of thumb from WP248 guidance.

**What prompted a closer look:** PA-002 (Employee Health Records Management) matched only one screening criterion (special category data) and was correctly reported as not requiring a DPIA under the tool's logic. This result was checked against real ICO/EDPB source guidance rather than accepted on the basis that the ranking looked reasonable, because special category data processing is exactly the kind of case where getting a screening tool's logic subtly wrong has real compliance consequences.

**What the check found:** Article 35(3)(b) names a third explicit, standalone DPIA trigger that the tool's logic did not implement at all: large-scale processing of special category (Article 9) or criminal offence (Article 10) data. This is a combined condition - both "large-scale" and "special category/criminal offence data" must be true together - not either alone. The tool's original logic had no path to this trigger, meaning any hypothetical activity that was large-scale special-category processing but had fewer than 2 of the other nine general criteria would have been incorrectly screened as not requiring a DPIA.

**Fix:** added the Article 35(3)(b) combined-condition trigger as its own standalone check, independent of the general 2-criteria threshold. PA-002's screening outcome did not change (it is correctly not large-scale, so the new trigger does not apply to it either) - but the logic is now complete against all three explicit Article 35(3) triggers, rather than two of three, closing a real gap that the existing sample data happened not to expose.

**Why this matters for this specific tool:** a DPIA screening tool that silently omits one of the three statutory automatic triggers is exactly the kind of quiet, hard-to-notice gap that could let a genuinely high-risk activity proceed without the legally required assessment. This is why the fix was pursued even though none of the five sample activities' outcomes changed as a result - the value was in closing the gap before it produced a wrong answer, not only in response to one it had already produced.

## Note on the "2 or more criteria" threshold

EDPB/WP248 and later commentary (e.g. CIPL's response to the ICO's draft guidance) describe the "two or more criteria" rule as a rule of thumb / strong indicator, not an absolute legal requirement - some sources note a single criterion can be sufficient in some cases, and organisations are expected to apply judgement on borderline cases rather than treat the threshold as purely mechanical. This tool implements the two-or-more threshold as a screening aid, consistent with common practitioner guidance, but its output is explicitly framed as a screening recommendation for review, not a final legal determination - see control-mapping.md.
