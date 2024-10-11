import pymysql.cursors
from typing import Optional
from model.model import *
from db.re_post_data import *
from service.common import *
from db.connection_pool import DBManager

DBManager.init_db_pool()

def db_get_popular_to_zset_posts(time_frame: int):
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
 
        sql = """
            SELECT content_id  
            FROM content
            WHERE content.content_type = 'Post'
            AND content.visibility = 'Public'
            AND content.created_at >= NOW() - INTERVAL %s DAY
            ORDER BY created_at DESC 
        """
        params = (time_frame,)
        cursor.execute(sql, params)
        post_ids = cursor.fetchall()

        post_id_list = []
        for row in post_ids:
            post_id_list.append(row["content_id"])

        return post_id_list

    except Exception as e:
        print(f"Error getting public post IDs : {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()