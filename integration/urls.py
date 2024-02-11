from django.urls import path
from .views import index,trapezoidal,simpson_one,simpson_three

urlpatterns = [
    path('',index,name='integration'),
    path('trapezoidal/',trapezoidal,name='trapezoidal'),
    path('simpson_one/',simpson_one,name='simpson_one'),
    path('simpson_three/',simpson_three,name='simpson_three'),
]