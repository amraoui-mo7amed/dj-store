from django.shortcuts import render
from dashboard.models import Stock, CATEGORY_CHOICES

def index(request):
    return render(request, 'index.html', {
        'products': Stock.objects.all().order_by('-created_at')[:6],
        'categories': CATEGORY_CHOICES,
    })
