from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, identifier=None, password=None):
        user = None
        try:
            if "@" in identifier:
                user = CustomUser.objects.get(email=identifier)
            else:
                user = CustomUser.objects.get(phone=identifier)
        except CustomUser.DoesNotExist:
            return None

        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
