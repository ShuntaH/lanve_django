from django.forms import ModelForm
from django.http import request

from .models import Issue, Comment, LanveUser


class IssueCreateForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('question', 'situation')


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserUpdateForm(ModelForm):
    class Meta:
        model = LanveUser
        fields = (
            'username',
            'profile_pic',
            'residence',
        )
