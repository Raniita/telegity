from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from app.forms import LoginForm, SignupForm, ChangePasswordForm
from app.models import User
from app import db, login_manager

auth_bp = Blueprint('auth', __name__)

#
# Login Page
#
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET -> requests serve Log-in page.
    POST -> requests validate and redirect user to dashboad
    """

    # Bypass if user is logged in:
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    form = LoginForm()

    # Validate Form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            # Update last login field on DB
            user.update_last_login(datetime.now())
            db.session.add(user)
            db.session.commit()
            current_app.logger.info('{} login'.format(user))
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.home'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)


#
# Sign Up Page
#
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page

    GET -> requests serve sign-up page
    POST -> requests validate form & user creation
    """

    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name = form.name.data,
                email = form.email.data,
                created_on = datetime.now(),
                role = 'user'
            )
            user.set_password(form.password.data)
            user.update_last_login(datetime.now())

            db.session.add(user)
            db.session.commit()
            current_app.logger.info('New {} registered'.format(user))
            #login_user(user)
            return redirect(url_for('dashboard.home'))

        error = 'An user already exists with that email address'
        flash(error)
        current_app.logger.error(error)

    #if current_user.is_authenticated:
    #    error = 'User already logged in. Sign out first.'
    #flash(error)
    #    current_app.logger.error(error)
    #    return redirect(url_for('dashboard.home'))
    #else:
    #    return render_template('auth/signup.html', form=form)

    if not current_user.is_authenticated:
        error = 'Contacta con soporte para que te creen una cuenta.'
        flash(error)
        current_app.logger.error('An user try to signup.')
        return redirect(url_for('auth.login'))
    elif current_user.is_admin():
        return render_template('auth/signup.html', form=form)
    else:
        error = 'No tienes permisos para hacer eso.'
        flash(error)
        current_app.logger.error('User {} try to signup a new account'.format(current_user))
        return redirect(url_for('dashboard.home'))


#
# Change password page
#
@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    User logged can change the password

    GET -> requests server change password page
    POST -> requests validate form & user info
    """

    # Hard bypass if admin_email try to change password
    if current_user.email == current_app.config['ADMIN_EMAIL']:
        flash('That account cant change password. Use your personal account.')
        current_app.logger.error('{} try to change password.'.format(current_user.email))
        return redirect(url_for('dashboard.home'))

    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user and user.check_password(password=form.password.data):
            # Actual password correct. Updating
            user.set_password(form.new_password.data)

            db.session.add(user)
            db.session.commit()
            current_app.logger.info('{} updated her password.'.format(user))
            flash('Contraseña actualizada. Vuelve a hacer login.')
            return redirect(url_for('auth.logout'))
        
        flash('Invalid password. Recheck inputs.')
        return redirect(url_for('auth.change_password'))

    return render_template('auth/change_password.html', form=form)


#
# Logout page
#
@auth_bp.route('/logout')
@login_required
def logout():
    """ User log-out logic. """

    logout_user()
    return redirect(url_for('dashboard.home'))

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""

    if user_id is not None:
        return User.query.get(user_id)
    return None@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""

    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))
