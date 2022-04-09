from django import forms
from blog.models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(max_length=250, required=True)