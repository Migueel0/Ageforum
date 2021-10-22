from django import forms

class AuthorCreateForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)
    passwordRepeat = forms.CharField(label='Repita contraseña', max_length=100, widget=forms.PasswordInput)
    avatar = forms.ImageField(label='Avatar', max_length=100, required=False)

class AuthorLoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)

class PostCreateForm(forms.Form):
    post_title = forms.CharField(label='Título', max_length=100, required=True)
    post_text = forms.CharField(label='Mensaje', widget=forms.Textarea)