from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView,
    UserCommentListView, CommentAcceptView, CommentDeleteView, subscriptions
)

app_name = 'board'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/', UserCommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/accept/', CommentAcceptView.as_view(), name='comment-accept'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
