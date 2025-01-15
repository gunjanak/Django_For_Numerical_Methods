from django.urls import path
from .views import index,matrix_view,linear_system_view
urlpatterns = [
    path('',index,name='linearAlgebra'),
    path('matrix/', matrix_view, name='eigen_vector'),
    path('linear/',linear_system_view,name='system_of_linear'),

]