from django.contrib.auth.backends import ModelBackend
from .models import User
from core.logger import logger


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email')

        if email is None or password is None:
            logger.warning("Email or password is missing in authentication attempt")
            return
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f"Authentication failed - Email not found: {email}")
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                logger.info(f"Successful email authentication for user: {user.username}")
                return user
            logger.warning(f"Authentication failed - Invalid password for email: {email}")


class MobileBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        mobile = kwargs.get('mobile')

        if mobile is None:
            logger.warning("Mobile number is missing in authentication attempt")
            return
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            logger.warning(f"Authentication failed - Mobile number not found: {mobile}")
            User().set_password(mobile)
        else:
            if self.user_can_authenticate(user):
                logger.info(f"Successful mobile authentication for user: {user.username}")
                return user
            logger.warning(f"Authentication failed - User cannot authenticate: {user.username}")
