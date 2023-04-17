import django_filters
from django.shortcuts import render

from .models import Book

class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['price', 'name']

def product_list(request):
    f = ProductFilter(request.GET, queryset=Book.objects.all())
    return render(request, 'books/a.html', context={'filter':f})


def book_list(request):
    books = ProductFilter(request.GET, queryset=Book.objects.order_by('name'))
    sort = request.GET.get('sort')
    print(sort)
    if sort != None:
        books = ProductFilter(queryset=Book.objects.order_by(sort))
    # else:
    #     f = ProductFilter(request.GET, queryset=Book.objects.all())
    #     return render(request, 'books/b.html', {'books': books})
    # sort = None
    return render(request, 'books/b.html', {'books': books})
