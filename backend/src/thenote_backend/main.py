from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .routing.hub import hub, router
from .routing.consciousness_ws import router as consciousness_router
from .routing.voice_chat import router as voice_chat_router
from .routing.singing_api import router as singing_router
from .routing.knowledge_api import router as knowledge_router
from .routing.emotional_api import router as emotional_router
from .utils.logging import configure_logging

app = FastAPI(title="The Note Backend", version="0.1.0")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (the interactive UI)
static_dir = Path(__file__).parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    async def root():
        """Serve the interactive UI"""
        return FileResponse(str(static_dir / "index.html"))

app.include_router(router)
app.include_router(consciousness_router)
app.include_router(voice_chat_router)
app.include_router(singing_router)
app.include_router(knowledge_router)
app.include_router(emotional_router)


@app.on_event("startup")
async def startup() -> None:
    configure_logging()
    await hub.initialize()
