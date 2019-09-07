from django.db import models

from posts.models import Post
from utils.django.models import AuthorTimeStampedModel


class CommentManager(models.Manager):
    def get_queryset(self):
        queryset = super().filter(parent=None)
        return queryset


class Comment(AuthorTimeStampedModel):
    post = models.ForeignKey(Post, verbose_name="게시글", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", verbose_name="부모 댓글", on_delete=models.PROTECT, null=True
    )

    content = models.TextField("내용")

    class Meta:
        ordering = ["-created"]
