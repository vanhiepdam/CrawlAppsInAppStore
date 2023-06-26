from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestHeartbeatApi:
    def test_heartbeat(self):
        # Arrange
        expected = {"Hello": "World"}

        # Act
        response = client.get("/heartbeat")

        # Assert
        assert response.status_code == 200
        assert response.json() == expected
