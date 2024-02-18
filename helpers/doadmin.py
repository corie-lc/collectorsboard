import bcrypt
import mysql
import mysql.connector
from random import randint
import MySQLdb
import logging
import boto3
from botocore.exceptions import ClientError
import os

from helpers import accounts, sensitive

from cachelib import file

def get_database():
    return mysql.connector.connect(
        host=sensitive.get_server_name(),
        # localhost or 192.168.0.26 for remote in home
        user="doadmin",
        password=sensitive.get_server_password(),
        database="collec",
        port=25060
    )


from boto3 import session, Session, s3
import io


def upload_file(file_name, actual_file, object_name=None):
    """Upload a file to an S3 bucket"""
    ACCESS_ID = sensitive.get_access_id_server()
    SECRET_KEY = sensitive.get_secret_key()

    # Initiate session
    session = Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url=sensitive.get_photo_server_name(),
                            aws_access_key_id=ACCESS_ID,
                            aws_secret_access_key=SECRET_KEY)

    # Upload a file to your Space
    print(actual_file)
    from werkzeug.utils import secure_filename

    client.upload_fileobj(
        actual_file,
        "post-photos",
        file_name,
        ExtraArgs={
            "ACL": "public-read",

        })

    # client.upload_file(actual_file, 'post-photos', "unt.jpg", ExtraArgs={'ACL':'public-read', "ContentType": actual_file.content_type})


def create_password(password):
    salt = bcrypt.gensalt(rounds=12)
    # Hashing the password
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    print(hashed)
    return hashed


def verify_password(password, entered_password, username):
    print(accounts.get_user_info(username))

    return bcrypt.checkpw(entered_password.encode("utf-8"), accounts.get_user_info(username)[2].encode("utf-8"))


