
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import EmailField
from tinymce.widgets import TinyMCE
from forum.models import Message, User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'avatar',)


class EditForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Dirección de correo electrónico", required=True)
    avatar = forms.ImageField(required=False)
    biography = forms.CharField(label = "Biografía",
                                widget=forms.Textarea,
                                required=False)

