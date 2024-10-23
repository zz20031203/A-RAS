# custom_auth_backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class PhoneAuthBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
