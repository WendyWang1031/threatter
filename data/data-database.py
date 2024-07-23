import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
database = os.getenv('AWS_DB_database')  
user = os.getenv('AWS_DB_USER')  
password = os.getenv('AWS_DB_PASSWORD')
host = os.getenv('AWS_DB_HOST', 'localhost')
port = int(os.getenv('AWS_DB_PORT'))

db =  pymysql.connect(
    host = host,
    port = port,
    user = user,
    password = password,
    db = database
)

cursor = db.cursor()

create_test_post_table_sql = """
        CREATE TABLE IF NOT EXISTS test_post (
        id int NOT NULL AUTO_INCREMENT,
        content TEXT,
        image_url varchar(255),
        PRIMARY KEY (id)   
        );
"""






try:
        cursor.execute("BEGIN;")
        cursor.execute(create_test_post_table_sql)

        db.commit()
except Exception as e :
        print("Error creating tables:" , e)
        db.rollback()
finally:
        cursor.close()
        db.close()







   