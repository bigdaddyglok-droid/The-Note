import uuid

from fastapi.testclient import TestClient

from tests.conftest import generate_sine_frame


def _create_session(api_client: TestClient) -> str:
    response = api_client.post(
        "/sessions",
        json={
            "user_id": "artist_creative",
            "intent": "creative_session",
            "tempo": 124.0,
            "key": "Am",
            "emotional_goal": "uplifting",
            "references": ["artist:Bonobo"],
        },
    )
    response.raise_for_status()
    return response.json()["metadata"]["session_id"]


def test_imagination_and_voice_pipeline(api_client: TestClient) -> None:
    session_id = _create_session(api_client)
    api_client.post(f"/sessions/{session_id}/audio", json=generate_sine_frame(session_id))

    generation_request = {
        "session_id": session_id,
        "request_id": f"gen_{uuid.uuid4().hex}",
        "prompt": "ignite the skyline",
        "modes": ["lyric", "metaphor"],
    }
    response = api_client.post(f"/sessions/{session_id}/generate", json=generation_request)
    response.raise_for_status()
    outputs = response.json()["outputs"]
    assert any(item["type"] == "lyric" for item in outputs)

    render_request = {
        "session_id": session_id,
        "render_id": f"render_{uuid.uuid4().hex}",
        "text": "ignite the skyline",
        "voice_profile": "luminous_alto",
        "dynamics": "mezzo-forte",
        "format": "wav",
    }
    render_response = api_client.post(f"/sessions/{session_id}/render", json=render_request)
    render_response.raise_for_status()
    audio_blob = render_response.json()["url_or_blob"]
    assert len(audio_blob) > 100
    api_client.post(f"/sessions/{session_id}/close")
