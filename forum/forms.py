from django.contrib.auth.forms import UserCreationForm

from forum.models import User


class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'avatar',)
