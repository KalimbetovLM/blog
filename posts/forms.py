from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from posts.models import Post,Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['picture','title','text']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        

