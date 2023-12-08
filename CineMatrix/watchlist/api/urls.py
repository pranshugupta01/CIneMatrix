from django.urls import path
from watchlist.api.views import (
    WatchDetail,
    WatchListAV,
    StreamPlatformList,
    StreamPlatformDetail,
    ReviewList,
    ReviewDetail,
    ReviewCreate
)

urlpatterns = [
    path("watch-list/", WatchListAV.as_view(), name="watch_list"),
    path("watch-list/<int:pk>/", WatchDetail.as_view(), name="watch_detail"),
    path("platform/", StreamPlatformList.as_view(), name="stream_platform"),
    path(
        "platform/<int:pk>/",
        StreamPlatformDetail.as_view(),
        name="stream_platform_detail",
    ),
    # path("reviews/", ReviewList.as_view(), name="review_list"),
    # path("reviews/<int:pk>/", ReviewDetail.as_view(), name="review_detail"),
    path ("review/<int:pk>/", ReviewDetail.as_view(),name="review_detail"),
    path("<int:pk>/review/", ReviewList.as_view(), name="review_list"),
    path("<int:pk>/review-create/", ReviewCreate.as_view(), name="review_create")
]
