from model.model import *
import pymysql.cursors
from typing import Any
from db.connection_pool import get_db_connection_pool
from datetime import datetime
from util.follow_util import *

def db_get_member_data(member_id : str , account_id : str ) -> MemberDetail | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """select name , account_id , avatar , self_intro , visibility 
            from member where account_id = %s
        """
        cursor.execute( sql , (account_id ,))
        member_data = cursor.fetchone()
        
        if not member_data:
            return None
        
        count_sql = """select Count(*) AS fans_count
            from member_relation
            where target_id = %s AND relation_state = %s
        """
        cursor.execute( count_sql , (account_id , RELATION_STATUS_FOLLOWING))
        fans_count_data = cursor.fetchone()
        fans_counts = fans_count_data['fans_count'] if fans_count_data else 0
        
        relation_sql = """
            SELECT relation_state
            FROM member_relation
            WHERE member_id = %s AND target_id = %s
        """
        cursor.execute(relation_sql, (member_id, account_id))
        relation_data = cursor.fetchone()
        follow_state = get_relation_status(relation_data)

        member_detail = MemberDetail(
            name = member_data['name'] , 
            account_id = member_data['account_id'] ,
            avatar = member_data.get('avatar', None) ,
            self_intro=member_data.get('self_intro', None) ,
            fans_counts = fans_counts ,
            visibility = member_data['visibility'],
            follow_state = follow_state
        )
        
        return member_detail
    
    except Exception as e:
        print(f"Error getting member data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def db_update_member_data(member_id : str  , member_data : MemberUpdateReq ) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        def validate(value):
            if value is None:
                return None
            return value.strip() or None
        
        data_tuple = (
            validate(member_data.name),
            validate(member_data.visibility),
            validate(member_data.self_intro),
            validate(member_data.avatar),
            member_id
        )
        
        sql = """update member 
            SET 
                name = COALESCE(NULLIF(%s, ''), name),
                visibility = COALESCE(NULLIF(%s, ''), visibility),
                self_intro = COALESCE(NULLIF(%s, ''), self_intro),
                avatar = COALESCE(NULLIF(%s, ''), avatar)
            where account_id = %s
        """
        cursor.execute(sql ,  data_tuple )
    
        connection.commit()
        
        return True
    
    except Exception as e:
        print(f"Error update Member Data: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()