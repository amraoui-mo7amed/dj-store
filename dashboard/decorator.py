from functools import wraps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
def with_pagination(per_page=10, context_name="page_obj", queryset_name="queryset", template="list.html"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            # If response is not a dict (e.g. HttpResponse), skip
            if not isinstance(response, dict):
                return response

            queryset = response.get(queryset_name)
            if queryset is None:
                return response

            page_number = request.GET.get("page", 1)
            paginator = Paginator(queryset, per_page)

            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

            response[context_name] = page_obj
            return render(request, f"{template}.html", response)

        return _wrapped_view
    return decorator


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def admin_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a superuser,
    redirecting to the login page or showing an error message as necessary.
    """
    def check_admin(user):
        return user.is_authenticated and user.is_superuser
    
    actual_decorator = user_passes_test(
        check_admin,
        login_url='login',  # Make sure you have a login URL defined
        redirect_field_name=None
    )
    
    def _wrapped_view(request, *args, **kwargs):
        if not check_admin(request.user):
            messages.error(request, _('You do not have permission to access this page.'))
            return redirect('dashboard')  # Redirect to dashboard or another appropriate page
        return actual_decorator(view_func)(request, *args, **kwargs)
    
    return _wrapped_view