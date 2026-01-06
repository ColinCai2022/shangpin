# 商品信息管理小系统（Flask）

## 功能概览

- 用户注册 / 登录 / 注销
  - 第一个注册的账号自动成为管理员
  - 管理员：可以新增 / 修改 / 删除商品，支持 Excel 批量导入
  - 普通用户：只能查询、查看商品信息
- 商品信息管理
  - 字段：型号、SKU、包装尺寸、外形尺寸、内部尺寸、毛重、净重、温度范围、功率、耗电量、压缩机品牌、制冷管路材质、能耗等级、实物图、参数图
  - 列表分页展示，支持按“型号 / SKU”搜索
  - 单条新增 / 编辑 / 删除
  - 上传商品实物图、参数图并在页面中查看
- Excel 导入
  - 支持从 `.xlsx` 表格批量导入 1000+ 条记录

## 环境准备

```bash
cd d:\shangpin
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 运行项目

```bash
python app.py
```

浏览器访问：`http://127.0.0.1:5000/`

第一次访问请先注册一个账号，该账号会自动成为管理员，之后再给同事注册普通账号即可。

## Excel 模板要求

- 文件格式：`.xlsx`（即 Excel 2007+）
- 第一行是表头，示例表头：

```text
型号, SKU, 包装尺寸, 外形尺寸, 内部尺寸, 毛重, 净重, 温度范围, 功率, 耗电量, 压缩机品牌, 制冷管路材质, 能耗等级
```

- 从第二行开始为数据行，对应每条商品；
- 若你的表头中文名称不同，可在 `products.py` 中 `import_products` 里调整列名映射。

## 目录结构（简要）

```text
app.py           # 程序入口 & Flask 工厂
models.py        # 数据模型（User / Product）
auth.py          # 登录 / 注册 / 权限控制
products.py      # 商品增删改查、Excel 导入
templates/       # 页面模板（Jinja2）
uploads/         # 运行时自动创建，用于存放上传图片
requirements.txt # Python 依赖
```

