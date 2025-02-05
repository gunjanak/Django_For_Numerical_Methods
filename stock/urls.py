from django.urls import path
from .views import symbol_view
urlpatterns = [
    path("",symbol_view,name='stock_home'),
]
