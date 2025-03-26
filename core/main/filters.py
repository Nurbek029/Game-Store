import django_filters
from .models import Game_Product

class GameProductListFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Game_Product
        fields = ('category', 'price')  # Только реальные поля модели
