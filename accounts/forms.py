from django.contrib.auth.forms import UserCreationForm

from forum.models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'avatar',)
