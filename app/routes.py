from flask import Blueprint, request, jsonify, current_app as app
from .db import get_conn
import jwt
import werkzeug
import werkzeug.security
import datetime
from functools import wraps

api_bp = Blueprint("api_bp",__name__, url_prefix="/api")
account_bp = Blueprint("account_bp", __name__, url_prefix="/account")
transaction_bp = Blueprint("transaction_bp", __name__, url_prefix="/transaction")
request_bp = Blueprint("request_bp", __name__, url_prefix="/request")
weather_bp = Blueprint("weather_bp", __name__, url_prefix="/weather")

api_bp.register_blueprint(account_bp)
api_bp.register_blueprint(transaction_bp)
api_bp.register_blueprint(request_bp)
api_bp.register_blueprint(weather_bp)

def check_data(f):
    @wraps(f)
    def wrapper(*args):
        if not request.is_json:
            return jsonify({'message':'Must be format JSON'}),400
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email:
            return jsonify({'message':'You not write your email'})
        if not password:
            return jsonify({"message": "You are not write your password"})
        return f(email,password,*args)
    return wrapper


@account_bp.route("/register", methods = ["POST"])
@check_data
def register(email,password):
    with get_conn() as conn:
        cursor = conn.cursor(dictionary=True)    
        cursor.execute(f"SELECT email FROM account")
        accounts = cursor.fetchall()
        for account in accounts:   
            if account['email'] == email:
                return jsonify({"message":"You have account in this app"}), 400
            
        hashed_password = werkzeug.security.generate_password_hash(password)
        token = jwt.encode({
            "email":email,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=48)
        },app.config["SECRET_KEY"], "HS256")

        cursor.execute(f"INSERT INTO account(email, password) VALUES('{email}', '{hashed_password}')")
        
        return jsonify({'token':token}),201
    

@account_bp.route("/login", methods=["POST"])
@check_data
def login(email,password):
    with get_conn() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT email,password FROM account")
        accounts = cursor.fetchall()
        for account in accounts:
            if account['email'] == email and account['password'] == password:
                token = jwt.encode({
                    'email': email,
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=48)
                },app.config['SECRET_KEY'], 'HS256')
                return jsonify({'token' : token}),200
    return jsonify({'message':'You are not register'}),400
         
@api_bp.route("/test", methods=["GET"])
def test():
    print(app.config['API_KEY'])
    return "OK"
