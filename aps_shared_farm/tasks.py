from celery import shared_task
from celery.schedules import crontab
# from celery import periodic_task
from aps_shared_farm.celery import app
from celery.schedules import crontab
import requests
import json
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


@shared_task
# @periodic_task(run_every=crontab(), name='create_organisation')
def sample_task():
    print("The sample task jussdfsdft ran.")


def hms_get_auth_token():
    try:
        data = {"username": "sharedfarm",
                "password": "AhXxdAlGdXPtoUZC",
                "fcm_token": "testToken"}
        res = requests.put(f"http://shurjohms.com/api-token-auth/", data=json.dumps(data))
        # headers = {'content-type': 'application/json'}
        # res = requests.post(f"{SmaxtecConfig.smaxtec_url}/users/session_token?user={email}&password={password}", headers=headers)
        token_json = res.json()
        # return token_json
        token = token_json['token']
        return token_json
    except Exception as e:
        return e


@app.task
def add(x, y):
    z = x + y
    print(z)


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        "schedule": crontab(minute="*/1"),
        'args': (16, 16)
    },
}


def signup_success_email(user, email, url):
    subject = 'welcome to adorsho praniSheba jouthoKhamar'
    # message = render_to_string('emails/signupWelcom.html', )
    # message = f'Hi {user}, thank you for registering in adrosho praniSheba jouthoKhamar.'
    htmly = get_template('emails/signupWelcom.html')
    d = {
        'user': user,
        'msg': "Thank you for registering in adrosho praniSheba jouthoKhamar. "
               "We're excited to have you get started. Just press the button below.",
        'url': url
    }
    html_content = htmly.render(d)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    msg = EmailMultiAlternatives(subject, html_content, email_from, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # print(url, "mail sent")
    # send_mail()


def order_payment_success_email(user, amount, cattle_no):
    subject = 'Payment Success Letter'
    htmly = get_template('emails/orderSuccess.html')
    d = {
        'user': user.phone,
        'to': "Dear Sir/ Madam, "
              "Congratulations!!",
        'msg': f"Welcome to adorsho praniSheba Shared Farming community. "
               "We are delighted to have you as a valuable investor on our team. ",
        'amount': f"Investment Amount: BDT.{amount} ",
        'no_of_cattle': f"Expected Number of Cattle Ownership: {cattle_no}",
        'msg_2': "We will update you on your portfolio via emails from time to time.",
    }
    html_content = htmly.render(d)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    msg = EmailMultiAlternatives(subject, html_content, email_from, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def password_reset_email(user, otp, valid_window):
    subject = 'Reset your password'
    htmly = get_template('emails/resetPassword.html')
    d = {
        'user': user.email,
        'otp': otp,
        'valid_window': valid_window,
    }
    html_content = htmly.render(d)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    msg = EmailMultiAlternatives(subject, html_content, email_from, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
