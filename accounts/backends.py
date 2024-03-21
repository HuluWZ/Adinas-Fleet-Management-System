from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned

import logging

UserModel = get_user_model()
logger = logging.getLogger(__name__)
class AFMSAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if password is not None:
            return self.authenticate_username_password(username, password)
        else:
            return self.authenticate_otp(request, username)

    def authenticate_username_password(self, username, password):
        try:
            # Find the user by username or email
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
            logger.debug("User found: %s", user)
        except UserModel.DoesNotExist:
            logger.debug("User not found for username/email: %s", username)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            logger.debug("Authentication successful for user: %s", user)
            return user
        else:
            logger.debug("Authentication failed for user: %s", user)
            return None

    def authenticate_otp(self, request, phone_number):
        try:
            # Find the user by phone_number
            user = UserModel.objects.get(phone_number__iexact=phone_number)
            logger.debug("User found for OTP: %s", user)
        except UserModel.DoesNotExist:
            logger.debug("User not found for phone number: %s", phone_number)
            return None
        except UserModel.MultipleObjectsReturned:
            logger.error("Multiple users found for the given phone number: %s", phone_number)
            return None

        if self.user_can_authenticate(user):
            logger.debug("Authentication successful for user: %s", user)
            return user
        else:
            logger.debug("Authentication failed for user: %s", user)
            return None
    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None