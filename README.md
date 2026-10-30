# FinGraph — Fraud Syndicate Analytics (Starter Project)

## Goal
Explore suspicious transfer networks using transaction data, transparent rules, SQL, and a lightweight interactive dashboard.

## Dataset
`transactions.csv` is a generated synthetic dataset (not real bank/customer data). It includes normal transactions and planted demonstration patterns:
- `starburst_fan_in`: many accounts send money to one hub account
- `starburst_fan_out`: a hub sends money to many accounts
- `circular_flow`: small three-account transfer cycles
- `normal`: ordinary simulated transfers

The `is_suspicious` field is synthetic ground-truth labeling for practice. Do not claim this model has been validated on real financial data.

## Setup (Windows)
1. Install Python 3.10+.
2. Open Command Prompt in this folder.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `.venv\\Scripts\\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run analysis: `python analyze.py`
7. Launch dashboard: `streamlit run app.py`

## Files
- `transactions.csv` — synthetic dataset
- `analyze.py` — data exploration, pattern summary, basic rule-based risk scoring
- `app.py` — Streamlit interactive dashboard
- `schema.sql` — MySQL schema and example investigation queries
- `requirements.txt` — Python dependencies

## Portfolio talking points
- Cleaned and summarized transaction records using pandas.
- Used SQL aggregations to investigate high-volume receiver accounts and transfer patterns.
- Built a transparent, rule-based account risk score.
- Built an interactive dashboard with filters and CSV export.

## Important limitation
This is a starter prototype, not a live streaming system. Kafka, Flink, Neo4j, graph algorithms, and real-time alerting are proposed future extensions from the advanced brief.
