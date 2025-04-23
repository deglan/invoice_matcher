from fastapi import FastAPI
import uvicorn
from app.routes import router

app = FastAPI(title="Smart Matcher API")

app.include_router(router, prefix="/api")

async def run_rest():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()