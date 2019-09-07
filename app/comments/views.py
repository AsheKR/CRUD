from django.urls import reverse_lazy

from comments.forms import CommentForm
from utils.django.forms import FormCreateView, FormUpdateView, FormDeleteView


class CommentCreateView(FormCreateView):
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy("posts:detail", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form):
        form = form.save(commit=False)
        form.parent_id = None
        form.post_id = self.kwargs.get("pk")
        return super().form_valid(form)


class CommentUpdateView(FormUpdateView):
    form_class = CommentForm
    template_name = "posts/update.html"

    def get_success_url(self):
        return reverse_lazy("posts:detail", kwargs={"pk": self.object.post_id})


class CommentDeleteView(FormDeleteView):
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy("posts:detail", kwargs={"pk": self.object.post_id})
