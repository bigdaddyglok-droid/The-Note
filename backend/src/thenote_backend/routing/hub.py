from __future__ import annotations

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from ..controller.session import SessionController
from ..modules.imagination import ImaginationEngine
from ..modules.language_lyric import LanguageLyricModule
from ..modules.live_audio import LiveAudioInput
from ..modules.memory import AdaptiveMemory
from ..modules.sound_understanding import SoundUnderstandingEngine
from ..modules.voice_performance import VoicePerformanceSynth
from ..schemas import (
    AnalysisFrame,
    AudioFrame,
    GenerationBundle,
    GenerationRequest,
    LyricInsight,
    LyricRequest,
    MemoryQuery,
    MemoryRecord,
    ModuleEvent,
    ModuleType,
    RenderInstruction,
    RenderedAudio,
    SessionMetadata,
    SessionState,
    TranscriptChunk,
)
from ..services.event_bus import event_bus
from ..services.telemetry import telemetry
from ..services.streaming import websocket_streamer


router = APIRouter()


class Hub:
    def __init__(self) -> None:
        self.sessions = SessionController()
        self.live_audio = LiveAudioInput()
        self.sound = SoundUnderstandingEngine()
        self.language = LanguageLyricModule()
        self.imagination = ImaginationEngine()
        self.voice = VoicePerformanceSynth()
        self.memory = AdaptiveMemory()
        self.streamer = websocket_streamer

    async def initialize(self) -> None:
        await event_bus.subscribe(ModuleType.SOUND_UNDERSTANDING, self.sound.on_event)
        await event_bus.subscribe("broadcast", self.streamer.broadcast)


hub = Hub()


@router.post("/sessions", response_model=SessionState)
async def create_session(metadata: SessionMetadata) -> SessionState:
    return await hub.sessions.create(metadata)


@router.post("/sessions/{session_id}/close", response_model=SessionState)
async def close_session(session_id: str) -> SessionState:
    return await hub.sessions.finalize(session_id)


@router.post("/sessions/{session_id}/audio", response_model=AudioFrame)
async def submit_audio(session_id: str, frame: AudioFrame) -> AudioFrame:
    if frame.session_id != session_id:
        raise HTTPException(status_code=400, detail="session mismatch")
    state = await hub.sessions.get(session_id)
    if not state or not state.active:
        raise HTTPException(status_code=404, detail="session inactive")
    return await hub.live_audio.ingest(frame)


@router.post("/sessions/{session_id}/transcript", response_model=TranscriptChunk)
async def submit_transcript(session_id: str, chunk: TranscriptChunk) -> TranscriptChunk:
    if chunk.session_id != session_id:
        raise HTTPException(status_code=400, detail="session mismatch")
    event = ModuleEvent(
        session_id=session_id,
        source=ModuleType.LIVE_AUDIO,
        target=ModuleType.LANGUAGE_LYRIC,
        payload=chunk.model_dump(),
    )
    await hub.sessions.dispatch(event)
    return chunk


@router.post("/sessions/{session_id}/lyrics/analyze", response_model=LyricInsight)
async def analyze_lyrics(session_id: str, request: LyricRequest) -> LyricInsight:
    if request.session_id != session_id:
        raise HTTPException(status_code=400, detail="session mismatch")
    return await hub.language.analyze(request)


@router.post("/sessions/{session_id}/generate", response_model=GenerationBundle)
async def generate_content(session_id: str, request: GenerationRequest) -> GenerationBundle:
    if request.session_id != session_id:
        raise HTTPException(status_code=400, detail="session mismatch")
    return await hub.imagination.generate(request)


@router.post("/sessions/{session_id}/render", response_model=RenderedAudio)
async def render_voice(session_id: str, instruction: RenderInstruction) -> RenderedAudio:
    if instruction.session_id != session_id:
        raise HTTPException(status_code=400, detail="session mismatch")
    return await hub.voice.render(instruction)


@router.post("/sessions/{session_id}/memory", response_model=MemoryRecord)
async def store_memory(session_id: str, record: MemoryRecord) -> MemoryRecord:
    if record.session_id != session_id:
        raise HTTPException(status_code=400, detail="session mismatch")
    await hub.memory.upsert(record)
    return record


@router.get("/memory/{user_id}", response_model=MemoryRecord | None)
async def get_recent_memory(user_id: str, limit: int = 5) -> MemoryRecord | None:
    records = await hub.memory.list_recent(MemoryQuery(user_id=user_id, limit=limit))
    return records[-1] if records else None


@router.get("/sessions/{session_id}/analysis/{frame_id}", response_model=AnalysisFrame | None)
async def get_analysis(session_id: str, frame_id: str) -> AnalysisFrame | None:
    return await hub.sound.get_analysis(session_id, frame_id)


@router.get("/telemetry")
async def get_telemetry() -> dict[str, float]:
    return await telemetry.snapshot()


@router.websocket("/ws/sessions/{session_id}")
async def session_stream(websocket: WebSocket, session_id: str) -> None:
    state = await hub.sessions.get(session_id)
    if not state or not state.active:
        await websocket.close(code=1008)
        return
    await hub.streamer.register(session_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await hub.streamer.unregister(session_id, websocket)
