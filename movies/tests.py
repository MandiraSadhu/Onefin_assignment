from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import UserFactory, CollectionFactory, MovieFactory
import requests_mock
from movies.models import Collection
from django.core.cache import cache
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()


# GET http://localhost:8000/movies/
@pytest.mark.django_db
def test_list_movies(api_client, user):
    api_client.force_authenticate(user=user)

    # Mocking the external API call
    with requests_mock.Mocker() as mocker:
        mocker.get('https://demo.credy.in/api/v1/maya/movies/', json=[
            {'title': 'Movie 1', 'description': 'Description 1', 'genres': 'Action', 'uuid': 'uuid1'},
            {'title': 'Movie 2', 'description': 'Description 2', 'genres': 'Drama', 'uuid': 'uuid2'},
        ])
        
        response = api_client.get(reverse('movie-list'))
        # print("response **********************",response.content)
        # print("response **********************",response.data)
        
        assert response.status_code == 200
        assert len(response.data) == 2


# POST http://localhost:8000/collection/
@pytest.mark.django_db
def test_create_collection(api_client, user):
    # client = APIClient()
    # user = UserFactory()
    api_client.force_authenticate(user=user)
    
    movie1 = MovieFactory()
    movie2 = MovieFactory()

    response = api_client.post(reverse('list-create-collection'), {
        'title': 'My Collection',
        'description': 'A collection description',
        'movies': [
            {'title': movie1.title, 'description': movie1.description, 'genres': movie1.genres, 'uuid': movie1.uuid},
            {'title': movie2.title, 'description': movie2.description, 'genres': movie2.genres, 'uuid': movie2.uuid},
        ]
    }, format='json')

    # print("Request Payload:", payload)
    # print("Response Content:", response.content)


    assert response.status_code == 201
    assert 'collection_uuid' in response.data


# GET http://localhost:8000/collection/
@pytest.mark.django_db
def test_list_collections(api_client, user):
    # client = APIClient()
    # user = UserFactory()
    api_client.force_authenticate(user=user)
    
    collection = CollectionFactory(user_id=user)
    collection.movies.set([MovieFactory(), MovieFactory()])

    response = api_client.get(reverse('list-create-collection'))
    
    assert response.status_code == 200
    assert response.data['is_success']
    assert len(response.data['data']['collections']) > 0
    assert 'favourite_genres' in response.data['data']


# PUT http://localhost:8000/collection/<collection_uuid>/ (updating title and description fields )
@pytest.mark.django_db
def test_update_collection(api_client, user):
    api_client.force_authenticate(user=user)
    
    collection = CollectionFactory(user_id=user)
    new_title = 'Updated Collection'
    new_description = 'Updated Description'

    response = api_client.put(reverse('collection-detail', args=[collection.uuid]), {
        'title': new_title,
        'description': new_description,
        'movies': []
    }, format='json')

    assert response.status_code == 200
    assert response.data['title'] == new_title
    assert response.data['description'] == new_description


# PUT http://localhost:8000/collection/<collection_uuid>/ (updating movie field only)
@pytest.mark.django_db
def test_add_movie_to_collection(api_client, user):
    api_client.force_authenticate(user=user)
    
    collection = CollectionFactory(user_id=user)
    movie = MovieFactory()

    response = api_client.put(reverse('collection-detail', args=[collection.uuid]), {
        'movies': [{'title': movie.title, 'description': movie.description, 'genres': movie.genres, 'uuid': str(movie.uuid)}]
    }, format='json')

    assert response.status_code == 200
    assert collection.movies.count() == 1
    assert collection.movies.first().title == movie.title


# DELETE http://localhost:8000/collection/<collection_uuid>/
@pytest.mark.django_db
def test_delete_collection(api_client, user):
    api_client.force_authenticate(user=user)
    
    collection = CollectionFactory(user_id=user)
    
    response = api_client.delete(reverse('collection-detail', args=[collection.uuid]))
    
    assert response.status_code == 204
    assert not Collection.objects.filter(uuid=collection.uuid).exists()



@pytest.mark.django_db
def test_request_count_middleware(api_client, user):
    api_client.force_authenticate(user=user)
    cache.set('request_count', 0)

    # Triggering some requests to increase the count
    for _ in range(5):
        api_client.get(reverse('list-create-collection')) # 5 requests

    # This is also a request. So, request got incremented to 1 making requests a total of 6
    response = api_client.get(reverse('count-requests')) 
    
    assert response.status_code == 200
    assert response.data['requests'] == 6

@pytest.mark.django_db
def test_reset_request_count(api_client, user):

    cache.set('request_count', 10)
    api_client.force_authenticate(user=user)

    # Reset request count
    response = api_client.post(reverse('reset-count-request')) 
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'request count reset successfully'







