from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models import Admin, User
from app.forms import (
    AdminRegisterForm, UserRegisterForm, LoginForm,
    ChangePasswordForm, ForgotPasswordForm
)

auth_bp = Blueprint('auth', __name__)


def _redirect_if_logged_in(expected_role):
    """Only short-circuit to a dashboard if the current session already
    matches the role of the login/signup page being visited. This lets
    someone logged in as a user still reach the admin login page (and
    vice versa) instead of being bounced to the wrong dashboard."""
    if current_user.is_authenticated and current_user.role == expected_role:
        if expected_role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    return None


# ---------- Admin auth ----------

@auth_bp.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    redirect_resp = _redirect_if_logged_in('admin')
    if redirect_resp:
        return redirect_resp

    form = AdminRegisterForm()
    if form.validate_on_submit():
        if Admin.query.filter_by(email=form.email.data.lower()).first():
            flash('An admin with that email already exists.', 'danger')
        else:
            admin = Admin(name=form.name.data, email=form.email.data.lower())
            admin.set_password(form.password.data)
            db.session.add(admin)
            db.session.commit()
            flash('Admin account created. Please log in.', 'success')
            return redirect(url_for('auth.admin_login'))
    return render_template('auth/admin_signup.html', form=form)


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    redirect_resp = _redirect_if_logged_in('admin')
    if redirect_resp:
        return redirect_resp

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data.lower()).first()
        if admin and admin.check_password(form.password.data):
            if current_user.is_authenticated:
                logout_user()
            login_user(admin, remember=form.remember.data)
            flash(f'Welcome back, {admin.name}!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid admin credentials.', 'danger')
    return render_template('auth/admin_login.html', form=form)


@auth_bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Admin logged out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def admin_change_password():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
    return render_template('auth/change_password.html', form=form, role='admin')


# ---------- User auth ----------

@auth_bp.route('/signup', methods=['GET', 'POST'])
def user_signup():
    redirect_resp = _redirect_if_logged_in('user')
    if redirect_resp:
        return redirect_resp

    form = UserRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('An account with that email already exists.', 'danger')
        else:
            user = User(
                full_name=form.full_name.data,
                email=form.email.data.lower(),
                phone=form.phone.data,
                address=form.address.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.user_login'))
    return render_template('auth/user_signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    redirect_resp = _redirect_if_logged_in('user')
    if redirect_resp:
        return redirect_resp

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            if current_user.is_authenticated:
                logout_user()
            if user.is_blocked:
                flash('Your account has been blocked. Contact support.', 'danger')
            elif not user.is_active_account:
                flash('Your account is deactivated. Contact support.', 'danger')
            else:
                login_user(user, remember=form.remember.data)
                flash(f'Welcome back, {user.full_name}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('user.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/user_login.html', form=form)


@auth_bp.route('/logout')
@login_required
def user_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Simple, self-service reset: verified only by matching email,
    per the 'simple implementation' requirement (no email sending)."""
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password reset successful. Please log in.', 'success')
            return redirect(url_for('auth.user_login'))
        flash('No account found with that email.', 'danger')
    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def user_change_password():
    if current_user.role != 'user':
        return redirect(url_for('main.index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('user.dashboard'))
    return render_template('auth/change_password.html', form=form, role='user')
