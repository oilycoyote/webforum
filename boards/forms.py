from django import forms
from django.contrib.auth.models import User
from .models import Topic, Post, Board

class TopicNewForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        fields = ['subject']

class PostNewForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['message']