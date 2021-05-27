from django.urls import path

from . import views



urlpatterns = [
    path('authors/', views.AuthorList.as_view(), name='list-of-authors'),
    path('books/', views.BookList.as_view(), name='list-of-books'),
    path('quotes/', views.QuoteList.as_view(), name='list-of-quotes'),
    path('tags/', views.TagList.as_view(), name='list-of-tags'),
    path('authors/<int:pk>/', views.AuthorDetails.as_view(), name='author-details'),
    path('books/<int:pk>/', views.BookDetails.as_view(), name='book-details'),
    path('quotes/<int:pk>/', views.QuoteDetails.as_view(), name='quote-details'),
    path('tags/<int:pk>/', views.TagDetails.as_view(), name='tag-details'),
    path('quotes/random/', views.RandomQuoteDetails.as_view(), name='random-quote-details'),

]