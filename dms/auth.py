from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
import functools
from werkzeug.security import generate_password_hash, check_password_hash
from dms.models import User
from dms import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                user = User(username, generate_password_hash(password), username + "@example.com")
                db.session.add(user)
                db.session.commit()
            except:
                error = f"Username {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=('GET', 'POST'))
def login():
    # Login not working due to cant retrieve user from db
    if request.method == "POST":
        username = request.form['username']
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            user = db.session.query(User).filter_by(name=username).first()
            
            if user is None:
                error = "Username is incorrect."
            elif not check_password_hash(user.password, password):
                error = "Password is incorrect."

        if user and error is None:
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
        g.user = db.session.query(User).filter_by(id=userId).first()


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
