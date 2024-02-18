import time
from operator import itemgetter
import mysql
import mysql.connector
from random import randint
from helpers.doadmin import get_database
from helpers import social
from helpers import accounts
from helpers.doadmin import upload_file
from datetime import datetime
from helpers.notif import *


def custom_post_id():
    post_id = randint(100000000000000, 999999999999999)

    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM collections")

    for item in cursor:
        if item[1] == post_id:
            post_id = randint(100000000000000, 999999999999999)

    return int(post_id)


# START CREATE OF POSTS ------------------------------------------------------------------------------------------------------------------------------------

def create_entry(photo, community, entry_title, username, details, visibility, cat, value, off_name, origin_country,
                 date_created):
    mydb = get_database()
    post_type = "post"

    id_num = custom_post_id()
    if off_name != "null" or origin_country != "null" or date_created != "null" or value != "null":
        post_type = "entry"

    mycursor = mydb.cursor()
    mycursor.execute('''

            INSERT INTO entry
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

        ''', (photo, community, id_num, entry_title, username, details, post_type, visibility, cat, value, off_name,
              origin_country, date_created))

    mydb.commit()

    return True


def create_post(photo, community, post_title, username, details, visibility, catagory, off_name, origin_country,
                date_created, value):
    mydb = get_database()

    public = accounts.is_account_public(username)

    if public == True:
        public = "public"
    else:
        public = "private"

    id_num = custom_post_id()
    photo_name = str(id_num) + ".jpg"

    post_type = "post"

    if off_name != "no data" or origin_country != "no data" or date_created != "no data" or value != "no data":
        post_type = "entry"

    if community == "Choose Community":
        community = "No Community"

    mycursor = mydb.cursor()
    mycursor.execute('''

            INSERT INTO posts
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, %s, %s);

        ''', (
        photo_name, community, id_num, post_title, username, details, post_type, visibility, catagory, off_name,
        origin_country,
        date_created, value, public, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    file_name = str(id_num) + ".jpg"
    upload_file(file_name, photo)


    mydb.commit()

    return id_num


# END CREATE OF POSTS ------------------------------------------------------------------------------------------------------------------------------------


# START COLLECTION OF POSTS ------------------------------------------------------------------------------------------------------------------------------------

def count_liked_post_lists(posts):
    posts = sorted(posts, key=lambda x: int(x[13]), reverse=True)

    return posts


def get_post_from_following(username):
    following = social.get_following(username)
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM posts")

    posts = []

    for user in following:
        for item in cursor:
            if item[4] == user[1]:
                if item[7] != "off":
                    posts.append(item)

    return posts


def get_all_viewable_posts_community(username, community):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = []

    for item in cursor:
        if item[1] == community:
            if social.is_follow(username, item[4]):
                posts.append(item)
            if item[14] == "public":
                posts.append(item)

    return posts


def get_all_viewable_posts(username):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = []

    for item in cursor:
        if social.is_follow(username, item[4]):
            posts.append(item)
        if item[14] == "public" and item not in posts:
            posts.append(item)

    return posts


def get_top_community_post(community, username):
    posts = []

    mydb = get_database()

    cursor = mydb.cursor()
    statmt_collection = "SELECT * FROM posts where community = %s"
    cursor.execute(statmt_collection, (community,))


    for item in cursor:
        if item[1] == community:
            if accounts.is_account_public(item[4]) == False:
                pass
            elif item[14] == "public" and item[7] == "on":
                posts.append(item)
            elif social.is_follow(username, item[4]) == True and item[7] == "on":
                posts.append(item)

    all = count_liked_post_lists(posts)

    return all

def get_top_posts(username, start_at=-1):
    public_posts = get_all_posts(date=False)
    posts = []

    followed_communities = accounts.get_followed_communties(username)

    i = start_at

    if start_at > -1:
        while i < start_at + 4 and i < len(public_posts):
            print(i)
            post_info = posts_entrys.get_post_by_id(public_posts[i][0])

            if accounts.is_account_public(public_posts[i][4]) == False:
                pass

            elif public_posts[i][14] == "public" and public_posts[i][7] == "on":
                posts.append(public_posts[i])
                i += 1
            elif social.is_follow(username, public_posts[i][4]) == True and public_posts[i][7] == "on":
                posts.append(public_posts[i])
                i += 1
            elif public_posts[i][1] in followed_communities:
                posts.append(public_posts[i])
                i += 1

    else:


        for item in public_posts:

            
            

            if accounts.is_account_public(item[4]) == False:
                pass
            elif item[14] == "public" and item[7] == "on":
                posts.append(item)
            elif social.is_follow(username, item[4]) == True and item[7] == "on":
                posts.append(item)
            elif item[1] in followed_communities:
                posts.append(item)
                
        all = count_liked_post_lists(posts)

    return all

def get_new_posts(username):
    posts = get_all_viewable_posts(username)

    return posts


def get_top_posts_of_community(username, community):
    posts = get_all_viewable_posts_community(username, community)
    all = count_liked_post_lists(posts)

    return all


def get_feed_posts(username, start_at = -1):
    public_posts = get_all_posts(date=True)
    posts = []
    i = start_at

    if start_at > -1:
        while i < start_at + 4 and i < len(public_posts):
            print(i)
            post_info = posts_entrys.get_post_by_id(public_posts[i][0])

            if public_posts[i][4] == username:
                pass
            elif accounts.is_account_public(public_posts[i][4]) == False:
                pass

            elif public_posts[i][14] == "public" and public_posts[i][7] == "on":
                posts.append(public_posts[i])
                i += 1
            elif social.is_follow(username, public_posts[i][4]) == True and public_posts[i][7] == "on":
                posts.append(public_posts[i])
                i += 1
            elif public_posts[i][1] in followed_communities:
                posts.append(public_posts[i])
                i += 1

    
    else:

        followed_communities = accounts.get_followed_communties(username)

        for item in public_posts:
            if item[4] == username:
                pass
            elif accounts.is_account_public(item[4]) == False:
                pass

            elif item[14] == "public" and item[7] == "on":
                posts.append(item)
            elif social.is_follow(username, item[4]) == True and item[7] == "on":
                posts.append(item)
            elif item[1] in followed_communities:
                posts.append(item)




    return posts


def get_all_posts(date=False ):


    if date:

        mydb = get_database()

        cursor1 = mydb.cursor()
        
        cursor1.execute("SELECT * FROM posts ORDER BY date DESC")

        posts = list(cursor1)

        
        
    else:
        mydb = get_database()

        cursor1 = mydb.cursor()

        cursor1.execute("SELECT * FROM posts")
        posts = list(cursor1)

    return posts


def get_user_posts(username):
    mydb = get_database()

    cursor = mydb.cursor()
    statmt = "select * FROM posts WHERE username = %s"
    cursor.execute(statmt, (username,))
    posts = []

    for item in cursor:
        if (item[4] == username):
            posts.append(item)
    return posts


def get_post_by_id(id):
    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM posts WHERE id_num = " + str(id))

    for item in cursor:

        if (str(item[2]) == str(id)):
            return item

    return None


def delete_post(post_id):
    mydb = get_database()

    cursor = mydb.cursor()

    statmt = "DELETE FROM posts WHERE id_num = %s"
    cursor.execute(statmt, (post_id,))

    statmt_collection = "DELETE FROM joint_cposts WHERE post_id = %s"
    cursor.execute(statmt_collection, (post_id,))

    mydb.commit()


def change_username_of_posts(old_username, new_username):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * FROM posts")
    

    for item in mycursor.fetchall():
        if item[4] == old_username:
            mycursor.execute("""
            UPDATE posts
            SET username=%s
            WHERE id_num=%s
            """, (new_username, item[2]))
    

    mycursor.execute("""
            UPDATE comments
            SET username=%s
            WHERE username=%s
            """, (new_username, old_username))
    
    mycursor.execute("""
            UPDATE collections
            SET username=%s
            WHERE username=%s
            """, (new_username, old_username))
    
    mycursor.execute("""
            UPDATE follow_community
            SET username=%s
            WHERE username=%s
            """, (new_username, old_username))
    
    mycursor.execute("""
            UPDATE save_collections
            SET username=%s
            WHERE username=%s
            """, (new_username, old_username))
    
    mycursor.execute("""
            UPDATE social_conn
            SET end_user=%s
            WHERE username=%s
            """, (new_username, old_username))
    
    mycursor.execute("""
            UPDATE social_conn
            SET origin_user=%s
            WHERE username=%s
            """, (new_username, old_username))
    
    mycursor.execute("""
            UPDATE like_posts
            SET username=%s
            WHERE username=%s
            """, (new_username, old_username))
    
    mycursor.execute("""
            UPDATE favorite_posts
            SET username=%s
            WHERE username=%s
            """, (new_username, old_username))


    mydb.commit()

    return True


from urllib.request import urlopen 
import json


def get_all_cat_new(username):
    url = "https://photo-storage-collecdb.nyc3.digitaloceanspaces.com/collectables.json"
    response = urlopen(url) 
    data = json.loads(response.read()) 

    new_dictionary = {"Your Communities": accounts.get_followed_communties(username)}
    new_dictionary.update(data)



    return new_dictionary








def get_all_catg(username):
    all = []
    yours = accounts.get_followed_communties(username)
    posts = []
    card = []
    earth = []
    currency = []
    transportation = []
    jewerly = []
    misc = []

    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM catg")

    for item in cursor:
        if item[1] == "Posts":
            posts.append(item)
        elif item[1] == "Card":
            card.append(item)
        elif item[1] == "Currency":
            currency.append(item)
        elif item[1] == "Earth":
            earth.append(item)
        elif item[1] == "Transportation":
            transportation.append(item)
        elif item[1] == "Jewerly":
            jewerly.append(item)
        else:
            misc.append(item)

        all = [yours, posts, card, currency, earth, transportation, jewerly, misc]

    return all


def add_comment(post_id, comment, username):
    mydb = get_database()

    mycursor = mydb.cursor()
    mycursor.execute('''

            INSERT INTO comments
            VALUES (%s, %s, %s);

        ''', (post_id, comment, username))

    mydb.commit()


    save_notification(get_post_by_id(post_id)[4], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "post", post_id, ("@" + username + " commented on your post! - " + comment)) 

    

    return True



def get_post_comments(post_id):
    comments = []

    mydb = get_database()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM comments")

    for comment in cursor:
        if comment[0] == post_id:
            comments.append(comment)


    return comments




def get_community_post(community, username):
    posts = []

    mydb = get_database()

    cursor = mydb.cursor()

    statmt_collection = "SELECT * FROM posts where community = %s ORDER BY date DESC"
    cursor.execute(statmt_collection, (community,))
    

    


    for item in cursor:
        if item[1] == community:
            if accounts.is_account_public(item[4]) == False:
                pass
            elif item[14] == "public" and item[7] == "on":
                posts.append(item)
            elif social.is_follow(username, item[4]) == True and item[7] == "on":
                posts.append(item)

    print(posts)
    return posts


def favorite_post(username, post_id):
    mydb = get_database()

    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM favorite_posts")

    for item in cursor:
        if item[0] == username and item[1] == post_id:
            statmt = "DELETE FROM favorite_posts WHERE username = %s AND post_id=%s"
            cursor.execute(statmt, (username, post_id))
            mydb.commit()
            return

    cursor.execute('''
        
        INSERT INTO favorite_posts
        VALUES (%s, %s);
    
    ''', (username, post_id))

    mydb.commit()


def is_post_favorited(username, post_id):
    mydb = get_database()
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM favorite_posts")

    for item in cursor:
        if item[0] == username and item[1] == post_id:
            return True

    return False


def get_saved_posts(username):
    mydb = get_database()
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM favorite_posts")
    posts = []

    for item in cursor:
        if item[0] == username:
            if get_post_by_id(item[1]) is not None:
                posts.append(get_post_by_id(item[1]))

    return posts


def update_likes(post_id, value):
    mydb = get_database()
    mycursor = mydb.cursor()

    sql = "UPDATE posts SET like_count = %s WHERE id_num = %s"
    val = (str(value), post_id)

    mycursor.execute(sql, val)

    mydb.commit()


def like_post(username, post_id):
    mydb = get_database()

    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM like_posts")

    for item in cursor:
        if item[0] == username and item[1] == post_id:
            statmt = "DELETE FROM like_posts WHERE username = %s AND post_id=%s"
            cursor.execute(statmt, (username, post_id))
            mydb.commit()
            update_likes(post_id, int(get_post_by_id(post_id)[13]) - 1)
            return

    cursor.execute('''
        
        INSERT INTO like_posts
        VALUES (%s, %s);
    
    ''', (username, post_id))

    mydb.commit()
    save_notification(get_post_by_id(post_id)[4], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "post", post_id, ("@" + username + " liked your post!")) 
    get_user_notis("laptop")
    update_likes(post_id, int(get_post_by_id(post_id)[13]) + 1)


def is_post_liked(username, post_id):
    mydb = get_database()
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM like_posts")

    for item in cursor:
        if item[0] == username and item[1] == post_id:
            return "liked"

    return "not_liked"


def edit_post(post_id, details, name, country, date, value, community):
    mydb = get_database()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
            UPDATE posts
            SET details=%s, off_name=%s, origin_country=%s, date_created=%s, value=%s, community=%s
            WHERE id_num=%s
            """, (details, name, country, date, value, get_post_by_id(post_id)[1], post_id))
    mydb.commit()

    return True


def get_related_community_posts(username):
    print("tryinh here")
    related_communties = accounts.get_followed_communties(username)
    all_posts = []
    rec_posts = []

    for item in related_communties:
        all_posts = all_posts + get_community_post(item, username)

    return all_posts

