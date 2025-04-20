import json
import asyncio
from db.mongo import save_invoice, save_transaction
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

async def load_data():
    with open("data/sample_data.json", encoding="utf-8") as f:
        data = json.load(f)

    for invoice in data["invoices"]:
        await save_invoice(invoice)

    for transaction in data["transactions"]:
        await save_transaction(transaction)

if __name__ == "__main__":
    asyncio.run(load_data())