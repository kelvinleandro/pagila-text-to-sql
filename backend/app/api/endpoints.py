from fastapi import APIRouter, HTTPException

from app.services.agent_service import agent_service
from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Receives a natural language question, processes it, and returns an answer.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    answer = agent_service.process_query(request.question)

    return QueryResponse(answer=answer)
