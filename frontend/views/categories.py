from django.shortcuts import render, get_object_or_404
from dashboard.models import Stock, CATEGORY_CHOICES

def category_list(request):
    categories_data = []
    for category_slug, category_name in CATEGORY_CHOICES:
        items = Stock.objects.filter(category=category_slug).order_by('-created_at')[:6]
        categories_data.append({'name': category_name, 'slug': category_slug, 'items': items})
    return render(request, 'category_list.html', {'categories': categories_data})

def category_details(request, category_slug):
    category_name = dict(CATEGORY_CHOICES).get(category_slug)
    products = Stock.objects.filter(category=category_slug)
    return render(request, 'category_details.html', {'category': {'name': category_name, 'slug': category_slug}, 'products': products})