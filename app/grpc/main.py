import asyncio
import grpc
from app.protos import matcher_pb2_grpc
from app.grpc.matcher_server import MatcherService  

async def serve():
    server = grpc.aio.server()
    matcher_pb2_grpc.add_MatcherServiceServicer_to_server(MatcherService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server running on port 50051")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
