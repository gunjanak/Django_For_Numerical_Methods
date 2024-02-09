from django.urls import path
from .views import index,trapezoidal

urlpatterns = [
    path('',index,name='index'),
    path('trapezoidal/',trapezoidal,name='trapezoidal'),
]