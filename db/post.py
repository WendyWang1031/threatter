from model.model import PostData
import pymysql.cursors
from typing import Optional
from db.connection_pool import get_db_connection_pool


def db_get_post_data() -> PostData | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        sql = "select * from test_post"
        cursor.execute( sql , )
        post_data = cursor.fetchall()
        connection.commit()
        
        if post_data:
            return post_data
        return None
        
    except Exception as e:
        print(f"Error getting post data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def db_update_post_data(post_data : PostData , image_url:str ) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        def validate(value: Optional[str]) -> Optional[str] :
            if value is None:
                return None
            return value.strip() or None
        
        content = validate(post_data.content)
        image_url = validate(image_url)
        
        sql = """
            INSERT INTO test_post (content, image_url)
            VALUES (%s, %s)
        """
        cursor.execute(sql , (content, image_url) )
    
        connection.commit()
        
        return True
    
    except Exception as e:
        print(f"Error inserting post Data: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()