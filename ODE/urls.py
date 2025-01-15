from django.urls import path
from .views import initial_value_view,index

urlpatterns = [
    path("",index,name='ode_home'),
    path('initial_value/', initial_value_view, name='initial_value'),
]
