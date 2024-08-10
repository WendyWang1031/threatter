import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool


def db_like_post(post_like : LikeReq , post_id : str , member_id : str) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        insert_update_sql = """
            INSERT INTO likes (content_id, content_type, member_id, like_state, created_at)
            VALUES (%s, 'Post', %s, %s, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE 
            like_state = VALUES(like_state), 
            created_at = CURRENT_TIMESTAMP
        """
        new_like_state = post_like.like
        cursor.execute(insert_update_sql, (post_id, member_id, new_like_state))

        # 計算讚數
        count_sql ="""
            SELECT COUNT(*) as total_likes FROM likes
            where content_id = %s AND like_state = TRUE
        """
        cursor.execute(count_sql , (post_id ,))
        total_likes = cursor.fetchone()["total_likes"]
        
        return total_likes
    
    except Exception as e:
        print(f"Error update post like: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

def db_like_comment_or_reply(comment_like : LikeReq , comment_id : str , member_id : str) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        if comment_id.startswith('C'):
            content_type = 'Comment'
        elif comment_id.startswith('R'):
            content_type = 'Reply'
        else:
            raise ValueError("Invalid comment_id prelix. Must start with 'C' or 'R'")

        insert_update_sql = """
            INSERT INTO likes (content_id, content_type, member_id, like_state, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE 
            like_state = VALUES(like_state), 
            created_at = CURRENT_TIMESTAMP
        """
        new_like_state = comment_like.like
        cursor.execute(insert_update_sql, (comment_id, content_type, member_id, new_like_state))


        count_sql ="""
            SELECT COUNT(*) as total_likes FROM likes
            where content_id = %s AND like_state = TRUE
        """
        cursor.execute(count_sql , (comment_id ,))
        total_likes = cursor.fetchone()["total_likes"]

        connection.commit()

        return total_likes
    
    except Exception as e:
        print(f"Error update comment or reply like: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

