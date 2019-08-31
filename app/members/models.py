from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class Member(AbstractUser):
    name = CharField("닉네임", blank=True, max_length=20)
