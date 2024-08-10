import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool


def db_get_like_counts(total_likes , content_id) -> FollowMember :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        # 更新讚數到 content 表
        update_content_sql = """
            UPDATE content 
            SET like_counts = %s 
            WHERE content_id = %s
        """
        cursor.execute(update_content_sql, (total_likes, content_id))

        connection.commit()

        like_res = LikeRes(
            total_likes= total_likes
        )
        
        return like_res

    
    except Exception as e:
        print(f"Error getting like counts details: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

def db_update_relpy_counts(content_id) -> FollowMember :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        count_reply_sql = """
            SELECT COUNT(*) as total_replies
            FROM content
            WHERE parent_id = %s 
        """
        cursor.execute(count_reply_sql, (content_id,))
        reply_count_row = cursor.fetchone()
        # print("reply_count_row:",reply_count_row)

        if reply_count_row:
            total_replies = reply_count_row['total_replies']
        else:
            total_replies = 0

        # print("total_replies:",total_replies)
        # 更新回覆數到 content 表
        update_content_sql = """
            UPDATE content 
            SET reply_counts = %s 
            WHERE content_id = %s
        """
        cursor.execute(update_content_sql, (total_replies, content_id))

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
    connection = get_db_connection_pool()
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
        print(f"Error getting reply counts details: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()