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


def db_create_comment_data(comment_data : CommentReq , post_id : str , member_id : str) -> bool :
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
        

        content_id = generate_short_uuid('Comment')
        

        sql = """
            INSERT INTO content 
            (member_id, parent_id, content_id, content_type, 
            visibility, text, image, video, audio)
            VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql , (member_id , post_id, content_id, 'Comment', 
                              comment_data.visibility, content, image_url, video_url, audio_url) )
        
        connection.commit()
        
        return True
    
    except Exception as e:
        print(f"Error inserting comment Data: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

def db_create_reply_data(comment_data : CommentReq , comment_id : str , member_id : str) -> bool :
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
        
        connection.commit()
        
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
        
        if member_id : 
            # 檢查已登入用戶
            relation_sql = """select relation_state
            FROM member_relation
            where member_id = %s AND target_id = %s
            """
            cursor.execute( relation_sql , (member_id , account_id) )
            relation = cursor.fetchone()
            if relation : 
                relation_state = relation['relation_state']
                if member_id == account_id or relation_state == 'Following':
                    visibility_clause = "(content.visibility = 'Public' OR content.visibility = 'Private')"
                else:
                    visibility_clause = "content.visibility = 'Public'"
        
        sql = f"""
        select content.* ,
            member.name , 
            member.account_id , 
            member.avatar,  
            likes.like_state
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
        print("comment_data:",comment_data)

        if not comment_data:
            return "No Comment Data" ,  None

        comment_ids = tuple(comment['content_id'] for comment in comment_data)
        
        print("comment_ids:",comment_ids)
        like_count_sql = """
            SELECT content_id, COUNT(*) as total_likes 
            FROM likes
            WHERE content_id IN %s AND like_state = TRUE
            GROUP BY content_id
        """
        cursor.execute(like_count_sql, (comment_ids,))
        likes_data = cursor.fetchall()
        # print("likes_data:",likes_data)

        comment_count_sql = """
            SELECT parent_id, COUNT(*) as total_replies 
            FROM content
            WHERE parent_id IN %s AND content_type = 'Comment'
            GROUP BY parent_id
        """
        cursor.execute(comment_count_sql, (comment_ids,))
        comments_data = cursor.fetchall()
        # print("comments_data:",comments_data)

        forward_count_sql = """
            SELECT parent_id, COUNT(*) as total_forwards 
            FROM content
            WHERE parent_id IN %s AND content_type = 'Post'
            GROUP BY parent_id
        """
        cursor.execute(forward_count_sql, (comment_ids,))
        forwards_data = cursor.fetchall()
        # print("forwards_data:",forwards_data)

        # 創建字典
        likes_dict = {like['content_id']: like['total_likes'] for like in likes_data}
        comments_dict = {comment['parent_id']: comment['total_replies'] for comment in comments_data}
        forwards_dict = {forward['parent_id']: forward['total_forwards'] for forward in forwards_data}

        reply_ids = tuple(reply['content_id'] for comment in comment_data for reply in comment_data)
        
        cursor.execute(like_count_sql, (reply_ids,))
        likes_data = cursor.fetchall()

        cursor.execute(comment_count_sql, (comment_ids,))
        likes_data = cursor.fetchall()

        cursor.execute(forward_count_sql, (comment_ids,))
        likes_data = cursor.fetchall()


        
        
        has_more_data = len(comment_data) > limit
        
        if has_more_data :
            comment_data.pop()

        comment_detail_list = []
        for data in comment_data:

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


            comment = Comment(
                comment_id = data['content_id'] ,
                user = MemberBase(
                    name = data['name'],
                    account_id = data['account_id'],
                    avatar = data['avatar']
                ),
                content = PostContent(
                    text = data['text'],
                    media = media,
                ),
                created_at = created_at ,
                like_state = bool(data.get('like_state' , False)),
                counts = PostCounts(
                    like_counts = int(total_likes or 0),
                    reply_counts = int(total_replies or 0),
                    forward_counts = int(total_forwards or 0),
                )
            )
            
            

            replies_sql = """
                SELECT content.*,
                    member.name,
                    member.account_id,
                    member.avatar
                FROM content
                LEFT JOIN member ON content.member_id = member.account_id
                WHERE content.parent_id = %s AND content.content_type = 'Reply'
            """
            cursor.execute(replies_sql, (data['content_id'],))
            reply_data = cursor.fetchall()
            # print("reply_data:",reply_data)

            replies = []
            
            if reply_data : 
                for reply in reply_data:
                    reply_media = Media(
                        images=reply.get('image'),
                        videos=reply.get('video'),
                        audios=reply.get('audio')
                    )

                    reply_created_at = reply['created_at']
                    if isinstance(reply_created_at, str):
                        reply_created_at = datetime.strptime(reply_created_at, '%Y-%m-%d %H:%M:%S')

                    reply_comment = Comment(
                        comment_id=reply['content_id'],
                        user=MemberBase(
                            name=reply['name'],
                            account_id=reply['account_id'],
                            avatar=reply['avatar']
                        ),
                        content=PostContent(
                            text=reply['text'],
                            media=reply_media,
                        ),
                        created_at=reply_created_at,
                        like_state=bool(reply.get('like_state', False)),
                        counts=PostCounts(
                            like_counts=int(reply.get('like_counts') or 0),
                            reply_counts=int(reply.get('reply_counts') or 0),
                            forward_counts=int(reply.get('forward_counts') or 0),
                        )
                    )
                    # print("reply_comment:",reply_comment)

                    replies.append(reply_comment)
            else:
                replies = []
        
            comment_detail = CommentDetail(
            comment = comment,
            replies = replies 
            )
            
            comment_detail_list.append(comment_detail)
            
        connection.commit()
        
        next_page = page + 1 if has_more_data else None
        
        return "Success" , CommentDetailListRes(next_page = next_page , data = comment_detail_list )
        
        # sql = f"""
        # SELECT
        #     content.* ,
        #     member.name , member.account_id , member.avatar , 
        #     likes.like_state , 
        #     COALESCE(comment_likes.total_likes, 0) as like_counts ,
        #     COALESCE(comment_replies.total_replies, 0) as reply_counts ,
        #     COALESCE(comment_forwards.total_forwards, 0) as forward_counts ,
            
        #     reply.content_id as reply_id ,
        #     reply.text as reply_text ,
        #     reply.created_at as reply_created_at ,
        #     reply_member.name as reply_name ,
        #     reply_member.account_id as reply_account_id ,
        #     reply_member.avatar as reply_avatar ,
        #     reply_likes.like_state as reply_like_state ,
        #     COALESCE(reply_likes_count.total_likes, 0) as reply_like_counts

        # FROM content
        # LEFT JOIN member ON content.member_id = member.account_id
        # LEFT JOIN likes ON content.content_id = likes.content_id AND likes.member_id = %s
        
        # LEFT JOIN (
        #     SELECT content_id , COUNT(*) as total_likes
        #     FROM likes
        #     where like_state = TRUE
        #     GROUP BY content_id
        # ) comment_likes ON content.content_id = comment_likes.content_id
        
        # LEFT JOIN (
        #     SELECT parent_id, COUNT(*) as total_replies
        #     FROM content
        #     WHERE content_type = 'Comment'
        #     GROUP BY parent_id
        # ) comment_replies ON content.content_id = comment_replies.parent_id
        
        # LEFT JOIN (
        #     SELECT parent_id, COUNT(*) as total_forwards
        #     FROM content
        #     WHERE content_type = 'Post'
        #     GROUP BY parent_id
        # ) comment_forwards ON content.content_id = comment_forwards.parent_id

        # LEFT JOIN content AS reply ON reply.parent_id = content.content_id 
        # AND reply.content_type = 'Reply'
        
        # LEFT JOIN member AS reply_member ON reply.member_id = reply_member.account_id

        # LEFT JOIN likes AS reply_likes ON reply.content_id = reply_likes.content_id 
        # AND reply_likes.member_id = %s

        # LEFT JOIN (
        #     SELECT content_id, COUNT(*) as total_likes
        #     FROM likes
        #     WHERE like_state = TRUE
        #     GROUP BY content_id
        # ) reply_likes_count ON reply.content_id = reply_likes_count.content_id

        # WHERE (content.content_type = 'Comment' OR content.content_type = 'Reply')
        #     AND content.parent_id = %s
        #     AND {visibility_clause}
        # ORDER BY content.created_at DESC 
        # LIMIT %s OFFSET %s

        # """
        # cursor.execute( sql , (member_id ,member_id, post_id , limit+1 , offset))
        # comment_data = cursor.fetchall()
        # # print("comment_data:",comment_data)

        # if not comment_data:
        #     return None
        
        # has_more_data = len(comment_data) > limit
        
        # if has_more_data :
        #     comment_data.pop()

        # comment_dict = {}
        # for data in comment_data:
        #     if data['content_type'] == 'Comment':
        #         comment_dict[data['content_id']] = {
        #             'comment': data,
        #             'replies': []
        #         }
        #     elif data['content_type'] == 'Reply':
        #         parent_id = data['parent_id']
        #         if parent_id in comment_dict:
        #             comment_dict[parent_id]['replies'].append(data)

        # print("comment_dict:",comment_dict)
        # comment_detail_list = []
        # for comment_id, details in comment_dict.items():

        #     comment_data = details['comment']
        #     reply_data_list = details['replies']
        
        #     media = Media(
        #     images=comment_data.get('image'),
        #     videos=comment_data.get('video'),
        #     audios=comment_data.get('audio')
        #     )

        #     created_at = comment_data['created_at']
        #     if isinstance(created_at, str):
        #         created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')


        #     comment = Comment(
        #         comment_id = comment_data['content_id'] ,
        #         user = MemberBase(
        #             name = comment_data['name'],
        #             account_id = comment_data['account_id'],
        #             avatar = comment_data['avatar']
        #         ),
        #         content = PostContent(
        #             text = comment_data['text'],
        #             media = media,
        #         ),
        #         created_at = created_at ,
        #         like_state = bool(comment_data.get('like_state' , False)),
        #         counts = PostCounts(
        #             like_counts = int(comment_data.get('like_counts' or 0)),
        #             reply_counts = int(comment_data.get('reply_counts' or 0)),
        #             forward_counts = int(comment_data.get('forward_counts' or 0)),
        #         )
        #     )



        #     replies = []
            
        #     if reply_data_list : 
        #         for reply in reply_data_list:
        #             reply_media = Media(
        #                 images=reply.get('image'),
        #                 videos=reply.get('video'),
        #                 audios=reply.get('audio')
        #             )

        #             reply_created_at = reply['created_at']
        #             if isinstance(reply_created_at, str):
        #                 reply_created_at = datetime.strptime(reply_created_at, '%Y-%m-%d %H:%M:%S')

        #             reply_comment = Comment(
        #                 comment_id=reply['content_id'],
        #                 user=MemberBase(
        #                     name=reply['name'],
        #                     account_id=reply['account_id'],
        #                     avatar=reply['avatar']
        #                 ),
        #                 content=PostContent(
        #                     text=reply['text'],
        #                     media=reply_media,
        #                 ),
        #                 created_at=reply_created_at,
        #                 like_state=bool(reply.get('like_state', False)),
        #                 counts=PostCounts(
        #                     like_counts=int(reply.get('like_counts') or 0),
        #                     reply_counts=int(reply.get('reply_counts') or 0),
        #                     forward_counts=int(reply.get('forward_counts') or 0),
        #                 )
        #             )
        #             # print("reply_comment:",reply_comment)

        #             replies.append(reply_comment)
        #     else:
        #         replies = None
        
        #     comment_detail = CommentDetail(
        #     comment = comment,
        #     replies = replies 
        #     )
            
        #     comment_detail_list.append(comment_detail)
            
        # connection.commit()
        
        # next_page = page + 1 if has_more_data else None
        
        # return CommentDetailListRes(next_page = next_page , data = comment_detail_list )
            



    except Exception as e:
        print(f"Error getting comment or reply data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()
