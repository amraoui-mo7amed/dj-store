from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count, DecimalField
from datetime import timedelta
from django.utils import timezone
from dashboard.models import Stock, Orders, FeedBack, CATEGORY_CHOICES
import json
@login_required
def dash_home(request):
    # ======= Stats Cards =======
    total_sales_amount = Orders.objects.filter(status="delivered").aggregate(
        total=Sum(F('quantity') * F('product__price'))
    )['total'] or 0
    total_sales_amount = float(total_sales_amount)  # <-- convert Decimal to float

    total_items_sold = Orders.objects.filter(status="delivered").aggregate(
        total=Sum('quantity')
    )['total'] or 0

    total_sales_count = Orders.objects.count()
    total_products = Stock.objects.count()

    total_stock_quantity = Stock.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_stock_value = Stock.objects.aggregate(
        total=Sum(F('quantity') * F('price'), output_field=DecimalField()))['total'] or 0
    total_stock_value = float(total_stock_value)

    total_feedbacks = FeedBack.objects.count()

    # ======= Sales Week Chart =======
    today = timezone.now().date()
    week_labels = []
    week_sales = []

    for i in range(6, -1, -1):  # past 7 days
        day = today - timedelta(days=i)
        day_sales = Orders.objects.filter(
            created_at__date=day
        ).aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
        week_labels.append(day.strftime('%a'))
        week_sales.append(float(day_sales))  # <-- convert Decimal to float

    # ======= Top 5 Products =======
    top_products_qs = Orders.objects.select_related('product')\
                        .values('product__product_name')\
                        .annotate(
                            total_qty=Sum('quantity'),
                            product_name=F('product__product_name')
                        )\
                        .order_by('-total_qty')[:5]

    top_products_data = list(top_products_qs)

    # ======= Products by Category Chart =======
    products_by_category_qs = Stock.objects.values('category').annotate(count=Count('category'))

    # Create a dictionary to map category keys to Arabic names
    category_dict = dict(CATEGORY_CHOICES)
    # Convert to Arabic labels
    category_labels = []
    for item in products_by_category_qs:
        category_labels.append(category_dict[item['category']])
    category_counts = [item['count'] for item in products_by_category_qs]

    # ======= Orders by Status Chart =======
    orders_by_status_qs = Orders.objects.values('status').annotate(count=Count('status'))
    STATUS_CHOICES = [
        ('pending', 'قيد الإنتظار'),
        ('confirmed', 'تم التأكيد'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('cancelled', 'تم الإلغاء'),
    ]
    status_choices_dict = dict(STATUS_CHOICES)
    status_labels = []
    for item in orders_by_status_qs:
        status_labels.append(status_choices_dict[item['status']])
    status_counts = [item['count'] for item in orders_by_status_qs]

    context = {
        'total_sales_amount': total_sales_amount,
        'total_items_sold': total_items_sold,
        'total_sales_count': total_sales_count,
        'total_products': total_products,
        'total_stock_quantity': total_stock_quantity,
        'total_stock_value': total_stock_value,
        'total_feedbacks': total_feedbacks,
        'week_labels': json.dumps(week_labels, ensure_ascii=False),
        'week_sales': json.dumps(week_sales, ensure_ascii=False),
        'top_products_data': top_products_data,
        'category_labels': json.dumps(category_labels, ensure_ascii=False),
        'category_counts': json.dumps(category_counts, ensure_ascii=False),
        'status_labels': json.dumps(status_labels, ensure_ascii=False),
        'status_counts': json.dumps(status_counts, ensure_ascii=False),
    }

    return render(request, 'dash/dash_home.html', context)
