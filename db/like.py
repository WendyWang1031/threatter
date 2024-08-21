import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool


def db_like_post(account_id : str , post_like : LikeReq , post_id : str , member_id : str) -> bool :
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

         # 更新 content 表的 like_counts 字段
        update_sql = """
            UPDATE content
            SET like_counts = %s
            WHERE content_id = %s AND content_type = 'Post'
        """
        cursor.execute(update_sql, (total_likes, post_id))

        # 在按讚的狀態是TRUE的條件下，更新 notification 表的資料
            # 先取出貼文內容資料
        if new_like_state :
            content_sql ="""
                SELECT text , image , video , audio
                FROM content
                where member_id = %s and content_id = %s
            """
            cursor.execute(content_sql, (account_id, post_id))
            post_content_data = cursor.fetchone()

            media_data = Media(
                images = post_content_data.get('image'),
                videos = post_content_data.get('video'),
                audios = post_content_data.get('audio')
            )

            notify_data_obj = NotifyContent(
                post_url = f"/member/{account_id}/post/{post_id}" ,
                content_id = post_id ,
                text = post_content_data['text'] ,
                media = media_data
            )
            event_data_json = notify_data_obj.model_dump_json()

            update_notification_sql ="""
                INSERT INTO notification(
                    member_id , target_id , event_type , event_data , is_read
                )
                VALUES(
                    %s , %s , 'Like' , %s , False
                )
            """
            cursor.execute(update_notification_sql, (member_id , account_id , event_data_json))

        connection.commit()
        
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

        # 更新 content 表的 like_counts 字段
        update_sql = """
            UPDATE content
            SET like_counts = %s
            WHERE content_id = %s AND content_type = %s
        """
        cursor.execute(update_sql, (total_likes, comment_id, content_type))

        connection.commit()

        return total_likes
    
    except Exception as e:
        print(f"Error update comment or reply like: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

