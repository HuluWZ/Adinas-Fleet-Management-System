from django import template
from rest_framework.authtoken.models import Token
from accounts.authentication import JWTAuthentication

register = template.Library()

# create_or_get_auth_token
@register.filter
def cog_auth_token(user):
    token = JWTAuthentication.create_jwt(user) 
    return token