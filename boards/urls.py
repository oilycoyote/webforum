from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topic/<int:board_id>', views.topics, name='topics'),
    path('topic/<int:board_id>/new_topic', views.new_topic, name='new_topic'),
    path('post/<int:topic_id>', views.post, name='post'),
    path('post/<int:topic_id>/reply_post', views.reply_post, name='reply_post'),
    path('post/<int:post_id>/edit_post', views.edit_post, name='edit_post')
]