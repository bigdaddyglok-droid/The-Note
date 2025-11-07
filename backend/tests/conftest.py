import asyncio
import base64
import uuid
from collections.abc import Iterator

import numpy as np
import pytest
from fastapi.testclient import TestClient

from thenote_backend.main import app
from thenote_backend.routing.hub import hub


@pytest.fixture(scope="session", autouse=True)
def initialize_hub_once() -> None:
    asyncio.run(hub.initialize())


@pytest.fixture
def api_client(tmp_path, monkeypatch) -> Iterator[TestClient]:
    monkeypatch.setenv("THE_NOTE_DATA_DIR", str(tmp_path))
    with TestClient(app) as client:
        yield client


def generate_sine_frame(session_id: str, frequency: float = 440.0) -> dict:
    sample_rate = 8000
    duration = 0.2
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False, dtype=np.float32)
    waveform = (0.6 * np.sin(2 * np.pi * frequency * t)).astype(np.float32)
    encoded = base64.b64encode(waveform.tobytes()).decode("ascii")
    return {
        "session_id": session_id,
        "frame_id": f"frame_{uuid.uuid4().hex}",
        "sample_rate": sample_rate,
        "channels": 1,
        "duration_ms": duration * 1000,
        "waveform_base64": encoded,
        "timestamp_ms": 0.0,
    }
