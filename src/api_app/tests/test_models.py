from django.test import TestCase

from api_app.models import Author, Book, Quote, QuoteTag, Tag



class ModelStringRepresentationTests(TestCase):
    fixtures = [
        'api_app/tests/fixtures/authors.json',
        'api_app/tests/fixtures/books.json',
        'api_app/tests/fixtures/quotes.json',
        'api_app/tests/fixtures/quote_tags.json',
        'api_app/tests/fixtures/tags.json',
        ]

    def test_author_model(self):
        author_with_full_name = Author.objects.get(pk=1)
        author_with_middle_name = Author.objects.get(pk=2)
        author_with_last_name = Author.objects.get(pk=3)
        self.assertEqual(str(author_with_full_name), 'William Shakespeare')
        self.assertEqual(str(author_with_middle_name), 'Ernest Miller Hemingway')
        self.assertEqual(str(author_with_last_name), 'Vydūnas')

    def test_book_model(self):
        book = Book.objects.get(pk=2)
        self.assertEqual(str(book), 'The Old Man and the Sea')

    def test_quote_model(self):
        short_quote = Quote.objects.get(pk=1)
        long_quote = Quote.objects.get(pk=2)
        self.assertEqual(str(short_quote), '[William Shakespeare] To be or not to be, that is the question.')
        self.assertEqual(str(long_quote), '[Ernest Miller Hemingway] But man is not made for defeat. A man can be destroyed but not d...')

    def test_tag_model(self):
        tag = Tag.objects.get(pk=1)
        self.assertEqual(str(tag), 'sea')

    def test_quote_tag_model(self):
        quote_tag = QuoteTag.objects.get(pk=1)
        self.assertEqual(str(quote_tag), '[prince] [William Shakespeare] To be or not to be, that is the question.')
        
        

        
