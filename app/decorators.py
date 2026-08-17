from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(view_func):
    """Restrict a route to authenticated Admin accounts only."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'role', None) != 'admin':
            flash('Please log in as an admin to access that page.', 'warning')
            return redirect(url_for('auth.admin_login'))
        return view_func(*args, **kwargs)
    return wrapped


def user_required(view_func):
    """Restrict a route to authenticated User accounts only."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'role', None) != 'user':
            flash('Please log in to access that page.', 'warning')
            return redirect(url_for('auth.user_login'))
        return view_func(*args, **kwargs)
    return wrapped
