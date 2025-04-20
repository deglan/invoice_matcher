from concurrent import futures
from app.protos import matcher_pb2_grpc, matcher_pb2
from ml.predict import predict_match
from db.mongo import get_all_invoices

class MatcherService(matcher_pb2_grpc.MatcherService):
    async def MatchInvoice(self, request, context):
        transaction = {
            "sender_name": request.sender_name,
            "amount": request.amount,
            "currency": request.currency,
            "transfer_date": request.transfer_date,
            "description": request.description
        }

        invoices = await get_all_invoices()

        best_match = None
        highest_prob = 0

        for invoice in invoices:
            prediction, prob = await predict_match(invoice, transaction)
            if prediction == 1 and prob > highest_prob:
                best_match = invoice
                highest_prob = prob

        if best_match:
            return matcher_pb2.MatchResponse(
                matched=True,
                invoice_number=best_match.get("number", ""),
                prediction=1,
                probability=highest_prob
            )
        else:
            return matcher_pb2.MatchResponse(matched=False)

