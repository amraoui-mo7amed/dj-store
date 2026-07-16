
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import send_mail
from django_eventstream import send_event
from dashboard.models import userNotification

from dashboard.models import userNotification
from django.contrib.auth import get_user_model
from django_eventstream import send_event

User = get_user_model()

def createNotification(user, message, icon, url=''):
    notification = userNotification.objects.create(
        user=user,
        message=message,
        icon=icon,
        url=url,
    )
    print(f'user:{user.pk}')
    send_event(
        f'user:{user.pk}',
        'notification',
        {
            'message': message,
            'icon': icon,
            'url': url,
            'is_read': notification.is_read
        }
    )
    return notification

def delete_item(model, pk, redirect_url):
    """
    Generic function to delete an item with JSON response.
    
    Args:
        model: The model class to delete from
        pk: Primary key of the item to delete
        redirect_url: URL to redirect to after deletion
    """
    try:
        item = get_object_or_404(model, pk=pk)
        
        # If no related objects or no related models to check, delete the item
        item.delete()
        
        return JsonResponse({
            'success': True,
            'message': "تم حذف العنصر بنجاح",
            "redirect_url" : redirect_url
        })
        
    except model.DoesNotExist:
        return JsonResponse(
            {'success': False, 'error': "العنصر غير موجود"}, 
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'success': False, 'error': "حدث خطأ أثناء حذف العنصر"}, 
            status=500
        )
