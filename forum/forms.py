from django import forms
from tinymce.widgets import TinyMCE


class AuthorCreateForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(
        label='Contraseña', min_length=8, max_length=100, widget=forms.PasswordInput)
    password_repeat = forms.CharField(
        label='Repita contraseña', min_length=8, max_length=100, widget=forms.PasswordInput)
    avatar = forms.ImageField(label='Avatar', required=False)


class AuthorLoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(
        label='Contraseña', max_length=100, widget=forms.PasswordInput)


class PostCreateForm(forms.Form):
    post_title = forms.CharField(label='Título', max_length=100, required=True)
    post_text = forms.CharField(
        label='Mensaje', widget=TinyMCE(attrs={'cols': 40, 'rows': 30}))


class ResponseForm(forms.Form):
    response_text = forms.CharField(
        widget=TinyMCE(attrs={'cols': 40, 'rows': 30}))
