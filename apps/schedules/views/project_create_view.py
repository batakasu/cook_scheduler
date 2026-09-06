from ..forms import ProjectForm
from ..models import Project, Membership
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'schedules/project_create.html'
    success_url = reverse_lazy('schedules:project_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        Membership.objects.create(
            project=self.object,
            user=self.request.user
        )
        
        return response