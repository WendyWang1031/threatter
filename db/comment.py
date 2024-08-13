import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool
from db.re_post_data import *
from service.common import *


def db_create_comment_data(comment_data : CommentReq , post_id : str , member_id : str) -> bool :
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
        # print("comment_data:",comment_data)

        if not comment_data:
            return "No Comment Data" ,  None
        
        # # 處理留言列表，準備回覆留言的字典
        # comment_detail_list = []
        # replies_map = {}
        # # print("comment_data:",comment_data)
        # for data in comment_data:
        #     if data['content_type'] == 'Comment':
        #         comment = generate_comment_object(data)
                
        #         comment_detail_list.append(CommentDetail(comment=comment, replies=[]))
        #     elif data['content_type'] == 'Reply':
        #         parent_id = data['parent_id']
        #         # print("parent_id:",parent_id)
        #         if parent_id not in replies_map:
        #             replies_map[parent_id] = []
        #         replies_map[parent_id].append(generate_comment_object(data))
        
        # # print("replies_map:",replies_map)
        # # 將回覆留言映射到相對應的留言
        # for comment_detail in comment_detail_list:
        #     comment_id = comment_detail.comment.comment_id
        #     if comment_id in replies_map:
        #         comment_detail.replies = replies_map[comment_id]
        # # print("comment_detail_list:",comment_detail_list)
        # connection.commit()
        
        # has_more_data = len(comment_data) > limit
        
        # if has_more_data:
        #     comment_data.pop()

        # next_page = page + 1 if has_more_data else None

        # return "Success" , CommentDetailListRes(next_page=next_page, data=comment_detail_list)

        
        
        has_more_data = len(comment_data) > limit
        
        if has_more_data :
            comment_data.pop()

        comment_detail_list = []
        for data in comment_data:


        
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
                    like_counts=int(data.get('like_counts', 0)),
                    reply_counts=int(data.get('reply_counts', 0)),
                    forward_counts=int(data.get('forward_counts', 0)),
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
        
        


    except Exception as e:
        print(f"Error getting comment or reply data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()
