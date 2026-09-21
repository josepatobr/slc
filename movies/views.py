from django.shortcuts import render, get_object_or_404
from .models import Movies
import ffmpeg
import os
from django.conf import settings

def movie(request, movie_id):
    movie_obj = get_object_or_404(Movies, id=movie_id)   
    recomendados = Movies.objects.order_by("?")[:5]

    context = {
        "movie": movie_obj,
        "recomendados": recomendados,
    } 
    return render(request, "movie.html", context)


def chuncks(movie_id):
  arq = get_object_or_404(Movies, id=movie_id)

  input_path = arq.file_movie.path

  output_dir = os.path.join(settings.MEDIA_ROOT, "movies", "hls")
  os.makedirs(output_dir, exist_ok=True)

  output_playlist = os.path.join(output_dir, f"movie_{movie_id}.m3u8")

  try:
    (
        ffmpeg.input(input_path)
        .output(
            output_playlist,
            format="hls",
            hls_time=10,
            hls_list_size=0,
            vcodec="libx264",
            acodec="aac",
        )
        .run(overwrite_output=True)
    )

    arq.hls_playlist = f"movies/hls/movie_{movie_id}.m3u8"
    arq.save()

    print("chunks feita com sucesso")
  except ffmpeg.Error as e:
    print(f"erro no FFmpeg: {e.stderr.decode()}")