from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, Avg, DecimalField
from django.utils import timezone
from datetime import timedelta
from dashboard.models import Stock, Orders, FeedBack, userNotification, CATEGORY_CHOICES
import json

@login_required
def reports_view(request):
    # 1. Stock Reports
    total_stock_items = Stock.objects.count()
    low_stock_threshold = 10
    low_stock_items = Stock.objects.filter(quantity__lt=low_stock_threshold)
    stock_by_category = Stock.objects.values('category').annotate(
        total_qty=Sum('quantity'),
        item_count=Count('id')
    )
    avg_product_price = Stock.objects.aggregate(avg_price=Avg('price'))['avg_price'] or 0

    # 2. Sales/Order Reports
    total_orders = Orders.objects.count()
    orders_by_status_qs = Orders.objects.values('status').annotate(count=Count('id'))
    orders_by_status = {item['status']: item['count'] for item in orders_by_status_qs}
    
    # Revenue aggregation
    total_revenue = Orders.objects.filter(status='delivered').aggregate(
        total=Sum(F('quantity') * F('product__price'), output_field=DecimalField())
    )['total'] or 0

    total_items_sold = Orders.objects.filter(status='delivered').aggregate(
        total_qty=Sum('quantity')
    )['total_qty'] or 0

    total_sales_count = Orders.objects.filter(status='delivered').count()

    # Additional stats from models
    pending_orders_count = orders_by_status.get('pending', 0)
    confirmed_orders_count = orders_by_status.get('confirmed', 0)
    shipped_orders_count = orders_by_status.get('shipped', 0)
    delivered_orders_count = orders_by_status.get('delivered', 0)
    cancelled_orders_count = orders_by_status.get('cancelled', 0)

    # Geographic reports (Wilayas)
    orders_by_wilaya = Orders.objects.values('wilaya').annotate(count=Count('id')).order_by('-count')

    # 3. Monthly Sales (Last 6 months)
    today = timezone.now()
    monthly_sales = []
    monthly_labels = []
    monthly_revenue = []
    for i in range(5, -1, -1):
        date = today - timedelta(days=i*30)
        month_name = date.strftime('%b %Y')
        sales_count = Orders.objects.filter(created_at__year=date.year, created_at__month=date.month).count()
        revenue = Orders.objects.filter(created_at__year=date.year, created_at__month=date.month, status='delivered').aggregate(
            total=Sum(F('quantity') * F('product__price'), output_field=DecimalField())
        )['total'] or 0
        monthly_sales.append({
            'month': month_name,
            'count': sales_count,
            'revenue': float(revenue)
        })
        monthly_labels.append(month_name)
        monthly_revenue.append(float(revenue))

    # 4. Feedback reports
    total_feedback = FeedBack.objects.count()
    approved_feedback = FeedBack.objects.filter(is_approved=True).count()

    # 5. User Notifications
    total_notifications = userNotification.objects.count()
    unread_notifications = userNotification.objects.filter(is_read=False).count()

    # Chart Data for Status
    status_dict = dict(Orders.STATUS_CHOICES)
    status_labels = [status_dict.get(item['status']) for item in orders_by_status_qs]
    status_values = [item['count'] for item in orders_by_status_qs]

    context = {
        'stock': {
            'total_items': total_stock_items,
            'low_stock_count': low_stock_items.count(),
            'low_stock_items': low_stock_items[:10],
            'by_category': stock_by_category,
            'avg_price': avg_product_price,
        },
        'sales': {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_items_sold': total_items_sold,
            'total_sales_count': total_sales_count,
            'pending_orders_count': pending_orders_count,
            'confirmed_orders_count': confirmed_orders_count,
            'shipped_orders_count': shipped_orders_count,
            'delivered_orders_count': delivered_orders_count,
            'cancelled_orders_count': cancelled_orders_count,
            'by_status': orders_by_status_qs,
            'by_wilaya': orders_by_wilaya[:10],
            'monthly': monthly_sales,
            'monthly_labels': json.dumps(monthly_labels),
            'monthly_revenue': json.dumps(monthly_revenue),
            'status_labels': json.dumps(status_labels),
            'status_values': json.dumps(status_values),
        },
        'feedback': {
            'total': total_feedback,
            'approved': approved_feedback,
        },
        'notifications': {
            'total': total_notifications,
            'unread': unread_notifications,
        },
        'category_choices': dict(CATEGORY_CHOICES),
        'status_choices': dict(Orders.STATUS_CHOICES),
    }

    return render(request, 'reports/reports.html', context)
