import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool


def db_get_search(search: str , page : int) -> FollowMemberListRes | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        limit = 15 
        offset = page * limit

        select_sql = """
        select DISTINCT member.name , member.account_id ,  member.avatar ,
        IFNULL(member_relation.relation_state, 'None') as relation_state
        FROM member_relation
        
        JOIN member ON member_relation.member_id = member.account_id
        
        WHERE member_relation.member_id like %s 
        
        LIMIT %s OFFSET %s
    """
        cursor.execute(select_sql, ('%'+search+'%' , limit , offset))
        search_member_data = cursor.fetchall()
        # print("beingFollow_data:",beingFollow_data)

        conut_sql = """
        SELECT COUNT(*) as total_fans
        FROM member_relation
        WHERE target_id = %s AND relation_state = 'Following'
    """
        cursor.execute(conut_sql, (search ,))
        total_fans = cursor.fetchone()['total_fans']
        # print("total_fans:",total_fans)

        has_more_data = len(search_member_data) > limit
        
        if has_more_data:
            search_member_data.pop()

        member_list = []
        for data in search_member_data:
            fans_member = FollowMember(
                user = MemberBase(
                    name = data['name'],
                    account_id = data['account_id'],
                    avatar = data['avatar']
                ),
                follow_state = data["relation_state"]
            )
            member_list.append(fans_member)
            
        connection.commit()
        next_page = page + 1 if has_more_data else None

        search_member_data = FollowMemberListRes(
            next_page = next_page , 
            fans_counts = total_fans ,
            data = member_list
        )
        
        return search_member_data
        
    except Exception as e:
        print(f"Error getting search member data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

