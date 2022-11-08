from django_filters import FilterSet,RangeFilter
from .models import Product

class Productfilters(FilterSet):
    price = RangeFilter()
    
    class Meta:
        model = Product   
        fields = {'gender': ['exact'], 'sale_type': ['exact'], 'accessory_type': ['exact']} 
    