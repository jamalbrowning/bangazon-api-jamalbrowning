from django.urls import path
from .views import expensiveproduct_list, inexpensiveproduct_list

urlpatterns = [
    path('reports/expensiveproducts', expensiveproduct_list),
    path('reports/inexpensiveproducts', inexpensiveproduct_list)
]
