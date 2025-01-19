from django.urls import path
from .views import home,home_Numerical_methods
urlpatterns = [
    path('',home,name='home'),
    path('nm',home_Numerical_methods,name="home_nm"),
]