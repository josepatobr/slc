from .utils import get_source_file_path
from signup.models import UserSingUp
from datetime import timedelta
from django.db import models




class Status(models.TextChoices):
    TERMINADO = "terminado", "Terminado"
    AINDA_LANCANDO = "ainda_lancando", "ainda lançando"
    EM_BREVE = "em_breve", "Em breve"
    DISPONIVEL = "disponivel", "disponivel"


class Genero(models.TextChoices):
    SEM_GENERO = "sem_genero", "sem genero"
    ROMANCE = "romance", "romance"


class Movies(models.Model):
    title_movie = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    status_movie = models.CharField(choices=Status, blank=False, null=False)
    gener_movie = models.CharField(choices=Genero, blank=True, null=True)

    file_movie = models.FileField(upload_to=get_source_file_path)
    hls_playlist = models.FileField(upload_to="movies/hls/", blank=True, null=True)
    movie_cover = models.FileField(upload_to=get_source_file_path, default=None)

    duration_all = models.DurationField(null=True, blank=True)
    current_time = models.DurationField(default=timedelta(seconds=0))

    def __str__(self):
        return self.title

    
    @property
    def duration_in_minutes(self):
        if self.duration_all:
            return int(self.duration_all.total_seconds() // 60)
        return 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class MoviesWatched(models.Model):
    user = models.ForeignKey(UserSingUp, on_delete=models.CASCADE, verbose_name="Usuário")
    movie_watched = models.ForeignKey(Movies, on_delete=models.CASCADE, verbose_name="Filme")
    watched_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Visualização")

    def __str__(self):
        return f"{self.user.username} assistiu {self.movie_watched.title} em {self.watched_at.strftime('%Y-%m-%d')}"


class Series(models.Model):
    title_serie = models.CharField(max_length=200)
    description = models.TextField()

    status_series = models.CharField(max_length=20, choices=Status.choices)
    gener_serie = models.CharField(choices=Genero, blank=True, null=True)


class Episode(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="episodes")
    title_episode = models.CharField(max_length=200)

    season_number = models.PositiveIntegerField(default=1)
    episode_number = models.PositiveIntegerField()

    file_episode = models.FileField(upload_to=get_source_file_path)

    duration_all = models.DurationField(null=True, blank=True)
    current_time = models.DurationField(default=timedelta(seconds=0))

    @property
    def duration_in_minutes(self):
        if self.duration_all:
            return int(self.duration_all.total_seconds() // 60)
        return 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class EpisodeWatched(models.Model):
    user = models.ForeignKey(UserSingUp, on_delete=models.CASCADE, verbose_name="Usuário")
    episode_watched = models.ForeignKey(Episode, on_delete=models.CASCADE, verbose_name="Episódio Assistido")
    watched_at = models.DateTimeField(auto_now=True, verbose_name="Última Visualização")

    class Meta:
        unique_together = ("user", "episode_watched")
        ordering = ["-watched_at"]

    def __str__(self):
        return f"{self.user.name} assistiu {self.episode_watched.title_episode}"


