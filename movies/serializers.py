from rest_framework import serializers
from .models import Collection, Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies', 'uuid']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(**validated_data)
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(**movie_data)
            collection.movies.add(movie)
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if movies_data is not None:
            instance.movies.clear()
            for movie_data in movies_data:
                movie, created = Movie.objects.get_or_create(**movie_data)
                instance.movies.add(movie)

        return instance
    