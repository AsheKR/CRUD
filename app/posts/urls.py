from django.urls import path

from .views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView

app_name = 'posts'
urlpatterns = [
    path('<int:pk>/detail/', PostDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', PostUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="delete"),
    path('list/', PostListView.as_view(), name="list"),
    path('create/', PostCreateView.as_view(), name="create"),
]
