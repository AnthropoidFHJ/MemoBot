from fastapi import FastAPI
from app.api import ai_endpoint, health_check
from app.config.config import settings

app = FastAPI(title="Personal AI Assistant")

app.include_router(health_check.router)
app.include_router(ai_endpoint.router)

@app.get("/")
async def root():
	return {"message": "Personal AI Assistant is running...."}