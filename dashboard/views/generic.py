from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _


from django.utils.translation import gettext as _

@login_required
def BaseDelete(request, Model, pk):
    try:
        # Get the model class dynamically
        model = Model
        instance = model.objects.get(pk=pk)
        instance.delete()
        return JsonResponse({'status': 'success', 'message': _('تم حذف العنصر بنجاح')})  # Translated message in Arabic
    except model.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': _('العنصر غير موجود')}, status=404)  # Translated message in Arabic
    except LookupError:
        return JsonResponse({'status': 'error', 'message': _('نموذج غير صالح')}, status=400)  # Translated message in Arabic
    
class BaseListView(LoginRequiredMixin, ListView):
    model = None  # This will be set dynamically
    template_name = 'dashboard/base_list.html'  # You can customize this template

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = context['object_list']  # Add the objects as 'objects' key
        return context