import django_filters
from .models import *
from django_filters import CharFilter
class OrderFilter(django_filters.FilterSet):
   # start_date = DateFilter(field_name="date_created", lookup_expr = 'gte')
   # end_date = DateFilter(field_name="date_created", lookup_expr = 'lte')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_created']
       
class ProductFilter(django_filters.FilterSet):
    productname = CharFilter(field_name="name", lookup_expr="icontains")
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['date_created', 'price', 'name']
        
class CustomerFilter(django_filters.FilterSet):
    customername = CharFilter(field_name="name", lookup_expr="icontains")
    class Meta:
        model = Customer
        fields = '__all__' 
        exclude = ['date_created', 'name']
       