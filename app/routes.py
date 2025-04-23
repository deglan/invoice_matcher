from fastapi import APIRouter
from app.schemas import Invoice, Transaction
from db.mongo import get_all_invoices, get_all_transactions, save_invoice, save_transaction, serialize_mongo_document
from service.matcher_service import get_match

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Smart Matcher is alive"}

@router.get("/match")
async def match():
    invoices_raw = await get_all_invoices()
    transactions_raw = await get_all_transactions()
    invoices = [serialize_mongo_document(inv) for inv in invoices_raw]
    transactions = [serialize_mongo_document(tx) for tx in transactions_raw]
    matched = get_match(invoices, transactions)
    return {"matched": matched}

@router.post("/invoice", status_code=201)
async def add_invoice(invoice: Invoice):
    await save_invoice(invoice)
    return {"status": "saved"}

@router.post("/transaction", status_code=201)
async def add_transaction(transaction: Transaction):
    await save_transaction(transaction)
    return {"status": "saved"}