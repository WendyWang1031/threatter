import pymysql.cursors
from typing import Optional
from model.model import *

from db.connection_pool import get_db_connection_pool
from db.check_relation import *
from db.get_member_data import *

RELATION_STATUS_PENDING = "Pending"

def db_follow_target(follow : FollowReq , member_id : str) -> FollowMember :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        visibility_sql = """
            SELECT visibility FROM member WHERE account_id = %s
        """
        cursor.execute(visibility_sql, (follow.account_id,))
        target_visibility = cursor.fetchone()["visibility"]

        if follow.follow == True :
            if target_visibility == "Private":
                relation_state = RELATION_STATUS_PENDING
                target_relation_state = "PendingBeingFollow"
            else:
                relation_state = "Following"
                target_relation_state = "BeingFollow"
        else:
            relation_state = "None"
            target_relation_state = "None"

        # 插入或更新當前用戶和目標用戶的關係
        insert_update_relation_sql = """
            INSERT INTO member_relation (member_id, target_id, relation_state)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE relation_state = VALUES(relation_state)
        """
        cursor.execute(insert_update_relation_sql, (member_id, follow.account_id, relation_state))

        # 插入或更新目標用戶和當前用戶的關係
        insert_update_target_relation_sql = """
            INSERT INTO member_relation (member_id, target_id, relation_state)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE relation_state = VALUES(relation_state)
        """
        cursor.execute(insert_update_target_relation_sql, (follow.account_id, member_id, target_relation_state))

        connection.commit()
        return relation_state ,  True 
    
    except Exception as e:
        print(f"Error inserting follow: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

def db_private_user_res_follow(followAns : FollowAns , account_id: str , member_id : str) -> FollowMember :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        if followAns.accept:
            relation_state = "Following"
            target_relation_state = "BeingFollow"
        else:
            relation_state = "None"
            target_relation_state = "None"
            
        # 插入或更新當前用戶和目標用戶的關係
        update_sql = """
            update member_relation 
            SET relation_state = %s
            where member_id = %s AND target_id = %s 
        """
        cursor.execute(update_sql , (relation_state , account_id , member_id ,))
      

        # 插入或更新目標用戶和當前用戶的關係
        update_target_sql = """
            INSERT INTO member_relation (member_id, target_id, relation_state)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE relation_state = %s
        """
        cursor.execute(update_target_sql, (member_id, account_id, target_relation_state, target_relation_state))
           
        connection.commit()
        return relation_state , True
    
    except Exception as e:
        print(f"Error update private follow: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()



def db_get_pending_target(member_id : str , page : int) -> FollowMemberListRes | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        limit = 15 
        offset = page * limit
     
        select_sql = """
            SELECT member.name, member.account_id, member.avatar, member_relation.relation_state
            FROM member_relation
            JOIN member ON member_relation.target_id = member.account_id
            WHERE member_relation.member_id = %s 
            AND member_relation.relation_state = 'PendingBeingFollow'
            LIMIT %s OFFSET %s
        """
        count_sql = """
            SELECT COUNT(*) as total
            FROM member_relation
            WHERE target_id = %s 
            AND relation_state = 'Pending'
        """
        cursor.execute(select_sql, (member_id , limit+1, offset))
        follow_data = cursor.fetchall()
        # print("follow_data:",follow_data)

        cursor.execute(count_sql, (member_id,))
        total_count = cursor.fetchone()['total']

        has_more_data = len(follow_data) > limit
        
        if has_more_data:
            follow_data.pop()

        connection.commit()

        return db_get_members_list_data(follow_data, total_count, page , has_more_data)
    
    except Exception as e:
        print(f"Error getting follow data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()



def db_get_follow_target(member_id : str ,account_id : str , page : int) -> FollowMemberListRes | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
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
            AND member_relation.relation_state = 'Following'
            LIMIT %s OFFSET %s
        """
        count_sql = """
            SELECT COUNT(*) as total
            FROM member_relation
            WHERE member_id = %s AND relation_state = 'Following'
        """
        cursor.execute(select_sql, (member_id , account_id , limit+1, offset))
        follow_data = cursor.fetchall()

        cursor.execute(count_sql, (account_id,))
        total_count = cursor.fetchone()['total']

        has_more_data = len(follow_data) > limit
        
        if has_more_data:
            follow_data.pop()

        connection.commit()

        return db_get_members_list_data(follow_data, total_count, page , has_more_data)
    
    except Exception as e:
        print(f"Error getting follow data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()



def db_get_follow_fans(member_id : str , account_id : str , page : int) -> FollowMemberListRes | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        limit = 15 
        offset = page * limit

        
        select_sql = """
                SELECT member.name, member.account_id, member.avatar, 
                IFNULL(relation.relation_state, 'None') AS relation_state
                FROM member_relation
                
                JOIN member ON member_relation.member_id = member.account_id
                LEFT JOIN member_relation AS relation 
                    ON relation.member_id = %s 
                   AND relation.target_id = member.account_id 
                
                WHERE member_relation.target_id = %s 
                AND member_relation.relation_state = 'Following'
                LIMIT %s OFFSET %s
            """
        count_sql = """
            SELECT COUNT(*) as total
            FROM member_relation
            WHERE target_id = %s AND relation_state = 'Following'
        """
        cursor.execute(select_sql, (member_id , account_id, limit+1, offset))
        follow_data = cursor.fetchall()
        print("follow_data:",follow_data)

        cursor.execute(count_sql, (account_id,))
        total_count = cursor.fetchone()['total']

        has_more_data = len(follow_data) > limit
        
        if has_more_data:
            follow_data.pop()

        connection.commit()

        return db_get_members_list_data(follow_data, total_count, page , has_more_data)
    
    except Exception as e:
        print(f"Error getting follow data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()




    # connection = get_db_connection_pool()
    # cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # try:
    #     connection.begin()

    #     user_sql = """
    #         SELECT member.name , member.account_id , member.avatar
    #         FROM member
    #         WHERE account_id = %s

    #     """
    #     cursor.execute(user_sql , (account_id,))
    #     member = cursor.fetchone()

        
    #     follow_member = FollowMember(
    #         user = MemberBase(
    #                 name = member['name'],
    #                 account_id = member['account_id'],
    #                 avatar = member['avatar']
    #             ),
    #         follow_state = relation_state
    #     )


    #     connection.commit()
        
    #     return follow_member
    
    # except Exception as e:
    #     print(f"Error getting member single data details: {e}")
    #     connection.rollback() 
    #     return False
    # finally:
    #     cursor.close()
    #     connection.close()