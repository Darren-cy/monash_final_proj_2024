import functools

from email_validator import EmailNotValidError, validate_email
from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, request, session, url_for)
from itsdangerous.exc import BadTimeSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from dms.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form["confirm-password"]
        error = None

        if not name:
            error = "Name is required."
        elif not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"
        elif password != password_confirmation:
            error = "Passwords must match"
        else:
            try:
                emailInfo = validate_email(email, check_deliverability=False)
                email = emailInfo.normalized
            except EmailNotValidError as e:
                error = str(e)

        if error is None:
            try:
                user = User(name=name, email=email,
                            password=generate_password_hash(password))
                session = current_app.db.session
                session.add(user)
                session.commit()
            except IntegrityError:
                error = f"An account with the email {
                    email} is already registered."
            else:
                flash("Account created.")
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form["password"]
        error = None

        if not email:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        else:
            try:
                emailInfo = validate_email(email, check_deliverability=False)
                email = emailInfo.normalized
            except EmailNotValidError as e:
                error = str(e)

        if error is None:
            try:
                statement = select(User).where(User.email == email)
                dbsession = current_app.db.session
                user = dbsession.scalars(statement).one()
            except NoResultFound:
                error = "No account found."
            else:
                if not check_password_hash(user.password, password):
                    error = "Password is incorrect."

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/forgot-password", methods=('GET', 'POST'))
def forgot_password():
    if request.method == "POST":
        email = request.form['email']
        error = None

        if not email:
            error = "Email is required."
        else:
            try:
                emailInfo = validate_email(email)
                email = emailInfo.normalized
            except EmailNotValidError:
                error = "You must enter a valid email address."

        if not error:
            serializer = URLSafeTimedSerializer(
                current_app.secret_key, salt="reset-password")
            current_app.logger.info(
                f'Password reset link for {email}: {url_for(
                    "auth.reset_password", token=serializer.dumps(email),
                    _external=True)}')
            flash("A password reset link has been sent.")
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/forgot-password.html")


@bp.route("/reset-password/<token>", methods=('GET', 'POST'))
def reset_password(token):
    serializer = URLSafeTimedSerializer(
        current_app.secret_key, salt="reset-password")
    try:
        token_email = serializer.loads(token, max_age=3600)
        user = User.query.filter_by(email=token_email).one()
    except (SignatureExpired, BadTimeSignature, NoResultFound) as e:
        current_app.logger.info("Password reset with invalid token: %s", e)
        abort(404)

    if request.method == "POST":
        form_email = request.form["email"]
        password = request.form["password"]
        conf_password = request.form["confirm-password"]
        error = None

        if not form_email:
            error = "Email is required"
        elif token_email != form_email:
            error = "Email is incorrect."
        elif not password:
            error = "Password is required."
        elif password != conf_password:
            error = "Passwords must match."

        if error is None:
            user.password = generate_password_hash(password)
            current_app.db.session.commit()
            flash("Your password has been changed.")
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/reset-password.html")


@bp.before_app_request
def load_logged_in_user():
    userId = session.get("user_id")

    if userId is None:
        g.user = None
    else:
        g.user = current_app.db.session.query(
            User).filter_by(id=userId).first()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
