import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool


def db_check_member_target_relation(member_id: Optional[str] , account_id : str ):
        connection = get_db_connection_pool()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:
            ## 確認未登入、私人對象用戶與本人的關係
            visibility_sql = """
                SELECT visibility FROM member WHERE account_id = %s
            """
            cursor.execute(visibility_sql, (account_id,))
            target_visibility = cursor.fetchone()["visibility"]

            if member_id is None and target_visibility == "Private":
                return None
            

            check_relation_sql = """
            SELECT relation_state 
            FROM member_relation
            WHERE member_id = %s AND target_id = %s
            """
            cursor.execute(check_relation_sql, (member_id, account_id))
            check_relation = cursor.fetchone()
            # print("check_relation:",check_relation)

            if check_relation is None:
                    check_relation_state = "None"
            else:
                    check_relation_state = check_relation["relation_state"]

            if check_relation_state in ["None", "Pending"] and target_visibility == "Private":
                    return None
            
            return True

        except Exception as e:
            print(f"Error getting follow and target relationship details: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

def has_permission_to_view(member_id: Optional[str], post_visibility: str, relation_state: Optional[str]) -> bool:
    # 如果貼文內容是公開，任何人都能觀看
    if post_visibility == "Public":
        return True
    
    # 如果未登入，且貼文內容是私人，就不能觀看
    if member_id is None and post_visibility == "Private":
        return False
    
    # 貼文內容是私人，關係是沒關係、確認中，就不能觀看
    if post_visibility == "Private" and relation_state in ["None", "Pending"]:
        return False
    
    return True