"""Create portfolio-ready exploratory charts from processed claims."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "outputs" / "claims_processed.csv"
OUT = ROOT / "visuals"
OUT.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(INPUT, parse_dates=["service_date"])
    denied = df[df["denied_flag"].astype(str).str.lower().isin(["true", "1"])].copy()
    sns.set_theme(style="whitegrid")

    # 1: Denial rate by payer
    payer = df.groupby("payer").agg(claims=("claim_id", "count"), denied=("denied_flag", "sum"))
    payer["denial_rate_pct"] = 100 * payer["denied"] / payer["claims"]
    payer = payer.sort_values("denial_rate_pct")
    ax = payer["denial_rate_pct"].plot(kind="barh", figsize=(9, 5))
    ax.set(title="Denial Rate by Payer", xlabel="Denial rate (%)", ylabel="Payer")
    plt.tight_layout(); plt.savefig(OUT / "denial_rate_by_payer.png", dpi=180); plt.close()

    # 2: Top denial codes by claim volume
    top = denied.groupby(["carc_code", "denial_reason"]).size().sort_values().tail(10)
    labels = [f"{code} — {reason}" for code, reason in top.index]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels, top.values)
    ax.set(title="Top Denial Reasons by Claim Count", xlabel="Denied claims", ylabel="")
    plt.tight_layout(); plt.savefig(OUT / "top_denial_reasons.png", dpi=180); plt.close()

    # 3: Monthly denial rate
    df["service_month"] = df["service_date"].dt.to_period("M").astype(str)
    monthly = df.groupby("service_month").agg(claims=("claim_id", "count"), denied=("denied_flag", "sum"))
    monthly["denial_rate_pct"] = 100 * monthly["denied"] / monthly["claims"]
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly.index, monthly["denial_rate_pct"], marker="o")
    ax.set(title="Monthly Denial Rate Trend", xlabel="Service month", ylabel="Denial rate (%)")
    ax.tick_params(axis="x", rotation=60)
    plt.tight_layout(); plt.savefig(OUT / "monthly_denial_trend.png", dpi=180); plt.close()

    # 4: Denied exposure by specialty
    specialty = denied.groupby("provider_specialty")["denied_amount"].sum().sort_values()
    ax = specialty.plot(kind="barh", figsize=(9, 5))
    ax.set(title="Denied Amount Exposure by Provider Specialty", xlabel="Exposure (currency units)", ylabel="Specialty")
    plt.tight_layout(); plt.savefig(OUT / "exposure_by_specialty.png", dpi=180); plt.close()

    # 5: Specialty x denial reason heatmap
    pivot = denied.pivot_table(index="provider_specialty", columns="carc_code",
                               values="claim_id", aggfunc="count", fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt="g", cmap="Blues", ax=ax)
    ax.set(title="Denied Claim Volume: Specialty vs CARC", xlabel="CARC code", ylabel="Provider specialty")
    plt.tight_layout(); plt.savefig(OUT / "specialty_carc_heatmap.png", dpi=180); plt.close()
    print(f"Charts saved to {OUT}")

if __name__ == "__main__":
    main()
