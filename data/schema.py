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


create_member_table_sql = """
        CREATE TABLE IF NOT EXISTS member (
        account_id varchar(255) not null ,
        name varchar(255) not null ,
        email varchar(255) unique not null ,
        password varchar(255) not null ,
        self_intro TEXT ,
        visibility ENUM('Public' , 'Private') DEFAULT 'Public' ,
        avatar TEXT ,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL ,
        
        PRIMARY KEY (account_id)   
        );
"""


create_member_relation_table_sql = """
        CREATE TABLE IF NOT EXISTS member_relation (
        member_id varchar(255) not null ,
        target_id varchar(255) not null ,
        relation_state ENUM('None', 'Following', 'BeingFollow', 'Pending') DEFAULT 'None' ,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL ,

        PRIMARY KEY (member_id , target_id) ,   
        FOREIGN KEY (member_id) REFERENCES member(account_id) ,
        FOREIGN KEY (target_id) REFERENCES member(account_id)
        );
"""

alter_member_relation_table_sql = """
        ALTER TABLE member_relation 
        MODIFY COLUMN relation_state 
        ENUM('None', 'Following', 'BeingFollow', 'Pending', 'PendingBeingFollow') 
        DEFAULT 'None';

"""


create_content_table_sql = """
        CREATE TABLE IF NOT EXISTS content (
        member_id varchar(255) not null ,
        parent_id varchar(255) DEFAULT NULL ,
        content_id varchar(255) not null ,
        content_type ENUM('Post', 'Comment', 'Reply') not null ,
        visibility ENUM('Public' , 'Private') DEFAULT 'Public' ,
        
        text TEXT ,
        image TEXT , 
        video TEXT , 
        audio TEXT,
        
        like_counts int DEFAULT '0' , 
        reply_counts int DEFAULT '0' , 
        forward_counts int DEFAULT '0' ,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL ,
        
        PRIMARY KEY (content_id) ,   
        FOREIGN KEY (member_id) REFERENCES member (account_id) ,
        FOREIGN KEY (parent_id) REFERENCES content (content_id) 
        );
"""

create_likes_table_sql = """
        CREATE TABLE IF NOT EXISTS likes (
        content_id varchar(255) not null ,
        content_type ENUM('Post', 'Comment', 'Reply') not null ,
        member_id varchar(255) not null ,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL ,
        
        like_state Boolean DEFAULT TRUE ,

        PRIMARY KEY (content_id , member_id) ,
        FOREIGN KEY (content_id) REFERENCES content (content_id) ,
        FOREIGN KEY (member_id) REFERENCES member (account_id)
        );
"""

create_notification_table_sql = """
        CREATE TABLE IF NOT EXISTS notification (
        id INT AUTO_INCREMENT PRIMARY KEY ,
        member_id varchar(255) not null ,
        target_id varchar(255) not null , 
        event_type ENUM('Follow', 'Reply', 'Like') NOT NULL ,
        event_data JSON NOT NULL , 
        is_read BOOLEAN DEFAULT FALSE , 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  NOT NULL , 
        
        FOREIGN KEY (member_id) REFERENCES member(account_id) ,
        FOREIGN KEY (target_id) REFERENCES member(account_id)
        );
"""

alter_member_relation_table_sql = """
        ALTER TABLE notification 
        MODIFY COLUMN event_data JSON NULL
        ;

"""



try:
        cursor.execute("BEGIN;")
        cursor.execute(create_member_table_sql)
        cursor.execute(create_member_relation_table_sql)
        # cursor.execute(alter_member_relation_table_sql)
        cursor.execute(create_content_table_sql)
        cursor.execute(create_likes_table_sql)
        cursor.execute(create_notification_table_sql)
        cursor.execute(alter_member_relation_table_sql)

        db.commit()
except Exception as e :
        print("Error creating tables:" , e)
        db.rollback()
finally:
        cursor.close()
        db.close()

