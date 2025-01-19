from django.urls import path
from .views import index,laplace_view,poisson_view

urlpatterns = [
    path("",index,name='pde_home'),
    path("laplace/",laplace_view,name='laplace'),
    path("poisson/",poisson_view,name='poisson'),
    
]
