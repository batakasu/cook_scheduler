from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..permissions import accessible_projects
from django.urls import reverse

class ProjectCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'schedules/project_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = accessible_projects(self.request.user).filter(members__user=self.request.user).exclude(scheduled_at=None)

        projects_data = []
        for p in projects:
            projects_data.append({
            'id': p.id,
            'title': p.title,
            'start': p.scheduled_at,
            'url': reverse('schedules:project_detail', kwargs={'project_pk': p.id})
        })

        context['projects_json'] = projects_data
        return context