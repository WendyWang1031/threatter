import pymysql.cursors
from typing import Optional
from model.model import *

from db.connection_pool import DBManager
from db.check_relation import *

DBManager.init_db_pool()

def db_get_members_list_data(member_data , total_count , page : int , has_more_data: bool) -> FollowMemberListRes | None:
    
    try:

        follow_list = []
        for data in member_data:
            follow_member = FollowMember(
                user = MemberBase(
                    name = data['name'],
                    account_id = data['account_id'],
                    avatar = data['avatar']
                ),
                follow_state = data["relation_state"]
            )
            follow_list.append(follow_member)
            
        
        next_page = page + 1 if has_more_data else None

        follow_result = FollowMemberListRes(
            next_page = next_page, 
            fans_counts = total_count,
            data = follow_list
        )
        
        return follow_result
        
    except Exception as e:
        print(f"Error getting member list data details: {e}")
        return None

       


def db_get_member_single_data(account_id: str , relation_state) -> FollowMember :
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        user_sql = """
            SELECT member.name , member.account_id , member.avatar
            FROM member
            WHERE account_id = %s

        """
        cursor.execute(user_sql , (account_id,))
        member = cursor.fetchone()

        
        follow_member = FollowMember(
            user = MemberBase(
                    name = member['name'],
                    account_id = member['account_id'],
                    avatar = member['avatar']
                ),
            follow_state = relation_state
        )


        connection.commit()
        
        return follow_member
    
    except Exception as e:
        print(f"Error getting member single data details: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()