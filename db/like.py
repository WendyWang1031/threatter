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

        if post_like.like:
            db_update_notification(member_id, account_id, post_id, post_id, 'Post')

        connection.commit()
        
        return total_likes
    
    except Exception as e:
        print(f"Error update post like: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

def db_like_comment_or_reply(account_id : str , post_id : str , comment_like : LikeReq , comment_id : str , member_id : str) -> bool :
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

        if comment_like.like:
            db_update_notification(member_id, account_id, post_id, comment_id, content_type)


        connection.commit()

        return total_likes
    
    except Exception as e:
        print(f"Error update comment or reply like: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

def db_update_notification(member_id: str, account_id: str, post_id: str, content_id: str, content_type: str):
    # 如果對自己的操作，不需紀錄
    if member_id == account_id:
        return
    
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        # 先檢查是否已經存在未讀的相同通知
        check_notification_sql = """
            SELECT id FROM notification
            WHERE member_id = %s 
            AND target_id = %s 
            AND event_type = 'Like' 
            AND JSON_UNQUOTE(JSON_EXTRACT(event_data, '$.content_id')) = %s 
            AND is_read = FALSE
        """
        cursor.execute(check_notification_sql, (member_id, account_id, content_id))
        existing_notification = cursor.fetchone()
        
        # 如果已經存在就不插入通知進去表
        if existing_notification:
            return
        
        # 在按讚的狀態是TRUE的條件下，更新 notification 表的資料
            # 先取出貼文內容資料
        
        content_sql = """
            SELECT text, image, video, audio
            FROM content
            WHERE member_id = %s AND content_id = %s
        """
        cursor.execute(content_sql, (account_id, post_id))
        post_content_data = cursor.fetchone()

        media_data = Media(
            images=post_content_data.get('image'),
            videos=post_content_data.get('video'),
            audios=post_content_data.get('audio')
        )

        notify_data_obj = NotifyContent(
            post_url=f"/member/{account_id}/post/{post_id}",
            content_id=content_id,
            text=post_content_data['text'],
            media=media_data
        )
        event_data_json = notify_data_obj.model_dump_json()

        # 插入通知
        update_notification_sql = """
            INSERT INTO notification(
                member_id, target_id, event_type, event_data, is_read
            )
            VALUES(
                %s, %s, 'Like', %s, False
            )
        """
        cursor.execute(update_notification_sql, (member_id, account_id, event_data_json))

        connection.commit()
    
    except Exception as e:
        print(f"Error updating notification: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
