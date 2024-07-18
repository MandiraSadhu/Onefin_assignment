import factory
from django.contrib.auth.models import User
from .models import Collection, Movie

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')

class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')
    genres = factory.Faker('word')
    uuid = factory.Faker('uuid4')

class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    user_id = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')

    @factory.post_generation
    def movies(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for movie in extracted:
                self.movies.add(movie)
