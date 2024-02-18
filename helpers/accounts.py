import boto3
import mysql
import mysql.connector
from helpers.doadmin import get_database, create_password, verify_password
from helpers import posts_entrys
from helpers import doadmin


def get_user_email(username):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")

    for user in cursor:
        if user[0] == username:
            return user[1]

    return False


def change_username(email, new):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
            UPDATE users
            SET username=%s
            WHERE email=%s
            """, (new, email))


    
    

    mydb.commit()



    return True


def change_password(email, new):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
            UPDATE users
            SET password=%s
            WHERE email=%s
            """, (doadmin.create_password(new), email))

    mydb.commit()
    return True


def change_bio(username, bio):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
            UPDATE users
            SET bio=%s
            WHERE username=%s
            """, (bio, username))

    mydb.commit()
    return True


def login(username, password):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")

    for user in cursor:
        print(username)
        print(password)
        if user[0] == username and verify_password(user[2], password, username):
            return True
        elif user[1] == username and verify_password(user[2], password, username):
            return True

    return False

def does_username_exist(username):
    mydb = get_database()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users")

    for user in mycursor:
        if user[0] == username:
            return True

    return False

def does_email_exist(email):
    mydb = get_database()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users")

    for user in mycursor:
        if user[1] == email:
            return True

    return False


def create_account(username, password, email):
    mydb = get_database()
    mycursor = mydb.cursor()

    if does_username_exist(username) == True:
        return "used_username"
    elif does_email_exist(email) == True:
        return "used_email"
    elif "@" in username:
        return "invalid"
    else:

        bio = "new account!"

        mycursor.execute('''
            
            INSERT INTO users
            VALUES (%s, %s, %s, %s, %s, %s);
        
        ''', (username, email, create_password(password), bio, "public", "https://photo-storage-collecdb.nyc3.cdn.digitaloceanspaces.com/avatars/2.jpg"))

        mydb.commit()

        return True


def get_user_info(username):
    mydb = get_database()

    cursor = mydb.cursor()
    #cursor.execute("SELECT * FROM users where username")

    statmt = "select * from users where username = %s or email = %s"
    cursor.execute(statmt, (username, username))

    for user in cursor:
        if user[0] == username:
            return user
        elif user[1] == username:
            return user
        
    print("False")
    return "False"


def get_all_users():
    users = []
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")

    for user in cursor:
        users.append(user)

    return users



def is_account_public(username):
    if get_user_info(username)[4] == "public":
        return True
    else:
        return False


def change_account_public(username, string):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
            UPDATE users
            SET public=%s
            WHERE username=%s
            """, (string, username))

    for item in posts_entrys.get_all_posts():
        mycursor.execute("""
            UPDATE posts
            SET user_public=%s
            WHERE username=%s
            """, (string, username))

    mydb.commit()
    return True


def if_account_public(username):
    if get_user_info(username)[4] == "public":
        return True
    else:
        return False


def get_followed_communties(username):
    mydb = get_database()

    cursor = mydb.cursor()
    
    statmt_collection = "SELECT * FROM follow_community where username = %s"
    cursor.execute(statmt_collection, (str(username),))

    followed = []

    for community in cursor:
        if community[0] == username:
            followed.append(community[1])

    return followed


from boto3 import session, Session, s3


def get_avatars():
    links = []
    i = 0
    template = 'https://photo-storage-collecdb.nyc3.cdn.digitaloceanspaces.com/avatars/'
    while i < 3:
        i += 1
        links.append(template + str(i) + ".jpg")

    return links


def change_avatar(item, username):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
                UPDATE users
                SET avatar=%s
                WHERE username=%s
                """, (item, username))

    mydb.commit()
    return True


def get_user_avatar(username):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")

    for user in cursor:
        if user[0] == username:
            return user[5]

# -------------------------------- membership stuff lol
        
# tiers are free, essentail and plus
        
def get_user_mem_tier(username):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM membership_services")

    for item in cursor:
        if item[0] == username:
            return item[2]
        
    return "free"


def get_user_autoprice_count(username):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM membership_services")

    for item in cursor:
        if item[0] == username:
            return item[3]
        
    return "null"
        
    
def add_to_membership(username, email, tier):
    mydb = get_database()
    mycursor = mydb.cursor()

    mycursor.execute('''
            
            INSERT INTO membership_services
            VALUES (%s, %s, %s, %s);
        
        ''', (username, email, tier, "0"))

    mydb.commit()

def add_to_autoprice_count(username):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    new = int(get_user_autoprice_count(username)) + 1

    mycursor.execute("""
            UPDATE membership_services
            SET autoprice_count=%s
            WHERE username=%s
            """, (new, username))
    
    mydb.commit()
