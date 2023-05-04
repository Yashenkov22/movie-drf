from django.urls import path
from .views import *


urlpatterns = [
    path('movies/', MovieListView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('review/', ReviewCreateView.as_view())
]