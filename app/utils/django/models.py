from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class AuthorTimeStampedModel(TimeStampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="작성자",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        abstract = True
