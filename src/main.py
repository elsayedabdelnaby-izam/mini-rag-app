from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    app.mongodb_conn = AsyncIOMotorClient(settings.MONGO_URI)
    app.db_client = app.mongodb_conn[settings.MONGO_DATABASE]

@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_conn.close()
    app.db_client.close()


app.include_router(base.router)
app.include_router(data.router)

