import pymysql.cursors
from typing import Optional
from model.model import *
import json

from db.connection_pool import get_db_connection_pool
from db.check_relation import *
from db.get_member_data import *



def db_get_notification(member_id : str , page : int) -> NotificationRes | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        limit = 15 
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

        
        has_more_data = len(notification_data) > limit
        
        if has_more_data:
            notification_data.pop()
        # print("notification_data:",notification_data)

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

            
            event_data_dict = json.loads(data['event_data'])
            # print("event_data_dict:",event_data_dict)

            created_at = data['created_at']
            if isinstance(created_at, str):
                created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            else:
                created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')

            event_data = None
            
            media_data = Media(
                images = event_data_dict.get('image'),
                videos = event_data_dict.get('video'),
                audios = event_data_dict.get('audio')
            )

            notify_content = NotifyContent(
                post_url = event_data_dict['post_url'] ,
                content_id = event_data_dict['content_id'] ,
                text = event_data_dict['text'] ,
                media = media_data
            )

            if data['event_type'] == 'Like':
                event_data = LikeNotify(
                    parent = notify_content
                )
            # print("event_data:",event_data)
            print("created_at:",created_at)
            notify_info = NotifyInfo(
                user = follow_member,
                event_type = data['event_type'],
                is_read = data['is_read'],
                created_at = created_at,
                event_data = event_data
            )
            print("notify_info:",notify_info)

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






