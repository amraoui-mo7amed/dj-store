from django.http import JsonResponse
from dashboard.models import userNotification

def unread_notifications_api(request, user_id):
    notifications = userNotification.objects.filter(user__id=user_id, is_read=False).order_by('-created_at')
    data = [
        {
            'message': n.message,
            'icon': n.icon,
            'url': n.url,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for n in notifications
    ]
    return JsonResponse({'success': True, 'notifications': data})

def mark_all_notifications_as_read_api(request, user_id):
    if request.method == 'POST':
        userNotification.objects.filter(user__id=user_id, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
