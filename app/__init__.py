import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import mlflow
import dagshub

# 加载环境变量
load_dotenv()

# 初始化数据库
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 配置数据库
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///tasks.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化数据库
    db.init_app(app)

    # 配置MLflow和DagsHub
    if os.getenv("DAGSHUB_REPO_OWNER") and os.getenv("DAGSHUB_REPO_NAME"):
        dagshub.init(
            os.getenv("DAGSHUB_REPO_NAME"), os.getenv("DAGSHUB_REPO_OWNER"), mlflow=True
        )

    if os.getenv("MLFLOW_TRACKING_URI"):
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

    if os.getenv("MLFLOW_EXPERIMENT_NAME"):
        mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME"))

    # 注册路由
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app
