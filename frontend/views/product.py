from django.shortcuts import render, get_object_or_404
from dashboard.models import Stock, CATEGORY_CHOICES
from utils import get_algerian_wilayas
import json
from django.http import JsonResponse
from django.core.paginator import Paginator

wilayas = get_algerian_wilayas()
wilayas_choices = [(code, name) for code, name in wilayas]

def product_list(request):
    products = Stock.objects.all()
    
    # Category filter
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Availability filter (in stock)
    in_stock = request.GET.get('in_stock')
    if in_stock == 'true':
        products = products.filter(quantity__gt=0)
    elif in_stock == 'false':
        products = products.filter(quantity=0)
    
    # Search filter
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(product_name__icontains=search_query)
    
    # Sort by various criteria
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('product_name')
    elif sort_by == 'name_desc':
        products = products.order_by('-product_name')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    elif sort_by == 'popular':
        products = products.order_by('-sales_count')

    # Pagination
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Labels for custom select display
    cat_dict = dict(CATEGORY_CHOICES)
    sort_labels = {
        'price_asc': 'السعر: الأقل',
        'price_desc': 'السعر: الأعلى',
        'newest': 'الأحدث',
        'popular': 'الأكثر شهرة',
    }

    return render(request, 'product_list.html', {
        'products': page_obj,
        'categories': CATEGORY_CHOICES,
        'wilayas_choices': wilayas_choices,
        'current_category': category,
        'current_category_label': cat_dict.get(category, ''),
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_in_stock': in_stock,
        'current_search': search_query,
        'current_sort': sort_by,
        'current_sort_label': sort_labels.get(sort_by, ''),
        'page_obj': page_obj,
    })


def product_detail(request, product_pk):
    product = get_object_or_404(Stock, pk=product_pk)
    return render(request, 'product_details.html', {
        'product': product,
        'wilayas_choices': wilayas_choices
    })


def get_coummunes(request, wilaya_code):
    
    # Load the algeria_cities.json data
    with open('algeria_cities.json', 'r', encoding='utf-8') as f:
        cities_data = json.load(f)
    
    # Filter communes by wilaya_code
    communes = [
        city for city in cities_data 
        if city.get('wilaya_code') == wilaya_code
    ]
    
    return JsonResponse({'communes': communes})