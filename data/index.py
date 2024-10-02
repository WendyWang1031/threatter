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

create_INDEX_on_content_sql = """
        CREATE INDEX 
        idx_content_member_type_visibility_created 
        ON 
        content 
        (member_id, content_type, created_at);
"""

create_INDEX_on_content_type_visibilty_sql = """
        CREATE INDEX 
        idx_content_type_visibility 
        ON 
        content
        (content_type, visibility);
"""

create_INDEX_on_member_sql = """
        CREATE INDEX 
        idx_member_relation_member_target 
        ON 
        member_relation 
        (member_id, target_id);
"""

try:
        cursor.execute("BEGIN;")
        
        cursor.execute(create_INDEX_on_content_sql)
        cursor.execute(create_INDEX_on_content_type_visibilty_sql)
        cursor.execute(create_INDEX_on_member_sql)

        db.commit()
except Exception as e :
        print("Error creating index:" , e)
        db.rollback()
finally:
        cursor.close()
        db.close()
