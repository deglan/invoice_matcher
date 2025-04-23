import grpc
from concurrent import futures
from app.protos import matcher_pb2_grpc
from app.grpc_api.matcher_server import MatcherService 

async def run_grpc():
    server = grpc.aio.server()
    matcher_pb2_grpc.add_MatcherServiceServicer_to_server(MatcherService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
