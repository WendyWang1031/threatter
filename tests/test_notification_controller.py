from fastapi.testclient import TestClient
from unittest.mock import Mock
from service.security import security_get_current_user
from app import app

def test_notification_controller():
    # 創建一個模擬的安全服務
    mock_security_service = Mock()
    mock_security_service.get_current_user.return_value = {'account_id': 'woof', 'name': 'woof'}
    
    app.dependency_overrides[security_get_current_user] = lambda: mock_security_service.get_current_user()

    client = TestClient(app)
    response = client.get("/api/notification")
    assert response.status_code == 200
    assert 'data' in response.json()

    # 清理依賴覆蓋
    app.dependency_overrides.clear()
