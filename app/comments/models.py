from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from posts.models import Post


class CommentManager(models.Manager):
    def get_queryset(self):
        queryset = super().filter(parent=None)
        return queryset


class Comment(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='작성자',
        on_delete=models.SET_NULL,
        null=True,
    )
    post = models.ForeignKey(
        Post,
        verbose_name='게시글',
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='부모 댓글',
        on_delete=models.PROTECT,
        null=True,
    )

    content = models.TextField(
        '내용',
    )

    class Meta:
        ordering = ['-created']
