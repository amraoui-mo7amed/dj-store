import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from dashboard.models import Orders, Stock
from django.core.paginator import Paginator
from dashboard.views.genric import BaseDeleteView
from django.urls import reverse
from django.db import transaction, DatabaseError
from django.db.models import F

from django.db.models import Sum, F
from utils import get_algerian_wilayas
wilayas = get_algerian_wilayas()
wilayas_choices = [(code, name) for code, name in wilayas]



@login_required
def sales_list(request):
    """List all stock items and sales summary"""
    
    # Pagination
    paginator = Paginator(Orders.objects.all().order_by('-created_at'), 10)  # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # Products for your select
    Products = [(product.pk, product.product_name) for product in Stock.objects.all()]

    return render(request, "sales/sales_list.html", {
        "page_obj": page_obj,
        "stock": Products,
    })


@login_required
def get_order_details(request, pk):
    order = get_object_or_404(Orders.objects.select_related('product'), pk=pk)
    data = {
        'name': order.name,
        'phone': order.phone,
        'address': order.address,
        'wilaya': order.get_wilaya_name,
        'commune': order.commune,
        'product_name': order.product.product_name,
        'quantity': order.quantity,
        'selected_size': order.selected_size,
        'selected_color': order.selected_color,
        'price': str(order.product.price),  # Convert Decimal to string
        'status_display': order.get_status_display(),
        'created_at': order.created_at.isoformat(),
    }
    return JsonResponse(data)


@csrf_exempt
@require_POST
@login_required
def update_order_status(request, pk):
    try:
        order = get_object_or_404(Orders, pk=pk)
        data = json.loads(request.body)
        new_status = data.get('status')

        if new_status and new_status in dict(Orders.STATUS_CHOICES):
            old_status = order.status
            order.status = new_status
            order.save(update_fields=['status'])

            if old_status != 'cancelled' and new_status == 'cancelled':
                Stock.objects.filter(pk=order.product.pk).update(
                    quantity=F('quantity') + order.quantity
                )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


class delete_order(BaseDeleteView):
    model = Orders