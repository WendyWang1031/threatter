import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import DBManager
from util.follow_util import *

DBManager.init_db_pool()

def db_check_existence_and_relations(account_id: str, 
                                     post_id: Optional[str] = None, 
                                     comment_id: Optional[str] = None, 
                                     member_id: Optional[str] = None) -> dict:
    connection = DBManager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        # 批次查詢
        query_parts = []
        params = []

        # 檢查用戶
        query_parts.append("""
            (SELECT EXISTS(SELECT 1 FROM member WHERE account_id = %s)) AS user_exists
        """)
        params.append(account_id)

        if post_id:
            # 檢查貼文
            query_parts.append("""
                (SELECT EXISTS(SELECT 1 FROM content WHERE member_id = %s AND content_id = %s)) AS post_exists
            """)
            params.extend([account_id, post_id])

        if comment_id:
            # 檢查留言
            if comment_id.startswith("C"):
                query_parts.append("""
                    (SELECT EXISTS(SELECT 1 FROM content WHERE parent_id = %s AND content_id = %s)) AS comment_exists
                """)
                params.extend([post_id, comment_id])
            else:
                query_parts.append("""
                    (SELECT EXISTS(SELECT 1 
                                   FROM content AS reply
                                   JOIN content AS comment ON reply.parent_id = comment.content_id
                                   WHERE comment.parent_id = %s AND reply.content_id = %s)) AS reply_exists
                """)
                params.extend([post_id, comment_id])

        if member_id:
            # 檢查關係
            query_parts.append("""
                (SELECT relation_state 
                 FROM member_relation 
                 WHERE member_id = %s AND target_id = %s) AS relation_state
            """)
            params.extend([member_id, account_id])

            # 檢查用戶的觀賞隱私權限
            query_parts.append("""
                (SELECT visibility 
                 FROM member 
                 WHERE account_id = %s) AS target_visibility
            """)
            params.append(account_id)

        # 拼接 sql 語句
        final_query = "SELECT " + ", ".join(query_parts)
        cursor.execute(final_query, tuple(params))
        result = cursor.fetchone()

        
        return result
    
    except Exception as e:
        print(f"Error in bulk existence and relation check: {e}")
        connection.rollback()
        return {}
    finally:
        cursor.close()
        connection.close()

def db_check_target_exist_or_not(account_id : str ):
        connection = DBManager.get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:

            check_exist_sql = """
            SELECT *
            FROM member
            WHERE account_id = %s 
            """
            cursor.execute(check_exist_sql, ( account_id))
            check_exist = cursor.fetchone()
            # print("check_exist:",check_exist)

            if check_exist :
                 return True
            else:
                 return False
    
        except Exception as e:
            print(f"Error getting follow and target relationship details: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()


def db_check_each_other_relation(member_id: str , account_id : str ):
        connection = DBManager.get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:

            check_relation_sql = """
            SELECT relation_state 
            FROM member_relation
            WHERE member_id = %s AND target_id = %s
            """
            cursor.execute(check_relation_sql, (member_id, account_id))
            check_relation = cursor.fetchone()

            return get_relation_status(check_relation)

        except Exception as e:
            print(f"Error getting each other relationship details: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

def db_check_member_target_relation(member_id: Optional[str] , account_id : str ):
        connection = DBManager.get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        try:
            if member_id == account_id:
                 return True
            
            ## 確認未登入、私人對象用戶與本人的關係
            visibility_sql = """
                SELECT visibility FROM member WHERE account_id = %s
            """
            cursor.execute(visibility_sql, (account_id,))
            target_visibility = cursor.fetchone()["visibility"]

            if member_id is None and target_visibility == "Private":
                return False
            
            check_relation_sql = """
            SELECT relation_state 
            FROM member_relation
            WHERE member_id = %s AND target_id = %s
            """
            cursor.execute(check_relation_sql, (member_id, account_id))
            check_relation = cursor.fetchone()

            relation_status = get_relation_status(check_relation)
            return get_visibility(target_visibility, relation_status)

        except Exception as e:
            print(f"Error getting follow and target relationship details: {e}")
            return False
        finally:
            cursor.close()
            connection.close()