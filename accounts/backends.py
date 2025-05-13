from django.contrib.auth.backends import ModelBackend
from .models import User


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email')

        if email is None or password is None:
            return
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class MobileBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        mobile = kwargs.get('mobile')

        if mobile is None:
            return
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            User().set_password(mobile)
        else:
            if self.user_can_authenticate(user):
                return user
