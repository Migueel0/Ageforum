from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timezone

from forum.models import Discussion, User

USERNAME = "user"
PASSWORD = "8cKk7fY9JXydWf"
EMAIL = "q@q.com"

HTTP_REDIRECT_CODE = 302
HTTP_OK_CODE = 200
HTTP_NOT_FOUND_CODE = 404


def create_user(username, email):
    """
    Create an user with the given parameters
    """
    return User.objects.create_user(username=username, password=PASSWORD, email=email,
                                    )


class AccountTests(TestCase):
    def test_sign_up_and_login_correct(self):
        """
        Test user sign up and login correctly
        """
        # sign up
        self.client.post(reverse('sign_up'), {'username': USERNAME,
                                              'email': EMAIL,
                                              'password1': PASSWORD,
                                              'password2': PASSWORD})
        self.assertEqual(User.objects.last().username, USERNAME)
        # login
        http_response = self.client.post(reverse('login'), {'username': USERNAME,
                                                            'password': PASSWORD})
        # if redirect -> logging in sucessfull
        self.assertEqual(http_response.status_code, HTTP_REDIRECT_CODE)

    def test_sign_up_incorrect_password_repeat(self):
        """
        Test user sign up with incorrect password repeat
        """
        self.client.post(reverse('sign_up'), {'username': USERNAME,
                                              'email': EMAIL,
                                              'password1': PASSWORD,
                                              'password2': "12345678"})
        self.assertEqual(User.objects.all().count(), 0)

    def test_user_detail(self):
        """
        Test user detail view
        """
        user = create_user(USERNAME, EMAIL)
        response = self.client.get(
            reverse('user_detail', kwargs={'user_id': str(user.id)}))
        self.assertEqual(response.status_code, HTTP_OK_CODE)
        self.assertContains(response, user.username)

    def test_user_detail_404(self):
        """
        Test user detail view passing a non existing user ID
        """
        user = create_user(USERNAME, EMAIL)
        response = self.client.get(
            reverse('user_detail', args=[str(user.id+1)]))
        self.assertEqual(response.status_code, HTTP_NOT_FOUND_CODE)

    def test_log_out_user(self):
        create_user(USERNAME, EMAIL)
        http_response = self.client.post(reverse('login'), {'username': USERNAME,
                                                            'password': PASSWORD})
        self.assertRedirects(http_response, '/accounts/profile/', status_code=HTTP_REDIRECT_CODE,
                             target_status_code=HTTP_OK_CODE, fetch_redirect_response=True)
        http_response = self.client.get(reverse('logout'))
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)
