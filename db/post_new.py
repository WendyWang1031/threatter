import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool
import uuid



def generate_short_uuid(content_type: str) -> str:
    prefix = {
        'Post': 'P-',
        'Comment': 'C-',
        'Reply': 'R-'
    }.get(content_type, 'O-')
    
    short_uuid = str(uuid.uuid4())[:8]  
    return f"{prefix}{short_uuid}"

def db_get_post_data(member_id: Optional[str] , page : int) -> Optional[PostListRes] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()

        limit = 15 
        offset = page * limit
        
        if member_id is None : 
            sql = """select content.* , 
            member.name , member.account_id , member.avatar, 
            likes.like_state
            FROM content
            
            Left Join member on content.member_id = member.account_id
            Left Join likes on content.content_id = likes.content_id
            WHERE content.visibility = 'Public'
            ORDER BY created_at DESC LIMIT %s OFFSET %s
            """
            cursor.execute( sql , (limit+1 , offset) )
        else:
            sql = """select content.* ,
            member.name , member.account_id , member.avatar,  
            likes.like_state
            FROM content
            
            Left Join member on content.member_id = member.account_id
            Left Join likes on content.content_id = likes.content_id AND likes.member_id = %s
            WHERE content.visibility = 'Public' OR 
            (content.visibility = 'Private' AND content.member_id = %s)
            ORDER BY created_at DESC LIMIT %s OFFSET %s
            """
            cursor.execute( sql , (member_id , member_id , limit+1 , offset) )
        
        
        post_data = cursor.fetchall()

        if not post_data:
            return None
        
        has_more_data = len(post_data) > limit
        
        if has_more_data :
            post_data.pop()

        posts = []
        for data in post_data:
        
            media = Media(
            images=data.get('image'),
            videos=data.get('video'),
            audios=data.get('audio')
            )

            created_at = data['created_at']
            if isinstance(created_at, str):
                created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')


            post = Post(
                post_id = data['content_id'] ,
                parent=ParentPostId(id=data['parent_id']) if data.get('parent_id') else None ,
                created_at = created_at ,
                user = MemberBase(
                    name = data['name'],
                    account_id = data['account_id'],
                    avatar = data['avatar']
                ),
                content = PostContent(
                    text = data['text'],
                    media = media,
                ),
                visibility = data['visibility'],
                like_state = bool(data.get('like_state' , False)),
                counts = PostCounts(
                    like_counts = int(data.get('like_counts') or 0),
                    reply_counts = int(data.get('reply_counts') or 0),
                    forward_counts = int(data.get('forward_counts') or 0),
                )
            )
            posts.append(post)

            print("posts:",posts)

        connection.commit()
        
        next_page = page + 1 if has_more_data else None
        return PostListRes(next_page = next_page , data = posts )
        
    except Exception as e:
        print(f"Error getting post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def db_create_post_data( post_data : PostCreateReq , member_id : str ) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        def validate(value: Optional[str]) -> Optional[str] :
            if value is None:
                return None
            return value.strip() or None
        
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