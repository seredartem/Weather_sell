from flask import Blueprint, request, jsonify, current_app as app
from .db import get_conn
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps
import requests

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
            
        hashed_password = generate_password_hash(password)
        token = jwt.encode({
            "email":email,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=48)
        },app.config["SECRET_KEY"], "HS256")

        cursor.execute(
            "INSERT INTO account (email, password) VALUES (%s, %s)",
            (email, hashed_password)
        )
        
        return jsonify({'token':token}),201
    
def auth_required(f):
    @wraps(f)
    def wrapper(*args):
        token = request.headers.get('Authorization')
        if token and token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
            try:
                jwt.decode(token,app.config["SECRET_KEY"], algorithms= "HS256")
                return f(*args)            
            except Exception as ex:
                print(ex)
                return jsonify({"message":"not auth"}),403
        else:
            return jsonify({"message":"Token is missing"}), 400
    return wrapper
    

@account_bp.route("/login", methods=["POST"])
@check_data
def login(email,password):
    #werkzeug.security.check_password_hash(hashpassword,password) -> True / False
    
    # if werkzeug.security.check_password_hash()
    with get_conn() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT password FROM account WHERE email = '{email}'")
        password_account = cursor.fetchone()
        if not password_account:
            return jsonify({'message':'You are not register'}),400

        if check_password_hash(password_account['password'],password):
            token = jwt.encode({
                'email': email,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=48)
            },app.config['SECRET_KEY'], 'HS256')
            return jsonify({'token' : token}),200
    return jsonify({'message':'Not correct password'}),400

@weather_bp.route("/", methods=['GET'])
@auth_required
def get_weather():
    with get_conn() as conn:
        req = request.headers.get("Authorization")
        token = req.split(' ')
        token = token[1]
        data = jwt.decode(token,app.config['SECRET_KEY'], 'HS256')
        email = data['email']


        cursor = conn.cursor(dictionary=True)    
        cursor.execute(f"SELECT email, requests FROM account WHERE email = '{email}'")
        account = cursor.fetchone()
        cursor.execute(f"UPDATE account SET requests = {account['requests'] + 1} WHERE email = '{email}'")
        print(account)





        
        

    
        if len(request.args.keys()) > 0:
            city = request.args.get('city')
        resp = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={app.config["KEY_WEATHER"]}')
        data = resp.json()
        # print(f"Windiness: {data['wind']['speed']}")

        description = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        return jsonify({'description': description, 'temp':temp ,'humidity': humidity, 'wind':wind}),200
        
        
         
@api_bp.route("/test", methods=["GET"])
def test():
    print(app.config['API_KEY'])
    return "OK"
