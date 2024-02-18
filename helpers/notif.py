import mysql
import mysql.connector
from random import randint
from helpers import posts_entrys
from helpers.doadmin import get_database
from datetime import datetime    

def get_user_notis(username):
    all_noti = []

    mydb = get_database()
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
                SELECT * FROM notif WHERE username = %s ORDER BY date DESC
                """, (username, ))


    # username | timestamp | messagtype | message | 

    for item in mycursor:
        if item[0] == username:
            all_noti.append(item)


    

    return all_noti


def get_noti_count(username):
    return len(get_user_notis(username))


def custom_noti_id():
    post_id = randint(100000000000000, 999999999999999)

    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM notif")

    for item in cursor:
        if (item[4] == post_id):
            post_id = randint(100000000000000, 999999999999999)

    return int(post_id)
    

def save_notification(username, timestamp, messagetype, n_id, message):
    mydb = get_database()
    mycursor = mydb.cursor()

    mycursor.execute("""
                SELECT * FROM notif WHERE username = %s ORDER BY date DESC
                """, (username, ))

    all_results = []

    for item in mycursor:
        all_results.append(item)




    try:
        if len(all_results) > 39:

            last_item = all_results[-1]

            query = "delete FROM notif WHERE username = %s and date = %s"
            mycursor.execute(query,(username, last_item[1]))

            
    except():
        print("lol")
        



    mycursor.execute('''
        
        INSERT INTO notif
        VALUES (%s, %s, %s, %s, %s);
    
    ''', (username, timestamp, (messagetype + ":"+ n_id), message, custom_noti_id())) 

    mydb.commit()

    




def clear_noti(noti_id):
    mydb = get_database()
    mycursor = mydb.cursor()

    
    statmt = "DELETE FROM notif WHERE id = %s"
    mycursor.execute(statmt, (noti_id, ))
    mydb.commit()
