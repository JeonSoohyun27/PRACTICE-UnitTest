import json
import jwt
import requests
from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Book, Author, AuthorBook, User

class AuthorView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Author.objects.filter(name = data["name"]).exists():
                return JsonResponse({'message':'DUPLICATED_NAME'}, status = 400)
            
            Author(
                name  = data['name'],
                email = data['email']
            ).save()
            return JsonResponse({'message':'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class AuthorBookView(View):
    def get(self, request, book_id):
        try:
            if Book.objects.filter(id = book_id).exists():
                book    = Book.objects.get(id = book_id)
                authors = list(AuthorBook.objects.filter(book = book).values('author'))
                return JsonResponse({'authors':authors}, status = 200)
            
            return JsonResponse({'message':'NO_AUTHOR'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

