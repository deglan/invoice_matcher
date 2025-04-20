import os
from typing import List
from app.schemas import Invoice, Transaction
from bson import ObjectId
from datetime import date, datetime
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "invoice_matcher")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

invoices_collection = db["invoices"]
transactions_collection = db["transactions"]

def prepare_invoice_for_db(invoice: Invoice | dict) -> dict:
    if isinstance(invoice, dict):
        data = invoice
    else:
        data = invoice.model_dump()

    issue_date = data.get("issue_date")
    if isinstance(issue_date, str) and issue_date.strip():
        data["issue_date"] = datetime.fromisoformat(issue_date)
    else:
        data["issue_date"] = None
    due_date = data.get("due_date")
    if isinstance(due_date, str) and due_date.strip():
        data["due_date"] = datetime.fromisoformat(due_date)
    else:
        data["due_date"] = None
    return data

async def save_invoice(invoice: Invoice):
    prepared = prepare_invoice_for_db(invoice)
    await invoices_collection.insert_one(prepared)

def prepare_transaction_for_db(transaction: Transaction | dict) -> dict:
    if isinstance(transaction, dict):
        data = transaction
    else:
        data = transaction.model_dump()

    transfer_date = data.get("transfer_date")
    if isinstance(transfer_date, str) and transfer_date.strip():
        data["transfer_date"] = datetime.fromisoformat(transfer_date)
    else:
        data["transfer_date"] = None
    return data

async def save_transaction(transaction: Transaction):
    prepared = prepare_transaction_for_db(transaction)
    await transactions_collection.insert_one(prepared)


async def get_all_invoices() -> List[dict]:
    invoices = await invoices_collection.find().to_list(length=None)
    return invoices

async def get_all_transactions() -> List[dict]:
    transactions = await transactions_collection.find().to_list(length=None)
    return transactions

def serialize_mongo_document(doc: dict) -> dict:
    doc = dict(doc)  # upewnij się że mamy kopię
    doc["_id"] = str(doc["_id"])
    for key, value in doc.items():
        if isinstance(value, (date, datetime)):
            doc[key] = value.isoformat()
    return doc