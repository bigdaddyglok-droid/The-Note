from __future__ import annotations

import asyncio
from collections import defaultdict
from statistics import mean
from typing import Dict, List


class Telemetry:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._counters: Dict[str, int] = defaultdict(int)
        self._timers: Dict[str, List[float]] = defaultdict(list)

    async def increment(self, key: str, value: int = 1) -> None:
        async with self._lock:
            self._counters[key] += value

    async def record_timing(self, key: str, duration_ms: float) -> None:
        async with self._lock:
            self._timers[key].append(duration_ms)

    async def snapshot(self) -> Dict[str, float]:
        async with self._lock:
            data: Dict[str, float] = {f"counter.{k}": float(v) for k, v in self._counters.items()}
            for key, samples in self._timers.items():
                if samples:
                    data[f"timer.{key}.mean_ms"] = float(mean(samples))
                    data[f"timer.{key}.count"] = float(len(samples))
                    data[f"timer.{key}.max_ms"] = float(max(samples))
            return data.copy()


telemetry = Telemetry()
