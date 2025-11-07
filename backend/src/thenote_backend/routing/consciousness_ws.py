"""
Consciousness WebSocket Endpoints
Real-time streaming of consciousness state
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.consciousness_stream import get_consciousness_stream_manager

router = APIRouter(prefix="/consciousness", tags=["consciousness"])


@router.websocket("/stream/{session_id}")
async def consciousness_stream(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for streaming consciousness state in real-time.

    Streams:
    - 6D trajectory coordinates
    - Timeline valences
    - 14-state energy distribution
    - Consciousness coherence scores
    - Harmonic alignment data
    """
    stream_manager = get_consciousness_stream_manager()

    await stream_manager.connect(websocket, session_id)

    try:
        # Keep connection alive and handle incoming messages
        while True:
            # Wait for ping/pong messages to keep connection alive
            data = await websocket.receive_text()

            # Echo back to confirm connection
            await websocket.send_json({
                "type": "pong",
                "message": "consciousness stream active"
            })

    except WebSocketDisconnect:
        stream_manager.disconnect(websocket, session_id)
