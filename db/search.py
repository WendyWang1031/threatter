import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool

from db.get_member_data import *


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
        SELECT COUNT(DISTINCT member.account_id) as total_members
        FROM member
        WHERE member.account_id LIKE %s
    """
        cursor.execute(conut_sql, ('%' + search + '%',))
        total_members = cursor.fetchone()['total_members']
        # print("total_fans:",total_fans)

        has_more_data = len(search_member_data) > limit
        
        if has_more_data:
            search_member_data.pop()
            
        connection.commit()
        return db_get_members_list_data(search_member_data, total_members, page , has_more_data)
        
        
    except Exception as e:
        print(f"Error getting search member data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

