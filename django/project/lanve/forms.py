from django.forms import ModelForm
from django.http import request

from .models import Issue, Comment, LanveUser
from .widgets import FileInputWithPreview


# django2.2以降,Metaのなかでgroup_byのクエリに対してorderingを使わない。
# viewsでorder_byでソートする
class IssueCreateForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('question', 'situation', 'language_to')


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
        widgets = {
            'profile_pic': FileInputWithPreview,
        }
