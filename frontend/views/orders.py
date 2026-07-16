from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from dashboard.models import Orders, Stock, userModel
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
import json
from utils import get_algerian_wilayas
from dashboard.utils import createNotification

wilayas = get_algerian_wilayas()
wilayas_choices = [(code, name) for code, name in wilayas]

@require_POST
def create_order(request, product_pk):
    try:
        product = Stock.objects.get(pk=product_pk)
        
        errors = []
        try:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            wilaya = request.POST.get('wilaya')
            commune = request.POST.get('commune')
            quantity = int(request.POST.get('quantity', 0))
            selected_size = request.POST.get('selected_size')
            selected_color = request.POST.get('selected_color')

            # Validate phone number format
            if not phone or len(phone) != 10 or not phone.isdigit():
                errors.append('رقم الهاتف يجب أن يكون 10 أرقام فقط')
            elif not phone.startswith(('05', '07', '06')):
                errors.append('رقم الهاتف يجب أن يبدأ بـ 05 أو 07 أو 06')

            # Validate sizes/colors if product has them
            if product.sizes and not selected_size:
                errors.append('الرجاء اختيار المقاس')
            if product.colors and not selected_color:
                errors.append('الرجاء اختيار اللون')

            # Get wilaya name from code
            if not wilaya:
                errors.append('الولاية المختارة غير صالحة')

            # Validate required fields
            if not all([name, phone, address, wilaya, commune]):
                errors.append('جميع الحقول مطلوبة')

            if quantity <= 0:
                errors.append('الكمية يجب أن تكون أكبر من صفر')

            if quantity > product.quantity:
                errors.append('الكمية المطلوبة أكبر من المتوفرة في المخزون')

            if errors:
                return JsonResponse({
                    'success': False,
                    'errors': errors
                }, status=400)

            try:    
                with transaction.atomic():
                    order = Orders.objects.create(
                        name=name,
                        phone=phone,
                        address=address,
                        wilaya=wilaya,
                        commune=commune,
                        product=product,
                        quantity=quantity,
                        selected_size=selected_size,
                        selected_color=selected_color
                    )
                    # Get admin and staff users to notify
                    admin_users = userModel.objects.filter(is_superuser=True)
                    staff_users = userModel.objects.filter(is_staff=True)
                    users_to_notify = admin_users | staff_users
                    
                    # Create notification for each user
                    for user in users_to_notify.distinct():
                        createNotification(
                            user=user,
                            message=f"تم إنشاء طلب جديد للمنتج: {product.product_name}",
                            icon="fas fa-shopping-cart"
                        )
                
                return JsonResponse({
                    'success': True,
                    'message': 'تم إرسال طلبك بنجاح!',
                    'ref_code': order.ref_code,
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'errors': [f'خطأ في إنشاء الطلب: {str(e)}']
                }, status=500)

        except (json.JSONDecodeError, ValueError):
            return JsonResponse({
                'success': False,
                'errors': ['بيانات الطلب غير صالحة']
            }, status=400)

    except Stock.DoesNotExist:
        return JsonResponse({
            'success': False,
            'errors': ['المنتج غير موجود']
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': [f'خطأ غير متوقع: {str(e)}']
        }, status=500)