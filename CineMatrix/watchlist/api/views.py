from watchlist.api.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
)
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.views import APIView
from watchlist.models import WatchList, StreamPlatform, Reviews
from watchlist.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Reviews.objects.filter(
            watchList=watchlist, author=review_user
        )
        print(f"Before creation - number_ratings: {watchlist.number_ratings}, avg_rating: {watchlist.avg_rating}")
        if review_queryset.exists():
            error_message = "Review already done by you"
            print(f"Error: {error_message}")
            raise PermissionDenied(f"Already reviewed by {review_user}")

        new_rating = serializer.validated_data["rating"]

        # Calculate new average rating and update number of ratings
        total_ratings = watchlist.avg_rating * watchlist.number_ratings
        watchlist.number_ratings = watchlist.number_ratings + 1
        watchlist.avg_rating = (total_ratings + new_rating) / watchlist.number_ratings

        # Save changes to the WatchList
        watchlist.save()
        print(f"After creation - number_ratings: {watchlist.number_ratings}, avg_rating: {watchlist.avg_rating}")

        # Save the new review and return the created instance
        serializer.save(author=review_user, watchList=watchlist)

        def perform_destroy(self, instance):
            print(f"Before deletion - number_ratings: {instance.watchList.number_ratings}, avg_rating: {instance.watchList.avg_rating}")

            watchlist = instance.watchList

            # Adjust the number_ratings and avg_rating when a review is deleted
            total_ratings = watchlist.avg_rating * watchlist.number_ratings

            # If there's only one review, reset avg_rating to 0
            if watchlist.number_ratings == 1:
                watchlist.avg_rating = 0
            else:
                # Calculate new avg_rating after removing the deleted review
                watchlist.avg_rating = (total_ratings - instance.rating) / (watchlist.number_ratings - 1)

            # Update number_ratings and save changes to the WatchList
            watchlist.number_ratings -= 1
            watchlist.save()

            print(f"After deletion - number_ratings: {watchlist.number_ratings}, avg_rating: {watchlist.avg_rating}")

            # Delete the review
            instance.delete()


class ReviewList(generics.ListAPIView):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]

        return Reviews.objects.filter(watchList=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [ReviewUserOrReadOnly]
    def perform_destroy(self, instance):
            print(f"Before deletion - number_ratings: {instance.watchList.number_ratings}, avg_rating: {instance.watchList.avg_rating}")

            watchlist = instance.watchList

            # Adjust the number_ratings and avg_rating when a review is deleted
            total_ratings = watchlist.avg_rating * watchlist.number_ratings

            # If there's only one review, reset avg_rating to 0
            if watchlist.number_ratings == 1:
                watchlist.avg_rating = 0
            else:
                # Calculate new avg_rating after removing the deleted review
                watchlist.avg_rating = (total_ratings - instance.rating) / (watchlist.number_ratings - 1)

            # Update number_ratings and save changes to the WatchList
            watchlist.number_ratings -= 1
            watchlist.save()

            print(f"After deletion - number_ratings: {watchlist.number_ratings}, avg_rating: {watchlist.avg_rating}")

            # Delete the review
            instance.delete()


# class ReviewList(
#     mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
# ):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView,
# ):


#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


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
