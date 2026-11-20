from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path(
        'post/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'comment/<int:comment_id>/reply/',
        views.add_reply,
        name='add_reply'
    ),
]