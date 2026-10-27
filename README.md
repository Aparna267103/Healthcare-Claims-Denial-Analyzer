# Healthcare Claims Denial & Leakage Analyzer

An end-to-end healthcare claims analytics project built using **Python, Pandas, SQL, and Power BI**. This project uses synthetic healthcare claims data to analyze denial patterns, identify revenue leakage risks, and track appeal recovery.

> **Disclaimer:** This project uses synthetic data for educational and portfolio purposes only. It does not contain real patient or payer data.

## Project Overview

Healthcare claim denials can create revenue cycle challenges for healthcare organizations. This project demonstrates how data analytics can help identify denial drivers, quantify denied-amount exposure, and monitor appeal recovery.

The solution combines data generation, data quality checks, feature engineering, SQL analysis, and interactive Power BI dashboards.

## Business Questions

- What percentage of claims are denied overall and by payer?
- Which Claim Adjustment Reason Codes (CARCs) contribute most to denial volume?
- Which provider specialties and CPT codes require operational review?
- How much denied exposure has been recovered through appeals?
- What is the appeal success rate?
- How does the denial rate change over time?

## Technology Stack

- **Python** — data generation and processing
- **Pandas** — data cleaning, quality checks, and feature engineering
- **SQL** — analytical queries using SQLite
- **Power BI** — interactive dashboards and KPI reporting
- **Matplotlib** — Python charts and visualizations, if implemented

## Project Architecture

```text
Synthetic Claims Data
        |
        v
Python Data Generation
        |
        v
Pandas Data Quality Checks
and Feature Engineering
        |
        v
SQLite Database
        |
        v
SQL Analysis
        |
        v
Power BI Dashboard
and Python Visualizations
```

## Repository Structure

```text
healthcare_claims_denial_analyzer/
|
|-- src/
|   |-- generate_data.py
|   |-- pipeline.py
|   |-- visualize.py
|
|-- sql/
|   |-- analysis_queries.sql
|
|-- data/
|   |-- claims_raw.csv
|
|-- outputs/
|   |-- claims_processed.csv
|   |-- data_quality_issues.csv
|   |-- claims_analyzer.db
|
|-- visuals/
|
|-- screenshots/
|   |-- Executive.png
|   |-- Root_Cause.png
|   |-- Recovery.png
|   |-- Action_Center.png
|
|-- requirements.txt
|-- README.md
```

*Note: This is the intended project structure. Keep only the files and folders that actually exist in your repository. Generated datasets, database files, and visualizations may be created when you run the pipeline.*

## Power BI Dashboard

The dashboard is organized into four pages to provide executive insights, denial root-cause analysis, appeal recovery monitoring, and operational prioritization.

### 1. Executive Overview

Provides a high-level summary of claims performance and financial exposure.

**Key KPIs**
- Total Claims
- Denial Rate %
- Denied Exposure
- Appeal Recovered
- Net Unrecovered

**Visualizations**
- Denial Rate % by Payer
- Denied Claims by CARC Code
- Monthly Denial Rate Trend
- Denied Exposure and Appeal Recovery by Payer, where supported by the data model

![Executive Overview](screenshots/Executive.png)

### 2. Denial Root Cause

Explores denial patterns across payer, provider specialty, procedure, and denial reason.

**Visualizations**
- Provider Specialty × CARC Code matrix
- Denied Exposure by CPT Code
- Claim-level details by payer, plan, CPT, and CARC
- Drill-through to claim details, if configured

![Denial Root Cause](screenshots/Root_Cause.png)

### 3. Appeals & Recovery

Tracks appeal outcomes and the recovery of denied amounts.

**Key KPIs**
- Appeals Submitted
- Appeals Won
- Appeal Success Rate %
- Appeal Recovered

**Visualizations**
- Appeal Success Rate by Payer
- Denial Volume vs. Exposure by Denial Reason
- Appeal status and recovered amount by Claim ID

![Appeals and Recovery](screenshots/Recovery.png)

### 4. Action Center

Supports prioritization of claims requiring operational review.

Suggested focus areas include high denied exposure, frequent denial reasons, unresolved appeals, and payer or specialty patterns that warrant investigation.

![Action Center](screenshots/Action_Center.png)

## Metric Definitions

| Metric | Definition |
|---|---|
| Total Claims | Count of claims in the analyzed dataset |
| Denial Rate | Claims with a denial code divided by all claims, based on the project's defined logic |
| Denied Exposure | For denied claims, the non-negative difference between billed and paid amounts |
| Appeal Recovered | Amount recorded as recovered through appeals |
| Net Unrecovered | Non-negative denied exposure less recorded appeal recovery |
| Appeal Success Rate | Appeals won divided by appeals submitted, subject to the dataset's status logic |

**Important:** Denied exposure is an analytical estimate, not confirmed financial loss. Net unrecovered exposure is not necessarily a final accounting write-off.

## Data Quality and Analytical Considerations

- The dataset represents synthetic claim-level records.
- Claim-level and service-line-level denial calculations may produce different results.
- Partial payments and adjustments require consistent business rules.
- Appeal success rates should ideally use resolved appeals as the denominator.
- CARC and RARC are distinct code sets and should not be treated as interchangeable.
- Code descriptions and operational rules should be validated against appropriate official references before real-world use.

## Getting Started

### Prerequisites

- Python 3.x
- pip
- Power BI Desktop
- SQLite-compatible database tools, if running SQL queries separately

### Installation

Clone the repository:

```bash
git clone https://github.com/Aparna267103/Healthcare-Claims-Denial-Analyzer.git
cd Healthcare-Claims-Denial-Analyzer
```

Create and activate a virtual environment on Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Pipeline

Run these commands only if the corresponding scripts exist in your repository:

```bash
python src/generate_data.py
python src/pipeline.py
python src/visualize.py
```

Expected outputs, depending on the implemented scripts:

- `data/claims_raw.csv` — synthetic raw claims
- `outputs/claims_processed.csv` — processed claims
- `outputs/data_quality_issues.csv` — data quality findings
- `outputs/claims_analyzer.db` — SQLite database
- `visuals/` — generated charts

Run the queries in `sql/analysis_queries.sql` against the generated database.

## Power BI Setup

1. Open the Power BI report.
2. Import `outputs/claims_processed.csv` or connect to the SQLite database.
3. Verify date, payer, plan, provider specialty, CPT, and denial-code fields.
4. Create and validate the KPI measures.
5. Configure slicers and their interactions across report visuals.
6. Validate the displayed metrics against the source data.

## Key Insights

Use this section to summarize findings from your completed dashboard, such as:

- Payers with comparatively high denial rates
- CARC codes contributing the most denial volume
- Specialties or CPT codes with high denied exposure
- Amounts recovered through appeals
- Areas recommended for further operational review

*Add findings calculated from your actual dataset rather than assuming example values are universal results.*

## Future Improvements

- Build a star schema with FactClaims, DimPayer, DimProvider, DimDate, and DimDenialReason.
- Separate claim-header and service-line data grains.
- Model the claim lifecycle, including initial denial, corrected claim, appeal, and final disposition.
- Add automated tests for duplicate IDs, invalid dates, negative amounts, and recovery inconsistencies.
- Improve appeal status handling and time-based analysis.
- Add refresh documentation and reproducible data validation checks.

## Privacy and Security

This portfolio project uses synthetic data. Real healthcare data requires appropriate authorization, minimum-necessary access, encryption, audit logging, and applicable privacy and security controls.

## Author

**Aparna V**

- GitHub: https://github.com/Aparna267103

## Project Summary

Built an end-to-end healthcare claims denial analytics solution using Python, Pandas, SQL, and Power BI to explore denial patterns, quantify denied-amount exposure, and monitor appeal recovery using synthetic data.
