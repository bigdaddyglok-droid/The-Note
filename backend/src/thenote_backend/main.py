from __future__ import annotations

from fastapi import FastAPI

from .routing.hub import hub, router
from .utils.logging import configure_logging

app = FastAPI(title="The Note Backend", version="0.1.0")
app.include_router(router)


@app.on_event("startup")
async def startup() -> None:
    configure_logging()
    await hub.initialize()
