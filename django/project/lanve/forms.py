from django.forms import ModelForm
from django.http import request

from .models import Issue


class IssueCreateForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('question', 'situation')
