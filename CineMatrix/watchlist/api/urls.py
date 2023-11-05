from django.urls import path
from watchlist.api.views import WatchDetail,WatchListAV,StreamPlatformList,StreamPlatformDetail

urlpatterns = [
    path("list/", WatchListAV.as_view(), name="watch_list"),
    path("<int:pk>/", WatchDetail.as_view(), name="watch_detail"),
    path("platform/", StreamPlatformList.as_view(), name="stream_platform"),
    path("platform/<int:pk>", StreamPlatformDetail.as_view(), name="stream_platform_detail"),
]
