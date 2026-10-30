"""FinGraph starter analytics: suspicious transaction and account analysis."""
import pandas as pd

DATA = "transactions.csv"

def main():
    df = pd.read_csv(DATA, parse_dates=["timestamp"])
    print("\\n=== DATASET OVERVIEW ===")
    print(f"Transactions: {len(df):,}")
    print(f"Unique sender accounts: {df['sender_account'].nunique():,}")
    print(f"Unique receiver accounts: {df['receiver_account'].nunique():,}")
    print(f"Total transaction value: ${df['amount'].sum():,.2f}")
    print(f"Rows labeled suspicious (synthetic ground truth): {df['is_suspicious'].sum():,}")

    print("\\n=== TOP RECEIVER ACCOUNTS BY TRANSACTION COUNT ===")
    print(df.groupby("receiver_account").agg(
        transaction_count=("transaction_id", "count"),
        total_inflow=("amount", "sum"),
        suspicious_count=("is_suspicious", "sum")
    ).sort_values("transaction_count", ascending=False).head(10).round(2))

    print("\\n=== PATTERN SUMMARY ===")
    print(df.groupby("pattern").agg(
        transactions=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        suspicious_rows=("is_suspicious", "sum")
    ).round(2).sort_values("transactions", ascending=False))

    # A simple transparent risk score; tune thresholds for a real dataset.
    inbound = df.groupby("receiver_account").agg(
        inbound_count=("transaction_id", "count"),
        inbound_amount=("amount", "sum"),
        suspicious_links=("is_suspicious", "sum")
    )
    outbound = df.groupby("sender_account").agg(
        outbound_count=("transaction_id", "count"),
        outbound_amount=("amount", "sum")
    )
    risk = inbound.join(outbound, how="outer").fillna(0)
    risk["risk_score"] = (
        (risk["inbound_count"] >= 20).astype(int) * 35
        + (risk["inbound_amount"] >= 50000).astype(int) * 25
        + (risk["suspicious_links"] >= 5).astype(int) * 40
    ).clip(0, 100)
    print("\\n=== HIGHEST-RISK ACCOUNTS (RULE-BASED DEMO) ===")
    print(risk.sort_values("risk_score", ascending=False).head(15).round(2))

    df[df["is_suspicious"] == 1].to_csv("flagged_transactions.csv", index=False)
    risk.sort_values("risk_score", ascending=False).to_csv("account_risk_scores.csv")
    print("\\nSaved flagged_transactions.csv and account_risk_scores.csv")

if __name__ == "__main__":
    main()
