from __future__ import annotations

import asyncio
from typing import Dict, Optional

from ..schemas import ModuleEvent, ModuleType, SessionMetadata, SessionState
from ..services.event_bus import event_bus
from ..services.telemetry import telemetry
from ..utils.logging import get_logger


class SessionController:
    def __init__(self) -> None:
        self._sessions: Dict[str, SessionState] = {}
        self._lock = asyncio.Lock()
        self._logger = get_logger("session_controller")

    async def create(self, metadata: SessionMetadata) -> SessionState:
        async with self._lock:
            if metadata.session_id in self._sessions:
                raise ValueError(f"session {metadata.session_id} already exists")
            state = SessionState(metadata=metadata)
            self._sessions[metadata.session_id] = state
            self._logger.info(
                "session_created",
                extra={"extra_data": {"session_id": metadata.session_id, "intent": metadata.intent}},
            )
            await telemetry.increment("sessions.created")
            await event_bus.publish(
                ModuleEvent(
                    session_id=metadata.session_id,
                    source=ModuleType.CONTROLLER,
                    target="broadcast",
                    payload={"event": "session_created"},
                )
            )
            return state

    async def get(self, session_id: str) -> Optional[SessionState]:
        async with self._lock:
            return self._sessions.get(session_id)

    async def dispatch(self, event: ModuleEvent) -> None:
        session = await self.get(event.session_id)
        if not session or not session.active:
            raise ValueError(f"session {event.session_id} is not active")
        self._logger.info(
            "session_dispatch",
            extra={"extra_data": {"session_id": event.session_id, "source": event.source, "target": event.target}},
        )
        await event_bus.publish(event)

    async def finalize(self, session_id: str) -> SessionState:
        async with self._lock:
            state = self._sessions.get(session_id)
            if not state:
                raise ValueError(f"session {session_id} does not exist")
            state.active = False
            self._logger.info("session_finalized", extra={"extra_data": {"session_id": session_id}})
            await telemetry.increment("sessions.closed")
            await event_bus.publish(
                ModuleEvent(
                    session_id=session_id,
                    source=ModuleType.CONTROLLER,
                    target="broadcast",
                    payload={"event": "session_closed"},
                )
            )
            return state
