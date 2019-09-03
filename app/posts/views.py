from django.urls import reverse_lazy

from utils.django.forms import FormListView, FormCreateView, FormDetailView, FormUpdateView, FormDeleteView
from .form import PostForm


class PostListView(FormListView):
    form_class = PostForm


class PostCreateView(FormCreateView):
    form_class = PostForm
    success_url = reverse_lazy('posts:list')


class PostDetailView(FormDetailView):
    form_class = PostForm


class PostUpdateView(FormUpdateView):
    form_class = PostForm
    success_redirect_with_kwargs = 'posts:detail'


class PostDeleteView(FormDeleteView):
    form_class = PostForm
    success_url = reverse_lazy('posts:list')
