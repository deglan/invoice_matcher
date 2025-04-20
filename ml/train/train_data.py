import asyncio
from db.mongo import get_all_invoices, get_all_transactions
from service.matcher_service import extract_features
import random
import csv

async def generate_training_data():
    invoices = await get_all_invoices()
    transactions = await get_all_transactions()
    data = []

    # 🟢 Pozytywne przykłady
    for invoice in invoices:
        for transaction in transactions:
            if abs(invoice["amount"] - transaction["amount"]) < 1.0:
                if invoice["number"] and invoice["number"] in (transaction.get("description") or ""):
                    features = extract_features(invoice, transaction)
                    data.append((features, 1))  # 1 = dopasowane
                    break

    # 🔴 Negatywne przykłady (losowe pary)
    for _ in range(len(data)):
        invoice = random.choice(invoices)
        transaction = random.choice(transactions)

        if invoice["number"] and invoice["number"] in (transaction.get("description") or ""):
            continue
        if abs(invoice["amount"] - transaction["amount"]) < 1.0:
            continue

        features = extract_features(invoice, transaction)
        data.append((features, 0))  # 0 = niedopasowane

    # 💾 Zapis CSV z nowymi nagłówkami
    with open("train_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "amount_diff", "net_diff", "tax_ratio",
            "days_diff", "days_to_due",
            "similarity_name", "similarity_desc", "label"
        ])
        for features, label in data:
            writer.writerow(features + [label])

            
if __name__ == "__main__":
    asyncio.run(generate_training_data())