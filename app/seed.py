import os
from app.extensions import db
from app.models import Admin


def seed_admin():
    """Create a default admin account on first run if none exists yet,
    using credentials from the environment (or safe defaults for local dev)."""
    if Admin.query.first():
        return

    name = os.environ.get('DEFAULT_ADMIN_NAME', 'Super Admin')
    email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin@123')

    admin = Admin(name=name, email=email)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
