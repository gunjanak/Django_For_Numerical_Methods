from django.urls import path
from .views import nonlinear_view
urlpatterns = [
    path('',nonlinear_view,name='nonlinear'),
]