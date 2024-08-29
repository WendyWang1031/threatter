import pymysql.cursors
from typing import Union, Optional
from model.model import *

from db.connection_pool import get_db_connection_pool
from db.check_relation import *

## 貼文
def db_get_post_data(query_sql: str, params: tuple, multiple: bool = True) -> Optional[Union[PostListRes, Post]]:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        cursor.execute(query_sql, params)
        
        if multiple:
            post_data = cursor.fetchall()
        else:
            post_data = cursor.fetchone()
        
        if not post_data:
            return None
        # print("post_data:",post_data)

        if multiple:
            limit = params[-2]  # 請看傳進來的參數為筆數上限
            page = int((params[-1])/(limit-1)) # 請看傳進來的參數為頁數
            return _generate_post_list(post_data, limit, page)
        else:
            return _generate_single_post(post_data)
        
    except Exception as e:
        print(f"Error getting post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()



def _generate_post_list(post_data, limit, page) -> PostListRes:
    limit = 15
    posts = []
    for data in post_data:
        post = _generate_post_object(data)
        posts.append(post)

    has_more_data = len(post_data) > limit
    
    if has_more_data:
        posts.pop()
    
    next_page = page + 1 if has_more_data else None
    return PostListRes(next_page = next_page, data = posts)

def _generate_single_post(post_data) -> Post:
    return _generate_post_object(post_data)

def _generate_post_object(data) -> Post:
    media = Media(
        images=data.get('image'),
        videos=data.get('video'),
        audios=data.get('audio')
    )

    created_at = data['created_at']
    if isinstance(created_at, str):
        created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

    parent_post = None
    if data.get('parent_id'):
        parent_post = ParentPostId(
            account_id=data.get('account_id'),
            post_id=data['parent_id']
        )

    return Post(
        post_id=data['content_id'],
        parent=parent_post,
        created_at=created_at,
        user=MemberBase(
            name=data['name'],
            account_id=data['account_id'],
            avatar=data['avatar']
        ),
        content=PostContent(
            text=data['text'],
            media=media,
        ),
        visibility=data['visibility'],
        like_state=bool(data.get('like_state', False)),
        counts=PostCounts(
            like_counts=int(data.get('like_counts', 0)),
            reply_counts=int(data.get('reply_counts', 0)),
            forward_counts=int(data.get('forward_counts', 0)),
        )
    )

## 留言
def db_get_data(query_sql: str, params: tuple, multiple: bool = True) -> Optional[Union[PostListRes, CommentDetailListRes]]:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        cursor.execute(query_sql, params)
        
        if multiple:
            data = cursor.fetchall()
        else:
            data = cursor.fetchone()
        
        if not data:
            return None

        if multiple:
            limit = params[-2]
            page = int((params[-1])/limit)
            return _generate_list(data, limit, page)
        
    except Exception as e:
        print(f"Error getting data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def generate_comment_object(data) -> CommentDetail:
    media = Media(
        images=data.get('image'),
        videos=data.get('video'),
        audios=data.get('audio')
    )

    created_at = data['created_at']
    if isinstance(created_at, str):
        created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

    comment = Comment(
        comment_id=data['content_id'],
        user=MemberBase(
            name=data['name'],
            account_id=data['account_id'],
            avatar=data['avatar']
        ),
        content=PostContent(
            text=data['text'],
            media=media,
        ),
        created_at=created_at,
        like_state=bool(data.get('like_state', False)),
        counts=PostCounts(
            like_counts=int(data.get('like_counts', 0)),
            reply_counts=int(data.get('reply_counts', 0)),
            forward_counts=int(data.get('forward_counts', 0)),
        )
    )
    return comment
   

def _generate_list(data, limit, page) -> CommentDetailListRes:
    comments = []
    for item in data:
        comment = generate_comment_object(item)
        comments.append(comment)
    
    has_more_data = len(data) > limit
    if has_more_data:
        data.pop()
    
    next_page = page + 1 if has_more_data else None
    return CommentDetailListRes(next_page=next_page, data=comments)



def get_replies_for_comment(comment_id: str) -> List[Comment]:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        replies_sql = """
            SELECT content.*, 
                   member.name, 
                   member.account_id, 
                   member.avatar 
            FROM content
            LEFT JOIN member ON content.member_id = member.account_id
            WHERE content.parent_id = %s AND content.content_type = 'Reply'
        """
        cursor.execute(replies_sql, (comment_id,))
        reply_data = cursor.fetchall()

        replies = []
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
                    like_counts=int(reply.get('like_counts', 0)),
                    reply_counts=int(reply.get('reply_counts', 0)),
                    forward_counts=int(reply.get('forward_counts', 0)),
                )
            )
            replies.append(reply_comment)
        
        return replies
    except Exception as e:
        print(f"Error getting replies: {e}")
        return []
    finally:
        cursor.close()
        connection.close()