import pymysql
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
import os

load_dotenv()

class DBManager:
    _db_pool = None

    @classmethod
    def init_db_pool(cls) -> None:
        if cls._db_pool is None:
            try:
                cls._db_pool = PooledDB(
                    creator=pymysql,
                    maxconnections=int(os.getenv('AWS_DB_maxconnections')),
                    database=os.getenv('AWS_DB_database'),
                    user=os.getenv('AWS_DB_USER'),
                    password=os.getenv('AWS_DB_PASSWORD'),
                    host=os.getenv('AWS_DB_HOST', 'localhost'),
                    port=int(os.getenv('AWS_DB_PORT'))
                )
                print("資料庫連線池初始化成功")
            except Exception as err:
                raise RuntimeError(f"初始化資料庫連線池失敗: {err}")
    
    @classmethod
    def get_connection(cls):
        if cls._db_pool is None:
            raise RuntimeError("資料庫連線池尚未初始化")
        try:
            connection = cls._db_pool.connection()
            print("資料庫連線成功")
            return connection
        except Exception as err:
            raise RuntimeError(f"取得資料庫連線失敗: {err}")
    
    @classmethod
    def close_db_pool(cls):
        if cls._db_pool:
            cls._db_pool = None
            print("資料庫連線池已關閉")