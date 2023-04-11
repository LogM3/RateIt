from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from users.models import User
from .validators import score_validator


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Жанр', unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Категория', unique=True
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256, unique=True, verbose_name='Произведение'
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        on_delete=models.SET_NULL, null=True
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выхода', validators=(
            MinValueValidator(0), MaxValueValidator(timezone.now().year))
    )
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        validators=[score_validator],
        verbose_name='Оценка произведения'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return f'Отзыв на "{str(self.title)}"'


class Comment(models.Model):
    text = models.TextField(max_length=200, verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий на "{str(self.review)}"'
