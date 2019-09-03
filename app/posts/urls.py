from django.urls import path, include

from comments.views import CommentCreateView
from .views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView

app_name = 'posts'

detail_patterns = [
    path('detail/', PostDetailView.as_view(), name="detail"),
    path('update/', PostUpdateView.as_view(), name="update"),
    path('delete/', PostDeleteView.as_view(), name="delete"),

    path('comment/', CommentCreateView.as_view(), name="comment"),
]

urlpatterns = [
    path('<int:pk>/', include(detail_patterns)),

    path('list/', PostListView.as_view(), name="list"),
    path('create/', PostCreateView.as_view(), name="create"),
]
