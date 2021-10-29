from django import forms
from django.forms import ModelForm

from tinymce.widgets import TinyMCE

from forum.models import Discussion, Message


class MessageCreateForm(ModelForm):
    text = forms.CharField(
        widget=TinyMCE(attrs={'cols': 40, 'rows': 30}))

    class Meta:
        model = Message
        fields = ['text']


class DiscussionCreateForm(MessageCreateForm):
    class Meta(MessageCreateForm.Meta):
        model = Discussion
        fields = ('title', 'text')
