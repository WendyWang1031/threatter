import pymysql.cursors
from typing import Optional
from model.model import *
from db.connection_pool import get_db_connection_pool



def db_follow_target(follow : FollowReq , member_id : str) -> FollowMember :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        visibility_sql = """
            SELECT visibility FROM member WHERE account_id = %s
        """
        cursor.execute(visibility_sql, (follow.account_id,))
        target_visibility = cursor.fetchone()["visibility"]

        if follow.follow == True :
            if target_visibility == "Private":
                relation_state = "Pending"
                target_relation_state = "Pending"
            else:
                relation_state = "Following"
                target_relation_state = "BeingFollow"
        else:
            relation_state = "None"
            target_relation_state = "None"

        check_relation_sql = """
            SELECT * FROM member_relation
            WHERE member_id = %s AND target_id = %s
        """
        cursor.execute(check_relation_sql, (member_id, follow.account_id))
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
            
    
        ## ”目標為本人“與對方的關係


        target_check_sql = """
            SELECT * FROM member_relation
            WHERE member_id = %s AND target_id = %s   
        """
        cursor.execute(target_check_sql, (follow.account_id, member_id))
        existing_target_relation = cursor.fetchone()

        if existing_target_relation :
            update_target_sql = """
                update member_relation 
                SET relation_state = %s
                where member_id = %s AND target_id = %s
            """
            cursor.execute(update_target_sql , (target_relation_state , follow.account_id , member_id ,))
            

        else:
            insert_target_sql = """
                INSERT INTO member_relation 
                (member_id, target_id, relation_state)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_target_sql , (follow.account_id , member_id , target_relation_state ,))
            

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

def db_private_follow(followAns : FollowAns , account_id: str , member_id : str) -> FollowMember :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()

        if followAns.accept is True :
            relation_state = "Following"
        else:
            relation_state = "None"
            

        check_sql = """
            SELECT * FROM member_relation
            WHERE member_id = %s AND target_id = %s
            AND relation_state = "Pending"
        """
        cursor.execute(check_sql, (account_id, member_id))
        existing_pending_relation = cursor.fetchone()

        if existing_pending_relation:
            update_sql = """
                update member_relation 
                SET relation_state = %s
                where member_id = %s AND target_id = %s
            """
            cursor.execute(update_sql , (relation_state , account_id , member_id ,))
            

            if relation_state == "Following":
                check_being_follow_sql ="""
                    SELECT relation_state FROM member_relation
                    where member_id = %s AND target_id = %s            
                """ 
                cursor.execute(check_being_follow_sql , (member_id , account_id ,))
                existing_relation = cursor.fetchone()

                if existing_relation:
                    if existing_relation['relation_state'] != 'BeingFollow':
                        update_being_follow_sql ="""
                        UPDATE member_relation
                        SET relation_state = "BeingFollow"
                        WHERE member_id = %s AND target_id = %s            
                """
                    cursor.execute(update_being_follow_sql , (member_id , account_id ,)) 
                else:
                    insert_being_follow_sql = """
                        INSERT into member_relation
                        (member_id , target_id , relation_state)
                        VALUES (%s , %s , 'BeingFollow')
                """
                    cursor.execute(insert_being_follow_sql , (member_id , account_id ,)) 
        else:
            print(f"No pending follow request found for {account_id} to {member_id}")
            

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
        print(f"Error update private follow: {e}")
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
        print("check_relation:",check_relation)

        if check_relation is None:
                check_relation_state = "None"
        else:
                check_relation_state = check_relation["relation_state"]

        if check_relation_state in ["None", "Pending"] and target_visibility == "Private":
                return None
        
        ## 顯示以下追蹤對象

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


def db_get_follow_fans(member_id: Optional[str] , account_id : str , page : int) -> FollowMemberListRes | None:
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
        
        JOIN member ON member_relation.member_id = member.account_id
        
        WHERE member_relation.target_id = %s 
        AND member_relation.relation_state = 'Following'
        LIMIT %s OFFSET %s
    """
        cursor.execute(select_sql, (account_id , limit , offset))
        beingFollow_data = cursor.fetchall()
        # print("beingFollow_data:",beingFollow_data)

        conut_sql = """
        SELECT COUNT(*) as total_fans
        FROM member_relation
        WHERE target_id = %s AND relation_state = 'Following'
    """
        cursor.execute(conut_sql, (account_id ,))
        total_fans = cursor.fetchone()['total_fans']
        # print("total_fans:",total_fans)

        has_more_data = len(beingFollow_data) > limit
        
        if has_more_data:
            beingFollow_data.pop()

        fans_list = []
        for data in beingFollow_data:
            fans_member = FollowMember(
                user = MemberBase(
                    name = data['name'],
                    account_id = data['account_id'],
                    avatar = data['avatar']
                ),
                follow_state = data["relation_state"]
            )
            fans_list.append(fans_member)
            
        connection.commit()
        next_page = page + 1 if has_more_data else None

        fans_data = FollowMemberListRes(
            next_page = next_page , 
            fans_counts = total_fans ,
            data = fans_list
        )
        
        return fans_data
        
    except Exception as e:
        print(f"Error getting follow tagret data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

