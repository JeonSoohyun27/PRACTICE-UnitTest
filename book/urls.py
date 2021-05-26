from django.urls import path
from .views      import AuthorView, AuthorBookView

urlpatterns = [
    path('/author', AuthorView.as_view()),
    path('/author-book/<int:book_id>', AuthorBookView.as_view()),
]
