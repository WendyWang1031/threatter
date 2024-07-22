import pymysql
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("connection_db_user")
password = os.getenv("connection_db_password")


pool = PooledDB(
    creator = pymysql,
    maxconnections = 10,
    database = "threatter",
    user = user,
    password = password,
    host = "localhost",
    port = 3306
)


def get_db_connection_pool():
    try:
        connetion = pool.connection()
        print("Database connect successful")
    except Exception as err:
        print(f"Database connection failed : {err}")
        raise
    return connetion
