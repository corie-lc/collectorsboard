from helpers.posts_entrys import *
from helpers.accounts import *
from helpers.collections import *


def get_posts_search(keywords, username):

    posts = get_all_posts()
    query = []

    for item in posts:
        if keywords.lower() in item[5].lower():
            query.append(item)
        elif keywords.lower() in item[9].lower():
            query.append(item)

    return query


def get_users_search(keyword):
    users = get_all_users()
    query = []

    for item in users:
        if keyword.lower() in item[0].lower():
            query.append(item)

    return query


def get_collection_search(keyword):
    collections = get_all_collections()
    query = []

    for item in collections:
        if keyword.lower() in item[0].lower():
            query.append(item)

    return query


def get_community_search(keyword):
    communties = []
    q = []

    for item in posts_entrys.get_all_posts():
        if item[1] not in communties:
            communties.append(item[1])

    for item in get_all_collections():
        if item[5] not in communties:
            communties.append(item[5])


    for item in communties:
        if str(keyword).lower() in str(item).lower():
            q.append(item)

    return q


def searh_posts_in_collection(keywords, collection_id, username):
    mydb = get_database()

    all_posts = get_collection_posts(collection_id, username)
    q_posts = []

    for item in all_posts:
        if str(keywords).lower() in str(item[5]).lower():
            q_posts.append(item)
        elif str(keywords).lower() in str(item[9]).lower():
            q_posts.append(item)

    return q_posts



