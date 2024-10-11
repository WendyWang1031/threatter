import pymysql.cursors
from typing import Optional
from model.model import *

from db.connection_pool import DBManager
from db.check_relation import *
from db.get_member_data import *
from db.notification import *
from util.follow_util import *

DBManager.init_db_pool()

async def db_follow_target(follow : FollowReq , member_id : str) -> str :
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        check_existing_relation_sql = """
            SELECT relation_state FROM member_relation 
            WHERE member_id = %s AND target_id = %s
        """
        cursor.execute(check_existing_relation_sql, (member_id, follow.account_id))
        existing_relation = cursor.fetchone()
        relation_status = get_relation_status(existing_relation)
        if follow.follow is True and relation_status != RELATION_STATUS_NONE:
            return "", False
        
        if follow.follow is False and relation_status == RELATION_STATUS_NONE:
            return "", False
        
        visibility_sql = """
            SELECT visibility FROM member WHERE account_id = %s
        """
        cursor.execute(visibility_sql, (follow.account_id,))
        target_visibility = cursor.fetchone()["visibility"]
   
        follow_status = RELATION_STATUS_NONE
        if follow.follow is True :
            if target_visibility == VISIBILITY_PRIVATE:
                follow_status = RELATION_STATUS_PENDING
            else:
                follow_status = RELATION_STATUS_FOLLOWING
        else:
            follow_status = RELATION_STATUS_NONE

        # 插入或更新當前用戶和目標用戶的關係
        insert_update_relation_sql = """
            INSERT INTO member_relation (member_id, target_id, relation_state)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE relation_state = VALUES(relation_state)
        """
        cursor.execute(insert_update_relation_sql, (member_id, follow.account_id, follow_status))

        connection.commit()
        
        if follow.follow:
            await db_update_notification(
                    member_id, follow.account_id , None , None , 'Follow' , None  , follow_status)

        return follow_status ,  True 
    
    except Exception as e:
        print(f"Error inserting follow: {e}")
        connection.rollback() 
        return "", False
    finally:
        cursor.close()
        connection.close()

async def db_private_user_res_follow(followAns : FollowAns , account_id: str , member_id : str) :
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        check_existing_relation_sql = """
            SELECT relation_state FROM member_relation 
            WHERE member_id = %s AND target_id = %s
        """
        cursor.execute(check_existing_relation_sql, (followAns.account_id, member_id))
        existing_relation = cursor.fetchone()
        relation_status = get_relation_status(existing_relation)
        if relation_status != RELATION_STATUS_PENDING:
            return "", False

        follow_status = RELATION_STATUS_NONE
        if followAns.accept:
            follow_status = RELATION_STATUS_FOLLOWING
        else:
            follow_status = RELATION_STATUS_NONE
            
        update_sql = """
            update member_relation 
            SET relation_state = %s
            where member_id = %s AND target_id = %s 
        """
        cursor.execute(update_sql , (follow_status , account_id , member_id ,))
    
        check_existing_relation_sql = """
            SELECT relation_state FROM member_relation 
            WHERE member_id = %s AND target_id = %s
        """
        cursor.execute(check_existing_relation_sql, (member_id, followAns.account_id))
        existing_relation = cursor.fetchone()
        relation_status = get_relation_status(existing_relation)
        
        connection.commit()

        if followAns.accept:
            await db_update_notification(
                member_id, account_id, None, None, 'Follow', None, 'Accepted')
            await db_update_notification(
                account_id, member_id, None, None, 'Follow', None, 'Following')
        
        return relation_status , True
    
    except Exception as e:
        print(f"Error update private follow: {e}")
        connection.rollback() 
        return "", False
    finally:
        cursor.close()
        connection.close()


# 誰對我提出請求，正在等待我的回應
def db_get_pending_target(member_id : str , page : int) -> FollowMemberListRes | None:
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        
        limit = 15 
        offset = page * limit
     
        select_sql = """
            SELECT member.name, member.account_id, member.avatar, member_relation.relation_state
            FROM member_relation
            JOIN member ON member_relation.member_id = member.account_id
            WHERE member_relation.target_id = %s 
            AND member_relation.relation_state = %s 
            LIMIT %s OFFSET %s
        """
        cursor.execute(select_sql, (member_id, RELATION_STATUS_PENDING, limit+1, offset))
        follow_data = cursor.fetchall()

        count_sql = """
            SELECT COUNT(*) as total
            FROM member_relation
            WHERE target_id = %s 
            AND relation_state = %s
        """
        cursor.execute(count_sql, (member_id, RELATION_STATUS_PENDING))
        total_count = cursor.fetchone()['total']

        has_more_data = len(follow_data) > limit
        if has_more_data:
            follow_data.pop()

        return db_get_members_list_data(follow_data, total_count, page , has_more_data)
    
    except Exception as e:
        print(f"Error getting follow data details: {e}")
        return None
    finally:
        cursor.close()
        connection.close()



def db_get_follow_target(member_id : str ,account_id : str , page : int) -> FollowMemberListRes | None:
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:

        limit = 15 
        offset = page * limit
        
        select_sql = """
            SELECT member.name, member.account_id, member.avatar, 
            IFNULL(relation.relation_state, 'None') AS relation_state
            FROM member_relation
            
            JOIN member ON member_relation.target_id = member.account_id
            LEFT JOIN member_relation AS relation 
            ON relation.target_id = member.account_id 
            AND relation.member_id = %s
            
            WHERE member_relation.member_id = %s 
            AND member_relation.relation_state = %s
            LIMIT %s OFFSET %s
        """
        cursor.execute(select_sql, (member_id, account_id, RELATION_STATUS_FOLLOWING , limit+1, offset))
        follow_data = cursor.fetchall()

        count_sql = """
            SELECT COUNT(*) as total
            FROM member_relation
            WHERE member_id = %s AND relation_state = %s
        """
        cursor.execute(count_sql, (account_id, RELATION_STATUS_FOLLOWING))
        total_count = cursor.fetchone()['total']

        has_more_data = len(follow_data) > limit
        if has_more_data:
            follow_data.pop()

        return db_get_members_list_data(follow_data, total_count, page , has_more_data)
    
    except Exception as e:
        print(f"Error getting follow data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()



def db_get_follow_fans(member_id : str , account_id : str , page : int) -> FollowMemberListRes | None:
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        
        limit = 15 
        offset = page * limit
        
        select_sql = """
                SELECT member.name, member.account_id, member.avatar, 
                IFNULL(relation.relation_state, 'None') AS relation_state
                FROM member_relation
                
                JOIN member ON member_relation.member_id = member.account_id
                LEFT JOIN member_relation AS relation 
                ON relation.target_id = member.account_id 
                AND relation.member_id = %s
                
                WHERE member_relation.target_id = %s 
                AND member_relation.relation_state = %s
                LIMIT %s OFFSET %s
            """
        cursor.execute(select_sql, (member_id , account_id, RELATION_STATUS_FOLLOWING, limit+1, offset))
        follow_data = cursor.fetchall()

        count_sql = """
            SELECT COUNT(*) as total
            FROM member_relation
            WHERE target_id = %s AND relation_state = %s
        """
        cursor.execute(count_sql, (account_id, RELATION_STATUS_FOLLOWING))
        total_count = cursor.fetchone()['total']

        has_more_data = len(follow_data) > limit
        if has_more_data:
            follow_data.pop()

        return db_get_members_list_data(follow_data, total_count, page , has_more_data)
    
    except Exception as e:
        print(f"Error getting follow data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()