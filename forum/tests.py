from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timezone
from forum.forms import *
from forum.models import *


def create_author(username, email):
    """
    Create an author with the given parameters
    """
    join_date = datetime.now(tz=timezone.utc)
    last_login_date = datetime.now(tz=timezone.utc)
    return Author.objects.create(username=username, password="1234", email=email,
                                 join_date=join_date, last_login_date=last_login_date)


def create_post(author, post_title, post_text):
    """
    Create a post with the given parameters
    """
    pub_date = datetime.now(tz=timezone.utc)
    return Post.objects.create(author=author, post_title=post_title,
                               post_text=post_text, pub_date=pub_date)


class IndexViewTests(TestCase):
    def test_no_post(self):
        """"
        If no posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay posts.")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_one_post(self):
        """"
        If posts exist, post is in post_list and no error mensaje is disaplayed.
        """
        author = create_author("author", "q@q.com")
        post = create_post(author, "This is a post", "This is a post message")
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            [post],
        )
        self.assertNotContains(response, "No hay posts.")


class PostDetailViewTests(TestCase):
    def test_post_detail(self):
        """
        If posts exist, post is in post_detail must be disaplayed.
        """
        author = create_author("author", "q@q.com")
        post = create_post(author, "This is a post",
                           "This is a post message")
        response = self.client.get(
            reverse('post_detail', kwargs={'post_id': post.id}))
        self.assertEqual(response.context['post'], post)


class AuthorTests(TestCase):
    def test_author_create(self):
        """
        Creates an AuthorCreateForm and checks if it is valid.
        """
        form_data = {"username": "author",
                     "email": "q@q.com",
                     "password": "1234",
                     "password_repeat": "1234",
                     }
        form = AuthorCreateForm(form_data)
        self.assertTrue(form.is_valid())

    def test_author_without_email_create(self):
        """
        Creates a wrong AuthorCreateForm and checks if it is invalid.
        """
        form_data = {"username": "author",
                     "password": "1234",
                     "password_repeat": "1234",
                     }
        form = AuthorCreateForm(form_data)
        self.assertFalse(form.is_valid())

    def test_author_login(self):
        """
        Logins an author and checks if it is valid.
        """
        username = "author"
        password = "1234"
        create_author(username, password)
        form_data = {"username": username,
                     "password": password,
                     }
        form = AuthorLoginForm(form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('author_login_form'), form_data)
        try:
            self.assertIsNone(response.context['login_error'])
        except TypeError:
            # login_error not found in context so test has passed
            pass

#TODO add avatar test