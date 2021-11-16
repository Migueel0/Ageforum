from typing import Text
from django import forms
from django.forms import ModelForm

from tinymce.widgets import TinyMCE

from forum.models import Discussion, Message


class MessageCreateForm(ModelForm):
    text = forms.CharField(label="Texto",
                           widget=TinyMCE(attrs={'cols': 40, 'rows': 30}),
                           required=False)

    class Meta:
        model = Message
        fields = ['text']


class DiscussionCreateForm(MessageCreateForm):
    def __init__(self, *args, **kwargs):
        super(DiscussionCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Título"
        self.fields['title'].widget.attrs['size'] = 80

    class Meta(MessageCreateForm.Meta):
        model = Discussion
        fields = ('title', 'text')


class ContactForm(forms.Form):
    email = forms.CharField(label="Tu email")
    subject = forms.CharField(label="Asunto")
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')
