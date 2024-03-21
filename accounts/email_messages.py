from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string,get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


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

        message1 = render_to_string('messages/acc_active_email.html', {
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
        print(e)
        return None

def sendWelcomeEmail(request,user):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Your Account has been Activated'
        message = get_template('messages/acc_activated_email.html').render({
            'domain': current_site.domain,
            'user': user,
        })
        to_email = user.email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return email
    except Exception:
        return None


def sendOrderCompleteEmail(request,orders):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Your Order Has been Completed'
        message = get_template('messages/order_complete_mail.html').render({
            'user': request.user,'order':orders,
        })
        to_email = request.user.email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return email
    except Exception:
        return None


def sendPaymentFailed(request,order):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Your Payment Is invalid'
        message = get_template('messages/payment_invalid_mail.html').render({
            'user': order.user,'order':order,
        })
        to_email = order.user.email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return email
    except Exception:
        return None

def sendPaymentCompleteEmail(request,order,payment):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Your Payment Has been Completed'
        message = get_template('messages/payment_complete_mail.html').render({
            'user': order.user,'payment':payment,'order':order,
        })
        to_email = order.user.email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return email
    except Exception as e:
        print(e)
        return None
    
def sendDeliveryStartedEmail(request,order):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Your Order Delivery has Started'
        message = get_template('messages/delivery_started_mail.html').render({
            'user': order.user,'order':order,
        })
        to_email = order.user.email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return email
    except Exception as e:
        print(e)
        return None