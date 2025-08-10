# api/test_views.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book

User = get_user_model()

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user (used for authenticated operations)
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
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

        # Base endpoints (adjust if your urls differ)
        self.list_url = '/api/books/'
        self.detail_url = lambda pk: f'/api/books/{pk}/'

    def test_list_books_returns_all(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # expect at least the 3 we created
        self.assertGreaterEqual(len(resp.json()), 3)

    def test_filter_books_by_publication_year(self):
        resp = self.client.get(self.list_url, {'publication_year': 2000})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # Only book1 has publication_year=2000
        titles = [b.get('title') for b in data]
        self.assertIn('First Book', titles)
        self.assertNotIn('The Shining', titles)

    def test_search_books_by_title_or_author(self):
        # search by a title word
        resp_title = self.client.get(self.list_url, {'search': 'Shining'})
        self.assertEqual(resp_title.status_code, status.HTTP_200_OK)
        titles = [b.get('title') for b in resp_title.json()]
        self.assertIn('The Shining', titles)

        # search by author name
        resp_author = self.client.get(self.list_url, {'search': 'Stephen'})
        self.assertEqual(resp_author.status_code, status.HTTP_200_OK)
        titles2 = [b.get('title') for b in resp_author.json()]
        self.assertIn('The Shining', titles2)

    def test_ordering_books_by_publication_year(self):
        resp = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        years = [b.get('publication_year') for b in data if 'publication_year' in b]
        # ensures descending ordering
        self.assertTrue(all(years[i] >= years[i+1] for i in range(len(years)-1)))

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author1.id
        }
        resp = self.client.post(self.list_url, payload, format='json')
        # Accept either 201 (created) or 200 depending on your view config
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))
        # verify it exists in DB
        exists = Book.objects.filter(title='New Book', publication_year=2021).exists()
        self.assertTrue(exists)

    def test_update_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        payload = {'title': 'First Book (Updated)', 'publication_year': 2000, 'author': self.author1.id}
        resp = self.client.put(self.detail_url(self.book1.id), payload, format='json')
        # Accept 200 or 202 depending on implementation
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'First Book (Updated)')

    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(self.detail_url(self.book2.id))
        # Accept 204 or 200 depending on implementation
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        exists = Book.objects.filter(pk=self.book2.id).exists()
        self.assertFalse(exists)
