-- SQLite-compatible queries. Table is created by src/pipeline.py.

-- 1. Overall claims and denial KPIs
SELECT
  COUNT(*) AS total_claims,
  SUM(CASE WHEN denied_flag = 1 THEN 1 ELSE 0 END) AS denied_claims,
  ROUND(100.0 * SUM(CASE WHEN denied_flag = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS denial_rate_pct,
  ROUND(SUM(billed_amount), 2) AS total_billed,
  ROUND(SUM(denied_amount), 2) AS denied_amount_exposure,
  ROUND(SUM(appeal_recovered_amount), 2) AS appeal_recovery,
  ROUND(SUM(net_unrecovered_amount), 2) AS net_unrecovered
FROM claims;

-- 2. Denial rate and exposure by payer
SELECT payer, COUNT(*) AS claims,
       ROUND(100.0 * SUM(denied_flag) / COUNT(*), 2) AS denial_rate_pct,
       ROUND(SUM(denied_amount), 2) AS denied_exposure,
       ROUND(SUM(appeal_recovered_amount), 2) AS recovered,
       ROUND(SUM(net_unrecovered_amount), 2) AS net_unrecovered
FROM claims
GROUP BY payer
ORDER BY denial_rate_pct DESC;

-- 3. Top denial reason codes
SELECT carc_code, denial_reason, COUNT(*) AS denied_claims,
       ROUND(SUM(denied_amount), 2) AS denied_exposure
FROM claims
WHERE denied_flag = 1
GROUP BY carc_code, denial_reason
ORDER BY denied_claims DESC
LIMIT 10;

-- 4. Denial rates by specialty and CPT
SELECT provider_specialty, cpt_code, COUNT(*) AS claims,
       ROUND(100.0 * SUM(denied_flag) / COUNT(*), 2) AS denial_rate_pct,
       ROUND(SUM(denied_amount), 2) AS exposure
FROM claims
GROUP BY provider_specialty, cpt_code
HAVING COUNT(*) >= 20
ORDER BY denial_rate_pct DESC;

-- 5. Appeal submission and success rates
SELECT payer,
       SUM(CASE WHEN denied_flag = 1 THEN 1 ELSE 0 END) AS denied_claims,
       SUM(CASE WHEN appeal_submitted = 1 THEN 1 ELSE 0 END) AS appeals_submitted,
       SUM(CASE WHEN appeal_won = 1 THEN 1 ELSE 0 END) AS appeals_won,
       ROUND(100.0 * SUM(CASE WHEN appeal_submitted = 1 THEN 1 ELSE 0 END)
         / NULLIF(SUM(CASE WHEN denied_flag = 1 THEN 1 ELSE 0 END), 0), 2) AS appeal_submission_rate_pct,
       ROUND(100.0 * SUM(CASE WHEN appeal_won = 1 THEN 1 ELSE 0 END)
         / NULLIF(SUM(CASE WHEN appeal_submitted = 1 THEN 1 ELSE 0 END), 0), 2) AS appeal_success_rate_pct,
       ROUND(SUM(appeal_recovered_amount), 2) AS recovered_amount
FROM claims
GROUP BY payer;

-- 6. Monthly trend
SELECT service_month, COUNT(*) AS claims,
       ROUND(100.0 * SUM(denied_flag) / COUNT(*), 2) AS denial_rate_pct,
       ROUND(SUM(denied_amount), 2) AS denied_exposure,
       ROUND(SUM(appeal_recovered_amount), 2) AS recovered_amount
FROM claims
GROUP BY service_month
ORDER BY service_month;

-- 7. Prioritize operational opportunities: volume x exposure
SELECT carc_code, denial_reason, COUNT(*) AS claim_count,
       ROUND(SUM(denied_amount), 2) AS exposure,
       ROUND(AVG(denied_amount), 2) AS avg_denied_amount
FROM claims
WHERE denied_flag = 1
GROUP BY carc_code, denial_reason
ORDER BY exposure DESC;
