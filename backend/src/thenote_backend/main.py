from __future__ import annotations

from fastapi import FastAPI

from .routing.hub import hub, router
from .routing.consciousness_ws import router as consciousness_router
from .routing.voice_chat import router as voice_chat_router
from .routing.singing_api import router as singing_router
from .utils.logging import configure_logging

app = FastAPI(title="The Note Backend", version="0.1.0")
app.include_router(router)
app.include_router(consciousness_router)
app.include_router(voice_chat_router)
app.include_router(singing_router)


@app.on_event("startup")
async def startup() -> None:
    configure_logging()
    await hub.initialize()
