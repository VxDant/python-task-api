import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Use the same API key as configured in your security.py
API_KEY = "demo-key-for-swagger-ui"
headers = {"Authorization": f"Bearer {API_KEY}"}


def test_health_check():
    """Test health endpoint (no auth required)"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"


def test_read_root():
    """Test root endpoint with authentication"""
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert "authenticated" in response.json()["status"]


def test_protected_endpoint_without_auth():
    """Test that protected endpoints require authentication"""
    response = client.get("/tasks/")
    assert response.status_code == 403  # Should be 403 (Forbidden) not 401


def test_create_task():
    """Test creating a task with authentication"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "high"
    }
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["completed"] == False
    assert "id" in data
    assert "created_at" in data


def test_read_tasks():
    """Test reading tasks with authentication"""
    # Create test tasks first
    for i in range(3):
        client.post("/tasks/",
                    json={"title": f"Task {i}", "description": f"Description {i}"},
                    headers=headers)

    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_read_single_task():
    """Test reading a single task"""
    # Create a task
    create_response = client.post("/tasks/",
                                  json={"title": "Single Task"},
                                  headers=headers)
    task_id = create_response.json()["id"]

    # Read the task
    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Single Task"


def test_update_task():
    """Test updating a task"""
    # Create a task
    create_response = client.post("/tasks/",
                                  json={"title": "Original Task"},
                                  headers=headers)
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {"title": "Updated Task", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["completed"] == True


def test_delete_task():
    """Test deleting a task"""
    # Create a task
    create_response = client.post("/tasks/",
                                  json={"title": "Task to Delete"},
                                  headers=headers)
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404


def test_invalid_api_key():
    """Test with invalid API key"""
    invalid_headers = {"Authorization": "Bearer invalid-key"}
    response = client.get("/tasks/", headers=invalid_headers)
    assert response.status_code == 401  # Should be 401 for invalid key


def test_admin_endpoint():
    """Test admin endpoint with demo key (should fail)"""
    response = client.get("/admin/usage", headers=headers)
    assert response.status_code == 403  # Demo key shouldn't have admin access
