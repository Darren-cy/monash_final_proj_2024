from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
import functools
from dms.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form["confirm-password"]
        error = None

        if not email:
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
                user = User(name=email, email=email, password=generate_password_hash(password))
                session = current_app.db.session
                session.add(user)
                session.commit()
            except IntegrityError:
                error = f"An account with the email {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=('GET', 'POST'))
def login():
    # Login not working due to cant retrieve user from db
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


@bp.before_app_request
def load_logged_in_user():
    userId = session.get("user_id")

    if userId is None:
        g.user = None
    else:
        g.user = current_app.db.session.query(User).filter_by(id=userId).first()


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
