from fastapi.testclient import TestClient


def test_create_and_close_session(api_client: TestClient) -> None:
    payload = {
        "user_id": "artist_unit",
        "intent": "creative_session",
        "daw": "Ableton",
        "key": "C#m",
        "tempo": 120.0,
        "emotional_goal": "uplifting",
        "references": ["demo:unit"],
    }
    response = api_client.post("/sessions", json=payload)
    assert response.status_code == 200
    session_state = response.json()
    session_id = session_state["metadata"]["session_id"]
    assert session_state["active"] is True

    close_response = api_client.post(f"/sessions/{session_id}/close")
    assert close_response.status_code == 200
    assert close_response.json()["active"] is False
