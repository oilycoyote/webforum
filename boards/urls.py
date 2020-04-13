from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/<int:board_id>', views.topics, name='topics'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('post/', views.post, name='post'),
    path('reply_post/', views.reply_post, name='reply_post')
]