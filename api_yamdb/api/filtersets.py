from django_filters import filters, filterset

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitleFilter(filterset.FilterSet):
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    category = CharFilterInFilter(
        field_name='category__slug',
        lookup_expr='in'
    )
    name = CharFilterInFilter(field_name='name', lookup_expr='in')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
