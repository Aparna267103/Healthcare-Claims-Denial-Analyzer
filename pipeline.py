"""Clean synthetic claims, derive metrics, export CSVs and load SQLite."""
from pathlib import Path
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

REQUIRED = [
    "claim_id", "service_date", "payer", "plan_type", "provider_id",
    "provider_specialty", "cpt_code", "icd10_code", "billed_amount",
    "paid_amount", "carc_code", "denial_reason", "appeal_submitted",
    "appeal_won", "appeal_recovered_amount", "claim_status"
]

def main():
    source = DATA / "claims_raw.csv"
    if not source.exists():
        raise FileNotFoundError("Run: python src/generate_data.py")
    df = pd.read_csv(source)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["service_date"] = pd.to_datetime(df["service_date"], errors="coerce")
    numeric = ["billed_amount", "paid_amount", "appeal_recovered_amount"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).clip(lower=0)
    for col in ["appeal_submitted", "appeal_won"]:
        df[col] = df[col].astype(str).str.lower().map({"true": True, "false": False, "1": True, "0": False}).fillna(False)

    df["carc_code"] = df["carc_code"].fillna("").astype(str).str.strip().str.upper()
    df["denied_flag"] = df["carc_code"].ne("")
    df["denied_amount"] = np.where(df["denied_flag"], (df["billed_amount"] - df["paid_amount"]).clip(lower=0), 0)
    df["potential_exposure"] = df["denied_amount"]
    df["net_unrecovered_amount"] = (df["denied_amount"] - df["appeal_recovered_amount"]).clip(lower=0)
    df["service_month"] = df["service_date"].dt.to_period("M").astype(str)
    df["appeal_eligible_flag"] = df["denied_flag"] & df["appeal_submitted"]
    df["appeal_won_flag"] = df["appeal_submitted"] & df["appeal_won"]

    # Quality checks; do not silently deduplicate claims without a business rule.
    df["data_quality_issue"] = ""
    df.loc[df["service_date"].isna(), "data_quality_issue"] += "Invalid service date; "
    df.loc[df["claim_id"].duplicated(keep=False), "data_quality_issue"] += "Duplicate claim ID; "
    df.loc[df["paid_amount"] > df["billed_amount"], "data_quality_issue"] += "Paid exceeds billed; "
    df.loc[df["appeal_recovered_amount"] > df["denied_amount"], "data_quality_issue"] += "Recovery exceeds denied amount; "

    df.to_csv(OUT / "claims_processed.csv", index=False)
    df[df["data_quality_issue"].ne("")].to_csv(OUT / "data_quality_issues.csv", index=False)

    engine = create_engine(f"sqlite:///{(OUT / 'claims_analyzer.db').as_posix()}")
    df.to_sql("claims", engine, if_exists="replace", index=False)
    print(f"Processed {len(df):,} rows")
    print(f"Quality issues: {(df['data_quality_issue'] != '').sum():,}")
    print(f"SQLite database: {OUT / 'claims_analyzer.db'}")

if __name__ == "__main__":
    main()
