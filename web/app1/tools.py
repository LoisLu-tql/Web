import random
from lxml import etree

from django.core.mail import send_mail
from django.template import loader

# from web1.settings import EMAIL_HOST_USER


def get_color():
    return random.randrange(256)


def generate_code():
    source = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    for i in range(4):
        result += random.choice(source)

    return result

# def send_email_change_password(username, receive_list, u_token):
#     subject = '%s Subject' % username
#     from_email = EMAIL_HOST_USER
#     recipient_list = [receive_list, ]
#     data = {
#         'username': username,
#         'change_password_url': 'http://127.0.0.1:8000/changepassword/?u_token=' + u_token,
#     }
#     html_message = loader.get_template('User Manage/change_password_email.html').render(data)
#     send_mail(subject=subject, message="", html_message=html_message, from_email=from_email, recipient_list=recipient_list)

def cut_content(text):
    response = etree.HTML(text=text)
    text = response.xpath('string(.)')
    if len(text) > 90 :
        return text[:90] + ' ...'
    return text

