import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import DBManager

DBManager.init_db_pool()

def db_check_post_exist_or_not(account_id : str , post_id : str):
        connection = DBManager.get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:

            check_exist_post_sql = """
            SELECT member_id , content_id
            FROM content
            WHERE member_id = %s AND content_id = %s
            """
            cursor.execute(check_exist_post_sql, ( account_id , post_id))
            check_post_exist = cursor.fetchone()
            # print("check_post_exist:",check_post_exist)

            if check_post_exist :
                 return True
            else:
                 return False
    
        except Exception as e:
            print(f"Error getting post existension details: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

def db_check_post_visibility(account_id : str , post_id : str):
        connection = DBManager.get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:

            check_exist_post_sql = """
            SELECT visibility
            FROM content
            WHERE member_id = %s AND content_id = %s
            """
            cursor.execute(check_exist_post_sql, ( account_id , post_id))
            check_visibility = cursor.fetchone()

            return check_visibility['visibility']

        except Exception as e:
            print(f"Error getting post existension details: {e}")
            return False
        finally:
            cursor.close()
            connection.close()