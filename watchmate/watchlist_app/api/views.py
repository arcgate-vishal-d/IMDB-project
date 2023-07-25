from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error)

@api_view(['GET','PUT', 'DELETE'])
def movie_detail(request, pk):
    
    if request.method == 'GET':
        try:
            movie = Movie.objects.get(pk=pk)
        except:
            data = {
                "msg":"No matching content"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        '''
        It's code written in serializer
        I am getting a purticular item to edit using get by id.
        if I don.t use get id so it will create new record
        '''
        try:
            movie = Movie.objects.get(pk=pk)
        except:
            data = {
                "msg":"No matching content"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            movie = Movie.objects.get(pk=pk)
        except:
            data = {
                "msg":"No matching content"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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