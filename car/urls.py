from django.urls import path
from . import views
from .views import (PostListView, 
                    PostDetailView, 
                    PostCreateView, 
                    PostUpdateView, 
                    PostDeleteView, 
                    UserPostListView,
                    CommentCreateView,
                    CommentDeleteView)

urlpatterns = [
    path('', PostListView.as_view(), name = 'car-home'),
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('post_like/<int:pk>', views.post_like, name = "post_like"),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name = 'post_comment'),
    path('post/<int:pk>/comment/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    path('about/', views.about, name = 'car-about'),
]