import pymysql
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
import os

load_dotenv()
maxconnections = int(os.getenv('AWS_DB_maxconnections'))
database = os.getenv('AWS_DB_database')  
user = os.getenv('AWS_DB_USER')  
password = os.getenv('AWS_DB_PASSWORD')
host = os.getenv('AWS_DB_HOST', 'localhost')
port = int(os.getenv('AWS_DB_PORT'))

pool = PooledDB(
    creator = pymysql,
    maxconnections = maxconnections,
    database = database,
    user = user,
    password = password,
    host = host,
    port = port
)


def get_db_connection_pool():
    try:
        connetion = pool.connection()
        print("Database connect successful")
    except Exception as err:
        print(f"Database connection failed : {err}")
        raise
    return connetion
