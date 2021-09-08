from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix="/conta")

from app.catalog import bp as catalog_bp
app.register_blueprint(catalog_bp)

from app.content import bp as content_bp
app.register_blueprint(content_bp)

from app.dashboard import bp as dashboard_bp
app.register_blueprint(dashboard_bp, url_prefix="/painel")

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp, url_prefix="/erro")

from app.logistics import bp as logistics_bp
app.register_blueprint(logistics_bp)

from app.offers import bp as offers_bp
app.register_blueprint(offers_bp)

from app.shop import bp as shop_bp
app.register_blueprint(shop_bp)

