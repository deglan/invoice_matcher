from concurrent import futures
from app.protos import matcher_pb2_grpc, matcher_pb2
from ml.predict import predict_match
from db.mongo import get_all_invoices
from app.logger import logger


class MatcherService(matcher_pb2_grpc.MatcherService):
     async def SendMatch(self, request, context):
        transaction = {
            "sender_name": request.sender_name,
            "amount": request.amount,
            "currency": request.currency,
            "transfer_date": request.transfer_date,
            "description": request.description
        }

        logger.info(f"Received transaction: {transaction}")

        invoices = await get_all_invoices()
        best = None
        best_prob = 0
        MIN_PROB_THRESHOLD = 0.75

        for invoice in invoices:
            prediction, prob = await predict_match(invoice, transaction)
            if prediction == 1 and prob > best_prob and prob >= MIN_PROB_THRESHOLD:
                best = invoice
                best_prob = prob
                logger.info(f"Best match found: {best}")

        logger.info(f"Best match probability: {best_prob}")

        if best:
            return matcher_pb2.MatchResult(
                invoice=matcher_pb2.Invoice(
                    number=best.get("number", ""),
                    client_name=best.get("client_name", ""),
                    seller_name=best.get("seller_name", ""),
                    tax_number=best.get("tax_number", ""),
                    total_net_amount=best.get("total_net_amount", 0.0),
                    total_tax_amount=best.get("total_tax_amount", 0.0),
                    amount=best.get("amount", 0.0),
                    currency=best.get("currency", ""),
                    issue_date=best.get("issue_date", ""),
                    due_date=best.get("due_date", "")
                ),
                transaction=request,
                prediction=1,
                probability=best_prob
            )
        else:
            return matcher_pb2.MatchResult(
                prediction=0,
                probability=0.0,
                transaction=request
            )

