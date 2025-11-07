from fastapi.testclient import TestClient


def _create_session(api_client: TestClient) -> str:
    response = api_client.post(
        "/sessions",
        json={
            "user_id": "artist_lyric",
            "intent": "creative_session",
            "references": ["poetry:surge"],
        },
    )
    response.raise_for_status()
    return response.json()["metadata"]["session_id"]


def test_lyric_analysis(api_client: TestClient) -> None:
    session_id = _create_session(api_client)
    payload = {
        "session_id": session_id,
        "section_id": "hook",
        "text": "Neon rivers sing in parallel lines\nEchoes bloom in ultraviolet tides",
    }
    response = api_client.post(f"/sessions/{session_id}/lyrics/analyze", json=payload)
    response.raise_for_status()
    data = response.json()
    assert data["lines"]
    assert len(data["term_suggestions"]) <= 5
    api_client.post(f"/sessions/{session_id}/close")
