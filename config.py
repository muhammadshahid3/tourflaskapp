import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Base configuration. Reads all sensitive values from environment
    variables so the same image can be pointed at any AWS RDS MySQL
    instance without code changes."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'change_me')

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'tour_booking')
    DB_USER = os.environ.get('DB_USER', 'admin')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'images', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB uploads

    WTF_CSRF_ENABLED = True
