from django import forms
from django.forms import ModelForm

from tinymce.widgets import TinyMCE

from forum.models import Discussion, Message


class MessageCreateForm(ModelForm):
    text = forms.CharField(label="Texto",
                           widget=TinyMCE(attrs={'cols': 40, 'rows': 30}),
                           required=True)

    class Meta:
        model = Message
        fields = ['text']


class DiscussionCreateForm(MessageCreateForm):
    def __init__(self, *args, **kwargs):
        super(DiscussionCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Título"

    class Meta(MessageCreateForm.Meta):
        model = Discussion
        fields = ('title', 'text')
