import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import DBManager

from db.get_member_data import *

DBManager.init_db_pool()

def db_get_search( search: str , page : int , member_id : str) -> FollowMemberListRes | None:
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        limit = 15 
        offset = page * limit

        select_sql = """
        SELECT 
            member.name, 
            member.account_id, 
            member.avatar, 
            IFNULL(member_relation.relation_state, 'None') AS relation_state
        FROM member
        LEFT JOIN member_relation ON member.account_id = member_relation.target_id AND member_relation.member_id = %s 
        WHERE 
            member.account_id LIKE %s 
        LIMIT %s OFFSET %s
    """
        cursor.execute(select_sql, (member_id, '%'+search+'%' , limit+1 , offset))
        search_member_data = cursor.fetchall()
        

        conut_sql = """
        SELECT COUNT(DISTINCT member.account_id) as total_members
        FROM member
        WHERE member.account_id LIKE %s 
    """
        cursor.execute(conut_sql, ('%' + search + '%',))
        total_members = cursor.fetchone()['total_members']

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

