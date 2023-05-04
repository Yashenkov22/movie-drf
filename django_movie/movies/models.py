from django.db import models
from datetime import date
from django.urls.base import reverse


class Category(models.Model):
    name = models.CharField('Категория',max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actors(models.Model):
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug' : self.name})
    
    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'



class Genre(models.Model):
    name = models.CharField('Жанр', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'



class Movie(models.Model):
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default=2022)
    country = models.CharField('Страна', max_length=100)
    directors = models.ManyToManyField(Actors, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actors, verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = models.DateField('Примьера в мире', default=date.today)
    budget = models.PositiveSmallIntegerField('Бюджет', default=0, help_text='указать сумму в долларах')
    fees_in_usa = models.PositiveSmallIntegerField('Сборы в США', default=0, help_text='указать сумму в долларах')
    fees_in_world = models.PositiveSmallIntegerField('Сборы в мире', default=0, help_text='указать сумму в долларах')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('current_movie', kwargs={'slug' : self.url})
    
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)
    
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShorts(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shorts/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'



class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self) -> str:
        return str(self.value)
    
    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ['-value']


class Rating(models.Model):
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name='звезда', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.star} - {self.movie}'
    
    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    movie = models.ForeignKey(Movie, verbose_name = 'Фильм', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self) -> str:
        return f'{self.name} - {self.movie}'
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'