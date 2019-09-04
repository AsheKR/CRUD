from django.urls import path, include

from comments.views import CommentUpdateView, CommentDeleteView

app_name = 'comments'

detail_patterns = [
    path('update/', CommentUpdateView.as_view(), name="update"),
    path('delete/', CommentDeleteView.as_view(), name="delete"),
]

urlpatterns = [
    path('<int:pk>/', include(detail_patterns)),
]
