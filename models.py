from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    # role: "admin" or "user"
    role = db.Column(db.String(16), nullable=False, default="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(128), nullable=False)  # 型号
    sku = db.Column(db.String(128), nullable=True)  # SKU
    package_size = db.Column(db.String(128), nullable=True)  # 包装尺寸
    outer_size = db.Column(db.String(128), nullable=True)  # 外形尺寸
    inner_size = db.Column(db.String(128), nullable=True)  # 内部尺寸
    gross_weight = db.Column(db.String(64), nullable=True)  # 毛重
    net_weight = db.Column(db.String(64), nullable=True)  # 净重
    temperature_range = db.Column(db.String(128), nullable=True)  # 温度范围
    power = db.Column(db.String(64), nullable=True)  # 功率
    power_consumption = db.Column(db.String(64), nullable=True)  # 耗电量
    compressor_brand = db.Column(db.String(128), nullable=True)  # 压缩机品牌
    cooling_pipe_material = db.Column(db.String(128), nullable=True)  # 制冷管路材质
    energy_level = db.Column(db.String(64), nullable=True)  # 能耗等级

    image_real = db.Column(db.String(256), nullable=True)  # 产品实物图路径
    image_param = db.Column(db.String(256), nullable=True)  # 参数图路径

