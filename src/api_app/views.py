import datetime
import random

from django.db.models import Q
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import Author, Book, Quote, QuoteTag, Tag
from .serializers import AuthorSerializer, BookSerializer, QuoteSerializer, TagSerializer
from .utils import levenshtein_distance


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
                    Q(last_name__contains=substr))
            else:
                authors = authors.none()

        # Check if any filters have been applied. When a filter is applied,
        # <books> gets 'query' parameter which stores a string with an SQL
        # statement. In case of no filters:

        if not hasattr(authors, 'query'):   # Return full list of Authors in case no filtering is applied
            authors = Author.objects.all()

        return authors.order_by('last_name')


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
                    Q(subtitle__contains=substr))
            else:
                books = books.none()

        if 'year' in self.request.query_params:
            year = self.request.query_params.get('year', None)
            if year:
                try:
                    books = books.filter(year__exact=year)
                except ValueError as e:
                    books = books.none()
            else:
                books = books.none()

        if 'isbn' in self.request.query_params:
            isbn = self.request.query_params.get('isbn', None)
            if isbn:
                books = books.filter(isbn__exact=isbn)
            else:
                books = books.none()

        if 'author' in self.request.query_params:
            author = self.request.query_params.get('author', None)
            if author:
                try:
                    books = books.filter(author_id__exact=author)
                except ValueError as e:
                    books = books.none()
            else:
                books = books.none()

        if not hasattr(books, 'query'):
            books = Book.objects.all()

        return books.order_by('title')


class BookDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data)


class QuoteList(ListAPIView):
    serializer_class = QuoteSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        quotes = Quote.objects

        if 'contains' in self.request.query_params:
            substr = self.request.query_params.get('contains', None)
            if substr:
                quotes = quotes.filter(text__contains=substr)
            else:
                quotes = quotes.none()

        if 'date' in self.request.query_params:
            date = self.request.query_params.get('date', None)
            if date:
                try:
                    date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    quotes = quotes.filter(date__exact=date)
                except ValueError as e:
                    quotes = quotes.none()
            else:
                quotes = quotes.none()

        if 'author' in self.request.query_params:
            author = self.request.query_params.get('author', None)
            if author:
                try:
                    quotes = quotes.filter(author_id__exact=author)
                except ValueError as e:
                    quotes = quotes.none()
            else:
                quotes = quotes.none()

        if 'book' in self.request.query_params:
            book = self.request.query_params.get('book', None)
            if book:
                try:
                    quotes = quotes.filter(book_id__exact=book)
                except ValueError as e:
                    quotes = quotes.none()
            else:
                quotes = quotes.none()

        if 'tags' in self.request.query_params:
            tags = self.request.query_params.get('tags', None)   # Expecting URL like "quotes/?tags=1,2,3"
            if tags:
                try:
                    # Get submitted tag ids as list. Find all quotes that are
                    # tagged with *ALL* of these tags

                    # TODO: Find a way to refactor the code to make it simpler

                    submitted_tag_ids = {int(t) for t in tags.split(',')}   # For example, {10, 6}
                    quote_tag_matches = QuoteTag.objects.filter(tag_id__in=submitted_tag_ids).values_list('quote_id', 'tag_id')   # <QuerySet [(4, 6), (8, 6), (4, 10)]>
                    quote_ids = {qt[0] for qt in quote_tag_matches}   # {8, 4}
                    tags_by_quote = {id: set() for id in quote_ids}   # {8: set(), 4: set()}

                    for q_id, t_id in quote_tag_matches:   # {8: {6}, 4: {10, 6}}
                        tags_by_quote[q_id].add(t_id)

                    matching_quote_ids = []

                    for q_id, t_ids in  tags_by_quote.items():
                        if t_ids == submitted_tag_ids:   # {10, 6} == {10, 6}
                            matching_quote_ids.append(q_id)

                    quotes = quotes.filter(id__in=matching_quote_ids)

                except ValueError as e:
                    quotes = quotes.none()

            else:
                quotes = quotes.none()

        if not hasattr(quotes, 'query'):
            quotes = Quote.objects.all()

        return quotes.order_by('text')


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

        tags = Tag.objects

        if 'starts_with' in self.request.query_params:
            substr = self.request.query_params.get('starts_with', None)
            if substr:
                tags = tags.filter(name__startswith=substr)
            else:
                tags = tags.none()

        if 'contains' in self.request.query_params:
            substr = self.request.query_params.get('contains', None)
            if substr:
                tags = tags.filter(name__contains=substr)
            else:
                tags = tags.none()

        if 'similar_to' in self.request.query_params:
            substr = self.request.query_params.get('similar_to', None)

            if substr:
                selected_items = []

                #for tag_obj in Tag.objects.all():
                for tag_obj in tags.all():

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

            else:
                tags = tags.none()
        
        if not hasattr(tags, 'query'):
            tags = Tag.objects.all()

        return tags.order_by('name')


class TagDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)


class RandomQuoteDetails(GenericAPIView):
    def get(self, request, format=None):
        pks = Quote.objects.values_list('pk', flat=True)
        random_pk = random.choice(pks)
        random_quote = Quote.objects.get(pk=random_pk)
        serializer = QuoteSerializer(random_quote, context={'request': request})
        return Response(serializer.data)