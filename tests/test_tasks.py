import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from app import create_app, db
import json
import pytest
from app import create_app, db
from app.models import Task


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_add_task(client):
    """测试添加任务"""
    response = client.post(
        "/tasks",
        data=json.dumps({"title": "Test Task", "priority": 3}),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Test Task"
    assert data["priority"] == 3
    assert data["completed"] is False


def test_get_tasks(client):
    """测试获取任务列表"""
    # 先添加两个任务
    client.post(
        "/tasks",
        data=json.dumps({"title": "Task 1", "priority": 2}),
        content_type="application/json",
    )
    client.post(
        "/tasks",
        data=json.dumps({"title": "Task 2", "priority": 5}),
        content_type="application/json",
    )

    # 获取所有任务
    response = client.get("/tasks")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2

    # 按优先级排序
    response = client.get("/tasks?sort_priority=true")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data[0]["priority"] == 5  # 优先级高的应该在前面


def test_complete_task(client):
    """测试标记任务为完成"""
    # 添加任务
    response = client.post(
        "/tasks",
        data=json.dumps({"title": "Task to complete", "priority": 1}),
        content_type="application/json",
    )
    task_id = json.loads(response.data)["id"]

    # 标记为完成
    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["completed"] is True


def test_delete_task(client):
    """测试删除任务"""
    # 添加任务
    response = client.post(
        "/tasks",
        data=json.dumps({"title": "Task to delete", "priority": 4}),
        content_type="application/json",
    )
    task_id = json.loads(response.data)["id"]

    # 删除任务
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # 确认任务已删除
    response = client.get("/tasks")
    data = json.loads(response.data)
    assert len(data) == 0


def test_update_priority(client):
    """测试更新任务优先级"""
    # 添加任务
    response = client.post(
        "/tasks",
        data=json.dumps({"title": "Task to update", "priority": 2}),
        content_type="application/json",
    )
    task_id = json.loads(response.data)["id"]

    # 更新优先级
    response = client.patch(
        f"/tasks/{task_id}/priority",
        data=json.dumps({"priority": 5}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["priority"] == 5
