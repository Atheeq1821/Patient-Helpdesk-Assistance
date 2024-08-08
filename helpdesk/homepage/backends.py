from django.contrib.auth.backends import BaseBackend
from .models import Member

class MemberBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            member = Member.objects.get(email=email, password=password)
            return member
        except Member.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None
