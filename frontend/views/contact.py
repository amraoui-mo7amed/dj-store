from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def contact_view(request):
    try:
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        errors = []
        
        # Validate form data
        if not all([full_name, email, subject, message]):
            errors.append(_('يرجى ملء جميع الحقول المطلوبة'))
        
        # Validate email format
        if email and '@' not in email:
            errors.append(_('صيغة البريد الإلكتروني غير صحيحة'))
        
        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
        
        # Send email
        try:
            email_subject = f"{subject} - من {full_name}"
            email_message = f"""
الاسم: {full_name}
البريد الإلكتروني: {email}
الموضوع: {subject}

الرسالة:
{message}
            """
            
            send_mail(
                email_subject,
                email_message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': _('تم إرسال رسالتك بنجاح. سنرد عليك قريباً')
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': [_('حدث خطأ أثناء إرسال الرسالة. يرجى المحاولة مرة أخرى لاحقاً')]
            }, status=500)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': [_('حدث خطأ غير متوقع')]
        }, status=500)
