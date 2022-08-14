from django_filters import FilterSet, CharFilter, ModelMultipleChoiceFilter

from apps.store.models import Category, Brand


class ProductFilter(FilterSet):
    category = ModelMultipleChoiceFilter(field_name='category__name', lookup_expr='iexact',
                                         queryset=Category.objects.all(), to_field_name='name')
    brand = ModelMultipleChoiceFilter(field_name='brand__name', lookup_expr='iexact',
                                      queryset=Brand.objects.all(), to_field_name='name')
    price_gte = CharFilter(field_name='price', lookup_expr='gte', )
    price_lte = CharFilter(field_name='price', lookup_expr='lte', )

    # class Meta:
    #     model = Product
    #     fields = ('status', )
