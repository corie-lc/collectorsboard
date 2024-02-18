import mysql
import mysql.connector
from helpers.doadmin import get_database
from helpers import accounts


def follow_community(username, community_name, request):
    mydb = get_database()
    mycursor = mydb.cursor()

    if request == "unfollow":
        statmt = "DELETE FROM follow_community WHERE username = %s AND community = %s"
        mycursor.execute(statmt, (username, community_name))
        mydb.commit()
    else:
        mycursor.execute('''
    
                    INSERT INTO follow_community
                    VALUES (%s, %s);
    
                ''', (username, community_name))

        mydb.commit()


def is_following_community(username, community):
    mydb = get_database()
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM follow_community")

    for connection in cursor:
        if connection[0] == username and connection[1] == community:

            return True


    return False


def create_follow_connection(origin_user, end_user):
    mydb = get_database()

    mycursor = mydb.cursor()

    statmt = "DELETE FROM social_conn WHERE origin_user = %s AND end_user = %s AND request_type = %s"
    mycursor.execute(statmt, (origin_user, end_user, "FR"))

    mycursor.execute('''

            INSERT INTO social_conn
            VALUES (%s, %s, %s);

        ''', (origin_user, end_user, "F"))

    mydb.commit()


def stop_request(origin_user, end_user):
    mydb = get_database()

    mycursor = mydb.cursor()
    statmt = "DELETE FROM social_conn WHERE origin_user = %s AND end_user = %s AND request_type = %s"
    mycursor.execute(statmt, (origin_user, end_user, "FR"))

    mydb.commit()


def create_unfollow_connection(origin_user, end_user):
    mydb = get_database()

    mycursor = mydb.cursor()
    statmt = "DELETE FROM social_conn WHERE origin_user = %s AND end_user = %s AND request_type = %s"
    mycursor.execute(statmt, (origin_user, end_user, "F"))

    mydb.commit()


def is_follow(origin_user, end_user):
    mydb = get_database()

    cursor = mydb.cursor()
    #cursor.execute("SELECT * FROM social_conn where origin_user = " + origin_user + "and end_user = " + str(end_user))

    statmt_collection = "SELECT * FROM social_conn where origin_user = %s and end_user = %s"
    cursor.execute(statmt_collection, (origin_user, end_user))

    for connection in cursor:
        if connection[2] == "F":
            return True
        elif connection[2] == "FR":
            return "requested"
        elif connection[2] == "BL":
            return "blocked"

    return False


def is_follow_request(origin_user, end_user):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM social_conn")

    for connection in cursor:

        if connection[0] == origin_user and connection[1] == end_user and connection[2] == "FR":
            return True

    return False


def get_following(username):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM social_conn")

    users = []

    for connection in cursor:
        if connection[0] == username and connection[2] == "F":
            users.append(connection)

    return users


def get_followers(username):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM social_conn")

    users = []

    for connection in cursor:
        if connection[1] == username and connection[2] == "F":
            users.append(connection)

    return users


def request_follow_connection(origin_user, end_user):
    mydb = get_database()

    if accounts.get_user_info(end_user)[4] == "public":
        create_follow_connection(origin_user, end_user)
        return "Followed"
    else:

        mycursor = mydb.cursor()
        mycursor.execute('''

                INSERT INTO social_conn
                VALUES (%s, %s, %s);

            ''', (origin_user, end_user, "FR"))

        mydb.commit()
        return "Requested"


def get_follow_requests(username):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM social_conn")

    users = []

    for connection in cursor:
        if connection[1] == username and connection[2] == "FR":
            users.append(connection)

    return users


def count_following(username):
    return len(get_following(username))


def count_followers(username):
    return len(get_followers(username))
