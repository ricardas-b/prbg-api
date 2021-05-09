import datetime

from django.db.models import Q
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import Author, Book, Quote, Tag
from .serializers import AuthorSerializer, BookSerializer, QuoteSerializer, TagSerializer
from .utils import levenshtein_distance


SIMILAR_TO_QUERY_SIZE = 50


class AuthorList(ListAPIView):
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        authors = Author.objects

        if 'contains' in self.request.query_params:
            substr = self.request.query_params.get('contains', None)
            if substr:
                authors = authors.filter(
                    Q(first_name__contains=substr) |
                    Q(middle_name__contains=substr) |
                    Q(last_name__contains=substr)).order_by('last_name')

        if not hasattr(authors, 'query'):   # Return full list of Authors in case no filtering is applied
            authors = Author.objects.all()

        return authors


class AuthorDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, context={'request': request})
        return Response(serializer.data)


class BookList(ListAPIView):
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        books = Book.objects

        if 'contains' in self.request.query_params:
            substr = self.request.query_params.get('contains', None)
            if substr:
                books = books.filter(
                    Q(title__contains=substr) |
                    Q(subtitle__contains=substr)).order_by('title')

        if 'year' in self.request.query_params:
            year = self.request.query_params.get('year', None)
            if year:
                books = books.filter(year__exact=year).order_by('title')

        if 'isbn' in self.request.query_params:
            isbn = self.request.query_params.get('isbn', None)
            books = books.filter(isbn__exact=isbn).order_by('title')

        if 'author' in self.request.query_params:
            author = self.request.query_params.get('author', None)
            books = books.filter(author_id__exact=author).order_by('title')

        # Check if any filters have been applied. When a filter is applied,
        # <books> gets 'query' parameter which stores a string with an SQL
        # statement. In case of no filters:

        if not hasattr(books, 'query'):
            books = Book.objects.all()

        return books


class BookDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)


class QuoteList(ListAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class QuoteDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        quote = Quote.objects.get(pk=pk)
        serializer = QuoteSerializer(quote, context={'request': request})
        return Response(serializer.data)


class TagList(ListAPIView):
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        ''' Tags can be filtered down by providing search keywords (like
            "starts_with", "contains", "similar_to") to specify the type of
            search and a search string. For example, tags/?similar_to=kultur '''

        tags = Tag.objects.all()

        if 'starts_with' in self.request.query_params:
            substr = self.request.query_params.get('starts_with', None)
            if substr:
                tags = Tag.objects.filter(tag__startswith=substr).order_by('tag')

        elif 'contains' in self.request.query_params:
            substr = self.request.query_params.get('contains', None)
            if substr:
                tags = Tag.objects.filter(tag__contains=substr).order_by('tag')

        elif 'similar_to' in self.request.query_params:
            substr = self.request.query_params.get('similar_to', None)

            if substr:
                selected_items = []

                for tag_obj in Tag.objects.all():

                    # Only consider tags that start with the same letter as search substring
                    if tag_obj.tag[0] == substr[0]:

                        # Only compare a part (the beginning) of tag string, which
                        # is sliced to the same length as search substring (this
                        # approach gives more relevant results)
                        selected_items.append((tag_obj, levenshtein_distance(substr, tag_obj.tag[:len(substr)])))

                # Sort by similarity (smallest Levenshtein distance first) and
                # then alphabetically (affects only the tags that have the same
                # similarity value)
                selected_items.sort(key=lambda item: (item[1], item[0].tag))

                # Drop tags that have Levenshtein distance > 3 to get more relevant results
                selected_items = [item for item in selected_items if item[1] <= 2]

                tags = [item[0] for item in selected_items]   # Strip away tag similarity values

        return tags


class TagDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

