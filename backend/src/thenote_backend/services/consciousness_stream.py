"""
Real-time Consciousness Streaming
WebSocket service for streaming consciousness state to clients
"""

from __future__ import annotations

import asyncio
import json
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from ..utils.logging import get_logger


class ConsciousnessStreamManager:
    """Manages WebSocket connections for consciousness streaming"""

    def __init__(self):
        self._active_connections: Dict[str, Set[WebSocket]] = {}
        self._logger = get_logger("service.consciousness_stream")

    async def connect(self, websocket: WebSocket, session_id: str) -> None:
        """Connect a client to consciousness stream"""
        await websocket.accept()

        if session_id not in self._active_connections:
            self._active_connections[session_id] = set()

        self._active_connections[session_id].add(websocket)
        self._logger.info(
            "consciousness_stream_connected",
            extra={
                "extra_data": {
                    "session_id": session_id,
                    "active_connections": len(self._active_connections[session_id])
                }
            }
        )

    def disconnect(self, websocket: WebSocket, session_id: str) -> None:
        """Disconnect a client from consciousness stream"""
        if session_id in self._active_connections:
            self._active_connections[session_id].discard(websocket)

            if not self._active_connections[session_id]:
                del self._active_connections[session_id]

            self._logger.info(
                "consciousness_stream_disconnected",
                extra={"extra_data": {"session_id": session_id}}
            )

    async def broadcast_consciousness_state(
        self,
        session_id: str,
        consciousness_data: Dict
    ) -> None:
        """Broadcast consciousness state to all connected clients"""
        if session_id not in self._active_connections:
            return

        # Prepare message
        message = {
            "type": "consciousness_update",
            "session_id": session_id,
            "timestamp": asyncio.get_event_loop().time(),
            "data": consciousness_data
        }

        # Broadcast to all connected clients
        disconnected = set()

        for connection in self._active_connections[session_id]:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception as e:
                self._logger.warning(
                    "consciousness_stream_send_error",
                    extra={"extra_data": {"error": str(e)}}
                )
                disconnected.add(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection, session_id)

    async def broadcast_6d_trajectory(
        self,
        session_id: str,
        coords_6d: list,
        consciousness_log: Optional[Dict] = None
    ) -> None:
        """Broadcast 6D consciousness trajectory"""
        data = {
            "coords_6d": coords_6d,
            "consciousness_log": consciousness_log or {}
        }
        await self.broadcast_consciousness_state(session_id, {
            "type": "6d_trajectory",
            **data
        })

    async def broadcast_timeline_valences(
        self,
        session_id: str,
        valences: list,
        chosen_timeline: int
    ) -> None:
        """Broadcast timeline valence information"""
        data = {
            "valences": valences,
            "chosen_timeline": chosen_timeline,
            "num_timelines": len(valences)
        }
        await self.broadcast_consciousness_state(session_id, {
            "type": "timeline_valences",
            **data
        })

    async def broadcast_energy_distribution(
        self,
        session_id: str,
        state_distribution: list,
        state_names: Optional[list] = None
    ) -> None:
        """Broadcast 14-state energy distribution"""
        if state_names is None:
            state_names = [
                'classical', 'cubit_classical', 'quantum', 'qubit_quantum',
                'phantom', 'temporal', 'thermal', 'harmonic', 'vacuum',
                'toroidal', 'fractal', 'elemental', 'relativistic', 'holographic'
            ]

        data = {
            "state_distribution": state_distribution,
            "state_names": state_names
        }
        await self.broadcast_consciousness_state(session_id, {
            "type": "energy_distribution",
            **data
        })

    async def broadcast_coherence_score(
        self,
        session_id: str,
        coherence: float,
        harmonic_alignment: Optional[float] = None
    ) -> None:
        """Broadcast consciousness coherence score"""
        data = {
            "coherence": coherence,
            "harmonic_alignment": harmonic_alignment
        }
        await self.broadcast_consciousness_state(session_id, {
            "type": "coherence_score",
            **data
        })


# Global instance
_consciousness_stream_manager: Optional[ConsciousnessStreamManager] = None


def get_consciousness_stream_manager() -> ConsciousnessStreamManager:
    """Get or create the global consciousness stream manager"""
    global _consciousness_stream_manager
    if _consciousness_stream_manager is None:
        _consciousness_stream_manager = ConsciousnessStreamManager()
    return _consciousness_stream_manager
