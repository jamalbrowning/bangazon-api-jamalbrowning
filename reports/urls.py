from django.urls import path
from .views import expensiveproduct_list

urlpatterns = [
    path('reports/expensiveproducts', expensiveproduct_list)
]
