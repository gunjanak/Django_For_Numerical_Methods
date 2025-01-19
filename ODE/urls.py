from django.urls import path
from .views import initial_value_view,index,second_order_ode_view,system_of_ode_view

urlpatterns = [
    path("",index,name='ode_home'),
    path('initial_value/', initial_value_view, name='initial_value'),
    path('second_ode/',second_order_ode_view,name="second_ode"),
    path('system_of_ode/',system_of_ode_view,name="system_of_ode"),
]
