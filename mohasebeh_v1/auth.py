import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from mohasebeh_v1.db import get_db
from mohasebeh_v1 import singleton


# این  بلو پرینت در اینیت معرفی شده است
bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_name = session.get("user")

    if user_name is None:
        g.user = None
    else:
        g.user = (
            get_db()
            .execute("SELECT * FROM users WHERE username = ?", (user_name,))
            .fetchone()
        )


@bp.route("/register", methods=["POST", "GET"])
def register():
    if "user" in session:
        return redirect("/")
    db = get_db()
    if request.method == "POST":
        # گرفتن یوزر نیم و پسورد از فرم
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        # این متغیر برای فرستادن بازخورد به کاربر توسط فلش است
        error = None
        # چک کردن اعتبار یوز نیم و پسورد
        if not username:
            error = "invalid user name"
        if not password:
            error = "invalid user password"
        if not email:
            error = "invalid user email"
        if error is None:
            try:
                password = generate_password_hash(password)
                db.execute(
                    "INSERT INTO users (username,password,email)VALUES(?,?,?)",
                    (username, password, email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"نام کاربری {username}تکرای است "
            else:
                flash("شما با موفقیت ثبت نام شدید لطفا وارد شوید ")
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html", title="ثبت نام")


@bp.route("/login", methods=["POST", "GET"])
def login():
    if "user" in session:
        return redirect("/")
    # change desine later
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        if not username:
            error = "نام کاربری را وارد نکردید " + singleton.incorrect_username

        if not password:
            error = "پسورد را وارد نکردید " + singleton.incorrect_password
        if error is None and check_password_hash(
            generate_password_hash(password), password
        ):
            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()

            if user is not None:
                session.clear()
                session["user"] = user["username"]
                return redirect(url_for("index"))
            else:
                error = "نام کاربری معتبر نیست " + singleton.invalid_username
        flash(error)
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.register"))
