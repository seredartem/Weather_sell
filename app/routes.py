from flask import Blueprint
from .db import get_conn

api_bp = Blueprint("api_bp",__name__, url_prefix="/api")
account_bp = Blueprint("account_bp", __name__, url_prefix="/account")
transaction_bp = Blueprint("transaction_bp", __name__, url_prefix="/transaction")
request_bp = Blueprint("request_bp", __name__, url_prefix="/request")
weather_bp = Blueprint("weather_bp", __name__, url_prefix="/weather")

api_bp.register_blueprint(account_bp)
api_bp.register_blueprint(transaction_bp)
api_bp.register_blueprint(request_bp)
api_bp.register_blueprint(weather_bp)

@account_bp.route("/login", methods=["POST"])
def login():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO account(email,password) VALUES('test@gmail.com','pass')")
    return "OK"