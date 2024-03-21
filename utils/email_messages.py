from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string,get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def sendUpcomingAndEndingEmail(to_email,event_type,data):
    try:
        mail_subject = f""" {event_type} Vehicle Booking Request - Action Required."""
        message = get_template('messages/upcoming_email.html').render({
            'data':data,
            "domain":"https://adinascarrent.com",        
            'subject': mail_subject
        })
        email = EmailMessage(
        mail_subject, message, to=to_email
        )
        email.content_subtype = "html"
        email.send()
        return email
    except Exception as e:
        return e



def sendEmailOTP(request,user,message):
    try:
        current_site = get_current_site(request)
        mail_subject = 'One Time Password Verification Required.'
        message = get_template('messages/otp_email.html').render({
            'user': user,
            'domain': current_site.domain,
            'message': message,
        })
        to_email = user.email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return email
    except Exception as e:
        return e
    
def sendEmailVerification(request,user):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Email Verification Required.'
        message = get_template('messages/acc_active_email.html').render({
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return email
    except Exception as e:
        return e
 