from django.contrib.auth.backends import BaseBackend
from .models import MUsua

class MUsuaBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = MUsua.objects.get(usua_chlogusu=username)
            if user.check_password(password):
                return user
        except MUsua.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return MUsua.objects.get(pk=user_id)
        except MUsua.DoesNotExist:
            return None