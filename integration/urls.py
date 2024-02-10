from django.urls import path
from .views import index,trapezoidal,simpson_one

urlpatterns = [
    path('',index,name='index'),
    path('trapezoidal/',trapezoidal,name='trapezoidal'),
    path('simpson_one/',simpson_one,name='simpson_one'),
]