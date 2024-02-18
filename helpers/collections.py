import mysql
import mysql.connector
from random import randint
from helpers import posts_entrys, accounts, social
from helpers.doadmin import get_database
from flask import Flask, get_template_attribute, jsonify
from datetime import datetime
import statistics




def custom_collection_id():
    collection_id = randint(100000000000000, 999999999999999)

    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM collections")

    for item in cursor:
        if (item[1] == collection_id):
            collection_id = randint(100000000000000, 999999999999999)

    return int(collection_id)


def get_collection_posts_full(collection_id):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM joint_cposts")
    posts = []

    for item in cursor:
        if (item[1] == collection_id):
            posts.append(item)

    list_posts = []

    for item in posts:
        list_posts.append(posts_entrys.get_post_by_id(item))

    return list_posts


def Reverse(lst):
   new_lst = lst[::-1]
   return new_lst


def get_collection_posts(collection_id, username):
    mydb = get_database()

    cursor = mydb.cursor()
    #cursor.execute("SELECT * FROM joint_cposts")

    statmt_collection = "SELECT * FROM joint_cposts WHERE collection_id = %s"
    cursor.execute(statmt_collection, (collection_id,))
    posts = []
    

    for item in cursor:
        if item[1] == collection_id:
        

            post_info = posts_entrys.get_post_by_id(item[0])

            if username == post_info[4]:
                posts.append(item)
            elif accounts.is_account_public(post_info[4]) == False:
                pass

            elif post_info[14] == "public" and post_info[7] == "on":
                posts.append(item)
            elif social.is_follow(username, post_info[4]) == True and post_info[7] == "on":
                posts.append(item)
        
            

    list_posts = []
    

    for item in posts:
        id_item = posts_entrys.get_post_by_id(item[0])
        if id_item is not None:
            list_posts.append(id_item)

    

    ts = '2013-01-12 15:27:43'
    f = '%Y-%m-%d %H:%M:%S'




    sorted_lst = sorted(list_posts, key=lambda x: datetime.strptime(str(x[15]), f))

    return Reverse(sorted_lst)


def create_collection(collection_title, photo, username, details, community):
    mydb = get_database()
    mycursor = mydb.cursor()

    id_num = custom_collection_id()

    mycursor.execute('''
        
        INSERT INTO collections
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    
    ''', (collection_title, id_num, photo, username, details, community, "0"))

    mydb.commit()
    return jsonify(id_num)


def add_to_collection(collection_id, post_id):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * FROM joint_cposts")

    for item in mycursor:
        if item[0] == post_id and item[1] == collection_id:
            sql = "DELETE FROM joint_cposts WHERE post_id = %s and collection_id = %s"
            adr = (post_id, collection_id)

            mycursor.execute(sql, adr)
            mydb.commit()
            return True

    mycursor.execute('''

            INSERT INTO joint_cposts
            VALUES (%s, %s);

            ''', (post_id, collection_id))

    mydb.commit()


def rempve_from_collection(post_id):
    mydb = get_database()

    mycursor = mydb.cursor()

    mycursor.execute("""
            UPDATE joint_cposts
            SET COLLECTIONID=%s
            WHERE POSTID=%s
            """, ('0', post_id))

    mydb.commit()


def is_post_in_collection(post_id):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM joint_cposts")
    posts = []

    for item in cursor:
        if item[0] == post_id:
            return item[1]

    return False


def is_post_in_spec_collection(post_id, collection_id):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM joint_cposts")
    posts = []

    for item in cursor:
        if item[0] == post_id and item[1] == collection_id:
            return item[1]

    return False


def get_all_collections():
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM collections")
    collections = []

    for item in cursor:
        collections.append(item)

    return collections


def get_feed_collections(username):
    collections = []
    all = get_all_collections()

    for item in all:
        if username != item[3] and accounts.is_account_public(item[3]) == True:
            collections.append(item)

    return collections


def get_collection_by_id(collection_id):
    for item in get_all_collections():
        if item[1] == collection_id:
            return item


def save_collection(username, collection_id):
    mydb = get_database()

    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM save_collections")

    for item in cursor:
        if item[0] == username and item[1] == collection_id:
            statmt = "DELETE FROM save_collections WHERE username = %s AND collection_id=%s"
            cursor.execute(statmt, (username, collection_id))
            mydb.commit()
            return

    cursor.execute('''
        
        INSERT INTO save_collections
        VALUES (%s, %s);
    
    ''', (username, collection_id))

    mydb.commit()


def delete_collection(collection_id):
    mydb = get_database()

    cursor = mydb.cursor()

    statmt = "DELETE FROM collections WHERE id = %s"
    cursor.execute(statmt, (collection_id, ))

    mydb.commit()


def is_collection_saved(username, post_id):
    mydb = get_database()
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM save_collections")

    for item in cursor:
        if item[0] == username and item[1] == post_id:
            return True

    return False


def get_user_collections(username):
    mydb = get_database()

    cursor = mydb.cursor()

    statmt_collection = "SELECT * FROM collections WHERE username = %s"
    cursor.execute(statmt_collection, (username,))

    collections = []

    for item in cursor:
        if (item[3] == username):
            collections.append(item)

    return collections


def get_saved_collections(username):
    mydb = get_database()
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM save_collections")
    collections = []

    for item in cursor:
        if item[0] == username:
            collections.append(get_collection_by_id(item[1]))

    return collections


def get_collections_with_post(username, post_id):
    collections_list = []
    for item in get_user_collections(username):
        if is_post_in_spec_collection(post_id, item[1]) != False:
            collections_list.append(item)

    return collections_list


def get_collection_byid(id):
    for item in get_all_collections():
        if item[1] == id:
            return item


def edit_collection(collection_id, name, desc, community, value_desc):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
            UPDATE collections
            SET title=%s, details=%s, community=%s, valued_at=%s
            WHERE id=%s
            """, (name, desc, community, value_desc, collection_id))
    mydb.commit()


    return True


def get_collections_by_community(community):
    all = get_all_collections()
    final = []

    for item in all:
        if item[5] == community and accounts.is_account_public(item[3]) == True:
            final.append(item)

    return final

def value_collection(collection_id, username):
    import numbers

    collection = get_collection_posts(str(collection_id), username)
    total = 0.0

    for item in collection:

        if item[12].replace(".", "").isnumeric():
            total = float(item[12]) + total

    return round(total, 2)
