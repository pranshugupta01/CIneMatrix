from django.urls import path
from watchlist.api.views import MovieDetail,MovieList
# from watchlist.api.views import movie_detail, movie_list

urlpatterns = [
    path("list/", MovieList.as_view(), name="movie_list"),
    path("<int:pk>/", MovieDetail.as_view(), name="movie_detail"),
]
