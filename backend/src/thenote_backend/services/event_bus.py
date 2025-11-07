from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Awaitable, Callable, Dict, List

from ..schemas.base import ModuleEvent, ModuleType
from ..utils.logging import get_logger
from .telemetry import telemetry

EventHandler = Callable[[ModuleEvent], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._queues: Dict[str, asyncio.Queue[ModuleEvent]] = defaultdict(asyncio.Queue)
        self._handlers: Dict[str, List[EventHandler]] = defaultdict(list)
        self._lock = asyncio.Lock()
        self._logger = get_logger("event_bus")

    async def publish(self, event: ModuleEvent) -> None:
        key = event.target.value if isinstance(event.target, ModuleType) else event.target
        queue = self._queues[key]
        await queue.put(event)
        # broadcast to handlers immediately
        async with self._lock:
            for handler in self._handlers.get(key, []):
                await handler(event)
            for handler in self._handlers.get("broadcast", []):
                await handler(event)
        self._logger.info(
            "event_published",
            extra={"extra_data": {"session_id": event.session_id, "source": event.source, "target": key}},
        )
        await telemetry.increment(f"events.{event.source}.{key}")

    async def subscribe(self, target: ModuleType | str, handler: EventHandler) -> None:
        async with self._lock:
            key = target.value if isinstance(target, ModuleType) else target
            self._handlers[key].append(handler)
            self._logger.info("handler_subscribed", extra={"extra_data": {"target": key, "handler": handler.__qualname__}})

    async def get(self, target: ModuleType | str) -> ModuleEvent:
        key = target.value if isinstance(target, ModuleType) else target
        queue = self._queues[key]
        return await queue.get()


event_bus = EventBus()
