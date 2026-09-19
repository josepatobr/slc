from django.shortcuts import render, get_object_or_404
from .models import Movies

def movie(request, movie_id):
    movie_obj = get_object_or_404(Movies, id=movie_id)   
    recomendados = Movies.objects.order_by("?")[:5]

    context = {
        "movie": movie_obj,
        "recomendados": recomendados,
    } 
    return render(request, "movie.html", context)