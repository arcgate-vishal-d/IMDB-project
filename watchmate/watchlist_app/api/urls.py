from django.urls import path
# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import WatchlistListAV, WatchlistDetailAV, PlatformListAv, PlatformDetailAV, ReviewList, ReviewDetail, ReviewCreate


urlpatterns = [
    path('list/', WatchlistListAV.as_view(), name="movie-list" ),
    path('detail/<int:pk>/', WatchlistDetailAV.as_view(), name="movie-detail"),

    # StreamPlatform
    path('stream/', PlatformListAv.as_view(), name="platform-list" ),
    path('stream/<int:pk>/', PlatformDetailAV.as_view(), name="platform-detail" ),

    # Review Urls
    # path('review/', ReviewList.as_view(), name="review-list"),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),


    # new urls for review
    path('<int:pk>/create-review/', ReviewCreate.as_view(), name="create-review"),
    path('<int:pk>/reviews/', ReviewList.as_view(), name="review-list"),
    path('review/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),  
] 