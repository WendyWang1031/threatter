import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool



def db_follow_target(follow : FollowReq , member_id : str) -> FollowMember :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        if follow.follow == True :
            relation_state = "Following"
        else:
            relation_state = "None"

        check_sql = """
            SELECT * FROM member_relation
            WHERE member_id = %s AND target_id = %s
        """
        cursor.execute(check_sql, (member_id, follow.account_id))
        existing_relation = cursor.fetchone()

        if existing_relation:
            update_sql = """
                update member_relation 
                SET relation_state = %s
                where member_id = %s AND target_id = %s
            """
            cursor.execute(update_sql , (relation_state , member_id , follow.account_id ,))
            

        else:
            insert_sql = """
                INSERT INTO member_relation 
                (member_id, target_id, relation_state)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_sql , (member_id , follow.account_id, relation_state ,))
            

        user_sql = """
            SELECT member.name , member.account_id , member.avatar
            FROM member
            WHERE account_id = %s

        """
        cursor.execute(user_sql , (follow.account_id,))
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
        print(f"Error inserting follow: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()

def db_get_follow_target(member_id: Optional[str] , account_id : str , page : int) -> FollowMemberListRes | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        limit = 15 
        offset = page * limit

        select_sql = """
        select member.name , member.account_id ,  member.avatar ,
        member_relation.relation_state
        FROM member_relation
        
        JOIN member ON member_relation.target_id = member.account_id
        
        WHERE member_relation.member_id = %s 
        AND member_relation.relation_state = 'Following'
        LIMIT %s OFFSET %s
    """
        cursor.execute(select_sql, (account_id , limit , offset))
        following_data = cursor.fetchall()

        conut_sql = """
        SELECT COUNT(*) as total_following
        FROM member_relation
        WHERE member_id = %s AND relation_state = 'Following'
    """
        cursor.execute(conut_sql, (account_id ,))
        total_following = cursor.fetchone()['total_following']

        has_more_data = len(following_data) > limit
        
        if has_more_data:
            following_data.pop()

        following_list = []
        for data in following_data:
            follow_member = FollowMember(
                user = MemberBase(
                    name = data['name'],
                    account_id = data['account_id'],
                    avatar = data['avatar']
                ),
                follow_state = data["relation_state"]
            )
            following_list.append(follow_member)
            
        connection.commit()
        next_page = page + 1 if has_more_data else None

        following_target_data = FollowMemberListRes(
            next_page = next_page , 
            fans_counts = total_following ,
            data = following_list
        )
        
        return following_target_data
        
    except Exception as e:
        print(f"Error getting follow tagret data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

