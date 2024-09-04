import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool
from db.re_post_data import *
from db.notification import *
from service.common import *
from util.follow_util import *

async def db_create_comment_data(comment_data : CommentReq , account_id: str,  post_id : str , member_id : str) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        content = validate(comment_data.content.text)
        image_url = video_url = audio_url = None

        if isinstance(comment_data.content.media, Media):
            image_url = validate(comment_data.content.media.images)
            video_url = validate(comment_data.content.media.videos)
            audio_url = validate(comment_data.content.media.audios)
        

        content_id = generate_short_uuid('Comment')
        

        sql = """
            INSERT INTO content 
            (member_id, parent_id, content_id, content_type, 
            visibility, text, image, video, audio)
            VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql , (member_id , post_id, content_id, 'Comment', 
                              comment_data.visibility, content, image_url, video_url, audio_url) )

       # 同時對貼文總回覆數 +1
        update_post_sql = """
            UPDATE content 
            SET reply_counts = reply_counts + 1 
            WHERE content_id = %s
        """
        cursor.execute(update_post_sql, (post_id,))


        connection.commit()

        if account_id != member_id:
            await db_update_notification(member_id, account_id, post_id, content_id, 'Reply')
        

        return True
    
    except Exception as e:
        print(f"Error inserting comment Data: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

async def db_create_reply_data(comment_data : CommentReq , account_id: str , post_id : str , comment_id : str , member_id : str) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        def validate(value: Optional[str]) -> Optional[str] :
            if value is None:
                return None
            return value.strip() or None
        
        content = validate(comment_data.content.text)
        image_url = video_url = audio_url = None

        if isinstance(comment_data.content.media, Media):
            image_url = validate(comment_data.content.media.images)
            # print("Validated image URL:", image_url)
            video_url = validate(comment_data.content.media.videos)
            audio_url = validate(comment_data.content.media.audios)
        

        content_id = generate_short_uuid('Reply')
        

        sql = """
            INSERT INTO content 
            (member_id, parent_id, content_id, content_type, 
            visibility, text, image, video, audio)
            VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql , (member_id , comment_id, content_id, 'Reply', 
                              comment_data.visibility, content, image_url, video_url, audio_url) )
        
        # 直接對該留言的回覆數 +1
        update_comment_sql = """
            UPDATE content 
            SET reply_counts = reply_counts + 1 
            WHERE content_id = %s
        """
        cursor.execute(update_comment_sql, (comment_id,))

        # 同時對貼文總回覆數 +1
        update_post_sql = """
            UPDATE content 
            SET reply_counts = reply_counts + 1 
            WHERE content_id = %s
        """
        cursor.execute(update_post_sql, (post_id,))
        
        connection.commit()
        
        if account_id != member_id:
            await db_update_notification(
                member_id, account_id, post_id, content_id, 'Reply' , comment_id)

        
        return True
    
    except Exception as e:
        print(f"Error inserting reply Data: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()


def db_delete_comment_and_reply(comment_id : str , member_id : str) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        delete_child_replies_sql = """
            DELETE FROM content 
            WHERE parent_id = %s
        """
        cursor.execute(delete_child_replies_sql, (comment_id,))

        delete_likes_sql = "DELETE FROM likes WHERE content_id = %s"
        cursor.execute(delete_likes_sql, (comment_id,))

        sql = "delete from content where content_id = %s and member_id = %s "
        cursor.execute(sql , ( comment_id , member_id ))
        connection.commit()  

        if cursor.rowcount > 0:
            return True
        return False
        
    
    except Exception as e:
        print(f"Error deleting user's comment or reply: {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()

def db_get_comments_and_replies_data(member_id: Optional[str] , account_id : str , post_id : str , page : int) -> Optional[PostListRes] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        

        limit = 15 
        offset = page * limit

        # 預設狀況下，用戶只能看到公開的內容
        visibility_clause = "content.visibility = 'Public'"
        # print("member_id:",member_id)

        if not member_id:
            member_id = None
        
        if member_id : 
            # 檢查已登入用戶
            relation_sql = """select relation_state
            FROM member_relation
            where member_id = %s AND target_id = %s
            """
            cursor.execute( relation_sql , (member_id , account_id) )
            relation = cursor.fetchone()
            if relation : 
                relation_state = get_relation_status(relation)
                if member_id == account_id or relation_state == RELATION_STATUS_FOLLOWING:
                    visibility_clause = "(content.visibility = 'Public' OR content.visibility = 'Private')"
                else:
                    visibility_clause = "content.visibility = 'Public'"
            
            # 如果用戶已登入，查詢該用戶的按讚狀態
            likes_clause = "likes.like_state"
        else:
            # 如果用戶未登入，按讚狀態應該為 False
            likes_clause = "FALSE AS like_state"

        sql = f"""
            select
                content.* ,
                member.name , 
                member.account_id , 
                member.avatar,  
                {likes_clause}
            
            FROM content
            
            Left Join member on content.member_id = member.account_id
            Left Join likes on content.content_id = likes.content_id AND likes.member_id = %s
            WHERE (content.content_type = "Comment" OR content.content_type = "Reply")
            AND content.parent_id = %s 
            AND {visibility_clause}
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        

        cursor.execute( sql , (member_id , post_id , limit+1 , offset) )    
        comment_data = cursor.fetchall()
        # print("comment_data:",comment_data)

        if not comment_data:
            return "No Comment Data" ,  None

        # 將所有留言的id取出存放在列表 ['C-3b8cec09', 'C-22c1d5e4',...]
        comment_ids = []
        for comment in comment_data :
            if comment['content_type'] == 'Comment' :
                comment_ids.append(comment['content_id'])
        # print("comment_ids:" , comment_ids)

        if comment_ids : 
            reply_sql =f"""
                SELECT 
                    content.*,
                    member.name,
                    member.account_id,
                    member.avatar,
                    {likes_clause}
                FROM content
                Left Join member on content.member_id = member.account_id
                Left Join likes on content.content_id = likes.content_id AND likes.member_id = %s
                WHERE content.parent_id IN ({','.join(['%s'] * len(comment_ids))})
                AND content.content_type = 'Reply'
                AND {visibility_clause}
                ORDER BY content.created_at DESC

            """
            cursor.execute( reply_sql , ([member_id] + comment_ids) )    
            reply_data = cursor.fetchall()
        else:
            reply_data = []

        # print("reply_data:" , reply_data)
        
        replies_map = {}
        for reply in reply_data :
            parent_id = reply['parent_id']
            if parent_id not in replies_map :
                replies_map[parent_id] = []
            replies_map[parent_id].append(reply)
        # print("replies_map:" , replies_map)

        comment_detail_list = []
        for comment in comment_data :
            if comment['content_type'] == 'Comment':
                comment_obj = generate_comment_object(comment)
                replies = replies_map.get(comment['content_id'],[])
                # print("replies:" , replies)
                reply_objects = [generate_comment_object(reply) for reply in replies]
                comment_detail_list.append(CommentDetail(comment = comment_obj , replies=reply_objects))
        # print("comment_data:" , comment_data)

        
        has_more_data = len(comment_data) > limit
        
        if has_more_data :
            comment_data.pop()

        
        next_page = page + 1 if has_more_data else None

        connection.commit()
        
        return "Success" , CommentDetailListRes(next_page = next_page , data = comment_detail_list )
        
        


    except Exception as e:
        print(f"Error getting comment or reply data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()
