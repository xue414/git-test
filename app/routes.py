from flask import Blueprint, request, jsonify
from app import db
from app.models import Task
import mlflow

main_bp = Blueprint("main", __name__)


@main_bp.route("/tasks", methods=["GET"])
def get_tasks():
    """获取所有任务，可按优先级排序"""
    sort_by_priority = request.args.get("sort_priority", "false").lower() == "true"

    with mlflow.start_run(run_name="get_tasks"):
        mlflow.log_param("sort_by_priority", sort_by_priority)

        if sort_by_priority:
            tasks = Task.query.order_by(Task.priority.desc()).all()
        else:
            tasks = Task.query.all()

        mlflow.log_metric("task_count", len(tasks))

        return jsonify([task.to_dict() for task in tasks])


@main_bp.route("/tasks", methods=["POST"])
def add_task():
    """添加新任务"""
    data = request.json

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    with mlflow.start_run(run_name="add_task"):
        mlflow.log_params(
            {"title": data.get("title"), "priority": data.get("priority", 1)}
        )

        new_task = Task(
            title=data.get("title"),
            description=data.get("description", ""),
            priority=data.get("priority", 1),
        )

        db.session.add(new_task)
        db.session.commit()

        mlflow.log_metric("task_id", new_task.id)

        return jsonify(new_task.to_dict()), 201


@main_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """删除任务"""
    with mlflow.start_run(run_name="delete_task"):
        mlflow.log_param("task_id", task_id)

        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted successfully"}), 200


@main_bp.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    """标记任务为完成"""
    with mlflow.start_run(run_name="complete_task"):
        mlflow.log_param("task_id", task_id)

        task = Task.query.get_or_404(task_id)
        task.completed = True
        db.session.commit()

        return jsonify(task.to_dict()), 200


@main_bp.route("/tasks/<int:task_id>/priority", methods=["PATCH"])
def update_priority(task_id):
    """更新任务优先级"""
    data = request.json

    if "priority" not in data:
        return jsonify({"error": "Priority is required"}), 400

    priority = data["priority"]
    if not isinstance(priority, int) or priority < 1 or priority > 5:
        return jsonify({"error": "Priority must be an integer between 1 and 5"}), 400

    with mlflow.start_run(run_name="update_priority"):
        mlflow.log_params({"task_id": task_id, "new_priority": priority})

        task = Task.query.get_or_404(task_id)
        old_priority = task.priority
        task.priority = priority
        db.session.commit()

        mlflow.log_metric("priority_change", priority - old_priority)

        return jsonify(task.to_dict()), 200
