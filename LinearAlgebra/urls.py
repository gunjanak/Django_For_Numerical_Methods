from django.urls import path
from .views import index,matrix_view,linear_system_view
urlpatterns = [
    path('',index,name='linearAlgebra'),
    path('matrix/', matrix_view, name='matrix_input'),
    path('linear/',linear_system_view,name='linear_input'),

]