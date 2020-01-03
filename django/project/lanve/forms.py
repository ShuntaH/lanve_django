from django.forms import ModelForm
from django.http import request

from .models import Issue, Comment


class IssueCreateForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('question', 'situation')


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'contributor')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['contributor'].widget.attrs['value'] = self.request.user

