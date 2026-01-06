from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import User, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(role: str | None = None):
    """装饰器：要求登录，可选角色控制（'admin' 或 'user'）"""

    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            user_id = session.get("user_id")
            if user_id is None:
                return redirect(url_for("auth.login"))

            user = db.session.get(User, user_id)
            if user is None:
                session.clear()
                return redirect(url_for("auth.login"))

            if role == "admin" and not user.is_admin:
                flash("无权限执行此操作（需要管理员权限）", "danger")
                return redirect(url_for("products.list_products"))

            return view(*args, **kwargs)

        return wrapped_view

    return decorator


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # 第一个注册的用户自动成为管理员
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "user")

        if not username or not password:
            flash("用户名和密码不能为空", "danger")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("用户名已存在", "danger")
            return render_template("register.html")

        user_count = User.query.count()
        if user_count == 0:
            role = "admin"

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("注册成功，请登录", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("用户名或密码错误", "danger")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user.id
        flash("登录成功", "success")
        return redirect(url_for("products.list_products"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("已退出登录", "success")
    return redirect(url_for("auth.login"))

