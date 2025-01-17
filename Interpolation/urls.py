from django.urls import path
from .views import interpolation_view
urlpatterns = [
    path('',interpolation_view,name='interpolation'),
]