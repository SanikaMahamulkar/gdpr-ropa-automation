# GDPR Data Mapping & ROPA Automation

Automated GDPR compliance tooling: catalogs data processing activities, applies ICO/EDPB DPIA screening logic to flag activities requiring a Data Protection Impact Assessment, and generates an Article 30-compliant Record of Processing Activities (ROPA).

This project extends the GRC/security engineering project series into privacy-specific compliance, a discipline increasingly bundled into GRC Analyst roles.

## Tech stack

- **Language:** Python 3 (no external dependencies)
- **Data:** structured JSON processing activity records
- **Output:** JSON DPIA screening results + audit-ready Markdown ROPA document

## Repository structure

- `data_model/schema.json` - the processing activity data model: Article 30(1) required fields + Article 35 DPIA screening fields
- `activities/processing_activities.json` - 5 sample processing activities with deliberately varied risk profiles
- `scripts/dpia_screening.py` - DPIA screening engine, implementing all three Article 35(3) explicit triggers plus the EDPB nine-criteria general screen
- `scripts/generate_ropa.py` - generates the full Article 30(1)-compliant ROPA document, combining activity data with DPIA screening outcomes
- `control-mapping.md` - maps every capability to its specific GDPR article, and documents the tool's scope and limitations
- `debugging-notes.md` - a real gap in the DPIA trigger logic, found via cross-checking against ICO/EDPB source guidance, and fixed

## Progress log

- [x] Processing activity data model covering Article 30(1) and Article 35 DPIA screening fields
- [x] 5 sample processing activities with deliberately varied risk profiles (routine transactional, sensitive HR data, ad-tech with international transfers, automated credit decisions, low-risk internal)
- [x] DPIA screening engine implementing all three Article 35(3) explicit triggers plus the EDPB nine-criteria general screen
- [x] Found and fixed a real gap: the tool initially implemented only 2 of 3 explicit Article 35(3) triggers, found via cross-checking against ICO/EDPB source guidance rather than accepting a plausible-looking result
- [x] ROPA generator producing a full Article 30(1)-compliant record
- [x] Control mapping to specific GDPR articles, with documented tool scope and limitations
- [ ] Full project report

## Sample findings

Of 5 sample processing activities, 2 were correctly flagged as requiring a DPIA: an automated credit risk-scoring system (automated decision-making with legal effect) and a website behavioural ad-targeting system (systematic monitoring, international transfers). A sensitive HR health-data activity was correctly screened as not requiring a DPIA under Article 35(3)(b) specifically because it is not large-scale processing - demonstrating the screening logic distinguishes between "sensitive data present" and the actual statutory trigger, rather than over-flagging on sensitivity alone.

## Author

Sanika Mahamulkar - MSc Cybersecurity, University of Bristol
