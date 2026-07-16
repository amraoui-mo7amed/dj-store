from django.http import JsonResponse
from dashboard.models import FeedBack
from django.shortcuts import render , redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from ..decorator import admin_required
from ..utils import delete_item
from django.utils.translation import gettext_lazy as _
from django.db import transaction # Import transaction
from dashboard.utils import createNotification
from dashboard.models import userNotification
from django.contrib.auth import get_user_model

User = get_user_model()

@method_decorator(admin_required, name='dispatch')
@method_decorator(require_http_methods(["GET"]), name='dispatch')
class FeedBackListView(ListView):
    """View for listing all courses."""
    model = FeedBack
    template_name = 'feedback/list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10
    def get_queryset(self):
        return FeedBack.objects.all().order_by('-created_at')
    
@require_http_methods(["POST"])
def create_feedback(request):
    try:
        
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        description = request.POST.get('description', '').strip()
        picture = request.FILES.get('picture')

        errors = []
        if not name:
            errors.append(_("الاسم مطلوب"))
        if not email:
            errors.append(_("البريد الإلكتروني مطلوب"))
        if not description:
            errors.append(_("الرسالة مطلوبة"))

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
        with transaction.atomic():
            feedback = FeedBack.objects.create(

                name=name,
                email=email,
                description=description,
                picture=picture
            )

            if picture:
                feedback.picture = picture
                feedback.save()
            
            admin_user = User.objects.filter(is_superuser=True).first()
            if admin_user:
                createNotification(
                    user=admin_user,
                    message=f"تم إرسال تقييم جديد بواسطة {name}",
                    icon="fas fa-comment"
                )

        return JsonResponse({
            'success': True,
            'message': _('شكراً لك على تقييمك!'),
            "redirect_url" : reverse('frontend:index')
        })
    except Exception as e:
        return JsonResponse(
            {'success': False, 'errors': [str(e)]},
            status=500
        )

@require_POST
def approve_feedback(request, pk):
    try:
        feedback = FeedBack.objects.get(pk=pk)
        feedback.is_approved = not feedback.is_approved
        feedback.save()
        return JsonResponse({
            "success": True,
            "redirect_url" : reverse('dash:feedback_list')
        })
    except FeedBack.DoesNotExist:
        return JsonResponse({
            "success": True,
            "errors": ["هذه المراجعة غير موجودة"]
        })

@admin_required
@require_http_methods(["POST"])
def delete_feedback(request, pk):
    """View for deleting a teacher (returns JSON response)."""
    return delete_item(
        model=FeedBack,
        pk=pk,
        redirect_url=reverse_lazy("dash:feedback_list")
    )