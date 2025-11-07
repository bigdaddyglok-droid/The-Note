from fastapi.testclient import TestClient


def test_telemetry_snapshot(api_client: TestClient) -> None:
    response = api_client.get("/telemetry")
    response.raise_for_status()
    assert isinstance(response.json(), dict)
