import json

import bcrypt

from .models        import Book, Author, AuthorBook, User
from django.test    import TestCase
from django.test    import Client
from unittest.mock  import patch, MagicMock

class AuthorTest(TestCase):
    def setUp(self):
        Author.objects.create(
            name  = 'Brendan Eich',
            email = 'BrendanEich@gmail.com'
        )

    def tearDown(self):
        Author.objects.all().delete()

    def test_authorkview_post_success(self):
        client = Client()
        author = {
            'name'  : 'Guido van Rossum',
            'email' : 'GuidovanRossum@gmail.com'
        }
        response = client.post('/book/author', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS'
            }
        )

    def test_authorkview_post_duplicated_name(self):
        client = Client()
        author = {
            'name'  : 'Brendan Eich',
            'email' : 'GuidovanRossum@gmail.com'
        }
        response = client.post('/book/author', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATED_NAME'
            }
        )

    def test_authorkview_post_invalid_keys(self):
        client = Client()
        author = {
            'first_name'  : 'Guido van Rossum',
            'email'       : 'GuidovanRossum@gmail.com'
        }
        response = client.post('/book/author', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_KEYS'
            }
        )

class AuthorBookTest(TestCase):
    def setUp(self):
        client = Client()
        Book.objects.create(
            id    = 1,
            title = 'python'
        )

        Book.objects.create(
            id    = 2,
            title = 'javascript'
        )

        Author.objects.create(
            id    = 1,
            name  = 'Guido van Rossum',
            email = 'GuidovanRossum@gmail.com'
        )

        Author.objects.create(
            id    = 2,
            name  = 'Brendan Eich',
            email = 'BrendanEich@gmail.com'
        )

        AuthorBook.objects.create(
            book   = Book.objects.get(id=1),
            author = Author.objects.get(id=1)
        )

        AuthorBook.objects.create(
            book   = Book.objects.get(id=1),
            author = Author.objects.get(id=2)
        )

        AuthorBook.objects.create(
            book   = Book.objects.get(id=2),
            author = Author.objects.get(id=1)
        )

        AuthorBook.objects.create(
            book   = Book.objects.get(id=2),
            author = Author.objects.get(id=2)
        )

    def tearDown(self):
        Book.objects.all().delete()
        Author.objects.all().delete()
        AuthorBook.objects.all().delete()

    def test_authorbook_get_success(self):
        client   = Client()
        response = client.get('/book/author-book/1')
        self.assertEqual(response.json(),
            {
                "authors" : [
                    {'author': 1}, 
                    {'author': 2}
                ]    
            }
        )
        self.assertEqual(response.status_code, 200)  
