from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    AdminUserViewSet,
    custom_token_obtain,
    user_self_get_patch,
    UserSignupAPIView,
    ReviewViewSet,
    CommentViewSet
)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='Title')
v1_router.register('categories', CategoryViewSet, basename='Category')
v1_router.register('genres', GenreViewSet, basename='Genre')
v1_router.register('users', AdminUserViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, 'reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    'comments'
)

urlpatterns = [
    path(
        'v1/users/me/',
        user_self_get_patch,
        name='self_user',
    ),
    path(
        'v1/auth/token/',
        custom_token_obtain,
        name='token_obtain',
    ),
    path(
        'v1/auth/signup/',
        UserSignupAPIView.as_view(),
        name='user_signup',
    ),
    path('v1/', include(v1_router.urls))
]
