from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timezone
from accounts.views import ROOT_URL

from forum.models import Discussion, User

USERNAME = "user"
PASSWORD = "8cKk7fY9JXydWf"
EMAIL = "q@q.com"

HTTP_REDIRECT_CODE = 302
HTTP_OK_CODE = 200
HTTP_NOT_FOUND_CODE = 404
HTTP_FORBIDDEN_CODE = 403

CHANGE_PROFILE_URL_NAME = 'change_user_detail'


def create_user(username, email):
    """
    Create an user with the given parameters
    """
    return User.objects.create_user(username=username, password=PASSWORD, email=email,
                                    )


def login_user(self, username, password):
    return self.client.post(reverse('login'), {'username': username,
                                               'password': password})


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
        """
        Test user logout
        """
        create_user(USERNAME, EMAIL)
        http_response = login_user(self, USERNAME, PASSWORD)
        self.assertRedirects(http_response, '/accounts/profile/', status_code=HTTP_REDIRECT_CODE,
                             target_status_code=HTTP_OK_CODE, fetch_redirect_response=True)
        http_response = self.client.get(reverse('logout'))
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)

    def test_edit_user_get(self):
        """
        Test user editing get page
        """
        create_user(USERNAME, EMAIL)
        login_user(self, USERNAME, PASSWORD)
        http_response = self.client.get(reverse(CHANGE_PROFILE_URL_NAME))
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)

    def test_edit_user_post(self):
        """
        Test user editing post page
        """
        create_user(USERNAME, EMAIL)
        login_user(self, USERNAME, PASSWORD)
        new_username = "user10"
        http_response = self.client.post(reverse(CHANGE_PROFILE_URL_NAME), {
                                         'username': new_username})
        self.assertRedirects(http_response, '/accounts/profile/', status_code=HTTP_OK_CODE,
                             target_status_code=HTTP_OK_CODE, fetch_redirect_response=True)
        http_response = self.client.get(reverse('logout'))
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)
        http_response = login_user(self, new_username, PASSWORD)
        self.assertEqual(http_response.status_code, HTTP_REDIRECT_CODE)

    def test_edit_user_without_user_logged_in(self):
        """
        Test user editing post page without user logged in
        """
        http_response = self.client.get(reverse(CHANGE_PROFILE_URL_NAME))
        self.assertRedirects(http_response, ROOT_URL, status_code=HTTP_REDIRECT_CODE,
                             target_status_code=HTTP_OK_CODE, fetch_redirect_response=True)

    def test_edit_user_unathorized_method(self):
        """
        Test user editing with unathorized HTTP method (PUT)
        """
        create_user(USERNAME, EMAIL)
        login_user(self,USERNAME,PASSWORD)
        http_response = self.client.put(reverse(CHANGE_PROFILE_URL_NAME))
        self.assertEqual(http_response.status_code, HTTP_FORBIDDEN_CODE)

    def test_edit_user_empty_username(self):
        """
        Test user editing post page with empty username
        """
        create_user(USERNAME, EMAIL)
        login_user(self, USERNAME, PASSWORD)
        http_response = self.client.post(reverse(CHANGE_PROFILE_URL_NAME), {
                                         'username': ''})
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)
        self.assertContains(http_response,'text-danger')

    def test_edit_user_username_already_exists(self):
        """
        Test user editing post page with an existing username
        """
        create_user(USERNAME, EMAIL)
        create_user('admin', 'admin@qwe.com')
        login_user(self, USERNAME, PASSWORD)
        http_response = self.client.post(reverse(CHANGE_PROFILE_URL_NAME), {
                                         'username': 'admin'})
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)
        self.assertContains(http_response,'existe')