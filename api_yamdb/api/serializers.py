import re

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category

    def validate_slug(self, value):
        if not re.match(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                f'Недопустимый slug: {value}'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        if not re.match(r'[\w.@+-]+', value):
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {value}'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre

    def validate_slug(self, value):
        if not re.match(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                f'Недопустимый slug: {value}'
            )
        return value


class ReadTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title
        read_only_fields = ('genre', 'category')


class UserPatchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
        )

    def validate_username(self, value):
        if not re.match(r'[\w.@+-]+', value) or value == 'me':
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {value}'
            )
        return value


class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if not re.match(r'[\w.@+-]+', value) or value == 'me':
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {value}'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь {username} уже существует'
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Пользователь с адресом {email} уже существует'
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review

    def validate(self, data):
        view = self.context.get('view')
        if view.action == 'create':
            if self.context.get('request').user.reviews.filter(
                    title_id=view.kwargs.get('title_id')
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на данное произведение!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Comment


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=40)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                'Неверный confirmation_code'
            )
        return data
