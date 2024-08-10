import pymysql.cursors
from typing import Optional
from model.model import *
from db.check_relation import *
from service.common import *
from db.connection_pool import get_db_connection_pool



def db_get_home_post_data(member_id: Optional[str] , page : int) -> Optional[PostListRes] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()

        limit = 15 
        offset = page * limit
        
        if member_id is None : 
            sql = """
            select content.* , 
            member.name , member.account_id , member.avatar, 
            likes.like_state
            FROM content
            
            Left Join member on content.member_id = member.account_id
            Left Join likes on content.content_id = likes.content_id
            
            WHERE content.content_type = 'Post' AND
            content.visibility = 'Public'
            ORDER BY created_at DESC LIMIT %s OFFSET %s
            """
            cursor.execute( sql , (limit+1 , offset) )
            post_data = cursor.fetchall()
        else:
            sql = """
            select content.* ,
            member.name , member.account_id , member.avatar,  
            likes.like_state,
            member.visibility, member_relation.relation_state
            FROM content
            
            LEFT JOIN member on content.member_id = member.account_id
            LEFT JOIN likes on content.content_id = likes.content_id AND likes.member_id = %s
            LEFT JOIN member_relation ON content.member_id = member_relation.target_id AND member_relation.member_id = %s

            WHERE content.content_type = 'Post' 
            ORDER BY created_at DESC LIMIT %s OFFSET %s
            """
            cursor.execute( sql , (member_id , member_id , limit+1 , offset) )
            post_data = cursor.fetchall()
            # print("post_data:",post_data)
        
        # 過濾後的資料
            filtered_post_data = []
            for post in post_data:
                post_visibility = post["visibility"]
                relation_state = post.get("relation_state")
                account_id = post.get("member_id")
                
                if has_permission_to_view(account_id, post_visibility, relation_state):
                    filtered_post_data.append(post)
            
            # print("filtered_post_data:",filtered_post_data)
            post_data = filtered_post_data

        if not post_data:
            return None
        
        has_more_data = len(post_data) > limit
        
        if has_more_data :
            post_data.pop()


        posts = []
        for data in post_data:

            parent_post = None
            if data.get('parent_id'):
                parent_post = ParentPostId(
                    account_id=data.get('account_id'),  
                    post_id=data['parent_id']       
                )

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
                parent = parent_post ,
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
                    like_counts = int(data.get('like_counts' , 0)),
                    reply_counts = int(data.get('reply_counts' , 0)),
                    forward_counts = int(data.get('forward_counts' , 0)),
                )
            )
            posts.append(post)

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
        WHERE content.member_id = %s 
        ORDER BY created_at DESC LIMIT %s OFFSET %s
        """
        cursor.execute( sql , (account_id , account_id , limit+1 , offset))
        post_data = cursor.fetchall()
        # print("post_data:",post_data)

    
        if not post_data:
            return None
        
        has_more_data = len(post_data) > limit
        
        if has_more_data :
            post_data.pop()

        post_ids = tuple(post['content_id'] for post in post_data)
        # print("post_ids:",post_ids)
        like_count_sql = """
            SELECT content_id, COUNT(*) as total_likes 
            FROM likes
            WHERE content_id IN %s AND like_state = TRUE
            GROUP BY content_id
        """
        cursor.execute(like_count_sql, (post_ids,))
        likes_data = cursor.fetchall()
        # print("likes_data:",likes_data)

        comment_count_sql = """
            SELECT parent_id, COUNT(*) as total_replies 
            FROM content
            WHERE parent_id IN %s AND content_type = 'Comment'
            GROUP BY parent_id
        """
        cursor.execute(comment_count_sql, (post_ids,))
        comments_data = cursor.fetchall()
        # print("comments_data:",comments_data)

        forward_count_sql = """
            SELECT parent_id, COUNT(*) as total_forwards 
            FROM content
            WHERE parent_id IN %s AND content_type = 'Post'
            GROUP BY parent_id
        """
        cursor.execute(forward_count_sql, (post_ids,))
        forwards_data = cursor.fetchall()
        # print("forwards_data:",forwards_data)

        # 創建字典
        likes_dict = {like['content_id']: like['total_likes'] for like in likes_data}
        comments_dict = {comment['parent_id']: comment['total_replies'] for comment in comments_data}
        forwards_dict = {forward['parent_id']: forward['total_forwards'] for forward in forwards_data}



        posts = []
        for data in post_data:

            total_likes = likes_dict.get(data['content_id'], 0)
            total_replies = comments_dict.get(data['content_id'], 0)
            total_forwards = forwards_dict.get(data['content_id'], 0)
        
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
                    like_counts = int(total_likes or 0),
                    reply_counts = int(total_replies or 0),
                    forward_counts = int(total_forwards or 0),
                )
            )
            posts.append(post)

            # print("posts:",posts)

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


def db_get_single_post_data(account_id : str , post_id : int) -> Optional[Post] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
    
        ## 顯示以下貼文內容

        sql = """select content.* ,
            member.name , member.account_id , member.avatar,  
            likes.like_state
        FROM content
        
        Left Join member on content.member_id = member.account_id
        Left Join likes on content.content_id = likes.content_id AND likes.member_id = %s
        WHERE content.member_id = %s 
        AND content.content_id = %s
        """
        cursor.execute( sql , (account_id , account_id , post_id) )
        post_data = cursor.fetchone()
        # print("post_data:",post_data)
  

        if not post_data:
            return None

        media = Media(
        images=post_data.get('image'),
        videos=post_data.get('video'),
        audios=post_data.get('audio')
        )

        created_at = post_data['created_at']
        if isinstance(created_at, str):
            created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')


        post = Post(
            post_id = post_data['content_id'] ,
            parent=ParentPostId(id=post_data['parent_id']) if post_data.get('parent_id') else None ,
            created_at = created_at ,
            user = MemberBase(
                name = post_data['name'],
                account_id = post_data['account_id'],
                avatar = post_data['avatar']
            ),
            content = PostContent(
                text = post_data['text'],
                media = media,
            ),
            visibility = post_data['visibility'],
            like_state = bool(post_data.get('like_state' , False)),
            counts = PostCounts(
                like_counts = int(post_data.get('like_counts', 0)),
                reply_counts = int(post_data.get('reply_counts', 0)),
                forward_counts = int(post_data.get('forward_counts', 0)),
            )
        )
            
        connection.commit()
        
        return post
        
    except Exception as e:
        print(f"Error getting single post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

