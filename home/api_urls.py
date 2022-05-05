from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .views import *

router = routers.DefaultRouter()
router.register(r'products/', ProductViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
   # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('product_filter/',ProductFilterViewSet.as_view(),name='Product_filter')
]