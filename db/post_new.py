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
                    FALSE AS like_state
                FROM content
                LEFT JOIN member ON content.member_id = member.account_id
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

def db_get_personalized_recommendations(
                        member_id: str,
                        page : int) -> Optional[PostListRes] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        limit = 15
        offset = page * limit

        
        
        sql = """
            SELECT content.*, 
                member.name, member.account_id, member.avatar,  
                likes.like_state,
                member.visibility, member_relation.relation_state,
                (content.like_counts * 2 + content.reply_counts * 1) AS popularity_score,
                CASE 
                    WHEN content.member_id = %s THEN 5
                    WHEN member.visibility = 'Private' AND content.visibility = 'Private' THEN 4
                    WHEN member.visibility = 'Private' AND content.visibility = 'Public' THEN 3
                    WHEN member.visibility = 'Public' AND content.visibility = 'Private' THEN 2
                    ELSE 1
                END AS priority_score
            FROM content
            LEFT JOIN member ON content.member_id = member.account_id
            LEFT JOIN (
                SELECT m1.target_id
                    FROM member_relation m1
                    WHERE m1.member_id = %s 
                    AND m1.relation_state = 'Following'
                UNION
                SELECT %s AS target_id  
            
            ) AS mutual_relations ON content.member_id = mutual_relations.target_id
            LEFT JOIN likes ON content.content_id = likes.content_id AND likes.member_id = %s
            LEFT JOIN member_relation ON content.member_id = member_relation.target_id AND member_relation.member_id = %s
            
            WHERE content.content_type = 'Post'
            AND ( content.member_id = mutual_relations.target_id )
            AND content.created_at >= NOW() - INTERVAL 5 DAY
            ORDER BY priority_score DESC, popularity_score DESC, created_at DESC 
            LIMIT %s OFFSET %s
        """
        params = (member_id, member_id, member_id, member_id, member_id, limit+1, offset)
    
        return db_get_post_data( sql, params, multiple=True)

        
        
    except Exception as e:
        print(f"Error getting home post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()


def db_get_popular_posts(member_id: Optional[str],
                        time_frame: int,
                        page : int) -> Optional[PostListRes] | None:
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
                    FALSE AS like_state, 
                    (content.like_counts * 2 + content.reply_counts * 1) AS popularity_score
                FROM content
                LEFT JOIN member ON content.member_id = member.account_id
                
                
                WHERE content.content_type = 'Post'
                AND content.visibility = 'Public'
                AND content.created_at >= NOW() - INTERVAL %s DAY
                ORDER BY popularity_score DESC, created_at DESC 
                LIMIT %s OFFSET %s
            """
            params = (time_frame, limit+1, offset)

        else:
            sql = """
                SELECT content.*, 
                    member.name, member.account_id, member.avatar,  
                    likes.like_state,
                    (content.like_counts * 2 + content.reply_counts * 1) AS popularity_score
                FROM content
                LEFT JOIN member ON content.member_id = member.account_id
                LEFT JOIN likes ON content.content_id = likes.content_id AND likes.member_id = %s
                
                
                WHERE content.content_type = 'Post'
                AND content.visibility = 'Public'
                AND content.created_at >= NOW() - INTERVAL %s DAY
                ORDER BY popularity_score DESC, created_at DESC 
                LIMIT %s OFFSET %s
            """
            params = (member_id,  time_frame, limit+1, offset)

        return db_get_post_data( sql, params, multiple=True)

        
        
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
        
        return True , content_id
    
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
        select_comment_sql = """
            SELECT content_id FROM content WHERE parent_id = %s
        """
        cursor.execute(select_comment_sql, (post_id,))
        child_comment_ids = [row['content_id'] for row in cursor.fetchall()]

        for child_id in child_comment_ids: 
            delete_child_reply_likes_sql = """
                DELETE FROM likes WHERE content_id IN 
                (SELECT content_id FROM content WHERE parent_id = %s)
            """
            cursor.execute(delete_child_reply_likes_sql, (child_id,))

            delete_child_reply_sql = """
                DELETE FROM content WHERE parent_id = %s
            """
            cursor.execute(delete_child_reply_sql, (child_id,))

        delete_child_comment_likes_sql = """
            DELETE FROM likes WHERE content_id IN (%s)
            """ % ','.join(['%s'] * len(child_comment_ids))
        if child_comment_ids:
            cursor.execute(delete_child_comment_likes_sql, tuple(child_comment_ids))


        delete_child_comment_sql = """
            DELETE FROM content 
            WHERE parent_id = %s
        """
        cursor.execute(delete_child_comment_sql, (post_id,))

        # 刪除 likes 表和 post 相關的紀錄
        delete_likes_sql = "DELETE FROM likes WHERE content_id = %s"
        cursor.execute(delete_likes_sql, (post_id,))
        
        # 刪除 content 表的紀錄
        delete_content_sql = "DELETE FROM content WHERE content_id = %s AND member_id = %s"
        cursor.execute(delete_content_sql, (post_id, member_id))
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

def db_get_member_post_data(member_id : Optional[str] , account_id : str , page : int) -> Optional[PostListRes] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
  
        ## 顯示以下貼文內容

        limit = 15 
        offset = page * limit

        if member_id is None:

            sql = """
            select content.* ,
                member.name , member.account_id , member.avatar,  
                FALSE AS like_state
            FROM content
            
            Left Join member on content.member_id = member.account_id
            Left Join likes on content.content_id = likes.content_id AND likes.member_id = %s
            WHERE content.member_id = %s 
                AND content.content_type = 'Post' AND content.visibility = 'Public'
            ORDER BY created_at DESC LIMIT %s OFFSET %s
        """
            params = (account_id, account_id, limit+1, offset)
        
        if member_id == account_id:

            sql = """
            select content.* ,
                member.name , member.account_id , member.avatar,  
                likes.like_state
            FROM content
            
            Left Join member on content.member_id = member.account_id
            Left Join likes on content.content_id = likes.content_id AND likes.member_id = %s
            WHERE content.member_id = %s AND content.content_type = 'Post'
            ORDER BY created_at DESC LIMIT %s OFFSET %s
        """
            params = (account_id, account_id, limit+1, offset)

        
        
        else:
            sql = """
            select content.* ,
                member.name , member.account_id , member.avatar,  
                likes.like_state
            FROM content
            
            LEFT JOIN member on content.member_id = member.account_id
            LEFT JOIN likes on content.content_id = likes.content_id AND likes.member_id = %s
            LEFT JOIN member_relation ON content.member_id = member_relation.target_id AND member_relation.member_id = %s
            WHERE content.member_id = %s 
                AND content.content_type = 'Post'
                AND (content.visibility = 'Public' 
                    OR (content.visibility = 'Private' AND 
                        (member_relation.relation_state = 'Following')))
            ORDER BY created_at DESC LIMIT %s OFFSET %s
            """
            params = (account_id, member_id, account_id, limit+1, offset)
        
        return db_get_post_data(sql, params, multiple=True)

    
        
    except Exception as e:
        print(f"Error getting member's post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()


def db_get_single_post_data(member_id: Optional[str] , account_id : str , post_id : int) -> Optional[Post] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
    
        ## 顯示以下貼文內容
        if member_id is None:
            sql = """
                select content.* ,
                member.name , member.account_id , member.avatar ,
                FALSE AS like_state
                FROM content
                
                Left Join member on content.member_id = member.account_id
                
                WHERE content.member_id = %s 
                AND content.content_id = %s
                AND content.content_type = 'Post' and content.visibility = 'Public'
            """
            params = (account_id, post_id)

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
                        AND content.content_id = %s
                        AND (content.visibility = 'Public' 
                        OR (content.visibility = 'Private' AND (member_relation.relation_state = 'Following'))
                        OR content.member_id = %s)
                ORDER BY created_at DESC 
            """
            params = (member_id , member_id , post_id, member_id)
    
        return db_get_post_data(sql, params, multiple=False)
  

        
    except Exception as e:
        print(f"Error getting single post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

