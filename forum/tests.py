from datetime import datetime, timezone
from django.http.response import HttpResponse

from django.test import TestCase
from django.urls import reverse

from forum.models import Discussion, Response, User
from forum.views import DISCUSSION_CREATE_TEMPLATE, INDEX_ROUTE

USERNAME = "user"
PASSWORD = "8cKk7fY9JXydWf"
EMAIL = "q@q.com"

HTTP_REDIRECT_CODE = 302
HTTP_OK_CODE = 200
HTTP_FORBIDDEN = 403

DISCUSSION_CREATE_URL_NAME = 'discussion_create'
RESPONSE_CREATE_URL_NAME = 'response_create'
LOGIN_URL_NAME = 'login'

DISCUSSION_TITLE = 'Discussion title'
NO_DISCUSSIONS_MESSAGE = "No hay discusiones"
LOREM_IPSUM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'


def create_user(username, email):
    """
    Create an user with the given parameters
    """
    return User.objects.create_user(username=username, password=PASSWORD, email=email)


def create_discussion(user, discussion_title, discussion_text):
    """
    Create a discussion with the given parameters
    """
    date_publication = datetime.now(tz=timezone.utc)
    return Discussion.objects.create(user=user, title=discussion_title,
                                     text=discussion_text, date_publication=date_publication)


def create_response(user, discussion, response_text):
    """
    Create a response for a discussion with the given parameters
    """
    date_publication = datetime.now(tz=timezone.utc)
    return Response.objects.create(user=user, topic=discussion,
                                   text=response_text, date_publication=date_publication)


class IndexViewTests(TestCase):
    def test_no_posts(self):
        """"
        If no posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, HTTP_OK_CODE)
        self.assertContains(response, NO_DISCUSSIONS_MESSAGE)
        self.assertQuerysetEqual(response.context['discussion_list'], [])

    def test_one_discussion(self):
        """
        If posts exist, post is in post_list and no error mensaje is disaplayed
        """
        user = create_user(USERNAME, EMAIL)
        discussion = create_discussion(
            user, "This is a post", "This is a post message")
        http_response_get = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            http_response_get.context['discussion_list'],
            [discussion],
        )
        self.assertEqual(http_response_get.status_code, HTTP_OK_CODE)
        self.assertNotContains(http_response_get, NO_DISCUSSIONS_MESSAGE)

    def test_one_hundred_discussions(self):
        """
        Create one hundred post and check they are stored properly
        """
        user = create_user(USERNAME, EMAIL)
        for _ in range(100):
            create_discussion(
                user, "This is a post", "This is a post message")
        http_response_get = self.client.get(reverse('index'))
        self.assertEqual(
            len(http_response_get.context['discussion_list']),
            100)


class DiscussionCreateViewTests(TestCase):
    def test_discussion_create_get_logged_in(self):
        """
        Check if accessing to Discussion create page with logged user shows creation form
        """
        create_user(USERNAME, EMAIL)
        # user login
        self.client.post(reverse(LOGIN_URL_NAME), {'username': USERNAME,
                                                   'password': PASSWORD})
        http_response = self.client.get(
            reverse(DISCUSSION_CREATE_URL_NAME))
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)
        self.assertContains(http_response, '<form')

    def test_discussion_create_post_logged_in(self):
        """
        Check if posting to Discussion create page creates discussion and shows it
        """
        create_user(USERNAME, EMAIL)
        # user login
        self.client.post(reverse(LOGIN_URL_NAME), {'username': USERNAME,
                                                   'password': PASSWORD})
        http_response = self.client.post(reverse(DISCUSSION_CREATE_URL_NAME), {'title': DISCUSSION_TITLE,
                                                                               'text': LOREM_IPSUM})
        self.assertRedirects(http_response, INDEX_ROUTE + '1', status_code=HTTP_REDIRECT_CODE,
                             target_status_code=HTTP_OK_CODE, fetch_redirect_response=True)

    def test_discussion_create_not_logged_in(self):
        """
        HTTP 403 forbidden must be raised when accessing discussion create without user logged in
        """
        http_response = self.client.get(reverse(DISCUSSION_CREATE_URL_NAME))
        self.assertTrue(http_response.status_code, HTTP_FORBIDDEN)


class ResponseCreateViewTests(TestCase):
    def test_response_create_not_logged_in(self):
        """
        HTTP 403 forbidden must be raised when accessing response create without user logged in
        """
        http_response = self.client.get(reverse(RESPONSE_CREATE_URL_NAME, kwargs={
                                        'discussion_id': str(0)}))
        self.assertTrue(http_response.status_code, HTTP_FORBIDDEN)

    def test_discussion_create_get_logged_in(self):
        """
        Check if accessing to Discussion create page with logged user shows creation form
        """
        create_user(USERNAME, EMAIL)
        # user login
        self.client.post(reverse(LOGIN_URL_NAME), {'username': USERNAME,
                                                   'password': PASSWORD})
        self.client.post(reverse(DISCUSSION_CREATE_URL_NAME),
                         {'title': DISCUSSION_TITLE,
                          'text': LOREM_IPSUM})
        http_response = self.client.get(reverse(RESPONSE_CREATE_URL_NAME, kwargs={
                                        'discussion_id': '1'}))
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)
        self.assertContains(http_response, '<form')

    def test_response_create_post_logged_in(self):
        """
        Check if posting to answering create Response and show it
        """
        create_user(USERNAME, EMAIL)
        # user login
        self.client.post(reverse(LOGIN_URL_NAME), {'username': USERNAME,
                                                   'password': PASSWORD})
        self.client.post(reverse(DISCUSSION_CREATE_URL_NAME), {'title': DISCUSSION_TITLE,
                                                               'text': LOREM_IPSUM})
        http_response = self.client.post(
            reverse(RESPONSE_CREATE_URL_NAME, kwargs={'discussion_id': '1'}), {'text': LOREM_IPSUM})
        self.assertRedirects(http_response, INDEX_ROUTE + '1', status_code=HTTP_REDIRECT_CODE,
                             target_status_code=HTTP_OK_CODE, fetch_redirect_response=True)


class DiscussionDetailViewTests(TestCase):
    def test_discussion_detail(self):
        """
        Check if Discussion detail show created Response
        """
        create_user(USERNAME, EMAIL)
        self.client.post(reverse(LOGIN_URL_NAME), {'username': USERNAME,
                                                   'password': PASSWORD})
        self.client.post(reverse(DISCUSSION_CREATE_URL_NAME), {'title': DISCUSSION_TITLE,
                                                               'text': 'Discussion title'})
        self.client.post(
            reverse(RESPONSE_CREATE_URL_NAME, kwargs={'discussion_id': '1'}), {'text': LOREM_IPSUM})
        http_response: HttpResponse = self.client.get(
            reverse('discussion_detail', kwargs={'discussion_id': '1'}))
        self.assertEqual(http_response.status_code, HTTP_OK_CODE)
        self.assertContains(http_response, LOREM_IPSUM)


    