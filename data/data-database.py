import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("connection_db_user")
password = os.getenv("connection_db_password")


db =  pymysql.connect(
    host = "mysql",
    port = 3306,
    user = user,
    password = password,
    db = "threatter"
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







   