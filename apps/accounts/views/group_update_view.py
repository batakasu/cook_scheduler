from django.views import generic
from django.urls import reverse
from ..models import CookingGroup
from ..forms import GroupForm
from ..permissions import accessible_groups
from django.contrib.auth.mixins import LoginRequiredMixin

class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    pk_url_kwarg = 'group_pk'
    model = CookingGroup
    template_name = 'accounts/group_update.html'
    context_object_name = 'group'
    form_class = GroupForm

    def get_queryset(self):
        groups = accessible_groups(self.request.user)
        return groups
    
    def get_success_url(self):
        return reverse('accounts:profile')