from django.views import generic
from django.urls import reverse
from ..models import CustomUser
from ..forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    template_name = 'accounts/profile_update.html'
    context_object_name = 'profile'
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('accounts:profile')