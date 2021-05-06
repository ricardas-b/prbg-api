from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import Author, Book, Quote, Tag
from .serializers import AuthorSerializer, BookSerializer, QuoteSerializer, TagSerializer
from .utils import levenshtein_distance


QUERY_SIZE = 10


class AuthorList(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AuthorDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, context={'request': request})
        return Response(serializer.data)


class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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
        tags = Tag.objects.all()   # Fallback

        if 'starts_with' in self.request.query_params:
            substr = self.request.query_params.get('starts_with', None)
            if substr:
                tags = Tag.objects.filter(tag__startswith=substr).order_by('tag')[:QUERY_SIZE]

        elif 'contains' in self.request.query_params:
            substr = self.request.query_params.get('contains', None)
            if substr:
                tags = Tag.objects.filter(tag__contains=substr).order_by('tag')[:QUERY_SIZE]

        elif 'similar_to' in self.request.query_params:
            substr = self.request.query_params.get('similar_to', None)
            if substr:
                similar_tag_ids = []

                for tag_obj in Tag.objects.all():
                    if levenshtein_distance(tag_obj.tag, substr) <= 1:   # TODO: Implement
                        similar_tag_ids.append(tag_obj.id)

                tags = Tag.objects.filter(id__in=similar_tag_ids).order_by('tag')[:QUERY_SIZE]

        return tags


class TagDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

