from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('detail/<slug>',DetailView.as_view(),name = 'detail'),
]