from datetime import datetime, timedelta
from collections import defaultdict

transactions = [
    {"user_id": 1, "amount": 500, "type": "credit", "timestamp": "2024-01-01 10:00:00", "status": "completed"},
    {"user_id": 1, "amount": 200, "type": "debit", "timestamp": "2024-01-01 11:00:00", "status": "completed"},
    {"user_id": 1, "amount": 100, "type": "debit", "timestamp": "2024-01-01 11:05:00", "status": "failed"},
    {"user_id": 2, "amount": 1000, "type": "credit", "timestamp": "2024-01-01 10:30:00", "status": "completed"},
    {"user_id": 2, "amount": 1200, "type": "debit", "timestamp": "2024-01-01 11:30:00", "status": "completed"},
    {"user_id": 2, "amount": 300, "type": "credit", "timestamp": "2024-01-01 12:00:00", "status": "completed"},
]

user_data = defaultdict(list)

for t in transactions:
    t["timestamp"] = datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S")
    user_data[t["user_id"]].append(t)

# 1. Balance
balances = {}
for user, txns in user_data.items():
    balance = 0
    for t in txns:
        if t["status"] != "completed":
            continue
        if t["type"] == "credit":
            balance += t["amount"]
        else:
            balance -= t["amount"]
    balances[user] = balance

print("Balances:", balances)


# 2. Suspicious Users
suspicious = []

for user, txns in user_data.items():
    total_credit = sum(t["amount"] for t in txns if t["type"] == "credit")
    total_debit = sum(t["amount"] for t in txns if t["type"] == "debit")

    # Rule 1
    if total_debit > total_credit:
        suspicious.append(user)
        continue

    # Rule 2 (3 txns in 1 hour)
    txns_sorted = sorted(txns, key=lambda x: x["timestamp"])
    for i in range(len(txns_sorted)):
        count = 1
        for j in range(i+1, len(txns_sorted)):
            if txns_sorted[j]["timestamp"] - txns_sorted[i]["timestamp"] <= timedelta(hours=1):
                count += 1
        if count > 3:
            suspicious.append(user)
            break

    # Rule 3
    for t in txns:
        if t["type"] == "debit" and t["amount"] > 0.7 * total_credit:
            suspicious.append(user)
            break

print("Suspicious Users:", set(suspicious))


# 3. Latest Valid Transaction
latest = {}

for user, txns in user_data.items():
    completed = [t for t in txns if t["status"] == "completed"]
    if completed:
        latest[user] = max(completed, key=lambda x: x["timestamp"])

print("Latest Transactions:", latest)