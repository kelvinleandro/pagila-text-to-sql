from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.api import endpoints

app = FastAPI(
    title="Chat with Pagila DB",
    description="An API to ask natural language questions about the Pagila database.",
    version="1.0.0",
)

app.include_router(endpoints.router, prefix="/api")


@app.get("/")
def read_root():
    return {"status": "API is running"}
