import os
from flask import Flask
from config import Config
from app.extensions import db, login_manager, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.user_login'

    from app.models import Admin, User

    @login_manager.user_loader
    def load_user(combined_id):
        # combined_id looks like "admin-3" or "user-7" — see get_id()
        # overrides on the Admin/User models.
        try:
            role, raw_id = combined_id.split('-', 1)
        except ValueError:
            return None
        if role == 'admin':
            return Admin.query.get(int(raw_id))
        if role == 'user':
            return User.query.get(int(raw_id))
        return None

    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.admin.routes import admin_bp
    from app.user.routes import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/account')

    from app.filters import register_filters
    register_filters(app)

    with app.app_context():
        db.create_all()
        from app.seed import seed_admin
        seed_admin()

    return app
