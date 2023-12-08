from watchlist.api.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
)
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.views import APIView
from watchlist.models import WatchList, StreamPlatform, Reviews
from watchlist.api.permissions import IsAdminOrReviewUserOrReadOnly, IsAdminOrReadOnly


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Reviews.objects.filter(
            watchList=watchlist, author=review_user
        )
        # print(f"Before creation -> number_ratings: {watchlist.number_ratings}, avg_rating: {watchlist.avg_rating}")
        if review_queryset.exists():
            error_message = "Review already done by you"
            raise PermissionDenied(f"Already reviewed by {review_user}")

        new_rating = serializer.validated_data["rating"]

        total_ratings = watchlist.avg_rating * watchlist.number_ratings
        watchlist.number_ratings = watchlist.number_ratings + 1
        watchlist.avg_rating = (total_ratings + new_rating) / watchlist.number_ratings

        watchlist.save()
        # print(f"After creation -> number_ratings: {watchlist.number_ratings}, avg_rating: {watchlist.avg_rating}")
        serializer.save(author=review_user, watchList=watchlist)


class ReviewList(generics.ListAPIView):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Reviews.objects.filter(watchList=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReviewUserOrReadOnly]

    def perform_destroy(self, instance):
        # print(f"Before deletion -> number_ratings: {instance.watchList.number_ratings}, avg_rating: {instance.watchList.avg_rating}")

        watchlist = instance.watchList
        total_ratings = watchlist.avg_rating * watchlist.number_ratings

        if watchlist.number_ratings == 1:
            watchlist.avg_rating = 0
        else:
            watchlist.avg_rating = (total_ratings - instance.rating) / (
                watchlist.number_ratings - 1
            )

        watchlist.number_ratings -= 1
        watchlist.save()

        # print(f"After deletion -> number_ratings: {watchlist.number_ratings}, avg_rating: {watchlist.avg_rating}")
        instance.delete()


class WatchListAV(APIView):
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetail(APIView):
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(
            movie,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformList(APIView):
    
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetail(APIView):
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            movie = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(
            movie,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            movie = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
