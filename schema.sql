CREATE DATABASE IF NOT EXISTS fingraph;
USE fingraph;

CREATE TABLE transactions (
  transaction_id VARCHAR(20) PRIMARY KEY,
  timestamp DATETIME NOT NULL,
  sender_account VARCHAR(20) NOT NULL,
  receiver_account VARCHAR(20) NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  currency CHAR(3) NOT NULL,
  channel VARCHAR(20),
  sender_ip VARCHAR(45),
  receiver_country CHAR(2),
  is_suspicious BOOLEAN NOT NULL DEFAULT FALSE,
  pattern VARCHAR(40)
);

-- Example investigation queries
SELECT receiver_account, COUNT(*) AS inbound_transactions,
       SUM(amount) AS total_inflow,
       SUM(is_suspicious) AS flagged_transactions
FROM transactions
GROUP BY receiver_account
ORDER BY inbound_transactions DESC
LIMIT 10;

SELECT pattern, COUNT(*) AS transaction_count, SUM(amount) AS total_amount
FROM transactions
GROUP BY pattern
ORDER BY transaction_count DESC;

SELECT sender_account, receiver_account, COUNT(*) AS transfers, SUM(amount) AS total_value
FROM transactions
GROUP BY sender_account, receiver_account
HAVING COUNT(*) >= 3
ORDER BY transfers DESC;
