import traceback
from datetime import datetime

import flask
from flask import Flask, get_template_attribute, jsonify, send_from_directory
from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from flask import flash
from gevent.pywsgi import WSGIServer
from gevent import monkey


from helpers import accounts, collections, posts_entrys, social, search, doadmin, average_price, notif, support, front_end_help

import itertools

## content="AymqwRC7u88Y4JPvfIF2F37QKylC04248hLCdJAsh8xgOfe/dVJPV3XS3wLFca1ZMVOtnBfVjaCMTVudWM//5g4AAAB7eyJvcmlnaW4iOiJodHRwczovL3d3dy5nb29nbGV0YWdtYW5hZ2VyLmNvbTo0NDMiLCJmZWF0dXJlIjoiUHJpdmFjeVNhbmRib3hBZHNBUElzIiwiZXhwaXJ5IjoxNjk1MTY3OTk5LCJpc1RoaXJkUGFydHkiOnRydWV9"

# START SESSION ---------------------------------
app = Flask(__name__)
app.secret_key = '681336'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

sess = Session()
sess.init_app(app)

Session(app)


def check_logged_redirect():
    if session.get('logged_in'):
        if session['logged_in'] != True:
            return False
        else:
            return True

    else:
        return False


# -- ALL MAIN PAGES

@app.route('/', methods=['POST', 'GET'])
def hello():
    return redirect(url_for('index'))


# start login & index systems -------------------------------------------

@app.route('/about_info', methods=['POST', 'GET'])
def about_info():
    return render_template("about_info.html")


@app.route('/privacypolicy', methods=['POST', 'GET'])
def privacypolicy():
    return render_template("privacypolicy.html")


@app.route('/membership', methods=['POST', 'GET'])
def membership():
    return render_template("membership.html")


@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'logout-button' in request.form:
            session.clear()

        elif "post_comment_button" in request.form:
            post_id = request.form.get('post_comment_button')
            comment = request.form.get('comment_input')

            posts_entrys.add_comment(post_id, comment, session['username'])

            return redirect(url_for("index"))

        elif session.get('logged_in') == True:
            return render_template('a.html')

        elif 'login-button' in request.form:
            username = request.form.get('login-username')
            password = request.form.get('login-password')

            if accounts.login(username, password):
                session["username"] = accounts.get_user_info(username)[0]
                session["password"] = password
                session['email'] = accounts.get_user_email(session['username'])
                session["logged_in"] = True
                session["collections"] = collections.get_user_collections(username)

                return render_template('a.html')
            else:

                session["logged_in"] = False
                return render_template('index.html')



        elif 'signup-button' in request.form:
            username = request.form.get("username")
            password = request.form.get("password")
            password2 = request.form.get("passwordTwo")
            email = request.form.get("email")

            if password != password2:
                session["logged_in"] = "match_fail"
                return render_template("index.html")

            result = accounts.create_account(username, password, email)

            if result == True:
                session["username"] = username
                session["password"] = password
                session['email'] = accounts.get_user_email(session['username'])
                accounts.add_to_membership(username, accounts.get_user_email(session['username']), "free")
                session["logged_in"] = True

                return render_template("a.html")
            else:
                if result == "used_username":
                    session["logged_in"] = "used_username"
                    return render_template("index.html")

                elif result == "used_email":
                    session["logged_in"] = "used_email"
                    return render_template("index.html")

                elif result == "invalid":
                    session["logged_in"] = "invalid"
                    return render_template("index.html")
        else:
            if session.get('logged_in') == True:
                return render_template('a.html')
    else:
        if session.get('logged_in') == True:
            return render_template('a.html')

    return render_template("index.html")


@app.route('/community/<community_name>', methods=['POST', 'GET'])
def community(community_name):
    if check_logged_redirect() == True:
        return render_template("community.html", para1=community_name)
    else:
        return render_template('index.html', para1='null')


# END create post and entry systems

# START edit collection systems


# END edit collection systems

# START viewuser  systems

@app.route('/viewuser/<username>', methods=['POST', 'GET'])
def viewuser(username):
    if check_logged_redirect() == True:

        if request.method == "POST":

            if "follow" in request.form:
                social.request_follow_connection(session['username'], username)
                return redirect(url_for('viewuser', username=username))
            elif "unfollow" in request.form:
                social.create_unfollow_connection(session['username'], username)
                return redirect(url_for('viewuser', username=username))
            elif "stop_request" in request.form:
                social.stop_request(session['username'], username)
                return redirect(url_for('viewuser', username=username))

        if username == session['username']:
            return redirect(url_for('profile'))
        else:
            return render_template("viewuser.html", para1=username)
    else:
        return render_template('index.html', para1='null')


@app.route('/viewpost/<postid>', methods=['POST', 'GET'])
def viewpost(postid):
    if check_logged_redirect() == True:
        return render_template("viewpost.html", para1=postid)

    else:
        return render_template('index.html', para1='null')


# END login & index systems

# START profile and profile systems


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if check_logged_redirect() == True:
        if request.method == "POST":
            if 'post_info' in request.form:
                stuff = request.form.get('post_info').split(',')

                collections.add_to_collection(stuff[0], stuff[1])

                return render_template("profile.html")
            elif 'current_delete_post' in request.form:
                post_id = request.form.get("current_delete_post")
                posts_entrys.delete_post(post_id)
                return render_template('profile.html')

            elif 'change_username' in request.form:
                new_username = request.form.get('new_username')
                email = session['email']
                current_password = request.form.get("current_password")

                if doadmin.verify_password(session['password'], current_password, session['username']):
                    if posts_entrys.change_username_of_posts(session['username'], new_username):
                        accounts.change_username(email, new_username)
                        session['username'] = new_username
                else:
                    flash('Looks like you put in the wrong current password! ')

            elif 'change_bio' in request.form:
                new_bio = request.form.get("new_bio")
                accounts.change_bio(session['username'], new_bio)

            elif 'change_password' in request.form:

                new_password = request.form.get('new_password')
                current_password = request.form.get("current_password")
                email = session['email']

                if doadmin.verify_password(session['password'], current_password, session['username']):
                    if accounts.change_password(email, new_password):
                        session['password'] = new_password

                else:
                    flash('Looks like you put in the wrong current password! ')
                    return render_template('profile.html')
            elif 'public_profile' in request.form:
                accounts.change_account_public(session['username'], "public")
            elif 'private_profile' in request.form:
                accounts.change_account_public(session['username'], "private")

        return render_template('profile.html')
    else:
        return render_template('index.html', para1='null')


@app.route('/add_to_collection', methods=['POST', 'GET'])
def add_to_collection():
    if request.method == "POST":
        collection_id = request.json['collectionId']
        post_id = request.json['postId']

        collections.add_to_collection(collection_id, post_id)

        return redirect(url_for('index'))


@app.route('/collectionview/<collection_id>', methods=['POST', 'GET'])
def collectionview(collection_id):
    if check_logged_redirect() == True:
        if request.method == "POST":
            if 'delete_from' in request.form:
                post_id = request.form.get("delete-from")
                collections.rempve_from_collection(post_id)

            return render_template('collectionview.html', para1=collection_id)
        else:
            return render_template('collectionview.html', para1=collection_id)
    else:
        return render_template('collectionview_guest.html', para1=collection_id)


@app.route('/searchq', methods=['POST', 'GET'])
def searchq():
    if check_logged_redirect() == True:
        if request.method == "POST":
            keyword = request.form.get("search_input")
            return render_template('search.html', para1=keyword)
    else:
        return render_template('index.html', para1='null')
    return render_template('search.html', para1='null')


@app.route('/searchq_collection/<collection_id>', methods=['POST', 'GET'])
def searchq_collection(collection_id):
    if check_logged_redirect() == True:
        if request.method == "POST":
            keyword = request.form.get("search_input_collection")
            return render_template('search_collection.html', para1=keyword, para2=collection_id)
    else:
        return render_template('index.html', para1='null')
    return render_template('search_collection.html', para1='null', para2=collection_id)


# ---- END ----

@app.route('/get_noti_count', methods=['POST', 'GET'])
def get_noti_count():
    return notif.get_user_notis(session['username'])


@app.route('/send_support_email', methods=['POST', 'GET'])
def send_support_email():
    support_type = request.json['type']
    message = request.json['message']

    if session.get('logged_in'):
        if session['logged_in']:
            print(support.send_support_email(session['email'], session['username'], support_type, message, True))
        else:
            print(support.send_support_email('null', 'null', support_type, message, False))
    else:
        print(support.send_support_email('null', 'null', support_type, message, False))

    return "success"


# END SESSION ----------------------------------------------------------------
@app.route('/follow_community', methods=['POST', 'GET'])
def follow_community():
    username = request.json['username']
    community = request.json['community']
    if social.is_following_community(username, community):
        social.follow_community(username, community, "unfollow")
        return jsonify("unfollow")
    else:
        social.follow_community(username, community, "follow")
        return jsonify("follow")


@app.route('/follow_request', methods=['POST', 'GET'])
def follow_request():
    follow_request = request.json['follow_request']
    username = request.json['username']

    response = "Followed"

    if "follow" == follow_request:
        response = social.request_follow_connection(session['username'], username)
    elif "unfollow" == follow_request:
        social.create_unfollow_connection(session['username'], username)
        response = "Follow"
    elif "stop_request" == follow_request:
        social.stop_request(session['username'], username)
        return "Follow"

    return jsonify(response)


@app.route('/get_market_eval', methods=['POST', 'GET'])
def get_market_eval():
    keywords = request.json['keywords']

    free_max = 12
    essentails_max = None

    user_max = int(accounts.get_user_autoprice_count(session['username']))

    if accounts.get_user_mem_tier(session['username']) == "free":
        if user_max >= free_max:
            return jsonify("You've hit your max, please upgrade!")
        else:
            accounts.add_to_autoprice_count(session['username'])
            return jsonify(str(average_price.get_market_eval(keywords)))

    elif accounts.get_user_mem_tier(session['username']) == "essentails":
        if user_max >= essentails_max:
            return jsonify("You've hit your max, please upgrade!")
        else:
            accounts.add_to_autoprice_count(session['username'])
            return jsonify(str(average_price.get_market_eval(keywords)))

    elif accounts.get_user_mem_tier(session['username']) == "plus":
        accounts.add_to_autoprice_count(session['username'])
        return jsonify(str(average_price.get_market_eval(keywords)))

    return "fail"


@app.route('/edit_collection', methods=['POST', 'GET'])
def edit_collection():
    collection_id = request.json['collection_id']
    name = request.json['name']
    desc = request.json['desc']
    community_name = request.json['community']
    value = request.json['value']

    collections.edit_collection(collection_id, name, desc, community_name, value)

    return "true"


@app.route('/value_collection', methods=['POST', 'GET'])
def value_collection():
    collection_id = request.json['collection_id']

    return str(collections.value_collection(collection_id, session['username']))


@app.route('/get_comments', methods=['POST', 'GET'])
def get_comments():
    postid = request.json['postId']
    comments = posts_entrys.get_post_comments(postid)
    counter = 0

    return jsonify(comments)

    return jsonify(posts_entrys.get_post_comments(postid))


@app.route('/update_account_status', methods=['POST', 'GET'])
def update_account_status():
    accounts.change_account_public(session['username'], "public")


@app.route('/delete_follower', methods=['POST', 'GET'])
def delete_follower():
    username = request.json['username']

    social.create_unfollow_connection(username, session['username'])

    return username


@app.route("/delete_noti", methods=['POST', 'GET'])
def delete_noti():
    noti_id = request.json['noti_id']

    notif.clear_noti(noti_id)

    return jsonify("true")


@app.route('/delete_following', methods=['POST', 'GET'])
def delete_following():
    username = request.json['username']

    social.create_unfollow_connection(session['username'], username)

    return jsonify(username)


@app.route('/accept_request', methods=['POST', 'GET'])
def accept_request():
    username = request.json['username']
    accept = request.json['accept']

    if accept == "true":

        if (social.is_follow_request(username, session['username']) == True):

            social.create_follow_connection(username, session['username'])

            hello = get_template_attribute('macros.html', 'profile_card')
            helloa = hello(username)

            return jsonify(helloa, username)

        else:
            return jsonify("null", username)

    else:

        if social.is_follow_request(username, session['username']) == True:

            social.stop_request(username, session['username'])

            hello = get_template_attribute('macros.html', 'profile_card')
            helloa = hello(username)

            return jsonify("null", username)

        else:
            return jsonify("null", username)


@app.route('/more_search_posts', methods=['POST', 'GET'])
def more_search_posts():
    number = request.json['number']
    q = request.json['q']
    posts = search.get_posts_search(q, session['username'])
    data = "none"

    while number < len(posts):
        if social.is_follow(session['username'], posts[number][4]) or accounts.is_account_public(posts[number][4]):
            post = posts[number]

            hello = get_template_attribute('macros.html', 'post_block')
            data += hello(post)
            number += 1

        else:

            number += 1

    return jsonify(data, number)


@app.route('/more_collectionview_feed', methods=['POST', 'GET'])
def more_collectionview_feed():
    number = request.json['number']
    id = request.json['id']
    data = ""

    posts = collections.get_collection_posts(id, session['username'], number)
    print(posts)

    for item in posts:
        hello = get_template_attribute('macros.html', 'post_block')
        data += hello(item)

    if data == "":
        data = "none"

    return jsonify(data, number)


@app.route('/more_collectionview_feed_guest', methods=['POST', 'GET'])
def more_collectionview_feed_guest():
    number = request.json['number']
    id = request.json['id']
    data = ""

    posts = collections.get_collection_posts(id, '@guest_unusable_1190090', number)
    print(posts)

    for item in posts:
        hello = get_template_attribute('macros.html', 'post_block_guest')
        data += hello(item)

    if data == "":
        data = "none"

    return jsonify(data, number)


@app.route('/get_edit_post', methods=['POST', 'GET'])
def get_edit_post():
    post_id = request.json['postId']

    hello = get_template_attribute('macros.html', 'post_block')
    data = hello(posts_entrys.get_all_posts()[0])

    return jsonify(data)


import time


@app.route('/more_feed_collection', methods=['POST', 'GET'])
def more_feed_collection():
    start = time.time()

    number = request.json['number']
    data = ""

    posts = [collections.get_feed_collections(session['username'])]

    if 'type' in request.json and request.json['type'] == "user_feed":
        posts = collections.get_feed_collections(session['username'])
    elif 'type' in request.json and request.json['type'] == "community_feed":
        posts = collections.get_collections_by_community(request.json['community'])
    else:
        posts = collections.get_feed_collections(session['username'])

    while number < len(posts):
        try:
            i = 0

            while i < 8:
                hello = get_template_attribute('macros.html', 'collection_card')
                data += hello(posts[number + i])
                i += 1

            break
        except:
            data = ""
            i = 0
            while i < len(posts) - number:
                hello = get_template_attribute('macros.html', 'collection_card')
                data += hello(posts[number + i])
                i += 1
            break

    if data == "":
        data = "none"

    end = time.time()

    return jsonify(data, number)


@app.route('/get_user_feed', methods=['POST', 'GET'])
def get_user_feed():
    number = request.json['number']
    posts = posts_entrys.get_feed_posts(session['username'], number)
    print(posts)
    data = ""

    for item in posts:
        hello = get_template_attribute('macros.html', 'post_block')
        data += hello(item)

    if data == "":
        data = "none"

    return jsonify(data, number)

@app.route('/get_toppost_feed', methods=['POST', 'GET'])
def get_toppost_feed():
    number = request.json['number']
    posts = posts_entrys.get_top_posts(session['username'], number)
    print(posts)
    data = ""

    for item in posts:
        hello = get_template_attribute('macros.html', 'post_block')
        data += hello(item)

    if data == "":
        print("none")
        data = "none"

    return jsonify(data, number)


@app.route('/your_communities_posts', methods=['POST', 'GET'])
def your_communities_posts():
    number = request.json['number']
    posts = posts_entrys.get_related_community_posts(session['username'], number)
    print(posts)
    data = ""

    for item in posts:
        hello = get_template_attribute('macros.html', 'post_block')
        data += hello(item)

    if data == "":
        print("none")
        data = "none"

    return jsonify(data, number)


@app.route('/get_comunity_posts', methods=['POST', 'GET'])
def get_comunity_posts():
    
    number = request.json['number']
    posts = posts_entrys.get_top_community_post(request.json['community'], session['username'], number)
    print(posts)
    data = ""

    for item in posts:
        hello = get_template_attribute('macros.html', 'post_block')
        data += hello(item)

    if data == "":
        print("none")
        data = "none"

    return jsonify(data, number)



@app.route('/more_feed', methods=['POST', 'GET'])
def more_feed():
    start = time.time()
    posts = []
    data = ""

    number = request.json['number']
    type = ""
    if 'type' in request.json:
        type = request.json['type']

    if 'type' in request.json and request.json['type'] == "user_feed":
        posts = posts_entrys.get_feed_posts(session['username'])
    elif 'type' in request.json and request.json['type'] == "community_feed":
        posts = posts_entrys.get_top_community_post(request.json['community'], session['username'])
    elif 'type' in request.json and request.json['type'] == "top_posts_feed":
        posts = posts_entrys.get_top_posts(session['username'])
    elif 'type' in request.json and request.json['type'] == "community_feed_new":
        posts = posts_entrys.get_community_post(request.json['community'], session['username'])
    elif 'type' in request.json and request.json['type'] == "your_communities_posts":
        posts = posts_entrys.get_related_community_posts(session['username'])
    else:
        posts = posts_entrys.get_feed_posts(session['username'])[2:]

    if number < len(posts):
        try:
            i = 0

            while i <= 4:
                hello = get_template_attribute('macros.html', 'post_block')
                if type == "top_posts_feed" or type == "community_feed_new":

                    data += hello(posts[number + i], 1)
                elif type == "your_communities_posts":
                    hello = get_template_attribute('macros.html', 'post_block')
                    data += hello(posts[number + i], 2)

                else:
                    data += hello(posts[number + i])
                i += 1

        except:
            data = ""
            i = 0
            while i < len(posts) - number:
                if type == "top_posts_feed" or type == "community_feed_new":
                    hello = get_template_attribute('macros.html', 'post_block')
                    data += hello(posts[number + i], 1)
                elif type == "your_communities_posts":
                    hello = get_template_attribute('macros.html', 'post_block')
                    data += hello(posts[number + i], 2)
                else:

                    hello = get_template_attribute('macros.html', 'post_block')
                    data += hello(posts[number + i])
                i += 1

    if data == "":
        data = "none"

    end = time.time()
    return jsonify(data, number)


@app.route('/change_avatar', methods=['POST', 'GET'])
def change_avatar():
    item = request.json['avatar']
    accounts.change_avatar(item, session['username'])
    return "True"


@app.route('/more_profile', methods=['POST', 'GET'])
def more_profile():
    number = request.json['number']
    data = ""

    posts = posts_entrys.get_user_posts(session['username'])

    while number < len(posts):
        try:
            i = 0
            while i < 8:
                hello = get_template_attribute('macros.html', 'post_block')
                data += hello(posts[number + i])
                i += 1
            break
        except:
            data = ""
            i = 0
            while i < len(posts) - number:
                hello = get_template_attribute('macros.html', 'post_block')
                data += hello(posts[number + i])
                i += 1
            break

    if data == "":
        data = "none"
    return jsonify(data, number)


@app.route('/more_viewuser', methods=['POST', 'GET'])
def more_viewuser():
    number = request.json['number']
    username = request.json['username']

    posts = posts_entrys.get_user_posts(username)

    if (number >= len(posts)):
        return jsonify("none")
    else:
        post = posts[number]

        hello = get_template_attribute('macros.html', 'post_block')
        helloa = hello(post)

        return jsonify(helloa)


# END profile and profile systems ------------------------------------------------------------------------------------------------------------------------

# START create post and entry systems ------------------------------------------------------------------------------------------------------------------------

@app.route('/make_entry', methods=['GET', 'POST'])
def make_entry():
    photo = request.form.get("entry-photo")
    community = request.form.get("entry-community")
    value = request.form.get("entry-value")
    entry_title = request.form.get("entry-title")
    off_name = request.form.get("entry-off-name")
    origin_country = request.form.get("entry-origin-country")
    date_created = request.form.get("entry-date")
    details = request.form.get("entry-details")
    cat = "a"
    visibility = request.form.get("visibility")

    if (visibility != "on"):
        visibility = "off"

    if community == "Choose Community":
        community = "None"

    if posts_entrys.create_entry('aa', community, entry_title, session["username"], details, visibility, cat, value,
                                 off_name, origin_country, date_created):
        return render_template('a.html')
    else:
        return render_template('a.html')


@app.route('/edit_post', methods=['GET', 'POST'])
def edit_post():
    post_id = request.json['postid']
    details = request.json['details']
    community = request.json['community']

    name = request.json['name']
    country = request.json['country']
    date = request.json['date']
    value = request.json['value']

    posts_entrys.edit_post(post_id, details, name, country, date, value, community)

    return "true"


@app.route('/make_post_ajax', methods=['GET', 'POST'])
def make_post_ajax():
    photo = request.files.get('myPhoto')
    community = request.form.get('post-community')
    post_title = request.form.get("post-title")
    details = request.form.get("post-details")
    visibility = request.form.get("visibility")
    off_name = request.form.get("entry-off-name")
    origin_country = request.form.get("entry-origin-country")
    date_created = request.form.get("entry-date")
    value = request.form.get("entry-value")
    collection_select = request.form.get("collection_select")

    if value == "":
        value = 'no data'
    if off_name == "":
        off_name = 'no data'
    if origin_country == "":
        origin_country = 'no data'
    if date_created == "":
        date_created = 'no data'

    if (visibility != "on"):
        visibility = "off"

    file = request.files.get('myPhoto')

    post_id = posts_entrys.create_post(photo, community, "null", session["username"], details, visibility, community,
                                       off_name,
                                       origin_country, date_created, value)

    # doadmin.upload_file(photo)

    if collection_select != "None":
        collections.add_to_collection(collection_select, post_id)

    return jsonify(post_id)


@app.route('/make_post', methods=['GET', 'POST'])
def make_post():
    photo = flask.request.files.get('myPhoto')
    community = request.form.get('post-community')
    post_title = request.form.get("post-title")
    details = request.form.get("post-details")
    visibility = request.form.get("visibility")
    off_name = request.form.get("entry-off-name")
    origin_country = request.form.get("entry-origin-country")
    date_created = request.form.get("entry-date")
    value = request.form.get("entry-value")
    collection_select = request.form.get("collection_select")

    if value == "":
        value = 'no data'
    if off_name == "":
        off_name = 'no data'
    if origin_country == "":
        origin_country = 'no data'
    if date_created == "":
        date_created = 'no data'

    if (visibility != "on"):
        visibility = "off"

    post_id = posts_entrys.create_post(photo, community, "null", session["username"], details, visibility, community,
                                       off_name,
                                       origin_country, date_created, value)

    # doadmin.upload_file(photo)

    if collection_select != "None":
        collections.add_to_collection(collection_select, post_id)

    return redirect(request.referrer)


@app.route('/make_collection', methods=['GET', 'POST'])
def make_collection():
    name = request.json['name']
    details = request.json['desc']
    community = request.json['community']

    return collections.create_collection(name, "null", session['username'], details, community)


@app.route('/fav_post_button', methods=["POST", "GET"])
def fav_post_button():
    if request.method == "POST":
        post_id = request.json['postId']

        posts_entrys.favorite_post(session['username'], post_id)

    return render_template('a.html')


@app.route('/like_post', methods=["POST", "GET"])
def like_post():
    if request.method == "POST":
        post_id = request.json['postId']

        posts_entrys.like_post(session['username'], post_id)

    return render_template('a.html')


@app.route('/save_collection', methods=["POST", "GET"])
def save_collection():
    if request.method == "POST":
        collection_id = request.json['collectionId']

        collections.save_collection(session['username'], collection_id)

    return render_template('a.html')


@app.route('/delete_collection', methods=["POST", "GET"])
def delete_collection():
    if request.method == "POST":
        collection_id = request.json['collectionId']

        collections.delete_collection(collection_id)

    return render_template('a.html')


@app.route('/add_comment', methods=['POST', 'GET'])
def add_comment():
    comment = request.json['comment']
    post_id = request.json['postId']

    posts_entrys.add_comment(post_id, comment, session['username'])

    return redirect(url_for("index"))


# END viewuser  systems
# ------------------------------------------------------------------------------------------------------------------------

# start search  systems
# ------------------------------------------------------------------------------------------------------------------------


app.jinja_env.globals.update(get_feed_posts=posts_entrys.get_feed_posts)
app.jinja_env.globals.update(get_post_comments=posts_entrys.get_post_comments)
app.jinja_env.globals.update(get_user_posts=posts_entrys.get_user_posts)
app.jinja_env.globals.update(get_all_catg=posts_entrys.get_all_catg)
app.jinja_env.globals.update(get_community_post=posts_entrys.get_community_post)
app.jinja_env.globals.update(is_post_favorited=posts_entrys.is_post_favorited)
app.jinja_env.globals.update(is_post_liked=posts_entrys.is_post_liked)
app.jinja_env.globals.update(get_saved_posts=posts_entrys.get_saved_posts)
app.jinja_env.globals.update(get_post_by_id=posts_entrys.get_post_by_id)
app.jinja_env.globals.update(get_top_posts=posts_entrys.get_top_posts)
app.jinja_env.globals.update(get_top_posts_of_community=posts_entrys.get_top_posts_of_community)
app.jinja_env.globals.update(get_community_search=search.get_community_search)

app.jinja_env.globals.update(get_user_collections=collections.get_user_collections)
app.jinja_env.globals.update(is_collection_saved=collections.is_collection_saved)
app.jinja_env.globals.update(get_collection_posts=collections.get_collection_posts)
app.jinja_env.globals.update(is_post_in_collection=collections.is_post_in_collection)
app.jinja_env.globals.update(is_post_in_spec_collection=collections.is_post_in_spec_collection)
app.jinja_env.globals.update(get_saved_collections=collections.get_saved_collections)
app.jinja_env.globals.update(get_collections_with_post=collections.get_collections_with_post)
app.jinja_env.globals.update(get_collection_byid=collections.get_collection_byid)
app.jinja_env.globals.update(get_collections_by_community=collections.get_collections_by_community)
app.jinja_env.globals.update(get_feed_collections=collections.get_feed_collections)
app.jinja_env.globals.update(get_user_collections=collections.get_user_collections)

app.jinja_env.globals.update(is_follow=social.is_follow)
app.jinja_env.globals.update(get_followers=social.get_followers)
app.jinja_env.globals.update(get_following=social.get_following)
app.jinja_env.globals.update(count_following=social.count_following)
app.jinja_env.globals.update(get_follow_requests=social.get_follow_requests)
app.jinja_env.globals.update(is_follow_request=social.is_follow_request)
app.jinja_env.globals.update(follow_community=social.follow_community)
app.jinja_env.globals.update(is_following_community=social.is_following_community)

app.jinja_env.globals.update(get_user_info=accounts.get_user_info)
app.jinja_env.globals.update(is_account_public=accounts.is_account_public)
app.jinja_env.globals.update(is_account_public=accounts.is_account_public)
app.jinja_env.globals.update(get_followed_communties=accounts.get_followed_communties)
app.jinja_env.globals.update(get_avatars=accounts.get_avatars)
app.jinja_env.globals.update(get_user_avatar=accounts.get_user_avatar)

app.jinja_env.globals.update(get_posts_search=search.get_posts_search)
app.jinja_env.globals.update(get_users_search=search.get_users_search)
app.jinja_env.globals.update(get_collection_search=search.get_collection_search)
app.jinja_env.globals.update(searh_posts_in_collection=search.searh_posts_in_collection)
app.jinja_env.globals.update(get_all_cat_new=search.get_all_cat_new)

app.jinja_env.globals.update(get_user_notis=notif.get_user_notis)


@app.route('/robots.txt')
@app.route('/sitemap.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    http = WSGIServer(('127.0.0.1', 5000), app.wsgi_app)

    # Serve your applicatio

    http.serve_forever()
