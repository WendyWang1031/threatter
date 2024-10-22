import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import DBManager

DBManager.init_db_pool()

def db_update_total_comment_count(post_id: str, 
                                comment_id: Optional[str] = None) -> FollowMember :
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        total_comments = 0

        count_direct_comment_sql = """
            SELECT COUNT(*) as direct_comments
            FROM content
            WHERE parent_id = %s 
        """
        cursor.execute(count_direct_comment_sql, (post_id,))
        direct_comment_row = cursor.fetchone()
        # print("reply_count_row:",reply_count_row)

        if direct_comment_row:
            total_comments = direct_comment_row['direct_comments']

        # 如果傳入留言的id
        if comment_id:
            
            count_reply_sql = """
                SELECT COUNT(*) as total_replies
                FROM content
                WHERE parent_id = %s 
            """
            cursor.execute(count_reply_sql, (comment_id,))
            reply_count_row = cursor.fetchone()

            if reply_count_row:
                total_comments += reply_count_row['total_replies']

        # print("total_replies:",total_replies)
        # 更新回覆數到 content 表
        update_content_sql = """
            UPDATE content 
            SET reply_counts = %s 
            WHERE content_id = %s
        """
        cursor.execute(update_content_sql, (total_comments, post_id))

        connection.commit()

        return True

    
    except Exception as e:
        print(f"Error getting reply counts details: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()



def db_update_forward_counts(content_id) -> FollowMember :
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        count_forwards_sql = """
            SELECT COUNT(*) as total_forwards
            FROM content
            WHERE parent_id = %s AND content_type = 'Post'
        """
        cursor.execute(count_forwards_sql, (content_id,))
        forwards_count_row = cursor.fetchone()
        # print("forwards_count_row:",forwards_count_row)

        if forwards_count_row:
            total_forwards = forwards_count_row['total_forwards']
        else:
            total_forwards = 0

        # 更新轉發數到 content 表
        update_content_sql = """
            UPDATE content 
            SET forward_counts = %s 
            WHERE content_id = %s
        """
        cursor.execute(update_content_sql, (total_forwards , content_id))

        connection.commit()
        
        return True

    
    except Exception as e:
        print(f"Error getting forwards counts details: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()