from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField('Author', through = 'AuthorBook')

    class Meta:
        db_table = 'books'

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        db_table = 'authors'

class AuthorBook(models.Model):
    book = models.ForeignKey('Book', on_delete= models.SET_NULL, null=True)
    author = models.ForeignKey('Author', on_delete= models.SET_NULL, null=True)

    class Meta:
        db_table = 'author_book'

class User(models.Model):
    kakao       = models.IntegerField(null=True)
    facebook    = models.IntegerField(null=True)
    nick_name   = models.CharField(max_length=25, unique=True)
    email       = models.CharField(max_length=50, null=True, unique=True)
    password    = models.CharField(max_length=400, null=True)

    class Meta:
        db_table = 'users'
