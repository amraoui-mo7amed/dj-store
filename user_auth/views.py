# In your user_auth/views.py file
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy, reverse

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('dash:dash_home'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        errors = []
        if username is None or password is None:
            errors.append('يرجى ملء جميع الحقول المطلوبة.')
        
        if errors:
            return JsonResponse(
                {
                    'success': False,
                    'errors': errors
                }
            )
        else:
            try:
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': True, 'redirect_url': reverse('dash:dash_home')})
                else:       
                    return JsonResponse(
                        {
                            'success': False,
                            'errors': ['خطأ في اسم المستخدم أو كلمة المرور. حاول مرة أخرى.']
                        }
                    )
            except Exception as e:
                return JsonResponse(
                    {
                        'success': False,
                        'errors': [str(e)]
                    }
                )

    
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('user_auth:login')