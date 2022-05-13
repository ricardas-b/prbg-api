import factory

from django.http import QueryDict
from django.urls import reverse
from rest_framework.test import APITestCase

from api_app.models import Author
from config.settings import REST_FRAMEWORK



class RandomAuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth')
    nationality = 'Latvian'
    

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


class TestPagination(APITestCase):
    ''' Test whether the pagination is enabled. Do not bother to test if
        pagination is working properly as this is a feature of DRF and it should
        have been tested by DRF project.

        Test it with only one resource as the pagination configuration is
        applied globally for all resources. '''
    
    over_page_size = REST_FRAMEWORK['PAGE_SIZE'] + 1   # Set the amount that would result in more that one page of data
    
    def setUp(self):
        for _ in range(self.over_page_size):
            author = RandomAuthorFactory()

    def test_pagination_is_enabled(self):
        page_1 = self.client.get(reverse('list-of-authors')).json()
        page_2 = self.client.get(page_1['next']).json()
        author_count = len(page_1['results']) + len(page_2['results'])
        self.assertEquals(author_count, self.over_page_size)
        























        
