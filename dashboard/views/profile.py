from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from dashboard.models import Profile
from utils import get_algerian_wilayas

@login_required
def profile_view(request):
    if request.method == 'POST':
        return update_profile(request)
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {
        'profile': profile,
        'wilayas': get_algerian_wilayas(),
    })

@require_POST
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    errors = []

    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    wilaya = request.POST.get('wilaya', '').strip()
    bio = request.POST.get('bio', '').strip()

    if not username:
        errors.append("اسم المستخدم مطلوب")
    if not email:
        errors.append("البريد الإلكتروني مطلوب")

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    try:
        request.user.username = username
        request.user.email = email
        request.user.save()

        profile.phone = phone
        profile.wilaya = wilaya
        profile.bio = bio
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        profile.save()

        return JsonResponse({
            'success': True,
            'message': 'تم تحديث الملف الشخصي بنجاح'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': [str(e)]
        }, status=500)
