import asyncio
from app.api import run_rest
from app.grpc_api.server_runner import run_grpc

async def main():
    await asyncio.gather(
        run_rest(),
        run_grpc()
    )

if __name__ == "__main__":
    asyncio.run(main())