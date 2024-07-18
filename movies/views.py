from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from movies.utils import fetch_movies
from movies.models import Collection, Movie
from movies.serializers import CollectionSerializer, MovieSerializer
from collections import Counter
from django.core.cache import cache

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=[AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        print(refresh)
        return Response({'access_token': str(refresh.access_token)})


class MovieListView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        data = fetch_movies(page)
        return Response(data, status=status.HTTP_200_OK)


class CollectionListCreateView(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        # response = super().create(request, *args, **kwargs)
        # collection_uuid = response.data.get('uuid')
        # return Response({'collection_uuid': collection_uuid}, status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        collection_uuid = serializer.data.get('uuid')
        return Response({'collection_uuid': collection_uuid}, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        collections = Collection.objects.filter(user_id=request.user)
        collection_data = CollectionSerializer(collections, many=True).data

        # Extracting genres from all movies in the user's collections
        genres = []
        for collection in collections:
            for movie in collection.movies.all():
                genres.extend(movie.genres.split(','))

        genres = [genre.strip() for genre in genres]
        genre_counts = Counter(genres)
        top_genres = [genre for genre, _ in genre_counts.most_common(3)]

        return Response({
            'is_success': True,
            'data': {
                'collections': collection_data,
                'favourite_genres': ', '.join(top_genres)
            }
        })


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get(self, request, *args, **kwargs):
        collection = self.get_object()
        # print(collection)
        return Response({
            "title": collection.title,
            "description": collection.description,
            "movies": MovieSerializer(collection.movies.all(), many=True).data
        }, status=status.HTTP_200_OK)
    

    def put(self, request, *args, **kwargs):
        collection = self.get_object()
        data = request.data

        if 'title' in data:
            collection.title = data['title']
        if 'description' in data:
            collection.description = data['description']

        if 'movies' in data:
            collection.movies.clear()
            for movie_data in data['movies']:
                movie, created = Movie.objects.get_or_create(
                    title=movie_data['title'],
                    description=movie_data['description'],
                    genres=movie_data['genres'],
                    uuid=movie_data['uuid']
                )
                collection.movies.add(movie)

        collection.save()
        return Response({
            "title": collection.title,
            "description": collection.description,
            "movies": MovieSerializer(collection.movies.all(), many=True).data
        }, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        collection = self.get_object()
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class RequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = cache.get('request_count', 0)
        return Response({'requests': count})
    

class RequestResetCountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cache.set('request_count', 0)
        return Response({'message': 'request count reset successfully'})