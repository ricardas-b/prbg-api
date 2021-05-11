from rest_framework import serializers

from .models import Author, Book, Quote, Tag, QuoteTag


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'nationality']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(view_name='author-details', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'author', 'title', 'subtitle', 'year', 'publisher', 'isbn']


class TagListField(serializers.Field):
    ''' A custom field which contains a list of <Tag> values of a particular <Quote> '''

    def to_representation(self, quote_id):
        tag_ids = QuoteTag.objects.filter(quote_id=quote_id).values_list('tag_id')
        items = Tag.objects.filter(pk__in=tag_ids).values_list('id', 'tag')
        tags = [{'id': id, 'tag': tag} for id, tag in items]
        return tags

    def to_internal_value(self, data):
        raise NotImplementedError


class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(view_name='author-details', read_only=True)
    book = serializers.HyperlinkedRelatedField(view_name='book-details', read_only=True)
    tags = TagListField(source='id')   # Custom field, not present in the <Quote> model

    class Meta:
        model = Quote
        fields = ['id', 'text', 'author', 'book', 'date', 'language', 'length_in_words', 'editors_comment', 'rating', 'tags']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag']

