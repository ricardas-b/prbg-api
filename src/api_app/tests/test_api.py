from django.http import QueryDict
from django.urls import reverse
from rest_framework.test import APITestCase


class TestAuthorsResource(APITestCase):
    fixtures = [
        'authors.json',
        ]
    
    def test_get_request_can_fetch_all_authors(self):
        response_payload = self.client.get(reverse('list-of-authors')).json()
        author_count = len(response_payload['results'])
        self.assertEquals(author_count, 3)

    def test_get_request_can_fetch_authors_filtered_by_full_name_contains(self):
        inputs = ['liam', 'Mill', 'Vyd', ]   # Use substrings from first, middle, and last names
        
        for input_ in inputs:
            query = QueryDict(f'contains={input_}')
            response_payload = self.client.get(f"{reverse('list-of-authors')}?{query.urlencode()}").json()
            author_count = len(response_payload['results'])
            self.assertEquals(author_count, 1)
        
