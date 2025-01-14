from django.urls import path
from .views import index,matrix_view
urlpatterns = [
    path('',index,name='linearAlgebra'),
    path('matrix/', matrix_view, name='matrix_input'),

]