from __future__ import annotations

import asyncio
from typing import Dict, Set

from fastapi import WebSocket

from ..schemas.base import ModuleEvent, ModuleType
from ..utils.logging import get_logger


class WebSocketStreamer:
    def __init__(self) -> None:
        self._connections: Dict[str, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()
        self._logger = get_logger("streaming.websocket")

    async def register(self, session_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.setdefault(session_id, set()).add(websocket)
        self._logger.info("ws_connected", extra={"extra_data": {"session_id": session_id}})

    async def unregister(self, session_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            if session_id in self._connections:
                self._connections[session_id].discard(websocket)
                if not self._connections[session_id]:
                    self._connections.pop(session_id)
        self._logger.info("ws_disconnected", extra={"extra_data": {"session_id": session_id}})

    async def broadcast(self, event: ModuleEvent) -> None:
        async with self._lock:
            sockets = list(self._connections.get(event.session_id, []))
        if not sockets:
            return
        payload = {
            "session_id": event.session_id,
            "source": event.source,
            "target": event.target,
            "payload": event.payload,
            "created_at": event.created_at.isoformat(),
        }
        for websocket in sockets:
            try:
                await websocket.send_json(payload)
            except Exception as exc:  # pragma: no cover - network errors
                self._logger.error(
                    "ws_send_failed",
                    extra={"extra_data": {"session_id": event.session_id, "error": str(exc)}},
                )


websocket_streamer = WebSocketStreamer()
