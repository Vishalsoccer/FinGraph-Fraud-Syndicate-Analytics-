import pandas as pd
import streamlit as st

st.set_page_config(page_title="FinGraph | Fraud Analytics", layout="wide")
st.title("FinGraph — Fraud Syndicate Analytics")
st.caption("Portfolio prototype using synthetic demonstration data only. Not for real financial decisions.")

df = pd.read_csv("transactions.csv", parse_dates=["timestamp"])
min_amount = float(df["amount"].min())
max_amount = float(df["amount"].max())
amount_range = st.sidebar.slider("Transaction amount (USD)", min_amount, max_amount, (min_amount, max_amount))
patterns = sorted(df["pattern"].unique())
selected = st.sidebar.multiselect("Transaction pattern", patterns, default=patterns)
view = df[df["amount"].between(*amount_range) & df["pattern"].isin(selected)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions", f"{len(view):,}")
c2.metric("Transaction value", f"${view['amount'].sum():,.0f}")
c3.metric("Flagged rows", f"{int(view['is_suspicious'].sum()):,}")
c4.metric("Accounts involved", f"{len(set(view.sender_account) | set(view.receiver_account)):,}")

st.subheader("Transaction volume by pattern")
pattern_summary = view.groupby("pattern", as_index=False).agg(
    transactions=("transaction_id", "count"), amount=("amount", "sum")
).sort_values("transactions", ascending=False)
st.bar_chart(pattern_summary.set_index("pattern")["transactions"])

st.subheader("Top receiver accounts")
receiver = view.groupby("receiver_account", as_index=False).agg(
    transactions=("transaction_id", "count"), total_inflow=("amount", "sum"),
    flagged=("is_suspicious", "sum")
).sort_values("transactions", ascending=False).head(15)
st.dataframe(receiver, use_container_width=True)

st.subheader("Transactions")
st.dataframe(view.sort_values("timestamp", ascending=False).head(500), use_container_width=True)
st.download_button("Download filtered CSV", view.to_csv(index=False).encode("utf-8"),
                   "filtered_transactions.csv", "text/csv")
