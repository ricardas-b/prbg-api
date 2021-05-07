from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import Author, Book, Quote, Tag
from .serializers import AuthorSerializer, BookSerializer, QuoteSerializer, TagSerializer
from .utils import levenshtein_distance


STARTS_WITH_QUERY_SIZE = 10
CONTAINS_QUERY_SIZE = 10
SIMILAR_TO_QUERY_SIZE = 5


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
                tags = Tag.objects.filter(tag__startswith=substr).order_by('tag')[:STARTS_WITH_QUERY_SIZE]

        elif 'contains' in self.request.query_params:
            substr = self.request.query_params.get('contains', None)
            if substr:
                tags = Tag.objects.filter(tag__contains=substr).order_by('tag')[:CONTAINS_QUERY_SIZE]

        elif 'similar_to' in self.request.query_params:
            substr = self.request.query_params.get('similar_to', None)

            if substr:
                items = []

                for tag_obj in Tag.objects.all():
                    # Only compare a part (the beginning) of tag string, which
                    # is sliced to the same length as search substring (this
                    # approach gives more relevant results)
                    items.append((tag_obj, levenshtein_distance(substr, tag_obj.tag[:len(substr)])))

                # Only consider tags that start with the same letter as search substring
                items = [item for item in items if item[0].tag[0] == substr[0]]

                # Sort by similarity (smallest Levenshtein distance first) and
                # then alphabetically (affects only the tags that have the same
                # similarity value)
                items.sort(key=lambda item: (item[1], item[0].tag))

                items = items[:SIMILAR_TO_QUERY_SIZE]

                # Drop tags that have Levenshtein distance > 3 to get more relevant results
                items = [item for item in items if item[1] <= 3]

                tags = [item[0] for item in items]   # Strip away tag similarity values


        return tags


class TagDetails(GenericAPIView):
    def get(self, request, pk, format=None):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

