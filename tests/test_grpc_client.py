import grpc
from app.protos import matcher_pb2, matcher_pb2_grpc
import asyncio


async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = matcher_pb2_grpc.MatcherServiceStub(channel)

        request = matcher_pb2.Transaction(
            sender_name="Jan Kowalsk",
            amount=1230.00,
            currency="PLN",
            transfer_date="2024-04-05",
            description="Opłata FV/2024/04/001"
        )

        response = await stub.SendMatch(request)
        print("--- Match Result ---")
        print("Prediction:", response.prediction)
        print("Probability:", response.probability)
        if response.prediction == 1:
            print("Matched invoice number:", response.invoice.number)
        else:
            print("No invoice matched.")

if __name__ == "__main__":
    asyncio.run(run())