from django.contrib.auth.backends import ModelBackend
from .models import MUsua

class MUsuaBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MUsua.objects.get(usua_chlogusu=username)
        except MUsua.DoesNotExist:
            return None
        
        if user.usua_chpasusu == password:
            return user
        else:
            return None