from rest_framework import serializers
from .models import *

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #fields = ['name', 'price', 'discounted_price', 'image','category','subcategory']
        fields = "__all__"