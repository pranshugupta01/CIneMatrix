from django.urls import path
from watchlist.api.views import movie_detail, movie_list

urlpatterns = [
    path("list/", movie_list, name="movie_list"),
    path("<int:pk>/", movie_detail, name="movie_detail"),
]
