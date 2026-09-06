from ..forms import MembershipForm
from ..models import Project, Membership
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

class MembershipCreateView(LoginRequiredMixin, CreateView):
    model = Membership
    form_class = MembershipForm
    template_name = 'schedules/membership_create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_pk = self.kwargs.get('project_pk')
        kwargs['project'] = get_object_or_404(Project, pk=project_pk)
        
        return kwargs
    
    def get_success_url(self):
        project_pk = self.kwargs.get('project_pk')
        return reverse_lazy('schedules:membership_list', kwargs={'project_pk': project_pk})