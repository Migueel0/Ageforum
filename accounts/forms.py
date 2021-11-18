
from django import forms
from django.contrib.auth.forms import UserCreationForm
from tinymce.widgets import TinyMCE
from forum.models import Message, User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'avatar',)


class EditForm(forms.Form):
    username = forms.CharField()
    avatar = forms.ImageField(required=False)
    biography = forms.CharField(label = "Biografía",
                                widget=forms.Textarea,
                                required=False)

