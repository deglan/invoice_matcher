from ml.predict import predict_match
from db.mongo import get_all_invoices


async def get_match(transaction):
    """
    Get the match for a transaction.
    """
    invoices = await get_all_invoices()
    results = []

    for invoice in invoices:
        # Call the predict_match function from the predict module
        prediction, probability = await predict_match(invoice, transaction)
        results.append({
            "invoice": invoice,
            "prediction": prediction,
            "probability": probability,
        })
    
    best = max(results, key=lambda x: x["probability"], default=None)
    if best:
        return {
            "invoice": best["invoice"],
            "transaction": transaction,
            "prediction": best["prediction"],
            "probability": best["probability"],
        }
    else:
        return None
