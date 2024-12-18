import pytest
from schemas.task_status_enum import TaskStatus

def test_create_task(client):
    response = client.post("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == TaskStatus.pending.value

def test_list_tasks(client):
    # Create tasks for testing
    client.post("/tasks")
    client.post("/tasks")
    
    response = client.get("/tasks?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "total_count" in data
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_task_count(client):
    status = TaskStatus.pending.value
    response = client.get(f"/tasks/count?status={status}")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "count" in data
    assert data["status"] == status
