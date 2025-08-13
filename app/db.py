from mysql.connector.pooling import MySQLConnectionPool
import mysql.connector
from contextlib import contextmanager
from flask import current_app, Flask, Blueprint,jsonify,request
from .config import Config


def init_pool(app):
    pool = MySQLConnectionPool(pool_name="flask_pool",pool_size=app.config["DB_CONFIG"].pop("pool_size"), **app.config["DB_CONFIG"])
    app.extensions["db_pool"] = pool

@contextmanager
def get_conn():
    pool = current_app.extensions["db_pool"]
    conn = pool.get_connection()
    try:
        yield conn
        conn.commit()
    except Exception():
        conn.rollback()
        raise
    finally:
        conn.close()

connectot = mysql.connector.connect(
    host = Config.DB_CONFIG['host'],
    user = Config.DB_CONFIG['user'],
    password = Config.DB_CONFIG['password'],
    database = Config.DB_CONFIG['database']
)
