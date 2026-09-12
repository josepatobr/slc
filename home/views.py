from django.shortcuts import render
from movies.models import Movies, Series

def home(request):
    movies = Movies.objects.all()   
    context = {
        "movies": movies,
    } 
    return render(request, "home.html", context)


def search(request):
    option = Movies, Series

    input_search = request.GET.get("input_navbar")
    if not input_search:
        return render(request, "search_erro.html")

    search_database = option.objects.filter(name_product__icontains=input_search)
    
    if not search_database.exists():
        return render(request, "search_erro.html")
    else:
        return render(request, "search_sucess.html", {"search_database": search_database})