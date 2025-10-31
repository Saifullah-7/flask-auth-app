from flask import Blueprint, render_template, redirect, url_for, session, flash
from ..forms.signup_form import SignupForm
from ..forms.login_form import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user_model import User, db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return render_template("index.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "warning")
            return redirect(url_for("auth.signup"))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=username, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Something went wrong. Please try again.", "danger")
            return redirect(url_for("auth.signup"))

        session["user_id"] = new_user.id
        flash("Account created successfully!", "success")

        # ✅ Redirect to thank you page
        return redirect(url_for("auth.success"))

    return render_template("signup.html", form=form)


@auth_bp.route("/success")
def success():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)
    return render_template("thankyou.html", user=user.username)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session["user_id"] = user.id
            return redirect(url_for("auth.profile"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)
    return render_template("profile.html", user=user.username)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.home"))
