from django.shortcuts import redirect  # Import added

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('user_auth:login')
        return super().dispatch(request, *args, **kwargs)