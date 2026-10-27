"""Generate clearly synthetic healthcare claims data for portfolio/demo use."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)

N = 5000
payers = ["Apex Health", "BlueRiver", "CedarCare", "NorthStar", "Unity Health"]
specialties = ["Primary Care", "Cardiology", "Orthopedics", "Dermatology", "Emergency Medicine", "Radiology"]
plans = ["PPO", "HMO", "EPO", "Medicare Advantage", "Medicaid Managed Care"]
cpts = ["99213", "99214", "93000", "71046", "73721", "80053", "36415", "29881"]
icds = ["I10", "E11.9", "M25.561", "J06.9", "R07.9", "L30.9", "Z00.00"]
carcs = ["", "CO-16", "CO-197", "CO-29", "PR-96", "CO-4", "CO-50", "CO-151"]
reason = {
    "": "Paid / No denial",
    "CO-16": "Missing information",
    "CO-197": "Authorization required",
    "CO-29": "Filing limit exceeded",
    "PR-96": "Non-covered charge",
    "CO-4": "Procedure / modifier mismatch",
    "CO-50": "Medical necessity",
    "CO-151": "Documentation insufficient",
}
denial_probs = [0.68, 0.09, 0.06, 0.035, 0.04, 0.035, 0.035, 0.025]
dates = pd.to_datetime(rng.choice(pd.date_range("2025-01-01", "2026-09-30", freq="D"), N))
billed = np.round(rng.lognormal(mean=5.2, sigma=0.75, size=N), 2)
status_codes = rng.choice(carcs, size=N, p=denial_probs)
paid = np.where(status_codes == "", np.round(billed * rng.uniform(0.55, 0.95, N), 2), 0.0)
# A portion of denied claims have a partial payment/adjustment; keep this synthetic and explicit.
partial = (status_codes != "") & (rng.random(N) < 0.08)
paid[partial] = np.round(billed[partial] * rng.uniform(0.05, 0.35, partial.sum()), 2)
appeal_eligible = (status_codes != "") & (rng.random(N) < 0.58)
appeal_submitted = appeal_eligible & (rng.random(N) < 0.62)
appeal_won = appeal_submitted & (rng.random(N) < 0.43)
recovered = np.where(appeal_won, np.round((billed - paid) * rng.uniform(0.35, 0.9, N), 2), 0.0)

df = pd.DataFrame({
    "claim_id": [f"CLM{i:06d}" for i in range(1, N + 1)],
    "service_date": dates,
    "payer": rng.choice(payers, N),
    "plan_type": rng.choice(plans, N),
    "provider_id": [f"PRV{x:04d}" for x in rng.integers(1, 181, N)],
    "provider_specialty": rng.choice(specialties, N),
    "cpt_code": rng.choice(cpts, N),
    "icd10_code": rng.choice(icds, N),
    "billed_amount": billed,
    "paid_amount": paid,
    "carc_code": status_codes,
    "denial_reason": [reason[x] for x in status_codes],
    "appeal_submitted": appeal_submitted,
    "appeal_won": appeal_won,
    "appeal_recovered_amount": recovered,
})
df["claim_status"] = np.where(df["carc_code"].eq(""), "Paid", np.where(df["paid_amount"].gt(0), "Partially Paid", "Denied"))
df.to_csv(OUT / "claims_raw.csv", index=False)
print(f"Created {len(df):,} synthetic claims at {OUT / 'claims_raw.csv'}")
