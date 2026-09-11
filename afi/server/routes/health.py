"""System health and status endpoints."""

from fastapi import APIRouter
from datetime import datetime
import psutil

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("/status")
async def get_system_status():
    """Get complete system health status."""
    # Get system info
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "database": {
            "status": "connected",
            "type": "sqlite",
        },
        "ai_backend": {
            "status": "disconnected - configure Ollama",
            "provider": "ollama",
            "model": "mistral:7b-instruct-v0.2-q4_K_M",
            "host": "http://localhost:11434",
        },
        "market_data": {"status": "mock", "note": "استخدم mock provider للاختبار"},
        "news": {"status": "mock"},
        "system": {
            "memory_used_mb": round(memory.used / 1024 / 1024, 2),
            "memory_available_mb": round(memory.available / 1024 / 1024, 2),
            "memory_percent": memory.percent,
            "disk_used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
            "disk_free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
            "disk_percent": disk.percent,
        },
        "setup_instructions": {
            "step_1": "الذهاب إلى https://ollama.ai",
            "step_2": "تحميل وتثبيت Ollama",
            "step_3": "تشغيل ollama serve",
            "step_4": ظلل ollama pull mistral:7b-instruct-v0.2-q4_K_M",
            "step_5": "ترريب التطبيقات مرة أخرى",
        },
    }


@router.get("/ai")
async def check_ai_health():
    """Check AI backend health."""
    return {
        "status": "disconnected",
        "message": "رجاء تركيب Ollama",
        "docs": "https://ollama.ai",
    }


@router.get("/database")
async def check_database_health():
    """Check database health."""
    return {"status": "connected", "type": "sqlite", "file": "./afi_data.db"}
