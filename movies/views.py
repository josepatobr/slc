from django.shortcuts import render
from .models import Movies

def movie(request, movie_id):
    movies = Movies.objects.filter(id=movie_id)   
    context = {
        "movies": movies,
    } 
    return render(request, "movie.html", context)