from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)

app_name = 'board'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # noqa: E501
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # noqa: E501
]
