# sens
import os

def get_access_id_server():
    return os.environ['access_id']

def get_secret_key():
    return os.environ['secret_key']

def get_server_password():
    return os.environ['password']

def get_server_name():
    return os.environ['server_name']

def get_photo_server_name():
    return os.environ['photo_server_name']


