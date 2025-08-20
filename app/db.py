from mysql.connector.pooling import MySQLConnectionPool
from contextlib import contextmanager
from flask import current_app


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
    except Exception as ex:
        conn.rollback()
        raise
    finally:
        conn.close()
