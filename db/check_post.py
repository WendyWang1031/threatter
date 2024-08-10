import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool

def db_check_post_exist_or_not(account_id : str , post_id : str):
        connection = get_db_connection_pool()
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
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()


def db_check_comment_exist_or_not(post_id : str , content_id : str):
        connection = get_db_connection_pool()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:

            if content_id.startswith("C"):
                check_exist_comment_sql = """
                SELECT 1
                FROM content 
                WHERE parent_id = %s AND content_id = %s
                """
                cursor.execute(check_exist_comment_sql, (post_id , content_id))
                check_comment_exist = cursor.fetchone()

                if check_comment_exist :
                    return True
                else:
                    return False

            else:
                check_exist_reply_sql = """
                SELECT 1
                FROM content AS reply
                JOIN content AS comment ON reply.parent_id = comment.content_id
                WHERE comment.parent_id = %s AND reply.content_id = %s
                """
                cursor.execute(check_exist_reply_sql, (post_id , content_id))
                check_reply_exist = cursor.fetchone()
                # print("check_comment_or_reply_exist:",check_comment_or_reply_exist)

                if check_reply_exist :
                    return True
                else:
                    return False
    
        except Exception as e:
            print(f"Error getting comment or reply existension details: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()


