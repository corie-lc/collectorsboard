import requests
import os


def send_support_email(from_who, username, support_type, message, logged_in):
    print(from_who)
    if logged_in:
        return requests.post(
            os.environ['mailgun_full'],
            auth=("api", os.environ['mailgun_key']),
            data={"from": str(username + " " + from_who),
                  "to": ["corieleclair.real@gmail.com"],
                  "subject": support_type,
                  "text": str(message)})
    else:
        return requests.post(
            os.environ['mailgun_full'],
            auth=("api", os.environ['mailgun_key']),
            data={"from": "Logged Out User <logged_out_user@YOUR_DOMAIN_NAME>",
                  "to": ["corieleclair.real@gmail.com"],
                  "subject": support_type,
                  "text": str(message)})

