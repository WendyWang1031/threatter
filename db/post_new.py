import pymysql.cursors
from typing import Optional
from model.model import *
from db.check_relation import *
from db.re_post_data import *
from service.common import *
from db.connection_pool import get_db_connection_pool



def db_get_home_post_data(member_id: Optional[str] , page : int) -> Optional[PostListRes] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        limit = 15
        offset = page * limit

        if member_id is None:
            sql = """
                SELECT content.*, 
                    member.name, member.account_id, member.avatar, 
                    likes.like_state
                FROM content
                LEFT JOIN member ON content.member_id = member.account_id
                LEFT JOIN likes ON content.content_id = likes.content_id
                WHERE content.content_type = 'Post' 
                AND content.visibility = 'Public'
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """
            params = (limit+1, offset)
        else:
            sql = """
                SELECT content.*, 
                    member.name, member.account_id, member.avatar,  
                    likes.like_state,
                    member.visibility, member_relation.relation_state
                FROM content
                LEFT JOIN member ON content.member_id = member.account_id
                LEFT JOIN likes ON content.content_id = likes.content_id AND likes.member_id = %s
                LEFT JOIN member_relation ON content.member_id = member_relation.target_id AND member_relation.member_id = %s
                WHERE content.content_type = 'Post'
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """
            params = (member_id, member_id, limit+1, offset)

        return db_get_post_data(sql, params, multiple=True)

        
        
    except Exception as e:
        print(f"Error getting home post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def db_create_post_data(post_data : PostCreateReq , member_id : str ) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        content = validate(post_data.content.text)
        image_url = video_url = audio_url = None

        if isinstance(post_data.content.media, Media):
            image_url = validate(post_data.content.media.images)
            video_url = validate(post_data.content.media.videos)
            audio_url = validate(post_data.content.media.audios)
        

        content_id = generate_short_uuid('Post')
        parent_id = post_data.post_parent_id

        sql = """
            INSERT INTO content 
            (member_id, parent_id, content_id, content_type, 
            visibility, text, image, video, audio)
            VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql , (member_id , parent_id, content_id, 'Post', 
                              post_data.visibility, content, image_url, video_url, audio_url) )
        
        connection.commit()
        
        return True
    
    except Exception as e:
        print(f"Error inserting post Data: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

def db_delete_post(post_id : str , member_id : str ) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "delete from content where content_id = %s and member_id = %s "
        cursor.execute(sql , ( post_id , member_id ))
        connection.commit()  

        if cursor.rowcount > 0:
            return True
        return False
        
    
    except Exception as e:
        print(f"Error deleting user's post: {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()

def db_get_member_post_data(account_id : str , page : int) -> Optional[PostListRes] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
  
        ## 顯示以下貼文內容

        limit = 15 
        offset = page * limit

        
        sql = """select content.* ,
            member.name , member.account_id , member.avatar,  
            likes.like_state
        FROM content
        
        Left Join member on content.member_id = member.account_id
        Left Join likes on content.content_id = likes.content_id AND likes.member_id = %s
        WHERE content.member_id = %s AND content.content_type = 'Post'
        ORDER BY created_at DESC LIMIT %s OFFSET %s
        """
        params = (account_id, account_id, limit+1, offset)
        return db_get_post_data(sql, params, multiple=True)

    
        
    except Exception as e:
        print(f"Error getting member's post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()


def db_get_single_post_data(account_id : str , post_id : int) -> Optional[Post] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
    
        ## 顯示以下貼文內容

        sql = """select content.* ,
            member.name , member.account_id , member.avatar 
            
        FROM content
        
        Left Join member on content.member_id = member.account_id
        
        WHERE content.member_id = %s 
        AND content.content_id = %s
        AND content.content_type = 'Post'
        """

        params = (account_id, post_id)
    
        return db_get_post_data(sql, params, multiple=False)
  

        
    except Exception as e:
        print(f"Error getting single post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

