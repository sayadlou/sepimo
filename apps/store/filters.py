from django_filters import FilterSet, CharFilter


class ProductFilter(FilterSet):
    category = CharFilter(field_name='category__name', lookup_expr='iexact', )
    brand = CharFilter(field_name='brand__name', lookup_expr='iexact', )
    price_gte = CharFilter(field_name='variant__price', lookup_expr='gte', )
    price_lte = CharFilter(field_name='variant__price', lookup_expr='lte', )

    # class Meta:
    #     model = Product
    #     fields = ('status', )
