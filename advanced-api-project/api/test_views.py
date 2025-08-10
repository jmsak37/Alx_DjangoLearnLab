# api/test_views.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book

User = get_user_model()

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user. Handle both default User (username) and custom user (email).
        self.password = 'testpass123'
        try:
            # prefer creating with email if the custom user requires it
            self.user = User.objects.create_user(
                email='testuser@example.com',
                password=self.password
            )
        except TypeError:
            # fallback for default user that expects username
            self.user = User.objects.create_user(
                username='testuser',
                password=self.password
            )

        # Create authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Stephen King')

        # Create books
        self.book1 = Book.objects.create(
            title='First Book', publication_year=2000, author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Shining', publication_year=1977, author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Another Book', publication_year=2010, author=self.author1
        )

        # Base endpoints (update if your URLs differ)
        self.list_url = '/api/books/'
        self.detail_url = lambda pk: f'/api/books/{pk}/'

    def do_login(self):
        """
        Try logging in with username first, else with email.
        Returns True if login succeeded.
        """
        # Try username login if user has username attribute (and it's not empty)
        if getattr(self.user, 'username', None):
            ok = self.client.login(username=self.user.username, password=self.password)
            if ok:
                return True

        # Try email login (useful if AUTH_USER_MODEL uses email as USERNAME_FIELD)
        if getattr(self.user, 'email', None):
            ok = self.client.login(email=self.user.email, password=self.password)
            if ok:
                return True

        # Last resort: try username with 'username' key even if empty (may still work)
        return self.client.login(username=getattr(self.user, 'username', ''), password=self.password)

    def test_client_login_works(self):
        """Smoke test: ensure self.client.login can authenticate the test user."""
        logged_in = self.do_login()
        self.assertTrue(logged_in, "self.client.login failed — check user creation and AUTHENTICATION backends")

    def test_list_books_returns_all(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 3)

    def test_filter_books_by_publication_year(self):
        resp = self.client.get(self.list_url, {'publication_year': 2000})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b.get('title') for b in resp.data]
        self.assertIn('First Book', titles)
        self.assertNotIn('The Shining', titles)

    def test_search_books_by_title_or_author(self):
        resp_title = self.client.get(self.list_url, {'search': 'Shining'})
        self.assertEqual(resp_title.status_code, status.HTTP_200_OK)
        titles = [b.get('title') for b in resp_title.data]
        self.assertIn('The Shining', titles)

        resp_author = self.client.get(self.list_url, {'search': 'Stephen'})
        self.assertEqual(resp_author.status_code, status.HTTP_200_OK)
        titles2 = [b.get('title') for b in resp_author.data]
        self.assertIn('The Shining', titles2)

    def test_ordering_books_by_publication_year(self):
        resp = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b.get('publication_year') for b in resp.data if 'publication_year' in b]
        if len(years) >= 2:
            self.assertTrue(all(years[i] >= years[i+1] for i in range(len(years)-1)))

    def test_create_book_using_client_login(self):
        # use self.client.login rather than force_authenticate
        self.assertTrue(self.do_login(), "login failed in create test")
        payload = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author1.id
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))
        exists = Book.objects.filter(title='New Book', publication_year=2021).exists()
        self.assertTrue(exists)

    def test_update_book_using_client_login(self):
        self.assertTrue(self.do_login(), "login failed in update test")
        payload = {'title': 'First Book (Updated)', 'publication_year': 2000, 'author': self.author1.id}
        resp = self.client.put(self.detail_url(self.book1.id), payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'First Book (Updated)')

    def test_delete_book_using_client_login(self):
        self.assertTrue(self.do_login(), "login failed in delete test")
        resp = self.client.delete(self.detail_url(self.book2.id))
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        exists = Book.objects.filter(pk=self.book2.id).exists()
        self.assertFalse(exists)
