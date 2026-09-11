"""API routes for chat and conversation."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    """Chat message."""

    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request."""

    message: str
    user_id: Optional[str] = None
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    """Chat response."""

    message: str
    agent: str
    timestamp: datetime
    confidence: float
    sources: list[str] = []


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send message to financial AI.

    In production, this will:
    1. Parse user intent
    2. Route to appropriate agent(s)
    3. Gather market data if needed
    4. Perform calculations
    5. Return structured response

    For now, returns mock response.
    """
    return ChatResponse(
        message="لم يتم الربط بعميل LLM بعد. الرجاء تركيب Ollama على الكمبيوتر المحلي.",
        agent="mock",
        timestamp=datetime.utcnow(),
        confidence=0.0,
    )


@router.get("/history")
async def get_chat_history(user_id: str, limit: int = 50):
    """Get chat history for user."""
    return {
        "user_id": user_id,
        "messages": [],
        "note": "الربط بالقاعدة لم يتم بعد",
    }


@router.post("/clear")
async def clear_history(user_id: str):
    """Clear chat history."""
    return {"status": "cleared", "user_id": user_id}
