from flask import Flask, g, session


def create_app():
    app = Flask(__name__)

    # 基础配置（生产环境请自行修改为更安全的配置）
    app.config["SECRET_KEY"] = "change-this-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

    from models import User, db

    db.init_app(app)

    # 创建数据库
    with app.app_context():
        db.create_all()

    # 注册蓝图
    from auth import auth_bp
    from products import product_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    @app.before_request
    def load_current_user():
        """在每个请求前把当前用户放到 g 里，模板中可直接使用 g.current_user。"""

        user_id = session.get("user_id")
        if user_id is None:
            g.current_user = None
        else:
            g.current_user = db.session.get(User, user_id)

    @app.route("/")
    def index():
        from flask import redirect, url_for

        return redirect(url_for("products.list_products"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

