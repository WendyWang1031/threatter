import pymysql.cursors
from typing import Optional
from model.model import *
import json

from db.connection_pool import get_db_connection_pool
from db.check_relation import *
from db.get_member_data import *
from service.redis import RedisManager



def db_get_notification(member_id : str , page : int, limit : int ) -> NotificationRes | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        offset = page * limit
     
        select_sql = """
            SELECT 
                notification.* , 

                target_member.name AS target_name, 
                target_member.account_id AS target_account_id, 
                target_member.avatar AS target_avatar,

                COALESCE(relation_state, 'None') AS follow_state
            FROM notification
            LEFT JOIN member AS target_member 
                ON notification.member_id = target_member.account_id
            LEFT JOIN member_relation 
                ON notification.member_id = member_relation.target_id 
                AND member_relation.member_id = %s
            WHERE notification.target_id = %s
            ORDER BY created_at DESC  
            LIMIT %s OFFSET %s
        """
    
        cursor.execute(select_sql, (member_id , member_id , limit+1, offset))
        notification_data = cursor.fetchall()
        # print("notification_data:",notification_data)

        
        has_more_data = len(notification_data) > limit
        
        if has_more_data:
            notification_data.pop()


        notification_list = []
        for data in notification_data:

            target_info = MemberBase(
                name = data['target_name'],
                account_id = data['target_account_id'],
                avatar = data['target_avatar']
            )

            follow_member = FollowMember(
                user = target_info,
                follow_state = data['follow_state']
            )
            
            event_data = None
            event_data_dict = None
            
            if data['event_data']:
                event_data_dict = json.loads(data['event_data'])

            # print("event_data_dict:",event_data_dict)

            created_at = data['created_at']
            if isinstance(created_at, str):
                created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            else:
                created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')

            

            
            
            if data['event_type'] == 'Like':
                event_data = LikeNotify(
                    parent=NotifyContent(
                        post_url=event_data_dict['parent']['post_url'],
                        content_id=event_data_dict['parent']['content_id'],
                        text=event_data_dict['parent'].get('text'),
                        media=Media(
                            images=event_data_dict['parent'].get('image'),
                            videos=event_data_dict['parent'].get('video'),
                            audios=event_data_dict['parent'].get('audio')
                        )
                    )
                )
                # print("event_data:",event_data)
            
            elif data['event_type'] == 'Reply':
                event_data = ContentReplyNotify(
                    parent=NotifyContent(
                        post_url=event_data_dict['parent']['post_url'],
                        content_id=event_data_dict['parent']['content_id'],
                        text=event_data_dict['parent'].get('text'),
                        media=Media(
                            images=event_data_dict['parent'].get('image'),
                            videos=event_data_dict['parent'].get('video'),
                            audios=event_data_dict['parent'].get('audio')
                        )
                    ),
                    children=NotifyContent(
                        post_url=event_data_dict['children']['post_url'],
                        content_id=event_data_dict['children']['content_id'],
                        text=event_data_dict['children'].get('text'),
                        media=Media(
                            images=event_data_dict['children'].get('image'),
                            videos=event_data_dict['children'].get('video'),
                            audios=event_data_dict['children'].get('audio')
                        )
                    )
                )
            elif data['event_type'] == 'Follow':
                event_data = NotifyMember(
                    follow_type= 'Follow',
                    status=event_data_dict.get('status')
                )
            # print("event_data:",event_data)
            # print("created_at:",created_at)
            notify_info = NotifyInfo(
                user = follow_member,
                event_type = data['event_type'],
                is_read = data['is_read'],
                created_at = created_at,
                event_data = event_data
            )
            # print("notify_info:",notify_info)

            notification_list.append(notify_info)
       
        
        next_page = page + 1 if has_more_data else None

        notification_result = NotificationRes(
            next_page = next_page, 
            data = notification_list
        )

        connection.commit()

        return notification_result
    
    except Exception as e:
        print(f"Error getting notification data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()






async def db_update_notification(
        member_id: str, 
        account_id: str, 
        post_id: str, 
        content_id: str, 
        content_type: str,
        parent_id: Optional[str] = None,
        is_private_accept: Optional[bool] = False,
        follow_status: Optional[str] = "Pending"):
    

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
            AND event_type = %s 
            AND JSON_UNQUOTE(JSON_EXTRACT(event_data, '$.content_id')) = %s 
            AND is_read = FALSE
        """
        cursor.execute(check_notification_sql, 
                       (member_id, account_id, content_type , content_id))
        existing_notification = cursor.fetchone()
        
        
        # 如果已經存在就不插入通知進去表
        if existing_notification:
            return
        

        if content_type == 'Reply':
            # 如果有提供 parent_id 表示是回覆留言，如果沒有就是回覆貼文
            parent_id = parent_id or post_id
            
            parent_sql = """
                SELECT member_id , text, image, video, audio
                FROM content
                WHERE content_id = %s
            """
            cursor.execute(parent_sql, (parent_id,))
            parent_content_data = cursor.fetchone()
            # print("parent_content_data:",parent_content_data)
            
            # 如果母內容和子內容的人是相同，跳過
            if parent_content_data and parent_content_data['member_id'] == member_id:
                return

            child_sql = """
                SELECT text, image, video, audio
                FROM content
                WHERE content_id = %s
            """
            cursor.execute(child_sql, (content_id,))
            child_content_data = cursor.fetchone()
            # print("child_content_data:",child_content_data)
            

            event_data_obj = ContentReplyNotify(
                parent=NotifyContent(
                    post_url=f"/member/{account_id}/post/{post_id}",
                    content_id=post_id,
                    text=parent_content_data['text'] if parent_content_data else None,
                    media=Media(
                        images=parent_content_data.get('image') if parent_content_data else None,
                        videos=parent_content_data.get('video') if parent_content_data else None,
                        audios=parent_content_data.get('audio') if parent_content_data else None
                    )
                ),
                children=NotifyContent(
                    post_url=f"/member/{account_id}/post/{post_id}",
                    content_id=content_id,
                    text=child_content_data['text'] if child_content_data else None,
                    media=Media(
                        images=child_content_data.get('image') if child_content_data else None,
                        videos=child_content_data.get('video') if child_content_data else None,
                        audios=child_content_data.get('audio') if child_content_data else None
                    )
                )
            )
            event_data_json = event_data_obj.model_dump_json()
        
        elif content_type == 'Like':
            
            content_sql = """
                SELECT text, image, video, audio
                FROM content
                WHERE content_id = %s
            """
            cursor.execute(content_sql, (content_id,))
            content_data = cursor.fetchone()

            if content_data:
                event_data_obj = LikeNotify(
                    parent=NotifyContent(
                        post_url=f"/member/{account_id}/post/{post_id}",
                        content_id=content_id,
                        text=content_data['text'] if content_data else None,
                        media=Media(
                            images=content_data.get('image') if content_data else None,
                            videos=content_data.get('video') if content_data else None,
                            audios=content_data.get('audio') if content_data else None
                        )
                    )
                )
                event_data_json = event_data_obj.model_dump_json()
            else:
                event_data_json = None
        
            # print("event_data_json:",event_data_json)

        elif content_type == 'Follow':
            if is_private_accept:
                # 私人用戶接受追蹤請求
                event_data_obj = {
                    "status": follow_status 
                }
            else:
                # 普通的追蹤請求
                event_data_obj = {
                    "status": follow_status,
                }
            event_data_json = json.dumps(event_data_obj)

        # 插入通知
        update_notification_sql = """
            INSERT INTO notification(
                member_id, target_id, event_type, event_data, is_read
            )
            VALUES(
                %s, %s, %s, %s, False
            )
        """
        cursor.execute(update_notification_sql, (member_id, account_id, content_type, event_data_json))

        connection.commit()

        # 將通知發佈到redis
        notification_res = db_get_notification(account_id, page=0, limit=1)
        if notification_res:
            for notification in notification_res.data:
                # print("notification:",notification)
                await RedisManager.publish_notification(notification, account_id)



    except Exception as e:
        print(f"Error updating notification: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


def db_post_read_notification(member_id: str, current_time: datetime):
    connection = get_db_connection_pool()
    cursor = connection.cursor()
    try:
        # print("db current_time:",current_time)
        # print("db current_user:",member_id)

        update_sql = """
            UPDATE notification 
            SET is_read = TRUE
            WHERE target_id = %s AND created_at <= %s AND is_read = FALSE
        """
        cursor.execute(update_sql, (member_id, current_time))

        connection.commit()
        return {"message": "All notifications marked as read."}
    except Exception as e:
        print(f"Error updating READED notification: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()