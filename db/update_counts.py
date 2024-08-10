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