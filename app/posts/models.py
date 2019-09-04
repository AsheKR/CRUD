from django.db import models
from model_utils.managers import SoftDeletableManager
from model_utils.models import SoftDeletableModel

from utils.django.models import AuthorTimeStampedModel


class Post(AuthorTimeStampedModel, SoftDeletableModel):
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")

    object = SoftDeletableManager()

    class Meta:
        ordering = ["-created"]

    @property
    def comments(self):
        return self.comment_set.all()
