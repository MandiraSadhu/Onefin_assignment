from django.contrib import admin
from django.urls import path
from .views import RegisterView, MovieListView, CollectionListCreateView, CollectionDetailView, RequestCountView, RequestResetCountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('collection/', CollectionListCreateView.as_view(), name='list-create-collection'),
    # path('user/collection/', UserCollectionView.as_view(), name='user-collections'),
    path('collection/<uuid:uuid>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('request-count/', RequestCountView.as_view(), name='count-requests'),
    path('request-count/reset/', RequestResetCountView.as_view(), name='reset-count-request')
]