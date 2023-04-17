from django.urls import path, include
from .views import product_list, book_list

urlpatterns = [
    path('', product_list),
    path('1', book_list, name='book_list'),
]
