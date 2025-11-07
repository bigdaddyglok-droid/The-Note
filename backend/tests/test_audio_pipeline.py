from fastapi.testclient import TestClient

from tests.conftest import generate_sine_frame


def test_audio_analysis_flow(api_client: TestClient) -> None:
    session_response = api_client.post(
        "/sessions",
        json={
            "user_id": "artist_audio",
            "intent": "analytics_only",
            "references": [],
        },
    )
    session_response.raise_for_status()
    session_id = session_response.json()["metadata"]["session_id"]

    frame = generate_sine_frame(session_id, frequency=330.0)
    ingest_response = api_client.post(f"/sessions/{session_id}/audio", json=frame)
    ingest_response.raise_for_status()
    body = ingest_response.json()
    assert body["rms"] > 0

    analysis = api_client.get(f"/sessions/{session_id}/analysis/{frame['frame_id']}")
    assert analysis.status_code == 200

    api_client.post(f"/sessions/{session_id}/close")
