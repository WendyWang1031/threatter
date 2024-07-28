import bcrypt
import uuid
import pymysql.cursors
from model.model_user import *
from typing import Any
from db.connection_pool import get_db_connection_pool


def db_insert_new_user(user_register_req : UserRegisterReq) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()

        sql = "insert into member (name , account_id , email , password) values (%s , %s , %s , %s)"
        cursor.execute(sql ,(user_register_req.account_id,  user_register_req.name , user_register_req.email , user_register_req.password))
        
        connection.commit()

        if cursor.rowcount>0:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error inserting new user: {e}") 
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def db_check_user_accountId_email_exists(check_exist : UserCheckExistReq) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()

        sql = "select account_id , email  from member where account_id = %s and email = %s"
        cursor.execute(sql , (check_exist.account_id , check_exist.email,))
        user_account_email = cursor.fetchone()

        connection.commit()

    except Exception as e:
        print(f"Error retrieving username: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()
    
    return user_account_email is not None   


def db_check_accountId_password(user_login : UserPutReq ) -> dict [str, Any] | bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        sql = "select  name , account_id , password from member where account_id = %s "
        cursor.execute(sql , ( user_login.account_id , ))
        user_record = cursor.fetchone()
        
        connection.commit()

        stored_password = user_record['password']
        if user_record :
            if bcrypt.checkpw(user_login.password.encode('utf-8') , stored_password.encode('utf-8')):
                user_info = {}
                for key in user_record:
                    if key!= 'password':
                        user_info[key] =  user_record[key]
                return user_info
        return False
        
    
    except Exception as e:
        print(f"Error checking user , wrong email or password : {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()