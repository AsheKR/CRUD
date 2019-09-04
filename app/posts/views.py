from django.urls import reverse_lazy

from comments.forms import CommentForm
from utils.django.forms import FormListView, FormCreateView, FormDetailView, FormUpdateView, FormDeleteView
from .form import PostForm


class PostListView(FormListView):
    form_class = PostForm


class PostCreateView(FormCreateView):
    form_class = PostForm
    success_url = reverse_lazy('posts:list')


class PostDetailView(FormDetailView):
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'comment_form': CommentForm,
        })
        return context_data


class PostUpdateView(FormUpdateView):
    form_class = PostForm
    view_name = 'posts:detail'


class PostDeleteView(FormDeleteView):
    form_class = PostForm
    success_url = reverse_lazy('posts:list')
