from django.shortcuts import render, get_object_or_404
from dashboard.models import Orders


def order_confirmation(request, ref_code):
    order = get_object_or_404(
        Orders.objects.select_related('product'),
        ref_code=ref_code
    )
    return render(request, 'order_confirmation.html', {
        'order': order,
    })


def order_lookup(request):
    order = None
    error = None
    if request.method == 'POST':
        ref_code = request.POST.get('ref_code', '').strip()
        phone = request.POST.get('phone', '').strip()
        try:
            order = Orders.objects.select_related('product').get(
                ref_code=ref_code, phone=phone
            )
        except Orders.DoesNotExist:
            error = 'لم يتم العثور على طلب بهذه المعلومات'

    return render(request, 'order_lookup.html', {
        'order': order,
        'error': error,
    })
