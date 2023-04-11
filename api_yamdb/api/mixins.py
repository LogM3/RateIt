from rest_framework import mixins, viewsets


class ViewSetMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Миксины для view классов жанров и категорий"""
    pass
