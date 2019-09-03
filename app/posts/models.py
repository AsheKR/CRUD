from django.conf import settings
from django.db import models
from model_utils.managers import SoftDeletableManager
from model_utils.models import TimeStampedModel, SoftDeletableModel


class Post(TimeStampedModel, SoftDeletableModel, models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='작성자',
        on_delete=models.SET_NULL,
        null=True,
    )

    title = models.CharField('제목', max_length=100)
    content = models.TextField('내용')

    object = SoftDeletableManager()

    class Meta:
        ordering = ['-created']

    @property
    def comments(self):
        return self.comment_set.all()
