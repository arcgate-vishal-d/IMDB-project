from watchlist_app.models import Watchlist, StreamPlatform, Review
from watchlist_app.api.serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.api.permissions import IsAdminOrReadOnly, ReviewUserOrReadOnly


from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

# Generic view and mixins for review 
from rest_framework import mixins
from rest_framework import generics

from rest_framework.exceptions import ValidationError

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle



class ReviewCreate(generics.CreateAPIView):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        # pk = self.kwargs['pk']
        pk = self.kwargs.get('pk')
        
        watchlist = Watchlist.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You already gave review to this movie")
            # return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating += 1
        watchlist.save()
    
        serializer.save(watchlist=watchlist, review_user=review_user)

        # movie = Review.objects.get(pk=pk)
        # serializer.save(watchlist=movie)

class ReviewList(generics.ListAPIView):
    # # It will give me all th review
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    

    # overiding the queryset for finding the specific movie review
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)  # this watchlist came form the model where we use watchlist as a foreign key
    
    # Here I am not using the post method for creating the Review. If I create than I have to select movie(watchlist) manually.
    # so I want it should be selected automatically So I used perform_create method in another view.
    
 
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [ReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# # using Mixins

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)




class PlatformListAv(APIView):

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
        return Response(serializer.data)


    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)


class PlatformDetailAV(APIView):

    def get_object(self,pk):
        try:
            return StreamPlatform.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        platform = self.get_object(pk)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = self.get_object(pk)
        serializer = StreamPlatformSerializer(platform)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        platform = self.get_object(pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class WatchlistListAV(APIView):
    def get(self, request):
        movies = Watchlist.objects.all()
        serializer = WatchlistSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchlistDetailAV(APIView):

    def get_object(self, pk):
        try:
            return Watchlist.objects.get(pk=pk)
        except:
            data = {
                "msg":"No matching content"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    def get(self, request,pk):
        movie = self.get_object(pk)
        serializer = WatchlistSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        '''
        It's code written in serializer
        I am getting a purticular item to edit using get by id.
        if I don.t use get id so it will create new record
        '''
        movie = self.get_object(pk)
        serializer = WatchlistSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET','PUT', 'DELETE'])
# def movie_detail(request, pk):
    
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except:
#             data = {
#                 "msg":"No matching content"
#             }
#             return Response(data, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         '''
#         It's code written in serializer
#         I am getting a purticular item to edit using get by id.
#         if I don.t use get id so it will create new record
#         '''
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except:
#             data = {
#                 "msg":"No matching content"
#             }
#             return Response(data, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'DELETE':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except:
#             data = {
#                 "msg":"No matching content"
#             }
#             return Response(data, status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================================================================================================
# Without serializer

# from django.shortcuts import render

# from watchlist_app.models import Movie
# from django.http import JsonResponse


# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {
#         'movies' : list(movies.values())
#     }
#     return JsonResponse(data)

# def movie_detail(request,pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#        'name': movie.name,
#        'description': movie.description,
#        'active': movie.active
#     }
#     return JsonResponse(data)